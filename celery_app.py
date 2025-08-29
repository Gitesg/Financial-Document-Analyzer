
from celery import Celery  

celery_app = Celery(
    "financial_document_analyzer",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks1"]   
)

