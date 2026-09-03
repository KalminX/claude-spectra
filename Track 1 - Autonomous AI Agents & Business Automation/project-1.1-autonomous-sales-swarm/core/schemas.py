from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class TradeNiche(str, Enum):
    PLUMBING = "Plumbing"
    HVAC = "HVAC"
    ROOFING = "Roofing"
    ELECTRICAL = "Electrical"

class PhoneLineType(str, Enum):
    MOBILE = "mobile"
    LANDLINE = "landline"
    VOIP = "voip"
    INVALID = "invalid"

class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FLAGGED = "FLAGGED"
    DISCARDED = "DISCARDED"

class ReplyIntentType(str, Enum):
    POSITIVE_INTEREST = "POSITIVE_INTEREST"
    OBJECTION_PRICE = "OBJECTION_PRICE"
    OBJECTION_COMPLEXITY = "OBJECTION_COMPLEXITY"
    OBJECTION_ALREADY_HAVE = "OBJECTION_ALREADY_HAVE"
    UNSUBSCRIBE = "UNSUBSCRIBE"
    UNCLEAR = "UNCLEAR"

class ReviewItem(BaseModel):
    author: str
    rating: int
    text: str
    date: str
    mentions_missed_call: bool = False

class RawLead(BaseModel):
    id: str
    company_name: str
    owner_name: Optional[str] = "Owner"
    niche: TradeNiche
    city: str
    state: str
    phone: str
    email: str
    website: str
    reviews: List[ReviewItem] = Field(default_factory=list)
    has_24_7_service_claim: bool = False

class VerificationResult(BaseModel):
    lead_id: str
    company_name: str
    email_valid: bool
    email_deliverability_score: float
    phone_type: PhoneLineType
    business_operational: bool
    status: VerificationStatus
    reason: str

class PersonalizedHook(BaseModel):
    lead_id: str
    company_name: str
    estimated_monthly_missed_calls: int
    estimated_ticket_value: float
    estimated_monthly_lost_revenue: float
    specific_pain_point: str
    subject_line: str
    email_body_3_sentences: str
    sms_body: str

class InboundReply(BaseModel):
    lead_id: str
    company_name: str
    channel: str = "email" # "email" or "sms"
    sender: str
    content: str
    timestamp: str

class CloserResponse(BaseModel):
    lead_id: str
    company_name: str
    detected_intent: ReplyIntentType
    confidence: float
    reasoning: str
    response_message: str
    action_taken: str
    demo_link_included: bool = False

class CampaignMetrics(BaseModel):
    total_leads_scouted: int = 0
    verified_leads: int = 0
    outreach_sent: int = 0
    replies_received: int = 0
    positive_replies: int = 0
    objections_handled: int = 0
    unsubscribes: int = 0
    demos_booked: int = 0

class PromptRefinement(BaseModel):
    batch_id: str
    analysis_summary: str
    weak_patterns_detected: List[str]
    improved_subject_lines: List[str]
    adjusted_hook_angles: List[str]
    expected_conversion_gain: str
