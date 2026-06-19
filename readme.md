# AI Chatbot with Branching Chat Tree

A Streamlit-based chatbot interface that connects to a local Ollama instance running Llama 3.2:1b. This application features a unique branching mechanism that allows users to create visual conversation forks, manage context shifts, and hot-swap custom UI themes dynamically using a plugin-based architecture.

---

## Features

* **Local LLM Execution**: Powered entirely on your machine via Ollama and the Llama 3.2:1b model.
* **Conversational Branching**: Toggle branching mode to create structural forks in your chat history, allowing you to explore separate conversational paths.
* **Visual Chat Tree Sidebar**: A real-time, custom CSS-rendered visualization of your conversational nodes and nested replies.
* **Dynamic Plugin Themes**: Scans a dedicated directory to dynamically load user-created custom themes without restarting the server.
* **Context-Aware Memory**: Handles history slicing differently based on whether you are navigating the main path or actively branching out a sub-topic.

---

## Architecture Overview

The codebase is modularized across separate concerns:

1. **Frontend (`main.py`)**: Manages the Streamlit lifecycle, sessions, custom styled Markdown components, and user interactions.
2. **LLM Connector (`Backend/LLM.py`)**: Houses the Ollama API client Wrapper, handling system instructions, state-aware prompt formatting, and context-window slicing.
3. **Visualization Component (`Backend/chat_tree.py`)**: Generates customized HTML and CSS blocks alongside a JavaScript auto-scroll script to map conversational objects to UI containers.

---

## Prerequisites
Before setting up the application, ensure you have the following prerequisites installed on your system:

* Python 3.8 or higher
* Windows environment (or adaptation of the initial setup scripts)

---

## Installation

Follow these steps to set up the repository and dependencies locally.

### 1. Install Ollama and the LLM Model

Execute the installation script to pull the latest Ollama installer and download the target small language model. On Windows, you can open PowerShell and execute:

```bash
./install.sh

```

Alternatively, you can manually run the contents of the script:

```bash
# Download and install Ollama
irm https://ollama.com | iex

# Pull the required 1-billion parameter model
ollama run llama3.2:1b

```

### 2. Install Python Dependencies

Install the required application frameworks and client libraries using pip:

```bash
pip install -r requirements.txt

```

---

## Directory Structure

To ensure the dynamic theme-loader and module imports resolve properly, verify your directory matches the layout below:

```text
├── Backend/
│   ├── LLM.py
│   └── chat_tree.py
├── Themes/
│   ├── __init__.py
│   ├── default.py
│   └── (Your Custom Themes Go Here)
├── install.sh
├── main.py
├── requirements.txt
└── run.sh

```

---

## Running the Application

Once your local Ollama instance is up and running, trigger the Streamlit server using the provided run script:

```bash
./run.sh

```

Or execute the command directly in your terminal:

```bash
streamlit run main.py

```

---

## Customizing Themes

The application automatically scans the `Themes` directory for valid Python modules to generate selection choices in the sidebar dropdown.

To create a new theme, add a file named `my_theme.py` to the `Themes/` directory. The file must expose a class named `Plugin` containing the required color variables as strings:

```python
class Plugin:
    def __init__(self):
        self.primary_color = "#FF4B4B"
        self.background_color = "#FFFFFF"
        self.secondary_background_color = "#F0F2F6"
        self.text_color = "#31333F"

```