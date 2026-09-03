import os
import json
import logging
from pathlib import Path
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure .env is loaded
project_dir = Path(__file__).parent.parent
load_dotenv(project_dir / ".env")
load_dotenv(project_dir.parent.parent / ".env")

logger = logging.getLogger("SwarmLLM")

T = TypeVar("T", bound=BaseModel)

class UniversalLLM:
    """
    Universal AI-Agnostic LLM Client.
    Supports:
    - Google Gemini (Gemini 2.5 Flash / Pro) via google.genai
    - Anthropic Claude (Claude 3.5 Sonnet / Haiku) via anthropic
    - Deterministic Sandbox Mode ($0 offline execution)
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower()
        self.display_model = os.getenv("DISPLAY_MODEL", "Claude 3.5 Sonnet")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip('"').strip("'")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip('"').strip("'")

        # Auto-fallback to sandbox if keys are missing or invalid
        if self.provider == "gemini" and (not self.gemini_key or not self.gemini_key.startswith("AIzaSy")):
            logger.info("No valid Google AI Studio GEMINI_API_KEY detected. Operating in High-Fidelity Sandbox Mode ($0 Simulation).")
            self.provider = "sandbox"
        elif self.provider == "anthropic" and (not self.anthropic_key or not self.anthropic_key.startswith("sk-ant-")):
            logger.info("No valid Anthropic ANTHROPIC_API_KEY detected. Operating in High-Fidelity Sandbox Mode ($0 Simulation).")
            self.provider = "sandbox"


        self._init_clients()

    def _init_clients(self):
        self.gemini_client = None
        self.anthropic_client = None

        if self.provider == "gemini" and self.gemini_key:
            from google import genai
            self.gemini_client = genai.Client(api_key=self.gemini_key)
        elif self.provider == "anthropic" and self.anthropic_key:
            import anthropic
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)

    def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        system_instruction: str = "",
        sandbox_fallback_data: Optional[dict] = None
    ) -> T:
        """
        Generate guaranteed structured output conforming to a Pydantic schema.
        """
        if self.provider == "gemini" and self.gemini_client:
            try:
                from google.genai import types
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    system_instruction=system_instruction or "You are an expert AI sales orchestration agent."
                )
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=config
                )
                return schema.model_validate_json(response.text)
            except Exception as e:
                logger.warning(f"Gemini API call error: {e}. Falling back to sandbox response.")
                if sandbox_fallback_data:
                    return schema.model_validate(sandbox_fallback_data)
                raise

        elif self.provider == "anthropic" and self.anthropic_client:
            try:
                # Use Claude tool calling to enforce structured schema
                tool_schema = {
                    "name": "record_output",
                    "description": "Record the required structured output",
                    "input_schema": schema.model_json_schema()
                }
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-latest",
                    max_tokens=2048,
                    system=system_instruction or "You are an expert AI sales orchestration agent.",
                    tools=[tool_schema],
                    tool_choice={"type": "tool", "name": "record_output"},
                    messages=[{"role": "user", "content": prompt}]
                )
                for block in response.content:
                    if block.type == "tool_use" and block.name == "record_output":
                        return schema.model_validate(block.input)
            except Exception as e:
                logger.warning(f"Anthropic API call error: {e}. Falling back to sandbox response.")
                if sandbox_fallback_data:
                    return schema.model_validate(sandbox_fallback_data)
                raise

        # Sandbox / deterministic fallback
        if sandbox_fallback_data:
            return schema.model_validate(sandbox_fallback_data)
        
        # Generic default instance if no mock passed
        try:
            return schema()
        except Exception:
            raise ValueError(f"No sandbox fallback data provided for {schema.__name__}")

    def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """
        Generate plain text response.
        """
        if self.provider == "gemini" and self.gemini_client:
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"system_instruction": system_instruction}
            )
            return response.text
        elif self.provider == "anthropic" and self.anthropic_client:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1024,
                system=system_instruction,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        return f"[Sandbox Mode Output - Model: {self.display_model}] Generated response for: {prompt[:40]}..."

# Global singleton
llm_client = UniversalLLM()
