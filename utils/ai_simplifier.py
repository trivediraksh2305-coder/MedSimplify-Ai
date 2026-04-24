# utils/ai_simplifier.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def simplify_report(text):
    try:
        # Make sure text is not empty
        if not text or len(text.strip()) == 0:
            return "❌ No text found in the report."
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant who simplifies medical reports."
                },
                {
                    "role": "user",
                    "content": f"""Here is a medical report. Please simplify it 
                    for a patient with no medical knowledge.
                    Explain what each value means in simple words.
                    Tell if values are normal or abnormal.
                    
                    MEDICAL REPORT:
                    {text}
                    
                    Please explain this in simple language."""
                }
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error simplifying report: {str(e)}"