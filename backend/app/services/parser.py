import pdfplumber
from fastapi import UploadFile
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.schemas.resume import ResumeSchema

def extract_text_from_pdf(file: UploadFile) -> str:
    """Extracts raw text from an uploaded PDF file safely."""
    raw_text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"
    return raw_text

def parse_resume_with_llm(resume_text: str, job_description_text: str, groq_api_key: str) -> dict:
    """Uses Groq to analyze the resume against the JD, generating gap analytics and mock interview questions."""
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=0.3,
        groq_api_key=groq_api_key
    )
    
    output_parser = JsonOutputParser(pydantic_object=ResumeSchema)
    
    prompt_template = """
    You are an expert technical interviewer and career coach.
    Analyze the candidate's resume against the target Job Description (JD).
    Extract their profile, identify missing skills, and formulate targeted mock interview practice questions (Technical, Behavioral, and Project-Specific) based on their background to help them ace the placement.

    Target Job Description:
    {job_description}

    Candidate Raw Resume Text:
    {resume_text}

    Formatting Requirements:
    {format_instructions}
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["resume_text", "job_description"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    
    chain = prompt | llm | output_parser
    return chain.invoke({"resume_text": resume_text, "job_description": job_description_text})