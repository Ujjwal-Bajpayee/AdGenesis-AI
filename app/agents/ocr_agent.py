import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class OCRAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="OCR Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        raw_texts = inputs.get("raw_texts", [])
        cleaned_texts = inputs.get("cleaned_texts", [])
        detected_ctas = inputs.get("detected_ctas", [])
        text_summary = inputs.get("text_on_screen_summary", "")

        system_prompt = (
            "You are an expert On-Screen Text & Typography Analyst for Instagram ad creatives. "
            "Clean and categorize screen text. Return JSON with keys: "
            "structured_text_lines (list of strings), primary_call_to_action (string), "
            "text_readability_score (string), and overlay_summary (string)."
        )

        user_prompt = (
            f"Extracted Raw Texts: {raw_texts}\n"
            f"Cleaned Text Lines: {cleaned_texts}\n"
            f"Detected CTAs: {detected_ctas}\n"
            f"Text Summary: {text_summary}\n\n"
            "Return valid JSON only."
        )

        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].strip()
            parsed = json.loads(content)
        except Exception:
            parsed = {
                "structured_text_lines": cleaned_texts,
                "primary_call_to_action": detected_ctas[0] if detected_ctas else "LINK IN BIO",
                "text_readability_score": "High contrast, high readability",
                "overlay_summary": text_summary
            }

        result = {
            "raw_texts": raw_texts,
            "cleaned_texts": parsed.get("structured_text_lines", cleaned_texts),
            "detected_ctas": detected_ctas or [parsed.get("primary_call_to_action", "SHOP NOW")],
            "primary_cta": parsed.get("primary_call_to_action", "SHOP NOW"),
            "text_readability_score": parsed.get("text_readability_score", "High"),
            "text_on_screen_summary": parsed.get("overlay_summary", text_summary)
        }

        self.log_complete()
        return result

ocr_agent = OCRAgent()
