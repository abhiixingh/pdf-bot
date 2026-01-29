import streamlit as st
import os
import tempfile
from rag_engine import RAGEngine

# Set page config
st.set_page_config(page_title="AI Prototype - Doc Chat", layout="wide")

# Title and Description
st.title("📄 AI Prototype Assessment: Chat with PDFs")
st.markdown("""
This prototype demonstrates a RAG-based QA system with hallucination guardrails and memory.
**Task 1**: LLM Prototype | **Task 2**: Guardrails | **Task 3**: Memory | **Task 4**: Architecture
""")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # For LangChain memory context

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    st.info("Using OpenAI (GPT-3.5)")
    
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if st.button("Initialize & Ingest"):
        if not uploaded_file:
            st.error("Please upload a file.")
        else:
            with st.spinner("Processing document..."):
                try:
                    # Save uploaded file to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    if not api_key:
                        st.error("Please enter your OpenAI API Key first.")
                    else:
                        # Initialize Engine
                        st.session_state.rag_engine = RAGEngine(api_key=api_key)
                    num_chunks = st.session_state.rag_engine.ingest_pdf(tmp_path)
                    
                    st.success(f"Ingested {num_chunks} chunks successfully!")
                    os.remove(tmp_path) # Clean up temp file
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### System Status")
    if st.session_state.rag_engine:
        st.success("✅ RAG Engine Active")
    else:
        st.info("⚠️ Waiting for PDF Ingestion")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View Sources (Task 2: Grounding)"):
                for idx, doc in enumerate(message["sources"]):
                    # Handle dict or object
                    meta = doc.get('metadata') if isinstance(doc, dict) else doc.metadata
                    content = doc.get('page_content') if isinstance(doc, dict) else doc.page_content
                    
                    page_num = meta.get('page', '?')
                    st.markdown(f"**Source {idx+1} (Page {page_num})**")
                    st.text(content[:300] + "...")

# User Input
if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    if st.session_state.rag_engine:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Pass chat_history for context (Task 3)
                    response, sources = st.session_state.rag_engine.chat(
                        prompt, 
                        chat_history=st.session_state.chat_history
                    )
                    
                    st.markdown(response)
                    
                    # Store history
                    st.session_state.chat_history.append((prompt, response))
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                    
                    # Task 2: Display Sources explicitly in UI
                    if sources:
                        with st.expander("View Sources (Task 2: Grounding)"):
                            for idx, doc in enumerate(sources):
                                # Handle dict or object
                                meta = doc.get('metadata') if isinstance(doc, dict) else doc.metadata
                                content = doc.get('page_content') if isinstance(doc, dict) else doc.page_content
                                
                                page_num = meta.get('page', '?')
                                st.markdown(f"**Source {idx+1} (Page {page_num})**")
                                st.text(content[:300] + "...")
                                
                except Exception as e:
                    st.error(f"Error during generation: {e}")
    else:
        st.warning("Please initialize the system in the sidebar first.")
