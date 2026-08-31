import llm


class AnswerAgent:
    def format_sources(self, evidence):
        sources = []
        seen = set()
        for e in evidence:
            key = (e["document"], e["page"])
            if key in seen:
                continue
            seen.add(key)
            sources.append(f"{e['document']}, page {e['page']}")
        return sources

    def generate(self, question, analysis_result):
        evidence = analysis_result["evidence"]
        analysis = analysis_result["analysis"]
        context = "\n\n".join(f"[{e['document']} p.{e['page']}] {e['text']}" for e in evidence)
        prompt = (
            "Write a clear final answer to the question using the analysis and evidence below. "
            "Add short inline citations like (document, page) after claims that need support. "
            "Keep the answer concise and well organized. If the evidence is not enough, say so "
            "instead of guessing.\n\n"
            f"Question: {question}\n\nAnalysis:\n{analysis}\n\nEvidence:\n{context}"
        )
        answer = llm.chat([{"role": "user", "content": prompt}])
        sources = self.format_sources(evidence)
        return {"answer": answer, "sources": sources}
