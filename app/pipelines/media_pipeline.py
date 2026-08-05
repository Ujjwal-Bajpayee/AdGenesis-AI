import os
from typing import Dict, Any
from app.utils.video_processor import video_processor
from app.utils.audio_processor import audio_processor
from app.utils.ocr_processor import ocr_processor
from app.storage.file_storage import file_storage
from app.core.logger import logger

class MediaExtractionPipeline:
    def process_media(self, analysis_id: str, video_path: str) -> Dict[str, Any]:
        logger.info(f"Extracting media features for analysis_id: {analysis_id}")
        frames_dir = file_storage.get_frames_dir(analysis_id)
        audio_path = file_storage.get_audio_path(analysis_id)
        
        video_meta = video_processor.extract_keyframes_and_metadata(video_path, frames_dir)
        
        has_audio = audio_processor.extract_audio(video_path, audio_path)
        audio_features = audio_processor.analyze_audio_features(audio_path if has_audio else "")
        transcript_data = audio_processor.transcribe_speech(audio_path if has_audio else "")
        
        raw_audio_data = {
            **audio_features,
            **transcript_data
        }
        
        ocr_data = ocr_processor.extract_text_from_frames(video_meta.get("frame_paths", []))
        
        return {
            "media_metadata": video_meta,
            "raw_audio_data": raw_audio_data,
            "raw_ocr_data": ocr_data
        }

media_pipeline = MediaExtractionPipeline()
