import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize the globally recognized, light-weight sentence-transformer model
# This runs completely locally on your computer for free!
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def calculate_cosine_similarity(vector_a: list, vector_b: list) -> float:
    """Computes the cosine similarity metric between two numerical arrays."""
    vec1 = np.array(vector_a)
    vec2 = np.array(vector_b)
    
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(dot_product / (norm_a * norm_b))

def analyze_semantic_match(resume_json: dict, job_description_text: str) -> dict:
    """
    Computes semantic alignment score between parsed profile contents 
    and target corporate job requirements.
    """
    # 1. Compile the extracted resume context into a dense descriptive string
    skills_string = ", ".join(resume_json.get("skills", []))
    projects_string = " ".join(resume_json.get("projects_summary", []))
    resume_context = f"Candidate Profile. Skills: {skills_string}. Projects and Background: {projects_string}"
    
    # 2. Vectorize both text blocks using the embedding model
    resume_vector = embedding_model.embed_query(resume_context)
    jd_vector = embedding_model.embed_query(job_description_text)
    
    # 3. Calculate mathematical similarity
    raw_similarity = calculate_cosine_similarity(resume_vector, jd_vector)
    
    # Convert numerical similarity (-1 to 1 scale) into an enterprise match percentage (0% to 100%)
    match_percentage = round(max(0.0, raw_similarity) * 100, 2)
    
    return {
        "match_percentage": match_percentage,
        "alignment_tier": "High Match" if match_percentage >= 75 else "Moderate Match" if match_percentage >= 45 else "Low Match"
    }