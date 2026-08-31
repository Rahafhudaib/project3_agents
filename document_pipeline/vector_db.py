import pickle
import os
import numpy as np
from document_pipeline import embeddings


class VectorDB:
    def __init__(self, path):
        self.path = path
        self.chunks = []
        self.vectors = None
        if os.path.exists(path):
            self.load()

    def add(self, chunk_records):
        texts = [c["text"] for c in chunk_records]
        vecs = embeddings.embed_texts(texts)
        if self.vectors is None:
            self.vectors = vecs
        else:
            self.vectors = np.vstack([self.vectors, vecs])
        self.chunks.extend(chunk_records)
        self.save()

    def search(self, query, top_k=15):
        if self.vectors is None or len(self.chunks) == 0:
            return []
        qvec = embeddings.embed_query(query)
        scores = self.vectors @ qvec
        idx = np.argsort(-scores)[:top_k]
        results = []
        for i in idx:
            record = dict(self.chunks[i])
            record["score"] = float(scores[i])
            results.append(record)
        return results

    def save(self):
        with open(self.path, "wb") as f:
            pickle.dump({"chunks": self.chunks, "vectors": self.vectors}, f)

    def load(self):
        with open(self.path, "rb") as f:
            data = pickle.load(f)
        self.chunks = data["chunks"]
        self.vectors = data["vectors"]

    def clear(self):
        self.chunks = []
        self.vectors = None
        if os.path.exists(self.path):
            os.remove(self.path)
