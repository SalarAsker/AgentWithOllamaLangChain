import os
from pathlib import Path

# Get the path of the parent directory /rag_experiment
BASE_DIR = Path(__file__).resolve().parent

# Create paths to the data nd chroma_db folder
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"

# If there is no environment variable named OLLAMA_BASE_URL
# The system will use the hardcoded ip
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://172.29.190.0:11434")
# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://192.168.0.126:11434")

# LLM_MODEL = "llama3.2:3b" # change what you are using such as, qwen3.5:9b
LLM_MODEL = "qwen3.5:9b"
EMBEDDING_MODEL = "nomic-embed-text:latest"

# Size of chunking files
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 3