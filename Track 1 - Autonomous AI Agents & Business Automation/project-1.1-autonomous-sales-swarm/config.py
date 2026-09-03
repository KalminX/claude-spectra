import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from project directory or root if present
project_dir = Path(__file__).parent
load_dotenv(project_dir / ".env")
load_dotenv(project_dir.parent.parent / ".env")

class Settings(BaseSettings):
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini").lower()
    DISPLAY_MODEL: str = os.getenv("DISPLAY_MODEL", "Claude 3.5 Sonnet")
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Offer config
    PRODUCT_NAME: str = os.getenv("PRODUCT_NAME", "SkillsVital Voice AI")
    OFFER_URL: str = os.getenv("OFFER_URL", "https://skillsvital.com/voice")
    DEMO_PHONE_NUMBER: str = os.getenv("DEMO_PHONE_NUMBER", "+1 (888) 548-3782")
    CALENDLY_URL: str = os.getenv("CALENDLY_URL", "https://calendly.com/skillsvital/voice-demo")
    STRIPE_CHECKOUT_URL: str = os.getenv("STRIPE_CHECKOUT_URL", "https://buy.stripe.com/test_voice_receptionist_monthly")
    
    # DB
    DATABASE_PATH: str = str(project_dir / os.getenv("DATABASE_PATH", "swarm_leads.db"))
    
    # Webhooks
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "127.0.0.1")
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", 8000))

settings = Settings()
