from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.core.logger import logger
from app.models.analysis import VideoAnalysisDocument
from app.models.brief import CreativeBriefDocument
from app.models.report import MarketingReportDocument
from app.models.workflow import WorkflowStateDocument

async def init_db():
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(
            database=client[settings.MONGODB_DATABASE],
            document_models=[
                VideoAnalysisDocument,
                CreativeBriefDocument,
                MarketingReportDocument,
                WorkflowStateDocument
            ]
        )
        logger.info(f"Successfully connected to MongoDB database: {settings.MONGODB_DATABASE}")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
