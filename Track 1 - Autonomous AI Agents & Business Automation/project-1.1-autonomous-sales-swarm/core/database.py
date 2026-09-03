import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from .schemas import RawLead, VerificationResult, PersonalizedHook, CloserResponse, CampaignMetrics

class SwarmDatabase:
    def __init__(self, db_path: str = "swarm_leads.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Leads Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    owner_name TEXT,
                    niche TEXT,
                    city TEXT,
                    state TEXT,
                    phone TEXT,
                    email TEXT,
                    website TEXT,
                    reviews_json TEXT,
                    has_24_7_service_claim INTEGER,
                    status TEXT DEFAULT 'SCOUTED',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Verification Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS verifications (
                    lead_id TEXT PRIMARY KEY,
                    email_valid INTEGER,
                    deliverability_score REAL,
                    phone_type TEXT,
                    business_operational INTEGER,
                    status TEXT,
                    reason TEXT,
                    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(lead_id) REFERENCES leads(id)
                )
            """)

            # Hooks Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hooks (
                    lead_id TEXT PRIMARY KEY,
                    missed_calls INTEGER,
                    ticket_value REAL,
                    lost_revenue REAL,
                    pain_point TEXT,
                    subject_line TEXT,
                    email_body TEXT,
                    sms_body TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(lead_id) REFERENCES leads(id)
                )
            """)

            # Conversations & Closer Actions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id TEXT NOT NULL,
                    direction TEXT, -- 'OUTBOUND' or 'INBOUND'
                    channel TEXT,   -- 'EMAIL' or 'SMS'
                    message_content TEXT,
                    detected_intent TEXT,
                    confidence REAL,
                    action_taken TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(lead_id) REFERENCES leads(id)
                )
            """)

            # Suppression List (Unsubscribes / Do Not Contact)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suppression_list (
                    email TEXT PRIMARY KEY,
                    phone TEXT,
                    reason TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_lead(self, lead: RawLead):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO leads 
                (id, company_name, owner_name, niche, city, state, phone, email, website, reviews_json, has_24_7_service_claim, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'SCOUTED')
            """, (
                lead.id,
                lead.company_name,
                lead.owner_name,
                lead.niche.value if hasattr(lead.niche, 'value') else lead.niche,
                lead.city,
                lead.state,
                lead.phone,
                lead.email,
                lead.website,
                json.dumps([r.model_dump() for r in lead.reviews]),
                1 if lead.has_24_7_service_claim else 0
            ))
            conn.commit()

    def save_verification(self, res: VerificationResult):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO verifications
                (lead_id, email_valid, deliverability_score, phone_type, business_operational, status, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                res.lead_id,
                1 if res.email_valid else 0,
                res.email_deliverability_score,
                res.phone_type.value if hasattr(res.phone_type, 'value') else res.phone_type,
                1 if res.business_operational else 0,
                res.status.value if hasattr(res.status, 'value') else res.status,
                res.reason
            ))
            cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (f"VERIFIED_{res.status.value}", res.lead_id))
            conn.commit()

    def save_hook(self, hook: PersonalizedHook):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO hooks
                (lead_id, missed_calls, ticket_value, lost_revenue, pain_point, subject_line, email_body, sms_body)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hook.lead_id,
                hook.estimated_monthly_missed_calls,
                hook.estimated_ticket_value,
                hook.estimated_monthly_lost_revenue,
                hook.specific_pain_point,
                hook.subject_line,
                hook.email_body_3_sentences,
                hook.sms_body
            ))
            cursor.execute("UPDATE leads SET status = 'HOOK_GENERATED' WHERE id = ?", (hook.lead_id,))
            conn.commit()

    def log_message(self, lead_id: str, direction: str, channel: str, message: str, intent: Optional[str] = None, confidence: float = 1.0, action: Optional[str] = None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations (lead_id, direction, channel, message_content, detected_intent, confidence, action_taken)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (lead_id, direction, channel, message, intent, confidence, action))
            conn.commit()

    def suppress_contact(self, email: str, phone: Optional[str] = None, reason: str = "Unsubscribe"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO suppression_list (email, phone, reason)
                VALUES (?, ?, ?)
            """, (email, phone, reason))
            cursor.execute("UPDATE leads SET status = 'SUPPRESSED' WHERE email = ?", (email,))
            conn.commit()

    def is_suppressed(self, email: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM suppression_list WHERE email = ?", (email,))
            return cursor.fetchone() is not None

    def get_metrics(self) -> CampaignMetrics:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM leads")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM verifications WHERE status = 'PASSED'")
            verified = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations WHERE direction = 'OUTBOUND'")
            outreach = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations WHERE direction = 'INBOUND'")
            replies = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations WHERE detected_intent = 'POSITIVE_INTEREST'")
            positives = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations WHERE detected_intent LIKE 'OBJECTION_%'")
            objections = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM suppression_list")
            unsubscribes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations WHERE action_taken = 'SENT_DEMO_LINK'")
            demos = cursor.fetchone()[0]

            return CampaignMetrics(
                total_leads_scouted=total,
                verified_leads=verified,
                outreach_sent=outreach,
                replies_received=replies,
                positive_replies=positives,
                objections_handled=objections,
                unsubscribes=unsubscribes,
                demos_booked=demos
            )

    def reset_database(self):
        """Clears all tables for a fresh simulation run."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS conversations")
            cursor.execute("DROP TABLE IF EXISTS hooks")
            cursor.execute("DROP TABLE IF EXISTS verifications")
            cursor.execute("DROP TABLE IF EXISTS leads")
            cursor.execute("DROP TABLE IF EXISTS suppression_list")
            conn.commit()
        self._init_db()

    def get_all_leads(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve leads enriched with verification and hook status."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    l.id, l.company_name, l.owner_name, l.niche, l.city, l.state, 
                    l.phone, l.email, l.website, l.reviews_json, l.has_24_7_service_claim, l.status,
                    v.status as verification_status, v.deliverability_score as email_deliverability_score, v.phone_type, v.reason as verification_reason,
                    h.lost_revenue, h.subject_line, h.email_body as hook_email, h.sms_body as hook_sms,
                    (SELECT COUNT(*) FROM conversations c WHERE c.lead_id = l.id) as conversation_count
                FROM leads l
                LEFT JOIN verifications v ON l.id = v.lead_id
                LEFT JOIN hooks h ON l.id = h.lead_id
                ORDER BY l.created_at DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("reviews_json"):
                    try:
                        item["reviews"] = json.loads(item["reviews_json"])
                    except Exception:
                        item["reviews"] = []
                else:
                    item["reviews"] = []
                results.append(item)
            return results

    def get_lead_detail(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get full lead details including conversation history."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
            lead_row = cursor.fetchone()
            if not lead_row:
                return None

            lead = dict(lead_row)
            if lead.get("reviews_json"):
                try:
                    lead["reviews"] = json.loads(lead["reviews_json"])
                except Exception:
                    lead["reviews"] = []

            # Verification
            cursor.execute("SELECT * FROM verifications WHERE lead_id = ?", (lead_id,))
            v_row = cursor.fetchone()
            lead["verification"] = dict(v_row) if v_row else None

            # Hook
            cursor.execute("SELECT * FROM hooks WHERE lead_id = ?", (lead_id,))
            h_row = cursor.fetchone()
            lead["hook"] = dict(h_row) if h_row else None

            # Conversations
            cursor.execute("SELECT * FROM conversations WHERE lead_id = ? ORDER BY timestamp ASC, id ASC", (lead_id,))
            lead["conversations"] = [dict(r) for r in cursor.fetchall()]

            return lead

    def get_all_conversations(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, l.company_name 
                FROM conversations c
                LEFT JOIN leads l ON c.lead_id = l.id
                ORDER BY c.timestamp DESC, c.id DESC
                LIMIT ?
            """, (limit,))
            return [dict(r) for r in cursor.fetchall()]

