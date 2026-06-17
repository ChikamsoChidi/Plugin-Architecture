def render_chat_tree(messages, primary_color, background_color, secondary_background_color, text_color):

    # Initialize the string with the base CSS styles using the external variables
    css_style = f"""
        <style>
            /* Master Wrapper that fills the viewport and forces items to the bottom */
            .chat-wrapper {{
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                width: 100%;
                
                overflow-y: auto;
            }}
            
            .main-bubble {{
                background-color: {secondary_background_color};
                border-left: 5px solid {primary_color};
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
                margin-bottom: 10px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            .reply-container {{
                display: flex;
                margin-left: 25px;
                margin-bottom: 8px;
                border-left: 2px dashed {primary_color};
                padding-left: 20px;
            }}
            .reply-bubble {{
                background-color: {background_color};
                border: 1px solid {secondary_background_color};
                padding: 12px;
                border-radius: 8px;
                width: 100%;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }}
            .bubble-text {{
                color: {text_color};
                font-family: sans-serif;
                font-size: 14px;
                margin: 0;
                line-height: 1.5;
            }}
            .bubble-label {{
                font-size: 11px;
                color: {primary_color};
                font-weight: bold;
                text-transform: uppercase;
                margin-bottom: 4px;
                font-family: sans-serif;
            }}
        </style>
        
        <div id="chat-tree-container" class="chat-wrapper">
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
                

    css_style += """
        </div>
        <script>
            (function() {
                const container = document.getElementById('chat-tree-container');
                if (container) {
                    container.scrollTop = container.scrollHeight;
                }
            })();
        </script>
    """

    # Return the entire block of CSS + HTML text
    return css_style