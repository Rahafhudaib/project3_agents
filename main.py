import os
import config
from document_pipeline.vector_db import VectorDB
from document_pipeline.ingest import ingest_directory
from agents.orchestrator import Orchestrator


def main():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    vector_db = VectorDB(config.VECTOR_DB_PATH)
    if len(vector_db.chunks) == 0:
        count = ingest_directory(config.DATA_DIR, vector_db)
        print(f"Indexed {count} chunks from {config.DATA_DIR}")
    else:
        print(f"Loaded existing index with {len(vector_db.chunks)} chunks")

    orchestrator = Orchestrator(vector_db)
    print("Type 'exit' to quit, 'reindex' to reload documents from the data folder")

    while True:
        question = input("\nYou: ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            break
        if question.lower() == "reindex":
            vector_db.clear()
            count = ingest_directory(config.DATA_DIR, vector_db)
            print(f"Reindexed {count} chunks")
            continue

        result = orchestrator.ask(question)
        print(f"\nAssistant: {result['answer']}")
        if result["sources"]:
            print("\nSources:")
            for s in result["sources"]:
                print(f"  - {s}")


if __name__ == "__main__":
    main()
