from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.analysis import VideoAnalysisDocument
from app.models.brief import CreativeBriefDocument
from app.models.report import MarketingReportDocument
from app.models.workflow import WorkflowStateDocument

class AnalysisRepository:
    async def create_analysis(self, analysis_id: str, filename: str, path: str, caption: str, goal: str) -> VideoAnalysisDocument:
        doc = VideoAnalysisDocument(
            analysis_id=analysis_id,
            video_filename=filename,
            video_path=path,
            caption=caption,
            campaign_goal=goal,
            status="processing"
        )
        await doc.insert()
        return doc

    async def get_analysis_by_id(self, analysis_id: str) -> Optional[VideoAnalysisDocument]:
        return await VideoAnalysisDocument.find_one(VideoAnalysisDocument.analysis_id == analysis_id)

    async def list_analyses(self, limit: int = 50) -> List[VideoAnalysisDocument]:
        return await VideoAnalysisDocument.find_all().sort("-created_at").limit(limit).to_list()

    async def update_analysis_results(self, analysis_id: str, updates: Dict[str, Any]) -> Optional[VideoAnalysisDocument]:
        doc = await self.get_analysis_by_id(analysis_id)
        if doc:
            for k, v in updates.items():
                if hasattr(doc, k):
                    setattr(doc, k, v)
            doc.updated_at = datetime.utcnow()
            await doc.save()
        return doc

    async def save_creative_brief(self, brief_doc: CreativeBriefDocument) -> CreativeBriefDocument:
        await brief_doc.insert()
        return brief_doc

    async def get_brief_by_analysis_id(self, analysis_id: str) -> Optional[CreativeBriefDocument]:
        return await CreativeBriefDocument.find_one(CreativeBriefDocument.analysis_id == analysis_id)

    async def save_marketing_report(self, report_doc: MarketingReportDocument) -> MarketingReportDocument:
        await report_doc.insert()
        return report_doc

    async def get_report_by_analysis_id(self, analysis_id: str) -> Optional[MarketingReportDocument]:
        return await MarketingReportDocument.find_one(MarketingReportDocument.analysis_id == analysis_id)

    async def save_workflow_state(self, workflow_doc: WorkflowStateDocument) -> WorkflowStateDocument:
        existing = await WorkflowStateDocument.find_one(WorkflowStateDocument.workflow_id == workflow_doc.workflow_id)
        if existing:
            existing.current_agent = workflow_doc.current_agent
            existing.status = workflow_doc.status
            existing.execution_order = workflow_doc.execution_order
            existing.agent_logs = workflow_doc.agent_logs
            existing.error = workflow_doc.error
            existing.updated_at = datetime.utcnow()
            await existing.save()
            return existing
        else:
            await workflow_doc.insert()
            return workflow_doc

    async def get_workflow_state(self, workflow_id: str) -> Optional[WorkflowStateDocument]:
        return await WorkflowStateDocument.find_one(WorkflowStateDocument.workflow_id == workflow_id)

analysis_repository = AnalysisRepository()
