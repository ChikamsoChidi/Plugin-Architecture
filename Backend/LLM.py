# Take a text and output a simple response

from groq import Groq
import os
from dotenv import load_dotenv

# Load variables from a .env file
load_dotenv() 
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def to_AI(message = ""):
    if message == "":
        return "Please provide a message to send to the AI."
    
    elif message:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
            {
                "role": "user",
                "content": message
            }
            ],
            temperature=1,
            top_p=1,
            stream=False,
            stop=None
        )

        return completion.choices[0].message.content