import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.services.parser import extract_text_from_pdf, parse_resume_with_llm
from app.services.matcher import analyze_semantic_match

load_dotenv()

app = FastAPI(
    title="AI Resume Analyzer & Interview Coach",
    description="Production backend engine combining vector matching and interview coaching features.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Resume Coach Backend Engine!"}

@app.post("/api/v1/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Groq API Key configuration missing.")
        
    try:
        raw_resume_text = extract_text_from_pdf(file)
        
        parsed_profile = parse_resume_with_llm(
            resume_text=raw_resume_text, 
            job_description_text=job_description, 
            groq_api_key=api_key
        )
        
        match_analytics = analyze_semantic_match(parsed_profile, job_description)
        
        return {
            "status": "success",
            "filename": file.filename,
            "match_score": match_analytics["match_percentage"],
            "alignment_tier": match_analytics["alignment_tier"],
            "parsed_profile": parsed_profile
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing AI analytics pipeline: {str(e)}")
@app.post("/api/v1/evaluate-answer")
async def evaluate_answer(
    question: str = Form(...),
    strategy: str = Form(...),
    user_answer: str = Form(...)
):
    api_key = os.getenv("GROQ_API_KEY")
    from langchain_groq import ChatGroq
    from langchain_core.prompts import PromptTemplate
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2, groq_api_key=api_key)
    
    prompt = PromptTemplate.from_template("""
    You are an expert technical interviewer. Evaluate the candidate's interview answer based on the given ideal strategy hint.
    Provide a score out of 10, a 2-sentence feedback critique, and an optimized version of how they should have phrased it.

    Question: {question}
    Ideal Strategy Hint: {strategy}
    Candidate's Answer: {user_answer}

    Return your output EXACTLY as a clean JSON object with these keys: 'score', 'feedback', 'better_phrasing'. Do not write markdown blocks around it.
    """)
    
    chain = prompt | llm
    response = chain.invoke({"question": question, "strategy": strategy, "user_answer": user_answer})
    import json
    return json.loads(response.content.replace("```json", "").replace("```", "").strip())