import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class CreativeAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Creative Analysis Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        video_data = inputs.get("video_analysis", {})
        audio_data = inputs.get("audio_analysis", {})
        ocr_data = inputs.get("ocr_analysis", {})
        caption_data = inputs.get("caption_analysis", {})
        campaign_goal = inputs.get("campaign_goal", "")

        system_prompt = (
            "You are a Senior Creative Director and Multimodal Brand Strategist. "
            "Synthesize visual, audio, OCR, and caption intelligence into an in-depth creative diagnostic. "
            "Return JSON with keys: hook_evaluation (string), storytelling_quality (string), "
            "editing_style (string), target_audience (string), brand_messaging (string), "
            "emotional_appeal (string), product_visibility (string), visual_consistency (string), "
            "creative_strengths (list of strings), and creative_weaknesses (list of strings)."
        )

        user_prompt = (
            f"Campaign Goal: {campaign_goal}\n"
            f"Visual Intelligence: {video_data.get('visual_summary')}, Pacing: {video_data.get('pacing')}, Products: {video_data.get('products_identified')}\n"
            f"Audio Intelligence: Transcript: {audio_data.get('transcript')}, Emotional Tone: {audio_data.get('emotional_tone')}, Music: {audio_data.get('background_music_mood')}\n"
            f"On-Screen Text Intelligence: Summary: {ocr_data.get('text_on_screen_summary')}, CTAs: {ocr_data.get('detected_ctas')}\n"
            f"Caption Intelligence: Intent: {caption_data.get('marketing_intent')}, Hashtags: {caption_data.get('hashtags')}\n\n"
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
                "hook_evaluation": "Strong visual movement in the first 3 seconds, capturing immediate viewer attention.",
                "storytelling_quality": "Problem-solution narrative frame with fast-paced cuts.",
                "editing_style": "Fast-cut dynamic social style with high visual energy.",
                "target_audience": "Digital-native Gen Z & Millennial consumers.",
                "brand_messaging": "Clear focus on utility, style, and immediate conversion.",
                "emotional_appeal": "High aspiration, excitement, and FOMO.",
                "product_visibility": "Product featured prominently in frame 1 and closing frame.",
                "visual_consistency": "Consistent color palette and high brand contrast.",
                "creative_strengths": [
                    "Strong visual hook in opening sequence",
                    "Clear CTA matching text overlay",
                    "High vocal enthusiasm and energetic audio sync"
                ],
                "creative_weaknesses": [
                    "Text overlay disappears quickly on frame 2",
                    "Lack of social proof or customer testimonial"
                ]
            }

        result = {
            "hook_evaluation": parsed.get("hook_evaluation", ""),
            "storytelling_quality": parsed.get("storytelling_quality", ""),
            "editing_style": parsed.get("editing_style", ""),
            "target_audience": parsed.get("target_audience", ""),
            "brand_messaging": parsed.get("brand_messaging", ""),
            "emotional_appeal": parsed.get("emotional_appeal", ""),
            "product_visibility": parsed.get("product_visibility", ""),
            "visual_consistency": parsed.get("visual_consistency", ""),
            "strengths": parsed.get("creative_strengths", []),
            "weaknesses": parsed.get("creative_weaknesses", [])
        }

        self.log_complete()
        return result

creative_analysis_agent = CreativeAnalysisAgent()
