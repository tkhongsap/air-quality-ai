import re
import html
import streamlit as st

def format_message(text):
    """
    This function is used to format the messages in the chatbot UI.

    Parameters:
    text (str): The text to be formatted.
    """
    text_blocks = re.split(r"```[\s\S]*?```", text)
    code_blocks = re.findall(r"```([\s\S]*?)```", text)

    text_blocks = [html.escape(block) for block in text_blocks]

    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f'<pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>'

    return formatted_text

def message_func(text, user_icon_base64, assistant_icon_base64, is_user=False, model="Claude-3 Haiku"):
    """
    This function is used to display the messages in the chatbot UI.

    Parameters:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or not.
    user_icon_base64 (str): Base64 encoded user avatar image.
    assistant_icon_base64 (str): Base64 encoded assistant avatar image.
    """

    # Escape special HTML characters in the text to avoid Markdown interpretation
    escaped_text = html.escape(text)

    avatar_base64 = user_icon_base64 if is_user else assistant_icon_base64

    if is_user:
        message_alignment = "flex-end"
        message_bg_color = "#D7E8FA"  # Light blue for user messages
        message_text_color = "#000000"  # Black text for user messages
        avatar_class = "user-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: {message_text_color}; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {escaped_text} \n </div>
                    <img src="{avatar_base64}" class="{avatar_class}" alt="avatar" style="width: 40px; height: 40px;" />
                </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        message_alignment = "flex-start"
        message_bg_color = "#FFFFFF"  # White for assistant messages
        message_text_color = "#000000"  # Black text for assistant messages
        avatar_class = "bot-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_base64}" class="{avatar_class}" alt="avatar" style="width: 40px; height: 40px;" />
                    <div style="background: {message_bg_color}; color: {message_text_color}; border-radius: 20px; padding: 10px; margin-left: 5px; max-width: 75%; font-size: 14px; border: 1px solid #E5E8E8;">
                        {text} \n </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
