
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import read_data_tool, analyze_investment_tool, create_risk_assessment_tool
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document_task = Task(
    description="""
    Maybe solve the user's query: {query} or something else that seems interesting.
    Read the uploaded financial document carefully, highlight key metrics like revenue growth,
    profitability, liquidity, and debt ratios. Provide insights and actionable observations.
    Find some potential market risks and note trends even if minor. Include credible URLs where relevant.
    """,
    expected_output="""
    - Summary of financial performance
    - Key metrics and insights
    - Notable trends or anomalies
    - Potential risks to consider
    - Optional: financial URLs or references
    """,
    agent=financial_analyst,
    tools=[read_data_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""
    Look at the financial data and recommend suitable investment strategies.
    Consider asset allocation, buy/hold/sell signals, and portfolio adjustments.
    Take risk appetite and long-term objectives into account.
    """,
    expected_output="""
    - Suggested investments and strategies
    - Asset allocation guidance
    - Short-term and long-term recommendations
    - Potential high-return opportunities
    - Optional: relevant financial references or URLs
    """,
    agent=investment_advisor,
    tools=[analyze_investment_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="""
    Create a detailed risk analysis based on the financial document.
    Identify potential financial, market, and regulatory risks.
    Provide both short-term and long-term perspectives and mitigation strategies.
    """,
    expected_output="""
    - List of key financial and market risks
    - Severity and potential impact
    - Mitigation and contingency suggestions
    - Highlight unusual or hidden risks
    """,
    agent=risk_assessor,
    tools=[create_risk_assessment_tool],
    async_execution=False,
)

## Creating a verification task
verification = Task(
    description="""
    Check if the uploaded file is a legitimate financial document.
    Consider quarterly reports, annual statements, or investor updates.
    Flag invalid or irrelevant files confidently. Explain reasoning if unsure.
    """,
    expected_output="""
    - Confirm validity of the document
    - Highlight suspicious or irrelevant content
    - Suggest missing financial sections
    - Optional: provide a pseudo file path for reference
    """,
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)
