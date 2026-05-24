from click import prompt
import streamlit as st
from Backend.LLM import to_AI

st.set_page_config(page_title="AI chatbot", page_icon=":robot:", layout="wide")


class Page1:
    def __init__(self): # This the main page of the app
        # The title of the app
        st.markdown("""
        <div style="
        font-size: 16px;
        font-family: 'Courier New', monospace;
        color: #4CAF50;
        text-align: center;
        margin-top: 0px;
        margin-bottom: 5px;
        padding: 0;
        line-height: 1;
        ">
        Chat. Inquire. Explore.
        </div>
        """, unsafe_allow_html=True)
        if "messages" not in st.session_state: #create the session state variable to store the messages
            st.session_state["messages"] = []
        st.markdown("""
            <style>
                /* Change the border color and style */
                div[data-testid="stChatInput"] {
                    outline: none;
                    border: 2px solid green !important;
                    border-radius: 8px;
                }
            </style>
        """, unsafe_allow_html=True)

        self.prompt:str = st.chat_input("Ask me anything...")

    def create_message(self):
        if self.prompt: #if someone writes a prompt, return placeholder
            st.session_state["messages"].append({"role": "User", "content": self.prompt})
            to_AI_response = to_AI(self.prompt)
            st.session_state["messages"].append({"role": "AI", "content": to_AI_response})

    def display_messages(self):
        self.display_text = ""
        if "messages" in st.session_state:
            for message in st.session_state["messages"]:
                if message["role"] == "User":
                    self.display_text += f"""<p style="text-align: right;">{message["role"]}:<br>{message["content"]}</p> """
                elif message["role"] == "AI":
                    self.display_text += f"""<p>{message["role"]}:<br>{message["content"]}</p> 
                    <hr style="border-top: 3px solid green;">"""

    def render(self):
        # The main content of the page
        st.write("""<div
                 style="
                 font-size: 14px;
                 text-align: center;
                 font-family: 'Courier New', monospace;
                 color: #FFFFFF;
                 ">
                 It is in your hands...
                 <div/>""", unsafe_allow_html=True)
        self.create_message()
        self.display_messages()


        st.markdown("""
                    <div class="chat">
                    {}
                    </div>
                    """.format(self.display_text), unsafe_allow_html=True)
            

    def sidebar(self):
        st.sidebar.title("Sidebar")
        st.sidebar.write("This is the sidebar content.")

