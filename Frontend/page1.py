import streamlit as st
from Backend.LLM import *
from Backend.chat_tree import render_chat_tree
import importlib
import sys
import os

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="AI chatbot", page_icon=":robot:", layout="wide")

@st.cache_resource
def get_theme_plugins():
    """
    Scans the Themes directory once and caches the available theme paths.
    This prevents slow disk reads on every user interaction.
    """
    file_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugins_directory = os.path.join(file_directory, "Themes")
    
    # Safely add to sys.path if it isn't already there
    if plugins_directory not in sys.path:
        sys.path.insert(0, plugins_directory)
        
    plugin_dict = {}
    if os.path.exists(plugins_directory):
        plugin_names = os.listdir(plugins_directory)
        for plugin in plugin_names:
            # find only python files, ignore __init__.py file
            if plugin.endswith(".py") and not plugin.startswith("__"): 
                plugin_dict[plugin[:-3].title()] = plugin
                
    return plugin_dict

class Page1:
    def __init__(self):
        if "messages" not in st.session_state: #create the session state variable to store the messages
            st.session_state["messages"] = []
        
        if "chat_tree_dict" not in st.session_state:
            st.session_state.chat_tree_dict = [] # Placeholder for the chat tree data structure
        if "parent_id" not in st.session_state:
            st.session_state.parent_id = None

        if "latest_id" not in st.session_state:
            st.session_state.latest_id = 0

        if "new_line" not in st.session_state:
            st.session_state.new_line = False
        
        if "theme" not in st.session_state:
            st.session_state.theme = "Default"

        self.plugin_dict = get_theme_plugins()

    def load_theme(self):
        # Take the theme from session state and call the plugins
        module = importlib.import_module(st.session_state.theme.lower())
        ThemeClass = getattr(module, "Plugin")
        theme = ThemeClass()

        # assign the theme variables to class attributes
        self.primary_color = theme.primary_color
        self.background_color = theme.background_color
        self.secondary_background_color = theme.secondary_background_color
        self.text_color = theme.text_color

    def create_message(self):
        if self.prompt: # if someone write a prompt chatgpt oss respond

            # Placeholder: !!!!! May cause errors
            id = st.session_state.latest_id
            parent_id = st.session_state.parent_id

            # Add the message to the chat tree
            if st.session_state.new_line == False and st.session_state.parent_id == None: # If there is no prompt to create a child and there is no parent, meaning that this is a new chat or a continuation of the main line
                parent_id = None
                id = st.session_state.latest_id
                
                st.session_state.chat_tree_dict.append({"id": id,
                                            "parent_id" : parent_id,
                                            "content": f"{self.prompt[:30].strip() + '...' if len(self.prompt) > 30 else self.prompt}"}) 
                st.session_state.latest_id += 1
                st.session_state.parent_id = None
            elif st.session_state.new_line == False and st.session_state.parent_id >= 0: # if there is no prompt to create a child but there is a parent id, this means the user has toggled off the branching option and wants to continue the main line of conversation
                parent_id = None
                id = st.session_state.latest_id
                
                st.session_state.chat_tree_dict.append({"id": id,
                                            "parent_id" : parent_id,
                                            "content": f"{self.prompt[:30].strip() + '...' if len(self.prompt) > 30 else self.prompt}"}) 
                st.session_state.latest_id += 1
                st.session_state.parent_id = None
            elif st.session_state.new_line == True and st.session_state.parent_id == None: # if there is an instruction to create a child but there is no parent id, meaning that the user has toggled on the branching
                st.session_state.parent_id = st.session_state.latest_id - 1

                parent_id = st.session_state.parent_id
                id = st.session_state.latest_id

                st.session_state.chat_tree_dict.append({"id": id,
                            "parent_id" : parent_id,
                            "content": f"{self.prompt[:30].strip() + '...' if len(self.prompt) > 30 else self.prompt}"})
                st.session_state.latest_id += 1
            elif st.session_state.new_line == True and st.session_state.parent_id >= 0:
                # If there is an instruction for a new line and a chat already exists, meaning the branching is activated and the chat wants to continue on that branch
                parent_id = st.session_state.parent_id
                id = st.session_state.latest_id
                st.session_state.chat_tree_dict.append({"id": id,
                            "parent_id" : parent_id,
                            "content": f"{self.prompt[:30].strip() + '...' if len(self.prompt) > 30 else self.prompt}"})
                st.session_state.latest_id += 1

            st.session_state["messages"].append({"id":id, "parent_id":parent_id, "role": "User", "content": self.prompt})
            
            # Ask the AI the prompt
            to_AI_response = to_AI(self.prompt, st.session_state["messages"], is_branching=st.session_state.new_line)

            st.session_state["messages"].append(
                {"id":id,
                 "parent_id":parent_id,
                 "role": "AI",
                 "content": to_AI_response})
           

    def display_messages(self):
        # This is where the text is displayed
        self.display_text = ""
        if "messages" in st.session_state:
            for message in st.session_state["messages"]:
                if message["role"] == "User":
                    self.display_text += f"""<p style="text-align: right;">{message["role"]}:<br>{message["content"]}</p> """
                elif message["role"] == "AI":
                    self.display_text += f"""<p>{message["role"]}:<br>{message["content"]}</p>
                    <hr style="border-top: 3px solid {self.primary_color};">"""

    def update_theme_callback(self):
        # This callback ensures Streamlit commits the value to state instantly
        st.session_state.theme = st.session_state.temp_theme
        
    def sidebar(self):
        with st.sidebar:
            with st.container(height = 50, border = False):
                st.markdown(
                    f"""
                    <div class="tree">
                    <p style="text-align: left; font-size: 22px; color: {self.primary_color}; margin-bottom: 0;">
                    Chat Tree
                    </p>
                    </div>
                    """,
                    unsafe_allow_html= True)
            with st.container(height=400, border = False): # Placeholder for the chat tree visualization
                chat_tree_css = render_chat_tree(st.session_state.chat_tree_dict, 
                            self.primary_color, self.background_color, 
                            self.secondary_background_color, self.text_color)
                st.html(chat_tree_css)
            with st.container(height="content", border = False, vertical_alignment="top"): # Placeholder for the branch button
                self.is_branched = st.toggle(label=f":color[Branch ⌥]{{background='{self.primary_color}'}}")

                if self.is_branched:
                    st.session_state.new_line = True
                else:
                    st.session_state.new_line = False
            with st.container(height = "content", border = False, vertical_alignment = "bottom"):
                # Get available themes
                themes_list = list(self.plugin_dict.keys())
                
                # Find the index of the current theme to keep the dropdown synchronized
                default_index = themes_list.index(st.session_state.theme) if st.session_state.theme in themes_list else 1

                # Render selectbox with a key and callback
                st.selectbox(
                    "Change Chat Theme", 
                    options=themes_list, 
                    index=default_index,
                    key="temp_theme",
                    on_change=self.update_theme_callback
                )

    def render(self):
    # The main content of the page
        self.load_theme()

        self.prompt:str = st.chat_input("Ask me anything...")

        self.create_message()
        self.display_messages()

        self.sidebar()

        # The title of the app
        self.title = st.markdown(f"""
        <div style="
        font-size: 16px;
        font-family: 'Courier New', monospace;
        font-weight: Bold;
        color: {self.primary_color};
        text-align: center;
        margin-top: 0px;
        margin-bottom: 5px;
        padding: 0;
        line-height: 1;
        ">
        Chat. Inquire. Explore.
        </div>
        """, unsafe_allow_html=True)

        #The next line
        st.write(f"""<div
            style="
            font-size: 14px;
            text-align: center;
            font-family: 'Courier New', monospace;
            color: {self.primary_color};
            ">
            It is in your hands...
            <div/>""", unsafe_allow_html=True)

        # The messaging box
        st.markdown(f"""
            <style>
                /* Change the border color and style */
                div[data-testid="stChatInput"] {{
                    outline: none;
                    border: 2px solid {self.primary_color} !important;
                    border-radius: 8px;
                }}
            </style>
        """, unsafe_allow_html=True)
        
        #The message between AI and user 
        st.markdown("""
                    <div class="chat">
                    {}
                    </div>
                    """.format(self.display_text), unsafe_allow_html=True)