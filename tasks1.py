# tasks.py
from celery_app import celery_app   # <-- IMPORT CELERY INSTANCE
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document_task

@celery_app.task(name="tasks.run_crew_task")
def run_crew_task(query: str, file_path: str):
    """Celery task to run the financial crew"""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document_task],
        process=Process.sequential,
    )
    result = financial_crew.kickoff({'query': query})
    return str(result)
