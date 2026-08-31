# Project 3 - Multi-Agent RAG System

A document chat system (PDF / DOCX / TXT) built with three cooperating
agents: Retriever Agent, Analyst Agent, and Answer Agent, backed by a
Document Pipeline that prepares files and a local Vector DB that stores
them.

## How it works

1. **Document Pipeline**: reads files from the `data/` folder, cleans the
   text, splits it into chunks, turns each chunk into an embedding, and
   stores everything in a local Vector DB (a pickle file).
2. **Retriever Agent**: rewrites the question, runs semantic search +
   keyword search (BM25), filters by metadata, reranks the results, then
   picks the best set of chunks.
3. **Analyst Agent**: analyzes the evidence, extracts numbers and tables,
   compares across documents, and decides whether the evidence is enough.
   If not, it loops back to the Retriever Agent (feedback loop).
4. **Answer Agent**: builds the final answer with citations (file name and
   page number).

The Orchestrator in `agents/orchestrator.py` ties the three agents
together.

## Requirements

- Python 3.10 or newer
- An OpenAI API key (used for query rewriting, analysis, and answer
  generation)

## Installation

```bash
cd project3_rag
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Then set your API key:

```bash
export OPENAI_API_KEY="sk-..."      # on Windows: set OPENAI_API_KEY=sk-...
```

## Usage

1. Put the PDF / DOCX / TXT files you want to query inside the `data/`
   folder.
2. Run the program:

```bash
python main.py
```

3. On the first run it will automatically index the files, then you can
   start asking questions right from the terminal.
4. If you add new files later, type `reindex` to rebuild the index.
5. Type `exit` to quit.

## Project structure
