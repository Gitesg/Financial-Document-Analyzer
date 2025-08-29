from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import uuid
import asyncio
from fastapi import APIRouter
from celery.result import AsyncResult
from tasks1 import run_crew_task
from datetime import datetime
from crewai import Crew, Process
from savedb import save_to_db
# from crewai.agent import Agent
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document_task, investment_analysis, risk_assessment, verification
from tasks1 import run_crew_task    

from celery_app import celery_app 

app = FastAPI(title="Financial Document Analyzer")

#harcoded path for now, can be changed later
def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    print(f"Running crew with query: {query} and file_path: {file_path}")
    financial_crew = Crew(
    agents=[financial_analyst, verifier, investment_advisor, risk_assessor],
    tasks=[verification, analyze_financial_document_task, risk_assessment, investment_analysis],
    process=Process.sequential,
    )
  
    print("f{}")
    
    result = financial_crew.kickoff({'query': query})
    return result


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    print(f"Received file: {file.filename}, saving to {file_path}")
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query=="" or query is None:
            query = "Analyze this financial document for investment insights"

        
            
        # added celery  
        response = run_crew_task.delay(query=query.strip(), file_path=file_path)
        
        return {
         "status": "processing",
         "query": query,
         "task_id": response.id,
         "file_processed": file.filename
}
        
        
        
     

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors




@app.get("/result/{task_id}")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=run_crew_task.app)
    
    response = {
        "task_id": task_id,
        "state": task_result.state,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    if task_result.state == "PENDING":
        response["status"] = "pending"
        response["message"] = "Task is still being processed."
    elif task_result.state == "SUCCESS":
        response["status"] = "success"

        # Ensure result is safely serialized
        response["result"] = getattr(task_result, "result", None)
        # response["result"] = getattr(task_result, "result", None)

        # Store result in MongoDB Atlas
        mongo_data = {
            "task_id": task_id,
            "state": task_result.state,
            "status": "success",
            "timestamp": response["timestamp"],
            "result": task_result.result
        }
        save_to_db(mongo_data)
    elif task_result.state == "FAILURE":
        response["status"] = "failure"
        response["error"] = str(getattr(task_result, "result", "Unknown error"))

    return response



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)




