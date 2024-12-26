import streamlit as st
import warnings
import base64
import json
import os
from openai import OpenAI
from datetime import datetime
from pathlib import Path

from utils.message_utils import message_func
from utils.openai_utils import generate_response
from utils.custom_css_banner import get_chat_assistant_banner

# Set page config
st.set_page_config(page_title="💡 Command Center", page_icon="", layout="wide")

# Display the custom banner in the UI
st.markdown(get_chat_assistant_banner(), unsafe_allow_html=True)

# Custom CSS for responsive layout
st.markdown("""
<style>
    /* Alert section styling */
    .alert-section {
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;  /* Add space between sections */
    }
    
    /* Chat section styling */
    .chat-section {
        padding: 1rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Alert card styling */
    .alert-card {
        padding: 1rem;
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ff4b4b;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

def get_latest_alert_file():
    alerts_dir = Path("output/alerts")
    alert_files = list(alerts_dir.glob("bangkok_aqi_alerts_*.json"))
    if not alert_files:
        return None
    return max(alert_files, key=lambda x: x.stat().st_mtime)

def load_alerts():
    latest_file = get_latest_alert_file()
    if not latest_file:
        return None
    
    try:
        # Open file with UTF-8 encoding and print the data for debugging
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data["alerts"]:
                first_alert = data["alerts"][0]
                # Print the loaded data for verification
                print("Loaded alert data:", first_alert)
                return first_alert
    except Exception as e:
        st.error(f"Error loading alerts: {str(e)}")
        return None
    return None

# # Alert Section
# st.markdown("### Air Quality Command Center")

# Load and display alert information
alert_data = load_alerts()
if alert_data:
    # Create columns for the metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    # AQI Card
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(to bottom, rgba(255, 75, 75, 0.1), rgba(255, 75, 75, 0.05)); padding: 0.9rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #FF4B4B; margin: 0;">{aqi}</div>
            <div style="color: #666; font-size: 0.8rem; margin: 0.2rem 0;">Current AQI</div>
            <div style="color: #FF4B4B; font-size: 0.7rem;">{level}</div>
        </div>
        """.format(
            aqi=alert_data["aqi"],
            level=alert_data["aqi_level"]
        ), unsafe_allow_html=True)

    # PM2.5 Card
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(to bottom, rgba(255, 139, 61, 0.1), rgba(255, 139, 61, 0.05)); padding: 0.9rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #FF8B3D; margin: 0;">{pm25} <span style="font-size: 0.8rem;">μg/m³</span></div>
            <div style="color: #666; font-size: 0.8rem; margin: 0.2rem 0;">PM2.5 Level</div>
            <div style="color: #FF8B3D; font-size: 0.7rem;">{type}</div>
        </div>
        """.format(
            pm25=alert_data["pm25_level"],
            type=alert_data["pm25_type"]
        ), unsafe_allow_html=True)

    # Temperature Card
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(to bottom, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05)); padding: 0.9rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #3B82F6; margin: 0;">{temp}°C</div>
            <div style="color: #666; font-size: 0.8rem; margin: 0.2rem 0;">Temperature</div>
            <div style="color: #3B82F6; font-size: 0.7rem;">{type}</div>
        </div>
        """.format(
            temp=alert_data["temperature_level"],
            type=alert_data["temperature_type"]
        ), unsafe_allow_html=True)

    # Humidity Card
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(to bottom, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05)); padding: 0.9rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #3B82F6; margin: 0;">{humidity}%</div>
            <div style="color: #666; font-size: 0.8rem; margin: 0.2rem 0;">Humidity</div>
            <div style="color: #3B82F6; font-size: 0.7rem;">{type}</div>
        </div>
        """.format(
            humidity=alert_data["humidity_level"],
            type=alert_data["humidity_type"]
        ), unsafe_allow_html=True)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Health Implications Section
    st.markdown("""
    <div style="background: linear-gradient(to bottom, rgba(255, 75, 75, 0.1), rgba(255, 75, 75, 0.05)); 
                padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">🫁</span>
            <span style="font-weight: 600; color: #FF4B4B;">Health Implications</span>
        </div>
        <p style="font-size: 0.85rem; color: #666; margin: 0; line-height: 1.5;">
            {health}
        </p>
    </div>
    """.format(
        health=alert_data["health_implications"]
    ), unsafe_allow_html=True)

    # Recommended Actions Section
    st.markdown("""
    <div style="background: linear-gradient(to bottom, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
                padding: 1.2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">🛡</span>
            <span style="font-weight: 600; color: #3B82F6;">Recommended Actions</span>
        </div>
        <div style="background: white; border-radius: 8px; padding: 1rem;">
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.85rem; color: #666; line-height: 1.8;">
                {actions}
            </ul>
        </div>
    </div>
    """.format(
        actions="\n".join([f"<li style='margin-bottom: 0.5rem;'>{action}</li>" for action in alert_data["recommended_actions"]])
    ), unsafe_allow_html=True)
else:
    st.warning("No alert data available")

# Chat Assistant Section
# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set assistant ID
assistant_id = "asst_cIHPEgKEw7XtmMcn8ovvCxSx"

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

# Display chat interface
st.markdown("### Air Quality Assistant")

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

    response = generate_response(prompt, assistant_id, None)
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    message_func(response, user_icon_base64, assistant_icon_base64)


