# Take a text and output a simple response
from ollama import chat


def to_AI(message = ""):
    if message == "":
        return "Please provide a message to send to the AI."
    elif message:
        try:
            response = chat(
                model = "llama3.2:1b",
                messages = [
                    {"role":"user",
                     "content": message}
                ],
                stream = False
            )
            # Return message
            return response["message"]["content"]
        except Exception as e:
            return f"Uhhh... I have an error, please help! Look at it:\n{e}"


def prompt_engine(prompt, session_messages, is_branching=False):
    # Combine the prompt with the session messages to create a context for the AI
    context = ""
    branch = ""
    recent_message_count = 6

    max_parent_id = None
    for message in session_messages[:-1][::-1]: #remove the last message (user query) and rearranges the code
        # Get the latest node on the main "path"
        max_parent_id = max([m["id"] for m in session_messages if m["parent_id"] is None], default=-1) 
        # Gather the latest messages in a sub branch and use as context
        if is_branching and message["parent_id"] == max_parent_id: 
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
        full_prompt = f"The following is a conversation between a user and you. Use the context: \"{context}\" \n as a guide to respond to the prompt: \"{prompt}\". The conversation starts at here: \{branch}\"\n Keep your response concise and relevant to the prompt, not more than two paragraphs."
    else:
        full_prompt = f"The following is a conversation between a user and you. Use the context: \"{context}\" \n as a guide to respond to the prompt: \"{prompt}\". Keep your response concise and relevant to the prompt, not more than two paragraphs."
    return full_prompt