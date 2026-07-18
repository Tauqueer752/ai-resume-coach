from pydantic import BaseModel, Field
from typing import List, Optional

class InterviewQuestion(BaseModel):
    question: str = Field(description="The mock interview question.")
    type: str = Field(description="Type: 'Technical', 'Behavioral', or 'Project-Specific'")
    ideal_answer_strategy: str = Field(description="A tip or structural hint (like the STAR method) on how to answer this question.")

class ResumeSchema(BaseModel):
    name: str = Field(description="The full name of the candidate.")
    email: Optional[str] = Field(description="The email address of the candidate.")
    skills: List[str] = Field(description="Technical skills found on the resume.")
    experience_years: float = Field(description="Total calculated years of experience.")
    projects_summary: List[str] = Field(description="Brief list of projects mentioned.")
    ats_formatting_critique: str = Field(description="A brief structural critique of the resume layout.")
    
    # THE INTERVIEW COACH TIER
    missing_skills: List[str] = Field(description="Critical technical skills from the job description missing from the resume.")
    recommended_courses: List[str] = Field(description="2-3 specific course topics or certifications to bridge the missing skill gap.")
    project_suggestions: List[str] = Field(description="1-2 portfolio project ideas the candidate can build.")
    
    # CORE INTERVIEW COACH COMPONENT
    mock_interview_questions: List[InterviewQuestion] = Field(description="A set of 3-4 customized technical, behavioral, and project-specific questions for the candidate to practice.")