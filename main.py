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

# Load and display alert information
alert_data = load_alerts()
if alert_data:
    # Alert and Health Implications in two columns
    col_alert, col_health = st.columns([1, 1])
    
    # Alert Card (Left Column)
    with col_alert:
        st.markdown("""
        <div style="background: linear-gradient(to bottom, rgba(255, 75, 75, 0.1), rgba(255, 75, 75, 0.05)); 
                    padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <span style="font-size: 1.4rem; margin-right: 0.5rem;">⚠️</span>
                <span style="font-weight: 700; color: #FF4B4B; font-size: 1.2rem;">Air Quality Warning</span>
            </div>
            <p style="font-size: 0.9rem; color: #666; margin: 0; line-height: 1.5;">
                <span style="margin-right: 0.5rem;">📍</span>
                {city}
            </p>
        </div>
        """.format(city=alert_data["city"]), unsafe_allow_html=True)

    # Health Implications Card (Right Column)
    with col_health:
        st.markdown("""
        <div style="background: linear-gradient(to bottom, rgba(255, 75, 75, 0.1), rgba(255, 75, 75, 0.05)); 
                    padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <span style="font-size: 1.4rem; margin-right: 0.5rem;">🛡</span>
                <span style="font-weight: 700; color: #FF4B4B; font-size: 1.2rem;">Health Implications</span>
            </div>
            <p style="font-size: 0.9rem; color: #666; margin: 0; line-height: 1.5;">
                {health}
            </p>
        </div>
        """.format(health=alert_data["health_implications"]), unsafe_allow_html=True)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Create columns for the metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    # AQI Card
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 2.5rem; font-weight: 800; color: #FF4B4B; margin-bottom: 0.5rem;">{aqi}</div>
            <div style="color: #333; font-size: 1rem; font-weight: 600;">Current AQI</div>
        </div>
        """.format(aqi=alert_data["aqi"]), unsafe_allow_html=True)

    # PM2.5 Card
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 2.5rem; font-weight: 800; color: #FF8B3D; margin-bottom: 0.5rem;">{pm25} <span style="font-size: 1rem;">μg/m³</span></div>
            <div style="color: #333; font-size: 1rem; font-weight: 600;">PM2.5 Level</div>
        </div>
        """.format(pm25=alert_data["pm25_level"]), unsafe_allow_html=True)

    # Temperature Card
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 2.5rem; font-weight: 800; color: #3B82F6; margin-bottom: 0.5rem;">{temp}°C</div>
            <div style="color: #333; font-size: 1rem; font-weight: 600;">Temperature</div>
        </div>
        """.format(temp=alert_data["temperature_level"]), unsafe_allow_html=True)

    # Humidity Card
    with col4:
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 2.5rem; font-weight: 800; color: #3B82F6; margin-bottom: 0.5rem;">{humidity}%</div>
            <div style="color: #333; font-size: 1rem; font-weight: 600;">Humidity</div>
        </div>
        """.format(humidity=alert_data["humidity_level"]), unsafe_allow_html=True)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Required Actions Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 1.4rem; margin-right: 0.5rem;">⚡</span>
            <span style="font-weight: 700; color: #3B82F6; font-size: 1.2rem;">Required Actions</span>
        </div>
        <div style="background: rgba(255, 75, 75, 0.1); padding: 0.3rem 0.8rem; border-radius: 15px;">
            <span style="color: #FF4B4B; font-size: 0.9rem; font-weight: 500;">{} Critical Actions</span>
        </div>
    </div>
    """.format(len(alert_data["recommended_actions"])), unsafe_allow_html=True)

    # Priority color mapping
    priority_colors = {
        "Immediate": {"bg": "rgba(255, 75, 75, 0.05)", "text": "#FF4B4B", "icon": ""},
        "Preventive": {"bg": "rgba(255, 193, 7, 0.05)", "text": "#FFC107", "icon": ""},
        "Long-Term": {"bg": "rgba(59, 130, 246, 0.05)", "text": "#3B82F6", "icon": ""}
    }

    # First row
    col1, col2 = st.columns(2)
    
    # First row - First card
    with col1:
        action_data = alert_data["recommended_actions"][0]
        priority_style = priority_colors.get(action_data["priority"], priority_colors["Immediate"])
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; height: 100%; margin-bottom: 1rem;">
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: {priority_style['text']}; font-size: 1.4rem;">{priority_style['icon']}</span>
                    <span style="color: #333; font-weight: 500; font-size: 1.1rem;">{action_data["action"]}</span>
                </div>
            </div>
            <div style="background: white; color: #333; border: 1px solid {priority_style['text']}; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; margin-left: 1rem; font-weight: 500;">
                {action_data["priority"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # First row - Second card
    with col2:
        action_data = alert_data["recommended_actions"][1]
        priority_style = priority_colors.get(action_data["priority"], priority_colors["Immediate"])
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; height: 100%; margin-bottom: 1rem;">
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: {priority_style['text']}; font-size: 1.4rem;">{priority_style['icon']}</span>
                    <span style="color: #333; font-weight: 500; font-size: 1.1rem;">{action_data["action"]}</span>
                </div>
            </div>
            <div style="background: white; color: #333; border: 1px solid {priority_style['text']}; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; margin-left: 1rem; font-weight: 500;">
                {action_data["priority"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Second row
    col3, col4 = st.columns(2)
    
    # Second row - First card
    with col3:
        action_data = alert_data["recommended_actions"][2]
        priority_style = priority_colors.get(action_data["priority"], priority_colors["Immediate"])
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; height: 100%; margin-bottom: 1rem;">
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: {priority_style['text']}; font-size: 1.4rem;">{priority_style['icon']}</span>
                    <span style="color: #333; font-weight: 500; font-size: 1.1rem;">{action_data["action"]}</span>
                </div>
            </div>
            <div style="background: white; color: #333; border: 1px solid {priority_style['text']}; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; margin-left: 1rem; font-weight: 500;">
                {action_data["priority"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Second row - Second card
    with col4:
        action_data = alert_data["recommended_actions"][3]
        priority_style = priority_colors.get(action_data["priority"], priority_colors["Immediate"])
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; height: 100%; margin-bottom: 1rem;">
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: {priority_style['text']}; font-size: 1.4rem;">{priority_style['icon']}</span>
                    <span style="color: #333; font-weight: 500; font-size: 1.1rem;">{action_data["action"]}</span>
                </div>
            </div>
            <div style="background: white; color: #333; border: 1px solid {priority_style['text']}; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; margin-left: 1rem; font-weight: 500;">
                {action_data["priority"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No alert data available")

# Chat Assistant Section
# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to convert images to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# Set assistant ID
assistant_id = "asst_cIHPEgKEw7XtmMcn8ovvCxSx"

warnings.filterwarnings("ignore")

# Initialize session state for chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Welcome to the Air Quality Command Center! 👋\n\nI'm your dedicated Air Quality Assistant, how can I assist you today?"}
    ]

# Load user and assistant icons
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


