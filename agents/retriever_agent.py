import llm
from rank_bm25 import BM25Okapi


class RetrieverAgent:
    def __init__(self, vector_db):
        self.vector_db = vector_db

    def rewrite_query(self, question, history=None):
        history_text = ""
        if history:
            history_text = "\n".join(f"{h['role']}: {h['content']}" for h in history[-4:])
        prompt = (
            "Rewrite the following user question into a clear, standalone search query. "
            "Expand abbreviations and resolve pronouns using the conversation history if needed. "
            "Return only the rewritten query, nothing else.\n\n"
            f"History:\n{history_text}\n\nQuestion: {question}"
        )
        result = llm.chat([{"role": "user", "content": prompt}])
        return result.strip() if result else question

    def keyword_search(self, query, top_k=15):
        if not self.vector_db.chunks:
            return []
        corpus = [c["text"].split() for c in self.vector_db.chunks]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(query.split())
        ranked = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]
        results = []
        for i in ranked:
            record = dict(self.vector_db.chunks[i])
            record["score"] = float(scores[i])
            results.append(record)
        return results

    def semantic_search(self, query, top_k=15):
        return self.vector_db.search(query, top_k)

    def metadata_filter(self, chunks, document=None, page=None):
        results = chunks
        if document:
            results = [c for c in results if document.lower() in c["document"].lower()]
        if page:
            results = [c for c in results if c["page"] == page]
        return results

    def rerank(self, chunks):
        merged = {}
        for c in chunks:
            key = (c["document"], c["page"], c["text"])
            if key not in merged:
                merged[key] = dict(c)
            else:
                merged[key]["score"] = merged[key].get("score", 0) + c.get("score", 0)
        return sorted(merged.values(), key=lambda x: x.get("score", 0), reverse=True)

    def select_context(self, chunks, top_n=6):
        seen = set()
        selected = []
        for c in chunks:
            if c["text"] in seen:
                continue
            seen.add(c["text"])
            selected.append(c)
            if len(selected) >= top_n:
                break
        return selected

    def retrieve(self, question, history=None, document_filter=None, top_k=15, top_n=6):
        query = self.rewrite_query(question, history)
        semantic_results = self.semantic_search(query, top_k)
        keyword_results = self.keyword_search(query, top_k)
        combined = semantic_results + keyword_results
        if document_filter:
            combined = self.metadata_filter(combined, document=document_filter)
        reranked = self.rerank(combined)
        return self.select_context(reranked, top_n)
