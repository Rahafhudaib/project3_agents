import llm
from tools.table_extractor import extract_numbers
from tools.document_comparison import group_by_document, build_comparison_context
from tools.data_analysis import summarize_values


class AnalystAgent:
    def __init__(self, retriever_agent):
        self.retriever_agent = retriever_agent

    def evaluate_evidence(self, question, evidence):
        if not evidence:
            return False, "no evidence retrieved yet"
        context = "\n\n".join(f"[{e['document']} p.{e['page']}] {e['text']}" for e in evidence)
        prompt = (
            "Decide whether the evidence below is enough to fully answer the question. "
            "Reply with YES or NO on the first line, then a short reason on the second line.\n\n"
            f"Question: {question}\n\nEvidence:\n{context}"
        )
        result = llm.chat([{"role": "user", "content": prompt}])
        if not result:
            return True, ""
        lines = result.strip().split("\n")
        enough = lines[0].strip().upper().startswith("YES")
        reason = lines[1].strip() if len(lines) > 1 else ""
        return enough, reason

    def analyze(self, question, evidence):
        grouped = group_by_document(evidence)
        comparison_context = build_comparison_context(grouped)
        numeric_hits = []
        for e in evidence:
            for n in extract_numbers(e["text"]):
                numeric_hits.append((e["document"], n))
        stats = summarize_values(numeric_hits) if numeric_hits else {}
        prompt = (
            "You are the analyst agent in a document QA system. Use the evidence below to write "
            "a reasoning summary that answers the question. Mention any relevant comparisons or "
            "calculations. Do not use information that is not present in the evidence.\n\n"
            f"Question: {question}\n\nEvidence:\n{comparison_context}\n\n"
            f"Detected numeric stats: {stats}"
        )
        analysis = llm.chat([{"role": "user", "content": prompt}])
        return {"analysis": analysis, "stats": stats}

    def run(self, question, history, document_filter=None, max_loops=2, top_k=15, top_n=6):
        evidence = self.retriever_agent.retrieve(question, history, document_filter, top_k, top_n)
        loops = 0
        enough, reason = self.evaluate_evidence(question, evidence)
        while not enough and loops < max_loops:
            follow_up = f"{question} - missing information: {reason}"
            more = self.retriever_agent.retrieve(follow_up, history, document_filter, top_k, top_n)
            existing = {e["text"] for e in evidence}
            for m in more:
                if m["text"] not in existing:
                    evidence.append(m)
                    existing.add(m["text"])
            enough, reason = self.evaluate_evidence(question, evidence)
            loops += 1
        result = self.analyze(question, evidence)
        result["evidence"] = evidence
        result["feedback_loops"] = loops
        return result
