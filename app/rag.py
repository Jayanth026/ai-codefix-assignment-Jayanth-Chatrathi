import os
from typing import List, Optional, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class SimpleRAGRetriever:
    def __init__(self, recipes_dir: str = "recipes"):
        self.recipes_dir = recipes_dir
        self.model: Optional[SentenceTransformer] = None
        self.index: Optional[faiss.IndexFlatIP] = None
        self.docs: List[str] = []
        self.doc_names: List[str] = []

    def _load_docs(self):
        for fname in os.listdir(self.recipes_dir):
            if fname.endswith(".txt"):
                path = os.path.join(self.recipes_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                self.docs.append(text)
                self.doc_names.append(fname)

    def _build_index(self):
        if not self.docs:
            self._load_docs()
        if not self.docs:
            return

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        embeddings = self.model.encode(self.docs, convert_to_numpy=True, normalize_embeddings=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def init(self):
        if self.index is None:
            self._build_index()

    def retrieve(self, query: str, top_k: int = 1) -> Optional[Tuple[str, str]]:
        """
        Returns (doc_text, doc_name) for top-1 match or None.
        """
        if self.index is None or self.model is None:
            return None

        q_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, indices = self.index.search(q_emb, top_k)
        best_idx = indices[0][0]
        best_doc = self.docs[best_idx]
        best_name = self.doc_names[best_idx]
        return best_doc, best_name
