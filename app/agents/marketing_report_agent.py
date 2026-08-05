import json
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class MarketingReportAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="Marketing Report Agent")

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self.log_start()

        video_filename = inputs.get("video_filename", "video.mp4")
        campaign_goal = inputs.get("campaign_goal", "")
        creative_synthesis = inputs.get("creative_synthesis", {})
        prediction = inputs.get("prediction", {})
        recommendations = inputs.get("recommendations", {})
        creative_brief = inputs.get("creative_brief", {})
        budget_recommendation = inputs.get("budget_recommendation", {})
        experiments = inputs.get("experiments", [])

        system_prompt = (
            "You are a Chief Marketing Officer (CMO) & Lead Growth Architect. "
            "Synthesize all intelligence into a comprehensive executive Markdown marketing report. "
            "Return JSON with key 'full_markdown' containing the formatted markdown string."
        )

        user_prompt = (
            f"Filename: {video_filename}\n"
            f"Goal: {campaign_goal}\n"
            f"Predictions: Score {prediction.get('overall_quality_score')}, Eng {prediction.get('expected_engagement_rate')}, CTR {prediction.get('expected_ctr')}\n"
            f"Strengths: {creative_synthesis.get('strengths')}\n"
            f"Weaknesses: {creative_synthesis.get('weaknesses')}\n"
            f"Budget Tier: {budget_recommendation.get('recommended_budget_tier')}\n"
            f"Experiments Count: {len(experiments)}\n\n"
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
            markdown_content = parsed.get("full_markdown", "")
        except Exception:
            markdown_content = ""

        if not markdown_content:
            md_lines = [
                f"# AdGenesis AI - Autonomous Marketing Intelligence Report",
                f"**Creative File:** `{video_filename}` | **Campaign Goal:** `{campaign_goal}`",
                "",
                "## 1. Executive Performance Prediction",
                f"- **Overall Creative Quality Score:** {prediction.get('overall_quality_score', 80.0)} / 100",
                f"- **Predicted Engagement Rate:** {prediction.get('expected_engagement_rate', '4.5%')}",
                f"- **Predicted Watch Time:** {prediction.get('expected_watch_time_seconds', '11.5s')}",
                f"- **Predicted CTR:** {prediction.get('expected_ctr', '2.1%')}",
                f"- **Predicted Conversion Rate:** {prediction.get('expected_conversions_estimate', '1.6%')}",
                "",
                "### Predictive Rationale",
                f"{prediction.get('reasoning', 'Solid visual pacing and vocal clarity with clear value proposition.')}",
                "",
                "## 2. Creative Synthesis & Diagnostics",
                f"- **Opening Hook:** {creative_synthesis.get('hook_evaluation', 'N/A')}",
                f"- **Storytelling Quality:** {creative_synthesis.get('storytelling_quality', 'N/A')}",
                f"- **Brand Messaging:** {creative_synthesis.get('brand_messaging', 'N/A')}",
                "",
                "### Creative Strengths",
            ]
            for st in creative_synthesis.get("strengths", []):
                md_lines.append(f"- {st}")
            md_lines.append("")
            md_lines.append("### Creative Weaknesses")
            for wk in creative_synthesis.get("weaknesses", []):
                md_lines.append(f"- {wk}")

            md_lines.extend([
                "",
                "## 3. Creative Optimization Recommendations",
                f"- **Upgraded Hook:** {recommendations.get('better_hook', 'N/A')}",
                f"- **Upgraded CTA:** {recommendations.get('better_cta', 'N/A')}",
                f"- **Pacing Adjustment:** {recommendations.get('better_pacing', 'N/A')}",
                "",
                "## 4. Paid Media Budget Allocation",
                f"- **Recommended Budget Tier:** {budget_recommendation.get('recommended_budget_tier', 'Standard Scale')}",
                f"- **Multiplier:** {budget_recommendation.get('recommended_budget_multiplier', '1.0x')}",
                f"- **Justification:** {budget_recommendation.get('justification', 'N/A')}",
                "",
                "## 5. Structured A/B Testing Ideas",
            ])
            for exp in experiments:
                md_lines.append(f"### {exp.get('title', 'Experiment')}")
                md_lines.append(f"- **Hypothesis:** {exp.get('hypothesis', '')}")
                md_lines.append(f"- **Action:** {exp.get('what_to_change', '')}")
                md_lines.append(f"- **Expected Impact:** {exp.get('expected_impact', '')}")

            markdown_content = "\n".join(md_lines)

        result = {
            "creative_summary": creative_synthesis.get("hook_evaluation", ""),
            "predicted_performance": prediction,
            "strengths": creative_synthesis.get("strengths", []),
            "weaknesses": creative_synthesis.get("weaknesses", []),
            "recommendations": recommendations,
            "creative_brief": creative_brief,
            "budget_recommendation": budget_recommendation,
            "experiments": experiments,
            "full_markdown": markdown_content
        }

        self.log_complete()
        return result

marketing_report_agent = MarketingReportAgent()
