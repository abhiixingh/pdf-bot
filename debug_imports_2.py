import importlib
import pkgutil
import langchain

print(f"LangChain version: {langchain.__version__}")

# Try direct import
try:
    from langchain.chains import ConversationalRetrievalChain
    print("Found in langchain.chains")
except ImportError as e:
    print(f"Not in langchain.chains: {e}")

# Try submodule
try:
    from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
    print("Found in langchain.chains.conversational_retrieval.base")
except ImportError as e:
    print(f"Not in langchain.chains.conversational_retrieval.base: {e}")

# Try community submodule
try:
    from langchain_community.chains.conversational_retrieval.base import ConversationalRetrievalChain
    print("Found in langchain_community.chains.conversational_retrieval.base")
except ImportError as e:
    print(f"Not in langchain_community.chains.conversational_retrieval.base: {e}")

# Inspect langchain dir
print(f"LangChain dir: {dir(langchain)}")
try:
    import langchain.chains
    print(f"LangChain chains dir: {dir(langchain.chains)}")
except ImportError:
    print("Could not import langchain.chains")
