from langgraph.graph import StateGraph, END
from app.graph.state import AdGenesisState
from app.graph.nodes import (
    video_analysis_node, audio_analysis_node, ocr_node, caption_node,
    creative_analysis_node, prediction_node, recommendation_node,
    creative_brief_node, experiment_node, budget_recommendation_node,
    marketing_report_node
)

def build_workflow():
    builder = StateGraph(AdGenesisState)

    builder.add_node("video_analysis", video_analysis_node)
    builder.add_node("audio_analysis", audio_analysis_node)
    builder.add_node("ocr_analysis", ocr_node)
    builder.add_node("caption_analysis", caption_node)
    builder.add_node("creative_synthesis", creative_analysis_node)
    builder.add_node("prediction", prediction_node)
    builder.add_node("recommendations", recommendation_node)
    builder.add_node("creative_brief", creative_brief_node)
    builder.add_node("experiments", experiment_node)
    builder.add_node("budget_recommendation", budget_recommendation_node)
    builder.add_node("marketing_report", marketing_report_node)

    builder.set_entry_point("video_analysis")
    
    builder.add_edge("video_analysis", "audio_analysis")
    builder.add_edge("audio_analysis", "ocr_analysis")
    builder.add_edge("ocr_analysis", "caption_analysis")
    builder.add_edge("caption_analysis", "creative_synthesis")
    
    builder.add_edge("creative_synthesis", "prediction")
    builder.add_edge("prediction", "recommendations")
    
    builder.add_edge("recommendations", "creative_brief")
    builder.add_edge("creative_brief", "experiments")
    builder.add_edge("experiments", "budget_recommendation")
    builder.add_edge("budget_recommendation", "marketing_report")
    
    builder.add_edge("marketing_report", END)

    return builder.compile()

compiled_workflow = build_workflow()
