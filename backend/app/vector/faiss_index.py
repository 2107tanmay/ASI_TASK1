import os
import pickle
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class VectorStore:
    """FAISS vector store for document page embeddings.
    Index is persisted to disk at ``settings.VECTOR_INDEX_PATH``.
    """

    def __init__(self):
        self.index_path = Path(settings.VECTOR_INDEX_PATH)
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.dim = 384  # default dimension for all‑MiniLM‑L6‑v2
        self.index = self._load_or_create_index()
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        # Mapping from FAISS internal id to page identifier (uuid)
        self.id_map_path = self.index_path / "id_map.pkl"
        if self.id_map_path.exists():
            with open(self.id_map_path, "rb") as f:
                self.id_map = pickle.load(f)
        else:
            self.id_map = {}

    def _load_or_create_index(self):
        index_file = self.index_path / "faiss.index"
        if index_file.exists():
            return faiss.read_index(str(index_file))
        # Create a new index (Flat L2 for simplicity)
        quantizer = faiss.IndexFlatL2(self.dim)
        index = faiss.IndexIDMap2(quantizer)
        faiss.write_index(index, str(index_file))
        return index

    def _persist(self):
        index_file = self.index_path / "faiss.index"
        faiss.write_index(self.index, str(index_file))
        with open(self.id_map_path, "wb") as f:
            pickle.dump(self.id_map, f)

    def add_page(self, page_id: str, text: str):
        """Add a single page embedding to the index.
        ``page_id`` is the UUID of the ``DocumentPage`` record.
        """
        embedding = self.model.encode([text], convert_to_numpy=True)
        vec = np.array(embedding, dtype="float32")
        # FAISS expects a 2‑D array
        self.index.add_with_ids(vec, np.array([int(page_id.replace('-', ''), 16) % (1 << 63)], dtype="int64"))
        self.id_map[page_id] = text
        self._persist()

    def search(self, query: str, top_k: int = 5):
        """Return a list of ``(page_id, score)`` tuples ordered by similarity.
        Score is the L2 distance (lower is better).
        """
        embedding = self.model.encode([query], convert_to_numpy=True)
        vec = np.array(embedding, dtype="float32")
        D, I = self.index.search(vec, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            # Find the page_id corresponding to this internal FAISS id
            # Reverse lookup via stored mapping
            page_id = next((k for k, v in self.id_map.items() if int(k.replace('-', ''), 16) % (1 << 63) == idx), None)
            results.append((page_id, float(dist)))
        return results
