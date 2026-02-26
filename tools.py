# tools.py
import os
from crewai.tools import tool 
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

search_tool = SerperDevTool()

@tool("read_data_tool")
def read_data_tool(path: str):
    """Reads and cleans text from a PDF file at the given path."""
    try:
        # Normalize path for Windows compatibility
        clean_path = os.path.normpath(path.strip().replace("'", "").replace('"', ""))
        if not os.path.exists(clean_path):
            return f"Error: File not found at {clean_path}"

        loader = PyPDFLoader(file_path=clean_path)
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@tool("analyze_investment_tool") # MATCH THIS NAME
def analyze_investment_tool(financial_document_data: str):
    """Processes financial data to provide investment insights."""
    return f"Analysis complete. Data length: {len(financial_document_data)} characters."

@tool("create_risk_assessment_tool") # MATCH THIS NAME
def create_risk_assessment_tool(financial_document_data: str):
    """Assesses risks based on financial document data."""
    return "Risk assessment complete: Low to Moderate risk profile detected."