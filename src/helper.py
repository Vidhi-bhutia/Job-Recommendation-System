import fitz 
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    doc=fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = " "
    for page in doc:
        text+=page.get_text()
    return text

def ask_gemini(prompt):
    """Send a prompt to Gemini and return the response."""
    if not GEMINI_API_KEY:
        return "Gemini API key not configured. Please set GEMINI_API_KEY in .env file."
    
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing resume with Gemini: {str(e)}"


import json

# ... existing imports ...

def match_resume_to_job(resume_text, job_title, job_snippet):
    """
    Compare resume with job description using Gemini.
    Returns a dict with 'percentage' (int) and 'tips' (list).
    """
    if not GEMINI_API_KEY:
        return {"percentage": 0, "tips": ["API Key missing"]}

    prompt = f"""
    Act as an ATS (Applicant Tracking System) expert.
    
    Resume Text:
    {resume_text[:2000]}
    
    Job Title: {job_title}
    Job Snippet: {job_snippet}
    
    Evaluate the match between the resume and the job.
    Return ONLY a JSON object with this exact structure:
    {{
        "percentage": <int between 0 and 100>,
        "tips": ["<tip 1>", "<tip 2>", "<tip 3>"]
    }}
    Provide 3 actionable tips to improve the match.
    """
    
    try:
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up code blocks if present
        if text.startswith("```json"):
            text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
        elif text.startswith("```"):
            text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
        return json.loads(text.strip())
    except Exception as e:
        print(f"Gemini Matching Error: {str(e)}") # Print to console for debugging
        return {"percentage": 0, "tips": ["Could not analyze match - API Error"]}
