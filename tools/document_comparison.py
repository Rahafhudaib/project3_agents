def group_by_document(chunks):
    grouped = {}
    for c in chunks:
        grouped.setdefault(c["document"], []).append(c)
    return grouped


def build_comparison_context(grouped):
    parts = []
    for doc, chunks in grouped.items():
        text = " ".join(c["text"] for c in chunks)
        parts.append(f"[{doc}]\n{text}")
    return "\n\n".join(parts)
