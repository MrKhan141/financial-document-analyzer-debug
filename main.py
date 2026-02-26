# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment

app = FastAPI(title="Financial Document Analyzer")
os.environ["LITELLM_LOG"] = "DEBUG"
def run_crew(query: str, file_path: str):
    financial_crew = Crew(
        # Include all 3 specialized agents
        agents=[financial_analyst, investment_advisor, risk_assessor],
        tasks=[analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )
    return financial_crew.kickoff(inputs={'query': query, 'path': file_path})

@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this document")
):
    file_id = str(uuid.uuid4())
    file_path = os.path.normpath(os.path.join("data", f"doc_{file_id}.pdf"))
    
    try:
        os.makedirs("data", exist_ok=True)
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
            
        result = run_crew(query=query.strip(), file_path=file_path)
        return {"status": "success", "analysis": str(result)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)