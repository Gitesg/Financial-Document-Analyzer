# import os
# from dotenv import load_dotenv
# load_dotenv()

# from langchain_community.document_loaders import PyPDFLoader as Pdf
# from crewai_tools import SerperDevTool
# from crewai.tools.base_tool import Tool

# ## Search tool
# search_tool = SerperDevTool()

# ## Custom PDF Reader Tool
# class FinancialDocumentTool:
#     @staticmethod
#     def read_data_tool(args: dict, kwargs: dict):
#       path = args.get("path", "data/sample.pdf")
#       docs = Pdf(file_path=path).load()
#       full_report = "\n".join(d.page_content.replace("\n\n", "\n") for d in docs)
#       return full_report

# ## Investment Analysis Tool
# class InvestmentTool:
#     @staticmethod
#     async def analyze_investment_tool(financial_document_data):
#         # TODO: implement actual analysis
#         processed_data = financial_document_data
#         i = 0
#         while i < len(processed_data):
#             if processed_data[i:i+2] == "  ":
#                 processed_data = processed_data[:i] + processed_data[i+1:]
#             else:
#                 i += 1
#         return "Investment analysis functionality to be implemented"

# ## Risk Assessment Tool
# class RiskTool:
#     @staticmethod
#     async def create_risk_assessment_tool(financial_document_data):
#         # TODO: implement actual risk assessment
#         return "Risk assessment functionality to be implemented"


# read_data_tool = Tool(
#     name="read_data_tool",
#     description="Read content of a financial PDF document",
#     func=FinancialDocumentTool.read_data_tool  
# )

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader as Pdf
from crewai_tools import SerperDevTool
from crewai.tools.base_tool import Tool
import re


search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))


class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(args: dict, kwargs: dict):
        """
        Reads a PDF file and returns its full content.
        Input example:
        {"args": {"path": "data/sample.pdf"}, "kwargs": {}}
        """
        path = args.get("path", "data/sample.pdf")
        if not os.path.exists(path):
            return f"Error: file {path} not found."
        docs = Pdf(file_path=path).load()
        full_report = "\n".join(d.page_content.replace("\n\n", "\n") for d in docs)
        return full_report

read_data_tool = Tool(
    name="read_data_tool",
    description="Read content of a financial PDF document. Input: {\"args\":{\"path\":\"data/sample.pdf\"},\"kwargs\":{}}",
    func=FinancialDocumentTool.read_data_tool
)


class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(args: dict, kwargs: dict):
        """
        Analyze financial document content and return insights.
        Input example:
        {"args": {"document": "<financial text here>"}, "kwargs": {}}
        """
        document = args.get("document", "")
        insights = []

        # Extract ratios (basic regex logic)
        pe_matches = re.findall(r"P/E\s*ratio[:\s]*([\d.]+)", document, re.IGNORECASE)
        debt_matches = re.findall(r"Debt[- ]to[- ]Equity[:\s]*([\d.]+)", document, re.IGNORECASE)

        if pe_matches:
            pe = float(pe_matches[0])
            if pe > 25:
                insights.append(f"P/E ratio {pe} → stock may be overvalued.")
            else:
                insights.append(f"P/E ratio {pe} → valuation reasonable.")
        if debt_matches:
            debt_ratio = float(debt_matches[0])
            if debt_ratio > 1.5:
                insights.append(f"Debt-to-Equity ratio {debt_ratio} → company carries high leverage.")
            else:
                insights.append(f"Debt-to-Equity ratio {debt_ratio} → leverage within safe range.")

        # Simple text-based insights
        if "revenue grew" in document.lower():
            insights.append("Revenue growth detected → positive long-term signal.")
        if "decline" in document.lower() or "decreased" in document.lower():
            insights.append("Revenue/Profit decline → exercise caution.")

        if not insights:
            return "No clear ratios found. Further analysis required."
        return "Investment Insights:\n- " + "\n- ".join(insights)

analyze_investment_tool = Tool(
    name="analyze_investment_tool",
    description="Analyze a financial document and return investment insights. Input: {\"args\":{\"document\":\"...\"},\"kwargs\":{}}",
    func=InvestmentTool.analyze_investment_tool
)

# --------------------------
# Risk Assessment Tool
# --------------------------
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(args: dict, kwargs: dict):
        """
        Perform risk assessment based on financial document data.
        Input example:
        {"args": {"document": "<financial text here>"}, "kwargs": {}}
        """
        document = args.get("document", "")
        risks = []

        if "high debt" in document.lower() or "debt-to-equity" in document.lower():
            risks.append("High leverage could increase default risk during downturns.")
        if "loss" in document.lower():
            risks.append("Company is reporting losses → potential sustainability issue.")
        if "regulation" in document.lower():
            risks.append("Regulatory risks detected → may impact operations.")
        if "volatility" in document.lower():
            risks.append("High market volatility → increased investment risk.")

        if not risks:
            return "No significant risks detected in the provided document."
        return "Risk Assessment:\n- " + "\n- ".join(risks)

create_risk_assessment_tool = Tool(
    name="create_risk_assessment_tool",
    description="Generate a risk assessment from financial data. Input: {\"args\":{\"document\":\"...\"},\"kwargs\":{}}",
    func=RiskTool.create_risk_assessment_tool
)
