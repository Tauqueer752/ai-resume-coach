import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="AI Resume Coach & Mock Interview Panel",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 700; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .score-card { background-color: #F3F4F6; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #E5E7EB; }
    .metric-value { font-size: 48px; font-weight: 800; color: #DC2626; }
    .coach-box { background-color: #EFF6FF; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 4px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Resume Coach & Practice Panel</div>', unsafe_allow_html=True)
st.write("---")

# 2. Initialize Persistent Session State Paths
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 3. Sidebar Console
st.sidebar.header("📂 Upload Center")
uploaded_file = st.sidebar.file_uploader("Upload your Resume (PDF format)", type=["pdf"])
job_description = st.sidebar.text_area("Paste Target Job Description", height=250, placeholder="Paste the job requirements here...")

analyze_button = st.sidebar.button("🚀 Analyze & Generate Coach Panel", use_container_width=True)

# Process the pipeline only when the main action trigger runs
if analyze_button:
    if uploaded_file and job_description:
        with st.spinner("Analyzing profile gaps and engineering mock interview questions..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"job_description": job_description}
                
                response = requests.post("http://127.0.0.1:8000/api/v1/analyze", files=files, data=data)
                
                if response.status_code == 200:
                    # Save the results securely into memory state
                    st.session_state.analysis_result = response.json()
                else:
                    st.error(f"Backend returned an error status: {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to the backend core engine: {str(e)}")
    else:
        st.sidebar.error("Please provide both a PDF resume and a Job Description text block!")

# 4. Main Rendering Interface (Reads from persistent memory state)
if st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    profile = result.get("parsed_profile", {})
    
    # Grid Layout Columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📊 Alignment Analytics")
        st.markdown(f"""
            <div class="score-card">
                <h4>Semantic Match Score</h4>
                <div class="metric-value">{result.get('match_score')}%</div>
                <p>Tier: <b>{result.get('alignment_tier')}</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🛠️ Extracted Skills")
        st.write(", ".join(profile.get("skills", [])))
        
        st.markdown("### ⚠️ Missing Critical Skills")
        for skill in profile.get("missing_skills", []):
            st.markdown(f"❌ `{skill}`")
            
    with col2:
        st.markdown("### 📋 ATS Layout Critique")
        st.info(profile.get("ats_formatting_critique", "No critique provided."))
        
        tab1, tab2 = st.tabs(["💡 Career Optimization Roadmap", "🎯 Practice Mock Interview"])
        
        with tab1:
            st.subheader("📚 Recommended Upskilling Courses")
            for course in profile.get("recommended_courses", []):
                st.write(f"🔹 {course}")
                
            st.subheader("🏗️ Strategic Portfolio Projects")
            for project in profile.get("project_suggestions", []):
                st.write(f"💡 {project}")
                
        with tab2:
            st.subheader("🎙️ Interactive Flashcards")
            questions = profile.get("mock_interview_questions", [])
            
            if questions:
                for idx, q in enumerate(questions):
                    with st.expander(f"Question {idx+1}: {q.get('question')} ({q.get('type')})"):
                        st.markdown(f"**Recruiter Intent:** *{q.get('intent')}*")
                        st.markdown(f"<div class='coach-box'><b>Strategy Hint:</b> {q.get('ideal_answer_strategy')}</div>", unsafe_allow_html=True)
                        
                        # Text box for candidate practice input
                        user_ans = st.text_area("Type your practice answer here to evaluate:", key=f"ans_{idx}", height=100)
                        
                        # Trigger evaluation without clearing page data
                        if st.button(f"Submit Answer {idx+1} for Grading", key=f"btn_{idx}"):
                            if user_ans.strip():
                                with st.spinner("Grading response..."):
                                    eval_res = requests.post(
                                        "http://127.0.0.1:8000/api/v1/evaluate-answer",
                                        data={
                                            "question": q.get('question'),
                                            "strategy": q.get('ideal_answer_strategy'),
                                            "user_answer": user_ans
                                        }
                                    ).json()
                                    
                                    st.metric("Coach Performance Score", f"{eval_res.get('score')}/10")
                                    st.warning(f"💡 Feedback: {eval_res.get('feedback')}")
                                    st.success(f"🌟 Better Way to Say It: {eval_res.get('better_phrasing')}")
                            else:
                                st.error("Please type out an answer before submitting for evaluation!")
            else:
                st.write("No mock interview questions compiled.")
else:
    # Initial dynamic user landing instructions
    st.info("💡 Complete the Upload Center configurations in the sidebar menu and click execute to trigger the pipeline dashboard layout.")