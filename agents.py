from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
import os
from dotenv import load_dotenv
from crewai import Agent

# FIX: Import only what exists in your tools.py to avoid ImportError
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

load_dotenv()

### Loading LLM (Gemini 1.5 Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

# 1. Senior Financial Analyst
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate, data-driven financial insights based on the provided document.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned Wall Street analyst known for meticulous attention to detail. "
        "Your expertise lies in identifying trends in quarterly reports and extracting "
        "key metrics like Revenue, Net Income, and EPS with 100% accuracy."
    ),
    tools=[read_data_tool, search_tool], # Uses the PDF reader and Internet search
    llm=llm,
    allow_delegation=False
)

# 2. Investment Advisor
investment_advisor = Agent(
    role="Investment Strategy Guru",
    goal="Translate complex financial data into actionable investment recommendations.",
    verbose=True,
    memory=True,
    backstory=(
        "You have 20 years of experience in portfolio management. You specialize in "
        "interpreting financial health to determine if a company is a 'Buy', 'Hold', or 'Sell'. "
        "You prioritize long-term value over market noise."
    ),
    tools=[analyze_investment_tool], # Uses the custom analysis tool
    llm=llm,
    allow_delegation=False
)

# 3. Risk Assessor 
risk_assessor = Agent(
    role="Risk Management Specialist",
    goal="Identify potential pitfalls, liabilities, and market risks within financial filings.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in forensic accounting and risk mitigation. You look past "
        "the highlights to find debt obligations, liquidity issues, and external "
        "economic threats that could impact investors."
    ),
    tools=[create_risk_assessment_tool], # Uses the specific risk tool
    llm=llm,
    allow_delegation=False
)

# Optional: Verifier (If needed in your tasks)
verifier = Agent(
    role="Document Integrity Specialist",
    goal="Ensure the uploaded document is a valid financial report.",
    verbose=True,
    backstory="You verify the authenticity and relevance of documents before analysis begins.",
    llm=llm,
    allow_delegation=False
)