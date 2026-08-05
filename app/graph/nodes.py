from datetime import datetime
from typing import Dict, Any
from app.graph.state import AdGenesisState
from app.agents import (
    video_analysis_agent, audio_analysis_agent, ocr_agent, caption_agent,
    creative_analysis_agent, prediction_agent, recommendation_agent,
    creative_brief_agent, experiment_agent, budget_recommendation_agent,
    marketing_report_agent
)
from app.core.logger import logger

def _record_agent_execution(state: AdGenesisState, agent_name: str) -> Dict[str, Any]:
    exec_order = list(state.get("execution_order", []))
    exec_order.append(agent_name)
    
    logs = list(state.get("agent_logs", []))
    logs.append({
        "agent": agent_name,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "success"
    })
    return {
        "current_agent": agent_name,
        "execution_order": exec_order,
        "agent_logs": logs
    }

async def video_analysis_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Video Analysis Node")
    media_meta = state.get("media_metadata", {})
    inputs = {
        "frame_paths": media_meta.get("frame_paths", []),
        "scenes_count": media_meta.get("scenes_count", 1),
        "pacing": media_meta.get("pacing", "Medium"),
        "motion_score": media_meta.get("motion_score", 10.0),
        "duration_seconds": media_meta.get("duration_seconds", 15.0),
        "campaign_goal": state.get("campaign_goal", "")
    }
    result = await video_analysis_agent.run(inputs)
    rec = _record_agent_execution(state, "Video Analysis Agent")
    return {"video_analysis": result, **rec}

async def audio_analysis_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Audio Analysis Node")
    audio_data = state.get("raw_audio_data", {})
    result = await audio_analysis_agent.run(audio_data)
    rec = _record_agent_execution(state, "Audio Analysis Agent")
    return {"audio_analysis": result, **rec}

async def ocr_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing OCR Node")
    raw_ocr = state.get("raw_ocr_data", {})
    result = await ocr_agent.run(raw_ocr)
    rec = _record_agent_execution(state, "OCR Agent")
    return {"ocr_analysis": result, **rec}

async def caption_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Caption Node")
    inputs = {
        "raw_caption": state.get("raw_caption", ""),
        "campaign_goal": state.get("campaign_goal", "")
    }
    result = await caption_agent.run(inputs)
    rec = _record_agent_execution(state, "Caption Understanding Agent")
    return {"caption_analysis": result, **rec}

async def creative_analysis_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Creative Analysis Node")
    inputs = {
        "video_analysis": state.get("video_analysis", {}),
        "audio_analysis": state.get("audio_analysis", {}),
        "ocr_analysis": state.get("ocr_analysis", {}),
        "caption_analysis": state.get("caption_analysis", {}),
        "campaign_goal": state.get("campaign_goal", "")
    }
    result = await creative_analysis_agent.run(inputs)
    rec = _record_agent_execution(state, "Creative Analysis Agent")
    return {"creative_synthesis": result, **rec}

async def prediction_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Prediction Node")
    inputs = {
        "creative_synthesis": state.get("creative_synthesis", {}),
        "video_analysis": state.get("video_analysis", {}),
        "audio_analysis": state.get("audio_analysis", {}),
        "campaign_goal": state.get("campaign_goal", "")
    }
    result = await prediction_agent.run(inputs)
    rec = _record_agent_execution(state, "Prediction Agent")
    return {"prediction": result, **rec}

async def recommendation_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Recommendation Node")
    inputs = {
        "creative_synthesis": state.get("creative_synthesis", {}),
        "prediction": state.get("prediction", {}),
        "caption_analysis": state.get("caption_analysis", {})
    }
    result = await recommendation_agent.run(inputs)
    rec = _record_agent_execution(state, "Recommendation Agent")
    return {"recommendations": result, **rec}

async def creative_brief_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Creative Brief Node")
    inputs = {
        "campaign_goal": state.get("campaign_goal", ""),
        "creative_synthesis": state.get("creative_synthesis", {}),
        "recommendations": state.get("recommendations", {})
    }
    result = await creative_brief_agent.run(inputs)
    rec = _record_agent_execution(state, "Creative Brief Agent")
    return {"creative_brief": result, **rec}

async def experiment_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Experiment Node")
    inputs = {
        "creative_synthesis": state.get("creative_synthesis", {}),
        "recommendations": state.get("recommendations", {})
    }
    result = await experiment_agent.run(inputs)
    rec = _record_agent_execution(state, "Experiment Agent")
    return {"experiments": result.get("experiments", []), **rec}

async def budget_recommendation_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Budget Recommendation Node")
    inputs = {
        "prediction": state.get("prediction", {})
    }
    result = await budget_recommendation_agent.run(inputs)
    rec = _record_agent_execution(state, "Budget Recommendation Agent")
    return {"budget_recommendation": result, **rec}

async def marketing_report_node(state: AdGenesisState) -> Dict[str, Any]:
    logger.info("Executing Marketing Report Node")
    inputs = {
        "video_filename": state.get("video_filename", ""),
        "campaign_goal": state.get("campaign_goal", ""),
        "creative_synthesis": state.get("creative_synthesis", {}),
        "prediction": state.get("prediction", {}),
        "recommendations": state.get("recommendations", {}),
        "creative_brief": state.get("creative_brief", {}),
        "budget_recommendation": state.get("budget_recommendation", {}),
        "experiments": state.get("experiments", [])
    }
    result = await marketing_report_agent.run(inputs)
    rec = _record_agent_execution(state, "Marketing Report Agent")
    return {"marketing_report": result, "status": "completed", **rec}
