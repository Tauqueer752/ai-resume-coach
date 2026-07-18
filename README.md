# 🤖 AI Resume Coach & Interactive Practice Panel

A full-stack AI system designed to audit engineering resumes against target job descriptions, calculate semantic alignments, extract core skill gaps, and provide interactive interview coaching.

## 🏗️ System Architecture
- **Backend Core**: Built with FastAPI. Features automated PDF text extraction (`pdfplumber`) and LangChain integrations.
- **AI Orchestration**: Uses Groq Cloud running `llama-3.3-70b-versatile` utilizing structured JSON outputs via Pydantic schemas.
- **Semantic Vector Matcher**: Employs local sentence-transformers models (`all-MiniLM-L6-v2`) to perform mathematical Cosine Similarity transformations between profile definitions and JD metadata.
- **Frontend Panel**: Multi-tab, fully responsive dashboard running on Streamlit with interactive session-state management and custom theme configurations.

## 🛠️ Step-by-Step Local Deployment
1. Clone the repository and navigate into the backend folder:
   ```bash
   cd backend
