# AI Prototype Assessment - Chat with PDFs

This project is a practical AI prototype designed for the **AI Prototyping Engineer** assessment. It features a completely local, RAG-based question-answering system for PDFs, using **Ollama** and **Python**.

## features

### ✅ Task 1: LLM-Powered AI Prototype
A robust RAG pipeline that runs locally.
- **LLM**: Local **Ollama** (supports `phi3`, `llama3`).
- **Vector DB**: **SimpleVectorStore** (JSON-based) for maximum portability and zero-setup requirements.
- **Ingestion**: Recursive chunking (1000 chars) for optimal context retrieval.
- **UI**: Clean **Streamlit** interface.

### ✅ Task 2: Hallucination & Quality Control
Implemented guardrails to ensure reliability.
- **Problem**: LLMs often hallucinate when context is missing or irrelevant.
- **Causes in this System**:
    - *Retrieval misses*: Relevant chunks not found in Top-K.
    - *Context overflow*: Too much noise in the prompt.
- **Implemented Guardrails**:
    1.  **Source Grounding**: The UI explicitly displays the "Source Chunks" used to generate the answer.
    2.  **Prompt Constraints**: The System Prompt explicitly instructs: *If the answer is not in the context, say "I cannot find the answer..."* and *ALWAYS cite the page number*.

### ✅ Task 3: Rapid Iteration (Memory Capability)
Advanced capability added: **Conversation Memory**.
- **Why**: Allows users to ask follow-up questions (e.g., "Summarize that section") without restating context.
- **Implementation**: Full chat history appended to the context window.
- **Trade-offs & Limitations**:
    - *Trade-off*: Increasing history consumes context window tokens, potentially pushing out document context.
    - *Limitation*: Current implementation uses a simple list; extremely long conversations may hit the model's context limit (e.g., 4096 tokens).

### ✅ Task 4: System Architecture
Full enterprise architecture design provided.
- See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the detailed diagram, component breakdown, and cost/monitoring strategies for an enterprise-grade version of this tool.

---

## Setup

1.  **Install Ollama**: Download from [ollama.com](https://ollama.com).
2.  **Pull Model**: Run `ollama pull phi3` (or `llama3`).
3.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```
