import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class BudgetRecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Budget Recommendation Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        prediction_data = inputs.get("prediction", {})
        score = prediction_data.get("overall_quality_score", 75.0)
        engagement = prediction_data.get("expected_engagement_rate", "3.0%")

        system_prompt = (
            "You are a Senior Media Director & Paid Social Budget Strategist. "
            "Evaluate the creative performance indicators and determine paid ad budget allocation. "
            "Return JSON with keys: recommended_budget_tier (string: e.g. 'Scale Tier ($1,000+/day)', 'Testing Tier ($100/day)', 'Hold / Revamp'), "
            "recommended_budget_multiplier (string e.g. '1.5x Standard Allocation'), "
            "scaling_recommendation (string), and justification (string explaining why)."
        )

        user_prompt = (
            f"Overall Quality Score: {score}/100\n"
            f"Predicted Engagement Rate: {engagement}\n"
            f"Predicted CTR: {prediction_data.get('expected_ctr')}\n"
            f"Reasoning: {prediction_data.get('reasoning')}\n\n"
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
            tier = "High Scale ($1,000+/day)" if score >= 80 else ("Testing Allocation ($100/day)" if score >= 60 else "Low / Pause & Revamp")
            parsed = {
                "recommended_budget_tier": tier,
                "recommended_budget_multiplier": "1.5x Base Budget",
                "scaling_recommendation": "Aggressive scaling across lookalike and broad interest audiences.",
                "justification": f"Overall quality score of {score}/100 and predicted CTR of {prediction_data.get('expected_ctr')} indicate high ROAS potential."
            }

        result = {
            "recommended_budget_tier": parsed.get("recommended_budget_tier", "Standard Scale"),
            "recommended_budget_multiplier": parsed.get("recommended_budget_multiplier", "1.0x"),
            "scaling_recommendation": parsed.get("scaling_recommendation", ""),
            "justification": parsed.get("justification", "")
        }

        self.log_complete()
        return result

budget_recommendation_agent = BudgetRecommendationAgent()
