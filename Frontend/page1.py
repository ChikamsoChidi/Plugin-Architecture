import streamlit as st
from Backend.LLM import *
from Backend.chat_tree import render_chat_tree

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

        if "chat_tree_dict" not in st.session_state:
            st.session_state.chat_tree_dict = [] # Placeholder for the chat tree data structure
        if "parent_id" not in st.session_state:
            st.session_state.parent_id = None

        if "latest_id" not in st.session_state:
            st.session_state.latest_id = 0

        if "new_line" not in st.session_state:
            st.session_state.new_line = False
        # {"id": 1, "parent_id": None, "user": "Root User 1 (Blue)", "text": "This is the first main topic."},

    def create_message(self):
        if self.prompt: # if someone write a prompt chatgpt oss respond

            st.session_state["messages"].append({"role": "User", "content": self.prompt})

            # Add the message to the chat tree
            if st.session_state.new_line == False: # If there is no prompt to create a child from the previous parent
                st.session_state.chat_tree_dict.append({"id": st.session_state.latest_id,
                                            "parent_id" : None,
                                            "content": f"{self.prompt[:10]}..."})
                
                st.session_state.latest_id += 1
                st.session_state.parent_id = None
            elif st.session_state.new_line == True and st.session_state.parent_id == None: # if there is an instruction to create a new_line
            # but this must be when and only when the parent id is false 
                # first create the new parent Id from the last known Id
                st.session_state.parent_id = st.session_state.latest_id - 1
                st.session_state.chat_tree_dict.append({"id": st.session_state.latest_id,
                            "parent_id" : st.session_state.parent_id,
                            "content": f"{self.prompt[:10]}..."})
                st.session_state.latest_id += 1
            elif st.session_state.new_line == True and st.session_state.parent_id:
                # If there is an instruction for a new line and a chat already exists
                self.prompt = self.prompt + " (Branch from: " + st.session_state.chat_tree_dict[st.session_state.parent_id]["content"] + ")"
                st.session_state.chat_tree_dict.append({"id": st.session_state.latest_id,
                            "parent_id" : st.session_state.parent_id,
                            "content": f"{self.prompt[:10]}..."})
                st.session_state.latest_id += 1

            self.prompt = prompt_engine(self.prompt, st.session_state["messages"])
                
            # take only the parent id prompts and use them as history when creating new message to create chain of inference
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
        print(st.session_state["messages"])
        
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

        chat_col, tree_col = st.columns([7.5,1], border= False)

        with chat_col:
            st.markdown("""
                        <div class="chat">
                        {}
                        </div>
                        """.format(self.display_text), unsafe_allow_html=True)
        with tree_col:
            with st.container(height = "stretch", border = False):
                st.markdown(
                    """
                    <div class="tree">
                    <p style="text-align: left; font-size: 18px; color: #4CAF50;">
                    Chat Tree
                    </p>
                    <p style="text-align: center;
                    """,
                 unsafe_allow_html= True)
            with st.container(height="content", border = False): # Placeholder for the chat tree visualization
                chat_tree_css = render_chat_tree(st.session_state.chat_tree_dict)
                st.html(chat_tree_css)
            with st.container(height=90, border = False, vertical_alignment="bottom"): # Placeholder for the chat tree visualization
                self.is_branched = st.toggle(label=":green-background[Branch ⌥]")

                if self.is_branched:
                    st.session_state.new_line = True
                else:
                    st.session_state.new_line = False

    def sidebar(self):
        st.sidebar.title("Sidebar")
        st.sidebar.write("This is the sidebar content.")

