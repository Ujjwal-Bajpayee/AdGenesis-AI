import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class CreativeBriefAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Creative Brief Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        campaign_goal = inputs.get("campaign_goal", "Direct Sales")
        creative_data = inputs.get("creative_synthesis", {})
        recommendation_data = inputs.get("recommendations", {})

        system_prompt = (
            "You are an Executive Creative Director. Produce a complete, production-ready Creative Brief for an upgraded video version. "
            "Return JSON with keys: campaign_goal (string), target_audience (string), "
            "video_duration (string), opening_hook (string), "
            "scene_by_scene_breakdown (list of objects with keys 'scene_number', 'timestamp', 'visual', 'audio', 'text_overlay'), "
            "voiceover_script (string), music_recommendation (string), visual_style (string), "
            "cta (string), caption (string), and hashtags (list of strings)."
        )

        user_prompt = (
            f"Campaign Goal: {campaign_goal}\n"
            f"Target Audience: {creative_data.get('target_audience')}\n"
            f"Recommended Hook: {recommendation_data.get('better_hook')}\n"
            f"Recommended Storytelling: {recommendation_data.get('better_storytelling')}\n\n"
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
                "campaign_goal": campaign_goal,
                "target_audience": "Tech-savvy professionals and digital creators aged 21-38",
                "video_duration": "15 Seconds",
                "opening_hook": recommendation_data.get("better_hook", "Stop scrolling if you want 3x conversions today!"),
                "scene_by_scene_breakdown": [
                    {"scene_number": 1, "timestamp": "0.0s - 3.0s", "visual": "Fast zoom-in on product, bold red overlay badge", "audio": "Punchy bass drop & voiceover hook", "text_overlay": "WANT 3X RESULTS?"},
                    {"scene_number": 2, "timestamp": "3.0s - 9.0s", "visual": "Side-by-side split screen showing before vs after", "audio": "Upbeat synth rhythm with upbeat narration", "text_overlay": "BEFORE vs AFTER"},
                    {"scene_number": 3, "timestamp": "9.0s - 15.0s", "visual": "Hero shot of product with glowing CTA button", "audio": "Vocal crescendo and final claim", "text_overlay": "CLAIM YOUR DISCOUNT NOW"}
                ],
                "voiceover_script": "Tired of low ad performance? Watch how simple changes can triple your engagement in seconds. Click link in bio to start!",
                "music_recommendation": "128 BPM Energetic Tech House track with build-up at second 3.",
                "visual_style": "Modern dark mode, neon accent highlights, high contrast typography.",
                "cta": recommendation_data.get("better_cta", "LINK IN BIO TO ORDER"),
                "caption": recommendation_data.get("better_caption", "Upgrade your marketing game today! Tap the link in our bio."),
                "hashtags": recommendation_data.get("better_hashtags", ["#AdGenesis", "#MarketingAI", "#ReelsStrategy"])
            }

        result = {
            "campaign_goal": parsed.get("campaign_goal", campaign_goal),
            "target_audience": parsed.get("target_audience", ""),
            "video_duration": parsed.get("video_duration", "15s"),
            "opening_hook": parsed.get("opening_hook", ""),
            "scene_by_scene_breakdown": parsed.get("scene_by_scene_breakdown", []),
            "voiceover_script": parsed.get("voiceover_script", ""),
            "music_recommendation": parsed.get("music_recommendation", ""),
            "visual_style": parsed.get("visual_style", ""),
            "cta": parsed.get("cta", ""),
            "caption": parsed.get("caption", ""),
            "hashtags": parsed.get("hashtags", [])
        }

        self.log_complete()
        return result

creative_brief_agent = CreativeBriefAgent()
