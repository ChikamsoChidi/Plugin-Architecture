# input be like 
messages = [{'id': 0, 'parent_id': None, 'content': 'Hello...'},
{'id': 1, 'parent_id': None, 'content': 'I want to ...'},
{'id': 2, 'parent_id': 1, 'content': 'Tell me wh...'},
{'id': 3, 'parent_id': 1, 'content': 'why? Tell ...'},
{'id': 4, 'parent_id': None, 'content': 'forget abo...'}]

def render_chat_tree(messages):
    # 1. Initialize the string with the base CSS styles
    css_style = """
        <style>
            /* Master Wrapper that fills the viewport and forces items to the bottom */
            .chat-wrapper {
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                min-height: 70vh; /* Takes up most of the page height to push items down */
                width: 100%;
            }
            
            .main-bubble {
                background-color: #cefad0;
                border-left: 5px solid #4CAF50;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
                margin-bottom: 10px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .reply-container {
                display: flex;
                margin-left: 25px;
                margin-bottom: 8px;
                border-left: 2px dashed #4CAF50;
                padding-left: 20px;
            }
            .reply-bubble {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                padding: 12px;
                border-radius: 8px;
                width: 100%;
                box-shadow: 0 1px 2px rgba(0,0,0,0.02);
            }
            .bubble-text {
                color: #1e293b;
                font-family: sans-serif;
                font-size: 14px;
                margin: 0;
                line-height: 1.5;
            }
            .bubble-label {
                font-size: 11px;
                color: #4CAF50;
                font-weight: bold;
                text-transform: uppercase;
                margin-bottom: 4px;
                font-family: sans-serif;
            }
        </style>
        
        <div class="chat-wrapper">
    """

    # 2. Get the main nodes and sub nodes
    main_nodes = [m for m in messages if m["parent_id"] is None]
    sub_nodes = [m for m in messages if m["parent_id"] is not None]

    # 3. Build the HTML structure dynamically inside the string
    for node in main_nodes:
        css_style += f"""
        <div class="main-bubble">
            <div class="bubble-label">Main Topic</div>
            <p class="bubble-text">{node['content']}</p>
        </div>
        """

        for sub_node in sub_nodes:
            if sub_node["parent_id"] == node["id"]:
                css_style += f"""
                <div class="reply-container">
                    <div class="reply-bubble">
                        <div class="bubble-label">Reply</div>
                        <p class="bubble-text">{sub_node['content']}</p>
                    </div>
                </div>
                """
                
    # 4. Return the entire block of CSS + HTML text
    return css_style

