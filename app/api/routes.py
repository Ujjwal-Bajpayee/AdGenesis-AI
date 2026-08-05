import os
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from app.services.analysis_service import analysis_service
from app.repositories.analysis_repository import analysis_repository
from app.schemas.api_schemas import (
    AnalysisRequestResponse, WorkflowStatusResponse,
    AnalysisDetailResponse, ExportReportResponse
)

router = APIRouter()

@router.post("/analyze", response_model=AnalysisRequestResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    caption: str = Form(""),
    campaign_goal: str = Form("Conversions")
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid video file upload")
        
    content = await file.read()
    analysis_id = await analysis_service.start_analysis(
        filename=file.filename,
        content=content,
        caption=caption,
        campaign_goal=campaign_goal
    )
    
    return AnalysisRequestResponse(
        analysis_id=analysis_id,
        status="processing",
        message="Video analysis pipeline launched successfully"
    )

@router.get("/status/{analysis_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(analysis_id: str):
    status_data = await analysis_service.get_workflow_status(analysis_id)
    if not status_data:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    return WorkflowStatusResponse(**status_data)

@router.get("/analysis/{analysis_id}", response_model=AnalysisDetailResponse)
async def get_analysis_detail(analysis_id: str):
    detail = await analysis_service.get_analysis_detail(analysis_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    return AnalysisDetailResponse(**detail)

@router.get("/brief/{analysis_id}")
async def get_creative_brief(analysis_id: str):
    brief = await analysis_repository.get_brief_by_analysis_id(analysis_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Creative brief not found for this analysis ID")
    return brief

@router.get("/report/{analysis_id}")
async def get_marketing_report(analysis_id: str):
    report = await analysis_repository.get_report_by_analysis_id(analysis_id)
    if not report:
        raise HTTPException(status_code=404, detail="Marketing report not found for this analysis ID")
    return report

@router.get("/report/{analysis_id}/pdf")
async def download_pdf_report(analysis_id: str):
    report = await analysis_repository.get_report_by_analysis_id(analysis_id)
    if not report or not report.pdf_path or not os.path.exists(report.pdf_path):
        raise HTTPException(status_code=404, detail="PDF report not found or not yet generated")
    return FileResponse(
        path=report.pdf_path,
        filename=f"AdGenesis_Report_{analysis_id}.pdf",
        media_type="application/pdf"
    )

@router.get("/history")
async def list_history(limit: int = 50):
    items = await analysis_repository.list_analyses(limit=limit)
    return [
        {
            "analysis_id": item.analysis_id,
            "video_filename": item.video_filename,
            "caption": item.caption,
            "campaign_goal": item.campaign_goal,
            "status": item.status,
            "overall_score": item.prediction.get("overall_quality_score", 0.0),
            "created_at": item.created_at.isoformat()
        }
        for item in items
    ]
