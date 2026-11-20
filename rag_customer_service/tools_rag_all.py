# tools_rag_all.py
from rag import ask_rag
from langchain_core.tools import tool

@tool
def search_company_policies(question: str) -> str:
    """Search company return, shipping, and warranty policies."""

    result = ask_rag(question)
    return result

