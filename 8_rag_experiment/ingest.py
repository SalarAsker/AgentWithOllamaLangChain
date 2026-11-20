# Import from the config.py
from config import (DATA_DIR, DB_DIR,OLLAMA_BASE_URL,EMBEDDING_MODEL,
                    CHUNK_SIZE,
                    CHUNK_OVERLAP)

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import shutil


# 1. Load files and create Document object
def load_documents() -> list[Document]:
    """Load all .txt policy files."""

    documents = []

    for file_path in sorted(DATA_DIR.glob("*.txt")):

        text = file_path.read_text(
            encoding="utf-8"
        )

        document = Document(
            page_content=text,
            metadata={
                "source": file_path.name
            }
        )

        documents.append(document)

    return documents

# 2. Split documents into chunks
def split_documents(documents):
    """Split documents into smaller chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.split_documents(documents)


# 3. Initialize Ollama embedded model
embedded_model = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )


# 4. Build vector database
def create_chroma_vector():

    # Step 1: Load documents
    documents = load_documents()

    if not documents:
        raise ValueError(
            "No .txt documents found in data/"
        )

    print("Documents loaded:", len(documents))

    # Step 2: Split documents
    chunks = split_documents(documents)

    print("Chunks created:", len(chunks))

    # Step 4: Rebuild local database
    # If the
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)

    vector_database = Chroma.from_documents(
        documents=chunks,
        embedding=embedded_model,
        collection_name="NordicTech",
        persist_directory=str(DB_DIR)
    )

    print("Knowledge base created successfully.")
    print("Database location:", DB_DIR)
    
    # Test
    # result = vector_database.similarity_search("How long do I have to report a damaged laptop", k=3)
    # print(result)

    return vector_database

if __name__ == "__main__":
    create_chroma_vector()