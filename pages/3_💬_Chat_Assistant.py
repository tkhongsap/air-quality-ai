import streamlit as st
import warnings
import base64
from openai import OpenAI

from utils.message_utils import message_func
from utils.openai_utils import generate_response
from utils.custom_css_banner import get_chat_assistant_banner

# Set page config
st.set_page_config(page_title="💬 Chat Assistant", page_icon="", layout="wide")

# Display the custom banner in the UI
st.markdown(get_chat_assistant_banner(), unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set assistant ID (customized assistant)
assistant_id = "asst_cIHPEgKEw7XtmMcn8ovvCxSx"  # air quality chat assistant

warnings.filterwarnings("ignore")

# Initialize session state for chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Welcome to the Air Quality Command Center! 👋\n\nI'm your dedicated Air Quality Assistant, how can I assist you today?"}
    ]

# Load user and assistant icons
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

user_icon_path = "image/user_icon.png"
assistant_icon_path = "image/air_quality_assistant_icon.png"
user_icon_base64 = get_image_base64(user_icon_path)
assistant_icon_base64 = get_image_base64(assistant_icon_path)

# Display the chat history
for message in st.session_state.chat_messages:
    is_user = message["role"] == "user"
    message_func(message["content"], user_icon_base64, assistant_icon_base64, is_user=is_user)

# Accept user input
prompt = st.chat_input("Your message")

# Handle user input
if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    message_func(prompt, user_icon_base64, assistant_icon_base64, is_user=True)

    # Generate response using the assistant
    response = generate_response(prompt, assistant_id, None)
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    message_func(response, user_icon_base64, assistant_icon_base64)


