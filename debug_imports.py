import importlib
import pkgutil
import langchain
import langchain.chains

print(f"LangChain version: {langchain.__version__}")
print(f"LangChain path: {langchain.__path__}")

try:
    from langchain.chains import ConversationalRetrievalChain
    print("Success: from langchain.chains import ConversationalRetrievalChain")
except ImportError as e:
    print(f"Failed: from langchain.chains import ConversationalRetrievalChain: {e}")

try:
    from langchain_community.chains import ConversationalRetrievalChain
    print("Success: from langchain_community.chains import ConversationalRetrievalChain")
except ImportError as e:
    print(f"Failed: from langchain_community.chains import ConversationalRetrievalChain: {e}")

# List attributes of langchain.chains
print("Attributes in langchain.chains:")
print(dir(langchain.chains))
