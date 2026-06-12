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

def prompt_engine(prompt, session_messages, is_branching=False):
    # Combine the prompt with the session messages to create a context for the AI
    context = ""
    branch = ""
    recent_message_count = 6

    max_parent_id = None
    for message in session_messages[:-1][::-1]:
        max_parent_id = max([m["id"] for m in session_messages if m["parent_id"] is None], default=-1)
        if is_branching and message["parent_id"] == max_parent_id: #gather the messages in a branch and use as context
            context = f"\n{message['role']}: {message['content']}" + context
            recent_message_count -= 1
        elif not is_branching and message["parent_id"] is None: # gather the messages on the the main and use as conext
            context = f"\n{message['role']}: {message['content']}" + context
            recent_message_count -= 1
        if recent_message_count <= 0:
            break
    for message in session_messages:
        if message["id"] == max_parent_id:
            branch += f"\n{message['role']}: {message['content']}"  

    if is_branching:
        full_prompt = "The following is a conversation between a user and you. Use the context: \"" + context + "\" \n as a guide to respond to the prompt: \"" + prompt + "\". The conversation starts at here: \"" + branch + "\"\n Keep your response concise and relevant to the prompt, not more than two paragraphs."
    else:
        full_prompt = "The following is a conversation between a user and you. Use the context: \"" + context + "\" \n as a guide to respond to the prompt: \"" + prompt + "\". Keep your response concise and relevant to the prompt, not more than two paragraphs."
    return full_prompt