# AI Prototype Assessment - Chat with PDFs

This project is a practical AI prototype designed for the **AI Prototyping Engineer** assessment. It features a RAG-based question-answering system for PDFs, now configured for **Streamlit Cloud** deployment using **OpenAI**.

## Features

### ✅ Task 1: LLM-Powered AI Prototype
A robust RAG pipeline that runs locally or in the cloud.
- **LLM**: **OpenAI GPT-3.5-Turbo** (via API).
- **Vector DB**: **SimpleVectorStore** (JSON-based) for maximum portability and zero-setup requirements.
- **Ingestion**: Recursive chunking (1000 chars) for optimal context retrieval.
- **UI**: Clean **Streamlit** interface with Sidebar Configuration.

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
    - *Trade-off*: Increasing history consumes context window tokens and increases API costs.
    - *Limitation*: Current implementation uses a simple list; extremely long conversations may hit the 4k/16k context limit.

### ✅ Task 4: System Architecture
Full enterprise architecture design provided.
- See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the detailed diagram, component breakdown, and cost/monitoring strategies for an enterprise-grade version of this tool.

---

## Setup & Deployment

| Platform | Instructions |
| :--- | :--- |
| **Local** | `pip install -r requirements.txt` -> `streamlit run app.py` |
| **Streamlit Cloud** | Connect GitHub Repo -> Deploy. (No secrets needed, user inputs Key in UI) |

### Usage
1.  Enter your **OpenAI API Key** in the sidebar.
2.  Upload a PDF document.
3.  Click "Initialize & Ingest".
4.  Start chatting!
