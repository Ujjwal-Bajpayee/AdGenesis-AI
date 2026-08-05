import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Recommendation Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        creative_data = inputs.get("creative_synthesis", {})
        prediction_data = inputs.get("prediction", {})
        caption_data = inputs.get("caption_analysis", {})

        system_prompt = (
            "You are a Conversion Rate Optimization (CRO) Expert and Viral Video Producer. "
            "Generate actionable creative optimization recommendations. Return JSON with keys: "
            "better_hook (string), better_opening (string), better_pacing (string), "
            "better_cta (string), better_caption (string), better_hashtags (list of strings), "
            "better_ending (string), and better_storytelling (string)."
        )

        user_prompt = (
            f"Current Weaknesses: {creative_data.get('weaknesses')}\n"
            f"Current Hook: {creative_data.get('hook_evaluation')}\n"
            f"Quality Score: {prediction_data.get('overall_quality_score')}\n"
            f"Current Caption: {caption_data.get('clean_caption')}\n\n"
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
                "better_hook": "Start with a high-contrast pattern interrupt question: 'Stop scrolling if you want X results in 5 seconds!'",
                "better_opening": "Use split-screen visual comparison in frame 1.",
                "better_pacing": "Increase cut speed by 15% between second 3 and 7 to prevent drop-off.",
                "better_cta": "Add animated text callout: 'Claim 20% Off - Link in Bio!'",
                "better_caption": "Lead with a bold hook line, add 3 bullet proof points, and conclude with direct link CTA.",
                "better_hashtags": ["#marketinghacks", "#instagramgrowth", "#viralreels"],
                "better_ending": "End on strong freeze-frame featuring product offer and countdown badge.",
                "better_storytelling": "Structure as: Pain Point -> Instant Solution -> Live Proof -> Immediate CTA."
            }

        result = {
            "better_hook": parsed.get("better_hook", ""),
            "better_opening": parsed.get("better_opening", ""),
            "better_pacing": parsed.get("better_pacing", ""),
            "better_cta": parsed.get("better_cta", ""),
            "better_caption": parsed.get("better_caption", ""),
            "better_hashtags": parsed.get("better_hashtags", []),
            "better_ending": parsed.get("better_ending", ""),
            "better_storytelling": parsed.get("better_storytelling", "")
        }

        self.log_complete()
        return result

recommendation_agent = RecommendationAgent()
