## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from tools import read_data_tool, analyze_investment_tool, create_risk_assessment_tool

from crewai.agent import Agent
from crewai.llm import LLM

from tools import search_tool, FinancialDocumentTool, InvestmentTool,RiskTool

### Loading LLM
llm = LLM(model="gpt-4o-mini", temperature=0.7, max_tokens=1500)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate, data-driven financial analysis based on the uploaded documents.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with deep expertise in corporate finance, "
        "investment strategies, and global market trends. You carefully read financial statements "
        "and highlight key insights such as revenue growth, profitability, liquidity, and debt ratios. "
        "Your recommendations are balanced, evidence-based, and focused on long-term value."
    ),
    tools=[read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=5,
    allow_delegation=True
)




verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify that uploaded files are valid financial documents before analysis.",
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in financial compliance and documentation standards. "
        "You carefully inspect uploaded files to ensure they are legitimate financial documents "
        "such as quarterly reports, annual statements, or investor updates. "
        "If a file is irrelevant (like a grocery list), you flag it as invalid."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=5,
    allow_delegation=False
)



investment_advisor = Agent(
    role="Investment Advisor",
    goal="Recommend suitable investment strategies based on verified financial documents.",
    verbose=True,
    backstory=(
        "You are a trusted investment advisor with expertise in asset allocation, "
        "portfolio diversification, and capital markets. "
        "You assess company fundamentals and provide clear, practical investment recommendations "
        "such as buy/hold/sell signals or portfolio strategies. "
        "Your advice is compliant, ethical, and aligned with investor goals and risk tolerance."
    ),
    llm=llm,
    tools=[analyze_investment_tool],
    max_iter=3,
    max_rpm=5,
    allow_delegation=False
)



risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify potential financial and market risks from the uploaded documents.",
    verbose=True,
    backstory=(
        "You are an expert in financial risk management, trained to detect and explain "
        "risks such as liquidity issues, credit exposure, market volatility, and regulatory concerns. "
        "You provide balanced risk assessments and help stakeholders understand both "
        "short-term and long-term risk implications."
    ),
    llm=llm,
    tools=[create_risk_assessment_tool],
    max_iter=3,
    max_rpm=5,
    allow_delegation=False
)

