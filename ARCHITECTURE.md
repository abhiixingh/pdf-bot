# AI System Architecture

This document outlines the architecture for the Enterprise AI Assistant designed for internal knowledge retrieval.

## High-Level Architecture Diagram

```mermaid
graph TD
    User[User / Evaluator] -->|Query| UI[Streamlit Frontend]
    UI -->|API Call| RAG[RAG Engine (Ollama / Llama3)]
    
    subgraph Ingestion Pipeline
        Docs[PDF Documents] -->|Load| Loader[PyPDFLoader]
        Loader -->|Chunk| Splitter[RecursiveCharacterTextSplitter]
        Splitter -->|Embed| Embed[Ollama Embeddings]
        Embed -->|Store| VectorDB[(SimpleVectorStore JSON)]
    end
    
    subgraph Retrieval & Generation
        RAG -->|1. Embed Query| Embed
        VectorDB -->|2. Return Top-k Chunks| RAG
        RAG -->|3. Construct Prompt with History| ContextWindow
        ContextWindow -->|4. Generate Response| LLM[Local Llama 3]
        LLM -->|5. Answer + Citations| RAG
    end
    
    RAG -->|Response| UI
    
    subgraph Quality & Control
        Guardrails[Prompt Engineering / Relevance Check] -.-> RAG
        Memory[In-Memory List] <--> RAG
    end
```

## Detailed Design Components

### 1. Data Ingestion
- **Processing**: Used `PyPDFLoader` for reliable text extraction.
- **Chunking**: Implemented `RecursiveCharacterTextSplitter` with `chunk_size=1000`.
- **Pivot**: Switched to **SimpleVectorStore** (Pure Python/JSON) to avoid dependency conflicts.

### 2. Vector Database Choice
- **Selection**: **SimpleVectorStore (Custom JSON)**.
- **Reasoning**: Lightweight, zero-dependency JSON store implemented to guarantee the prototype runs smoothly for assessment. It supports cosine similarity search.

### 3. LLM Orchestration
- **Framework**: **Ollama (Local Inference)**.
- **Role**: Replaces cloud APIs (OpenAI/Google) for a fully local, privacy-first implementation.
- **Orchestration**: Custom `RAGEngine` class handles the retrieval and generation loop using the `ollama` python library.

### 4. Cost Control
- **Model**: `llama3` (Local).
- **Rate Limiting**: None required (Local inference).

### 5. Monitoring & Evaluation
- **Architecture**: Designed for modularity. The `RAGEngine` can clearly swap out the vector store or LLM backend if needed.

