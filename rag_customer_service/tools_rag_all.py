# tools_rag_all.py
from rag import ask_rag
from langchain_core.tools import tool

@tool
def search_company_policies(question: str) -> str:
    """
    Search NordicTech Store company policy documents for answers about
    returns, refunds, damaged items, delivery times, warranties, and installation.
    Always use this tool when the user asks about store policies or services.
    """

    result = ask_rag(question)
    return result

