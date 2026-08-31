import os
from document_pipeline.loader import load_file
from document_pipeline.cleaner import clean_text
from document_pipeline.chunker import chunk_text
import config


def ingest_file(path, vector_db):
    pages = load_file(path)
    doc_name = os.path.basename(path)
    records = []
    for page in pages:
        text = clean_text(page["text"])
        if not text:
            continue
        pieces = chunk_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        for piece in pieces:
            records.append({
                "text": piece,
                "document": doc_name,
                "page": page["page"]
            })
    if records:
        vector_db.add(records)
    return len(records)


def ingest_directory(directory, vector_db):
    total = 0
    if not os.path.isdir(directory):
        return total
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            try:
                total += ingest_file(path, vector_db)
            except Exception as e:
                print(f"Skipped {name}: {e}")
    return total
