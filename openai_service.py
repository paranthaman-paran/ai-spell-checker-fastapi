from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_spelling(text: str):
    """
    Checks the spelling and grammar of the given text using OpenAI.
    """
    if not text:
        return {"corrected_text": "", "changes": []}

    prompt = f"""
    You are a helpful assistant that corrects spelling and grammar.
    Correct the following text.
    Return ONLY a JSON object with the following structure:
    {{
        "corrected_text": "The corrected text",
        "changes": ["List of changes made, e.g., 'Fixed spelling of necessary'"]
    }}
    
    Text to correct:
    {text}
    """


    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or gpt-4o if available/preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {"corrected_text": text, "changes": ["Error: Could not process text."]}
