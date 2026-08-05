import json
import re
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.utils.embeddings import embedding_service
from langchain_core.messages import SystemMessage, HumanMessage

class CaptionUnderstandingAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Caption Understanding Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        raw_caption = inputs.get("raw_caption", "")
        campaign_goal = inputs.get("campaign_goal", "Conversions")

        hashtags = re.findall(r"#\w+", raw_caption)

        system_prompt = (
            "You are an expert Social Media Copywriting & Instagram Algorithm Analyst. "
            "Analyze the caption text and return JSON with keys: "
            "clean_caption (string), extracted_hashtags (list of strings), caption_cta (string), "
            "marketing_intent (string), and copy_sentiment (string)."
        )

        user_prompt = (
            f"Instagram Caption: {raw_caption}\n"
            f"Campaign Goal: {campaign_goal}\n"
            f"Extracted Hashtags: {hashtags}\n\n"
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
                "clean_caption": raw_caption,
                "extracted_hashtags": hashtags or ["#marketing", "#reels", "#viral"],
                "caption_cta": "Tap link in bio to shop!",
                "marketing_intent": f"Direct response driving towards {campaign_goal}",
                "copy_sentiment": "Urgent, High Energy"
            }

        embedding = embedding_service.generate_embedding(raw_caption)

        result = {
            "clean_caption": parsed.get("clean_caption", raw_caption),
            "hashtags": parsed.get("extracted_hashtags", hashtags),
            "cta": parsed.get("caption_cta", ""),
            "marketing_intent": parsed.get("marketing_intent", campaign_goal),
            "copy_sentiment": parsed.get("copy_sentiment", "Positive"),
            "semantic_embedding": embedding
        }

        self.log_complete()
        return result

caption_agent = CaptionUnderstandingAgent()
