import numpy as np
from typing import List
from app.core.config import settings
from app.core.logger import logger

class EmbeddingService:
    def __init__(self):
        self._model = None
        self.dimension = 384

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
                self.dimension = self._model.get_sentence_embedding_dimension()
            except Exception as e:
                logger.warning(f"Sentence Transformers load fallback: {str(e)}")
                self._model = None

    def generate_embedding(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self.dimension
        self._load_model()
        if self._model is not None:
            emb = self._model.encode(text)
            return emb.tolist() if hasattr(emb, "tolist") else list(emb)
        else:
            np.random.seed(abs(hash(text)) % (2**32))
            dummy = np.random.normal(0, 1, self.dimension)
            norm = np.linalg.norm(dummy)
            return (dummy / (norm if norm > 0 else 1.0)).tolist()

    def build_faiss_index(self, embeddings: List[List[float]]):
        if not embeddings:
            return None
        try:
            import faiss
            data = np.array(embeddings, dtype=np.float32)
            dimension = data.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(data)
            return index
        except Exception as e:
            logger.warning(f"FAISS index build fallback: {str(e)}")
            return None

embedding_service = EmbeddingService()
