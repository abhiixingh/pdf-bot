try:
    import google.generativeai as genai
    print("Google GenAI imported successfully")
except ImportError as e:
    print(f"Import failed: {e}")
