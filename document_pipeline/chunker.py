def chunk_text(text, chunk_size=400, overlap=60):
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(chunk_size - overlap, 1)
    start = 0
    while start < len(words):
        piece = " ".join(words[start:start + chunk_size])
        if piece:
            chunks.append(piece)
        if start + chunk_size >= len(words):
            break
        start += step
    return chunks
