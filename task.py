from crewai import Task
from agents import financial_analyst, investment_advisor, risk_assessor
from tools import read_data_tool

analyze_financial_document = Task(
    description="Extract Revenue, Net Income, and EPS from {path} to answer: {query}",
    expected_output="Structured summary of key metrics.",
    agent=financial_analyst,
    tools=[read_data_tool]
)

investment_analysis = Task(
    description="Provide an investment outlook based on the data in {path}.",
    expected_output="A professional investment report.",
    agent=investment_advisor, # Corrected Agent
    tools=[read_data_tool]
)

risk_assessment = Task(
    description="Identify 3-5 financial risks from the file at {path}.",
    expected_output="A detailed risk profile.",
    agent=risk_assessor, # Corrected Agent
    tools=[read_data_tool]
)