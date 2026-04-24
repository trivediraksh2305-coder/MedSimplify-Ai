# utils/advice.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_personalized_advice(abnormal_df, report_text):
    try:
        if abnormal_df.empty:
            return "✅ Your report looks normal! Maintain a healthy lifestyle."

        issues = abnormal_df['Test'].tolist()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant."
                },
                {
                    "role": "user",
                    "content": f"""Give simple health advice for a patient
                    with abnormal values in: {issues}
                    Keep it simple and friendly."""
                }
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error getting advice: {str(e)}"