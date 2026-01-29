try:
    import openai
    print("OpenAI imported")
except ImportError as e:
    print(f"OpenAI failed: {e}")

try:
    import chromadb
    print("ChromaDB imported")
except ImportError as e:
    print(f"ChromaDB failed: {e}")

try:
    import tiktoken
    print("Tiktoken imported")
except ImportError as e:
    print(f"Tiktoken failed: {e}")
