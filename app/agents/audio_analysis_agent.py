import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class AudioAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Audio Analysis Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        transcript = inputs.get("transcript", "")
        wpm = inputs.get("speaking_speed_wpm", 0.0)
        tempo = inputs.get("tempo_bpm", 120.0)
        music_mood = inputs.get("music_mood", "Upbeat")
        energy_level = inputs.get("energy_level", "Moderate")

        system_prompt = (
            "You are an expert Audio and Vocal Intelligence Analyst for social media video ads. "
            "Analyze the voice transcript, tempo, and energy to return JSON with keys: "
            "refined_transcript (string), speaking_speed_evaluation (string), "
            "emotional_tone (string), background_music_analysis (string), and has_voiceover (bool)."
        )

        user_prompt = (
            f"Transcript: {transcript}\n"
            f"Speaking Speed (WPM): {wpm}\n"
            f"Music Tempo (BPM): {tempo}\n"
            f"Music Mood: {music_mood}\n"
            f"Energy Level: {energy_level}\n\n"
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
                "refined_transcript": transcript,
                "speaking_speed_evaluation": f"{wpm} WPM - Optimal pacing for viewer retention",
                "emotional_tone": "Energetic, Convincing & Friendly",
                "background_music_analysis": f"{music_mood} track at {tempo} BPM matching visual flow.",
                "has_voiceover": len(transcript) > 10
            }

        result = {
            "transcript": parsed.get("refined_transcript", transcript),
            "speaking_speed_wpm": wpm,
            "speaking_speed_evaluation": parsed.get("speaking_speed_evaluation", ""),
            "emotional_tone": parsed.get("emotional_tone", "Positive"),
            "background_music_mood": music_mood,
            "background_music_analysis": parsed.get("background_music_analysis", ""),
            "has_voiceover": parsed.get("has_voiceover", True)
        }

        self.log_complete()
        return result

audio_analysis_agent = AudioAnalysisAgent()
