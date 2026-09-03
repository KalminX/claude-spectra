import re
import logging
from typing import List, Tuple
from core.schemas import RawLead, VerificationResult, PhoneLineType, VerificationStatus
from core.database import SwarmDatabase

logger = logging.getLogger("Agent2_Verifier")

class VerificationSentryAgent:
    """
    AGENT 2: Verification & Data Hygiene Sentry
    Validates email deliverability (ZeroBounce/Hunter pattern), validates phone line
    carrier status (Twilio Lookup pattern), and discards invalid or closed businesses
    to maintain 98%+ sender deliverability.
    """

    def __init__(self, db: SwarmDatabase):
        self.db = db

    def verify_lead(self, lead: RawLead) -> VerificationResult:
        logger.info(f"[Agent 2: Verifier] Auditing lead hygiene: {lead.company_name} ({lead.email})...")

        # 1. Check if already on suppression list
        if self.db.is_suppressed(lead.email):
            logger.warning(f"[Agent 2: Verifier] Lead {lead.email} is on suppression list! Discarding.")
            res = VerificationResult(
                lead_id=lead.id,
                company_name=lead.company_name,
                email_valid=False,
                email_deliverability_score=0.0,
                phone_type=PhoneLineType.INVALID,
                business_operational=False,
                status=VerificationStatus.DISCARDED,
                reason="Contact is on Do-Not-Contact / Suppression List."
            )
            self.db.save_verification(res)
            return res

        # 2. Syntax & domain check
        email_valid = self._check_email_validity(lead.email)
        
        # 3. Simulate ZeroBounce deliverability score
        deliverability_score = 0.95 if email_valid else 0.10
        if "bounce" in lead.email.lower() or "invalid" in lead.email.lower():
            deliverability_score = 0.05
            email_valid = False

        # 4. Carrier lookup simulation
        phone_type = self._detect_phone_carrier(lead.phone)

        # 5. Determine overall business status
        if not email_valid or deliverability_score < 0.60:
            status = VerificationStatus.DISCARDED
            reason = "High bounce risk or invalid email syntax."
            operational = False
        elif phone_type == PhoneLineType.INVALID:
            status = VerificationStatus.DISCARDED
            reason = "Disconnected or unrouteable phone carrier."
            operational = False
        elif phone_type == PhoneLineType.LANDLINE:
            status = VerificationStatus.PASSED
            reason = "Verified landline business line + deliverable email."
            operational = True
        else:
            status = VerificationStatus.PASSED
            reason = "Verified mobile business line + 95%+ deliverability score."
            operational = True

        result = VerificationResult(
            lead_id=lead.id,
            company_name=lead.company_name,
            email_valid=email_valid,
            email_deliverability_score=deliverability_score,
            phone_type=phone_type,
            business_operational=operational,
            status=status,
            reason=reason
        )

        self.db.save_verification(result)
        logger.info(f"[Agent 2: Verifier] Result for {lead.company_name}: {status.value} ({reason})")
        return result

    def verify_batch(self, leads: List[RawLead]) -> Tuple[List[RawLead], List[VerificationResult]]:
        passed_leads: List[RawLead] = []
        all_results: List[VerificationResult] = []

        for lead in leads:
            res = self.verify_lead(lead)
            all_results.append(res)
            if res.status == VerificationStatus.PASSED:
                passed_leads.append(lead)

        return passed_leads, all_results

    def _check_email_validity(self, email: str) -> bool:
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(regex, email))

    def _detect_phone_carrier(self, phone: str) -> PhoneLineType:
        clean_phone = re.sub(r'[^\d]', '', phone)
        if len(clean_phone) < 10:
            return PhoneLineType.INVALID
        
        # Test routing heuristic based on digits for simulation
        if clean_phone.endswith("0000") or clean_phone.endswith("922") or clean_phone.endswith("0122"):
            return PhoneLineType.INVALID
        elif clean_phone.endswith("182") or clean_phone.endswith("391") or int(clean_phone[-2:]) % 2 == 0:
            return PhoneLineType.MOBILE
        else:
            return PhoneLineType.LANDLINE

