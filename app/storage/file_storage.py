import os
import shutil
from typing import Tuple
from app.core.config import settings

class FileStorageService:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or settings.STORAGE_DIR
        os.makedirs(self.base_dir, exist_ok=True)

    def get_analysis_dir(self, analysis_id: str) -> str:
        path = os.path.join(self.base_dir, analysis_id)
        os.makedirs(path, exist_ok=True)
        return path

    def get_frames_dir(self, analysis_id: str) -> str:
        path = os.path.join(self.get_analysis_dir(analysis_id), "frames")
        os.makedirs(path, exist_ok=True)
        return path

    def get_audio_path(self, analysis_id: str) -> str:
        return os.path.join(self.get_analysis_dir(analysis_id), "extracted_audio.wav")

    def save_uploaded_file(self, analysis_id: str, filename: str, content: bytes) -> str:
        analysis_dir = self.get_analysis_dir(analysis_id)
        file_path = os.path.join(analysis_dir, filename)
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

file_storage = FileStorageService()
