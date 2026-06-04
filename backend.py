from google import genai
from google.genai import types


client = genai.Client()

def ai_module(pname):
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=f"The user searched for the Pokémon name '{pname}', but it doesn't exist. Guess what official Pokémon they were trying to type. Return ONLY the corrected name as a single word. Do not add punctuation.",
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=10
            )
        )
        
        
        if response.text:
            return response.text.strip()
            
        
        if response.candidates and response.candidates[0].content.parts:
            raw_text = response.candidates[0].content.parts[0].text
            if raw_text:
                return raw_text.strip()
                
        return "another Pokémon"
        
    except Exception as e:
        return f"Error: {str(e)}"
    
print(ai_module("charmonderrr"))