# Take a text and output a simple response
from ollama import chat


def to_AI(prompt, session_messages, is_branching=False):
    if not prompt:
        return "Please provide a message to send to the AI."

    # --- Combine session messages into context for the AI ---
    context = ""
    branch = ""
    recent_message_count = 6

    max_parent_id = max(
        [m["id"] for m in session_messages if m["parent_id"] is None],
        default=-1
    )

    for message in session_messages[:-1][::-1]:  # remove last msg (user query), walk backwards
        # Gather the latest messages in a sub branch and use as context
        if is_branching and message["parent_id"] == max_parent_id:
            context = f"\n{message['role']}: {message['content']}" + context
            recent_message_count -= 1
        # Gather the messages on the main path and use as context
        elif not is_branching and message["parent_id"] is None:
            context = f"\n{message['role']}: {message['content']}" + context
            recent_message_count -= 1
        if recent_message_count <= 0:
            break

    for message in session_messages:
        if message["id"] == max_parent_id:
            branch += f"\n{message['role']}: {message['content']}"

    # --- Build the system message (instructions + context) ---
    if is_branching:
        system_message = (
            "This is a conversation between a user and you (AI). "
            f"Use the context: \"{context}\" as a guide to respond to the user's prompt. "
            f"The conversation starts here: \"{branch}\"\n"
            "Keep your response concise and relevant to the prompt, not more than two paragraphs."
        )
    else:
        system_message = (
            "This a conversation between a user and you (AI). "
            f"Use the context: \"{context}\" as a guide to respond to the user's prompt. "
            "Keep your response concise and relevant to the prompt, not more than two paragraphs."
        )

    # --- Call the AI model ---
    try:
        response = chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        # Return message
        return response["message"]["content"]
    except Exception as e:
        return f"Uhhh... I have an error, please help! Look at it:\n{e}"