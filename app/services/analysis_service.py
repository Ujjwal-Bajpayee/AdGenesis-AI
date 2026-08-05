import os
import uuid
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from app.storage.file_storage import file_storage
from app.repositories.analysis_repository import analysis_repository
from app.pipelines.media_pipeline import media_pipeline
from app.graph.workflow import compiled_workflow
from app.models.brief import CreativeBriefDocument
from app.models.report import MarketingReportDocument
from app.models.workflow import WorkflowStateDocument
from app.utils.pdf_exporter import pdf_exporter
from app.core.logger import logger

class AnalysisService:
    async def start_analysis(self, filename: str, content: bytes, caption: str, campaign_goal: str) -> str:
        analysis_id = str(uuid.uuid4())
        file_path = file_storage.save_uploaded_file(analysis_id, filename, content)
        
        await analysis_repository.create_analysis(
            analysis_id=analysis_id,
            filename=filename,
            path=file_path,
            caption=caption,
            goal=campaign_goal
        )

        wf_doc = WorkflowStateDocument(
            workflow_id=analysis_id,
            analysis_id=analysis_id,
            current_agent="media_pipeline",
            status="processing",
            execution_order=["Media Extraction Pipeline"],
            agent_logs=[{
                "agent": "Media Extraction Pipeline",
                "timestamp": datetime.utcnow().isoformat(),
                "status": "started"
            }]
        )
        await analysis_repository.save_workflow_state(wf_doc)

        asyncio.create_task(self._run_async_pipeline(analysis_id, file_path, filename, caption, campaign_goal))

        return analysis_id

    async def _run_async_pipeline(self, analysis_id: str, file_path: str, filename: str, caption: str, campaign_goal: str):
        try:
            extracted_media = media_pipeline.process_media(analysis_id, file_path)
            
            initial_state = {
                "analysis_id": analysis_id,
                "video_path": file_path,
                "video_filename": filename,
                "raw_caption": caption,
                "campaign_goal": campaign_goal,
                "media_metadata": extracted_media.get("media_metadata", {}),
                "raw_ocr_data": extracted_media.get("raw_ocr_data", {}),
                "raw_audio_data": extracted_media.get("raw_audio_data", {}),
                "video_analysis": {},
                "audio_analysis": {},
                "ocr_analysis": {},
                "caption_analysis": {},
                "creative_synthesis": {},
                "prediction": {},
                "recommendations": {},
                "creative_brief": {},
                "experiments": [],
                "budget_recommendation": {},
                "marketing_report": {},
                "current_agent": "video_analysis",
                "execution_order": ["Media Extraction Pipeline"],
                "agent_logs": [],
                "error": "",
                "status": "processing"
            }

            final_state = await compiled_workflow.ainvoke(initial_state)

            pdf_filename = f"report_{analysis_id}.pdf"
            pdf_path = os.path.join(file_storage.get_analysis_dir(analysis_id), pdf_filename)
            
            report_dict = final_state.get("marketing_report", {})
            pdf_exporter.generate_pdf_report(final_state, pdf_path)

            brief_data = final_state.get("creative_brief", {})
            brief_doc = CreativeBriefDocument(
                brief_id=str(uuid.uuid4()),
                analysis_id=analysis_id,
                campaign_goal=campaign_goal,
                target_audience=brief_data.get("target_audience", ""),
                video_duration=brief_data.get("video_duration", ""),
                opening_hook=brief_data.get("opening_hook", ""),
                scene_by_scene_breakdown=brief_data.get("scene_by_scene_breakdown", []),
                voiceover_script=brief_data.get("voiceover_script", ""),
                music_recommendation=brief_data.get("music_recommendation", ""),
                visual_style=brief_data.get("visual_style", ""),
                cta=brief_data.get("cta", ""),
                caption=brief_data.get("caption", ""),
                hashtags=brief_data.get("hashtags", [])
            )
            await analysis_repository.save_creative_brief(brief_doc)

            report_doc = MarketingReportDocument(
                report_id=str(uuid.uuid4()),
                analysis_id=analysis_id,
                title=f"Marketing Intelligence Report - {filename}",
                markdown_content=report_dict.get("full_markdown", ""),
                json_data=final_state,
                pdf_path=pdf_path
            )
            await analysis_repository.save_marketing_report(report_doc)

            await analysis_repository.update_analysis_results(analysis_id, {
                "status": "completed",
                "video_analysis": final_state.get("video_analysis", {}),
                "audio_analysis": final_state.get("audio_analysis", {}),
                "ocr_analysis": final_state.get("ocr_analysis", {}),
                "caption_analysis": final_state.get("caption_analysis", {}),
                "creative_synthesis": final_state.get("creative_synthesis", {}),
                "prediction": final_state.get("prediction", {}),
                "recommendations": final_state.get("recommendations", {}),
                "experiments": final_state.get("experiments", []),
                "budget_recommendation": final_state.get("budget_recommendation", {}),
                "embeddings": final_state.get("video_analysis", {}).get("visual_embedding", [])
            })

            wf_state = await analysis_repository.get_workflow_state(analysis_id)
            if wf_state:
                wf_state.status = "completed"
                wf_state.current_agent = "marketing_report"
                wf_state.execution_order = final_state.get("execution_order", [])
                wf_state.agent_logs = final_state.get("agent_logs", [])
                await wf_state.save()

        except Exception as e:
            logger.error(f"Error in async analysis pipeline for {analysis_id}: {str(e)}")
            await analysis_repository.update_analysis_results(analysis_id, {"status": "failed"})
            wf_state = await analysis_repository.get_workflow_state(analysis_id)
            if wf_state:
                wf_state.status = "failed"
                wf_state.error = str(e)
                await wf_state.save()

    async def get_workflow_status(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        wf = await analysis_repository.get_workflow_state(analysis_id)
        if not wf:
            return None
        return {
            "analysis_id": wf.analysis_id,
            "status": wf.status,
            "current_agent": wf.current_agent,
            "execution_order": wf.execution_order,
            "agent_logs": wf.agent_logs,
            "error": wf.error
        }

    async def get_analysis_detail(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        doc = await analysis_repository.get_analysis_by_id(analysis_id)
        if not doc:
            return None
        return {
            "analysis_id": doc.analysis_id,
            "video_filename": doc.video_filename,
            "caption": doc.caption,
            "campaign_goal": doc.campaign_goal,
            "status": doc.status,
            "video_analysis": doc.video_analysis,
            "audio_analysis": doc.audio_analysis,
            "ocr_analysis": doc.ocr_analysis,
            "caption_analysis": doc.caption_analysis,
            "creative_synthesis": doc.creative_synthesis,
            "prediction": doc.prediction,
            "recommendations": doc.recommendations,
            "experiments": doc.experiments,
            "budget_recommendation": doc.budget_recommendation,
            "created_at": doc.created_at.isoformat()
        }

analysis_service = AnalysisService()
