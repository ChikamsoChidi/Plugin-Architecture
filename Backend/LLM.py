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
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                {
                    "role": "user",
                    "content": message
                }
                ],
                temperature=0.6,
                top_p=0.5,
                stream=False,
                stop=None
            )
            return completion.choices[0].message.content
        except Exception as e:
            return "Sorry, AI cannot be reached at this moment. Check internet connection."



def prompt_engine(prompt, session_messages):
    # Combine the prompt with the session messages to create a context for the AI
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session_messages[-5:]])  # Use the last 5 messages for context
    full_prompt = "The following is a conversation between a user and you. Use the context \"" + context + "\"as a guide to respond to the prompt \"" + prompt + "\". Keep your response concise and relevant to the prompt, not more than two paragraphs."
    return full_prompt
    
