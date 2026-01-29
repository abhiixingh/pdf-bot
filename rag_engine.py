import os
import json
import math
from pypdf import PdfReader
import ollama
import tiktoken
from typing import List, Tuple, Dict

class SimpleVectorStore:
    def __init__(self, persist_path: str = "./simple_db.json"):
        self.persist_path = persist_path
        self.documents = [] # List of dicts: {"text": str, "metadata": dict, "embedding": List[float], "id": str}
        self.load()

    def add(self, documents: List[str], metadatas: List[dict], ids: List[str], embeddings: List[List[float]]):
        for doc, meta, id_, emb in zip(documents, metadatas, ids, embeddings):
            self.documents.append({
                "text": doc,
                "metadata": meta,
                "embedding": emb,
                "id": id_
            })
        self.save()

    def query(self, query_embedding: List[float], k: int = 3):
        # Calculate cosine similarity with all docs
        scores = []
        q_mag = math.sqrt(sum(x*x for x in query_embedding))
        
        for doc in self.documents:
            d_emb = doc["embedding"]
            # Dot product
            dot = sum(a*b for a, b in zip(query_embedding, d_emb))
            d_mag = math.sqrt(sum(x*x for x in d_emb))
            
            if q_mag * d_mag == 0:
                sim = 0
            else:
                sim = dot / (q_mag * d_mag)
            
            scores.append((sim, doc))
            
        # Sort desc
        scores.sort(key=lambda x: x[0], reverse=True)
        top_k = scores[:k]
        
        # Format like Chroma results: {'documents': [[...]], 'metadatas': [[...]]}
        return {
            "documents": [[x[1]["text"] for x in top_k]],
            "metadatas": [[x[1]["metadata"] for x in top_k]]
        }

    def save(self):
        try:
            with open(self.persist_path, "w") as f:
                json.dump(self.documents, f)
        except Exception as e:
            print(f"Failed to save DB: {e}")

    def load(self):
        if os.path.exists(self.persist_path):
            try:
                with open(self.persist_path, "r") as f:
                    self.documents = json.load(f)
            except Exception:
                self.documents = []

class RAGEngine:
    def __init__(self):
        # Switched to phi3 for better performance on lower RAM
        self.model_name = "phi3" 
        # We don't need an API Key for Ollama
        
        # Use SimpleVectorStore
        self.db = SimpleVectorStore()
        
    def get_embedding(self, text: str) -> List[float]:
        # Ollama Embeddings
        # Ensure llama3 is pulled: `ollama pull llama3`
        try:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            return response['embedding']
        except Exception as e:
            print(f"Ollama Embedding Error: {e}")
            return []

    def recursive_split(self, text, chunk_size=1000, chunk_overlap=100) -> List[str]:
        """Simple recursive character splitter implementation"""
        import re
        chunks = []
        if len(text) <= chunk_size:
            return [text]
            
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        
        step = chunk_size - chunk_overlap
        if step <= 0: step = 1
        
        for i in range(0, len(tokens), step):
            chunk_tokens = tokens[i : i + chunk_size]
            chunks.append(enc.decode(chunk_tokens))
            
        return chunks

    def ingest_pdf(self, file_path: str):
        """Task 1: PDF Ingestion & Chunking"""
        import time
        reader = PdfReader(file_path)
        
        documents = []
        metadatas = []
        ids = []
        embeddings = []
        
        doc_id_counter = len(self.db.documents)
        
        # Process pages
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                chunks = self.recursive_split(text)
                for chunk in chunks:
                    documents.append(chunk)
                    metadatas.append({"page": i + 1, "source": os.path.basename(file_path)})
                    ids.append(f"doc_{doc_id_counter}")
                    
                    # Generate embedding
                    emb = self.get_embedding(chunk)
                    if emb:
                        embeddings.append(emb)
                    # No rate limit sleep needed for local Ollama usually
                    
                    doc_id_counter += 1
        
        if documents:
            self.db.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
        return len(documents)

    def chat(self, query: str, chat_history: List[Tuple[str, str]] = None):
        """Execute the chat chain with Ollama (Llama 3)"""
        # 1. Embed query
        query_emb = self.get_embedding(query)
        
        # 2. Retrieve relevant chunks (Reduced k to save context/RAM)
        results = self.db.query(query_embedding=query_emb, k=2)
        
        context_text = ""
        sources = []
        
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                context_text += f"[Page {meta['page']}] {doc}\n\n"
                sources.append({"page_content": doc, "metadata": meta})
        
        # 3. Construct Prompt with History (Task 3)
        
        history_block = ""
        if chat_history:
            for q, a in chat_history:
                history_block += f"User: {q}\nModel: {a}\n"
        
        system_prompt = """You are a helpful AI assistant for internal knowledge.
        Use the provided context to answer the user's question.
        If the answer is not in the context, say "I cannot find the answer in the provided document."
        ALWAYS cite the page number explicitly (e.g., [Page 5])."""
        
        final_prompt = f"""{system_prompt}

Context:
{context_text}

Conversation History:
{history_block}

User Question: {query}
"""

        # 4. Generate Response (Task 1 & 2)
        # Added options to limit context window (save RAM)
        response = ollama.chat(
            model=self.model_name, 
            messages=[{'role': 'user', 'content': final_prompt}],
            options={'num_ctx': 4096} 
        )
        
        answer = response['message']['content']
        return answer, sources
