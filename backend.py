from google import genai
from google.genai import types
import requests

client = genai.Client(api_key="AIzaSyBM0TUfn-9_87RuIFqhTVaw-ElRYb8tf-M")

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
    


def main(pname):
    url=f"https://pokeapi.co/api/v2/pokemon/{pname}"
    
    data=requests.get(url)
    if(data.status_code==200):
        signal="green"
        
        response=data.json()
        image_url=response.get('sprites', {}).get('other', {}).get('official-artwork', {}).get('front_default')
        idd=response.get('id')

        hight=response.get('height')
        weight=response.get('weight')/10
        return signal,idd,weight,hight,image_url


    elif(data.status_code==404):
        signal="red"
        idd=None
        weight=None
        hight=None
        image_url=None
        return signal,idd,weight,hight,image_url
    else:
        signal="black"
        idd=None
        weight=None
        hight=None
        image_url=None
        return signal,idd,weight,hight,image_url