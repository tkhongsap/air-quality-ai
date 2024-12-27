import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from utils.custom_css_banner import get_dashboard_banner
from utils.custom_css_style import get_dashboard_css, get_priority_colors
from utils.create_folium_map import create_aqi_heat_map

# Page Configuration
def setup_page():
    st.set_page_config(page_title="📊 Dashboard", page_icon="", layout="wide")
    st.markdown(get_dashboard_banner(), unsafe_allow_html=True)
    st.markdown(get_dashboard_css(), unsafe_allow_html=True)

# Data Loading Functions
def get_latest_alert_file():
    alerts_dir = Path("output/alerts")
    alert_files = list(alerts_dir.glob("bangkok_alerts_*.json"))
    return max(alert_files, key=lambda x: x.stat().st_mtime) if alert_files else None

def load_alert_data():
    latest_file = get_latest_alert_file()
    if not latest_file:
        return None
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading alert data: {str(e)}")
        return None

# UI Component Functions
def display_alert_card(alert_data):
    location_name = alert_data.get("city") or alert_data.get("station_name", "Bangkok")
    alert_type = alert_data.get("alert_type", "Air Quality Warning")
    
    st.markdown(f"""
    <div class="alert-section">
        <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
            <span style="font-size: 1.4rem; margin-right: 0.5rem;">⚠️</span>
            <span style="font-weight: 700; color: #FF4B4B; font-size: 1.2rem;">{alert_type}</span>
        </div>
        <p style="font-size: 0.9rem; color: #666; margin: 0; line-height: 1.5;">
            <span style="margin-right: 0.5rem;">📍</span>
            {location_name}
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_metric_card(value, label, color="#FF4B4B", unit=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: {color}">{value}{unit}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def display_metrics_row(alert_data):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_metric_card(alert_data["aqi"], "Current AQI")
    with col2:
        display_metric_card(alert_data["pm25_level"], "PM2.5 Level", "#FF8B3D", " μg/m³")
    with col3:
        display_metric_card(alert_data["temperature_level"], "Temperature", "#3B82F6", "°C")
    with col4:
        display_metric_card(alert_data["humidity_level"], "Humidity", "#3B82F6", "%")

def create_alerts_table(alerts_data):
    table_data = []
    for index, alert in enumerate(alerts_data, 1):
        table_data.append({
            "No.": index,
            "Station": alert.get("station_name", ""),
            "City": alert.get("city", ""),
            "AQI": alert.get("aqi", ""),
            "AQI Level": alert.get("aqi_level", ""),
            "PM2.5 (μg/m³)": alert.get("pm25_level", ""),
            "Temperature (°C)": alert.get("temperature_level", ""),
            "Humidity (%)": alert.get("humidity_level", ""),
            "Alert Type": alert.get("alert_type", ""),
            "Timestamp": datetime.fromisoformat(alert.get("timestamp", "").replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(table_data)

def display_paginated_table(df):
    rows_per_page = 20
    total_rows = len(df)
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page

    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    start_idx = st.session_state.current_page * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)

    # Pagination controls
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            Showing {start_idx + 1}-{end_idx} of {total_rows} records
        </div>
        """, unsafe_allow_html=True)

    # Display table
    st.dataframe(
        df.iloc[start_idx:end_idx],
        use_container_width=True,
        column_config=get_column_config()
    )

def get_column_config():
    return {
        "No.": st.column_config.NumberColumn("No.", format="%d"),
        "Station": st.column_config.TextColumn("Station"),
        "City": st.column_config.TextColumn("City"),
        "AQI": st.column_config.NumberColumn("AQI", format="%d"),
        "AQI Level": st.column_config.TextColumn("AQI Level"),
        "PM2.5 (μg/m³)": st.column_config.NumberColumn("PM2.5 (μg/m³)", format="%d"),
        "Temperature (°C)": st.column_config.NumberColumn("Temperature (°C)", format="%.1f"),
        "Humidity (%)": st.column_config.NumberColumn("Humidity (%)", format="%.1f"),
        "Alert Type": st.column_config.TextColumn("Alert Type"),
        "Timestamp": st.column_config.TextColumn("Timestamp")
    }

def display_required_actions(alert_data):
    """Display the required actions section with action cards"""
    # Required Actions Header
    st.markdown(f"""
    <div class="action-header">
        <div class="action-title">
            <span style="font-size: 1.4rem; margin-right: 0.5rem;">⚡</span>
            <span style="font-weight: 700; color: #3B82F6; font-size: 1.2rem;">Required Actions</span>
        </div>
        <div class="action-count">
            <span style="color: #FF4B4B; font-size: 0.9rem; font-weight: 500;">{len(alert_data["recommended_actions"])} Critical Actions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def create_action_card(action_data):
        """Helper function to create a single action card"""
        priority_style = get_priority_colors().get(action_data["priority"], get_priority_colors()["Immediate"])
        return f"""
        <div class="action-card">
            <div class="action-content">
                <span style="color: {priority_style['text']}; font-size: 1.4rem;">{priority_style['icon']}</span>
                <span style="color: #333; font-weight: 500; font-size: 1.1rem;">{action_data["action"]}</span>
            </div>
            <div class="priority-badge" style="color: #333; border: 1px solid {priority_style['text']};">
                {action_data["priority"]}
            </div>
        </div>
        """

    # Display action cards in two rows of two
    actions = alert_data["recommended_actions"]
    for i in range(0, len(actions), 2):
        col1, col2 = st.columns(2)
        with col1:
            if i < len(actions):
                st.markdown(create_action_card(actions[i]), unsafe_allow_html=True)
        with col2:
            if i + 1 < len(actions):
                st.markdown(create_action_card(actions[i + 1]), unsafe_allow_html=True)

def main():
    setup_page()

    # Add AQI Map
    create_aqi_heat_map()
    st.markdown("<br>", unsafe_allow_html=True)
    
    data = load_alert_data()
    if not data or "alerts" not in data or not data["alerts"]:
        st.warning("No alert data available")
        return

    first_alert = data["alerts"][0]
    
    # Display main dashboard components
    col_alert, col_health = st.columns([1, 1])
    with col_alert:
        display_alert_card(first_alert)
    with col_health:
        st.markdown(f"""
        <div class="alert-section">
            <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                <span style="font-size: 1.4rem; margin-right: 0.5rem;">🛡</span>
                <span style="font-weight: 700; color: #FF4B4B; font-size: 1.2rem;">Health Implications</span>
            </div>
            <p style="font-size: 0.9rem; color: #666; margin: 0; line-height: 1.5;">
                {first_alert["health_implications"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    display_metrics_row(first_alert)
    st.markdown("<br>", unsafe_allow_html=True)


    
    # Add Required Actions section
    display_required_actions(first_alert)
    st.markdown("<br>", unsafe_allow_html=True)


    # # Display detailed measurements
    # st.markdown("""
    # <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
    #     <span style="font-size: 1.4rem; margin-right: 0.5rem;">📊</span>
    #     <span style="font-weight: 700; color: #3B82F6; font-size: 1.2rem;">Detailed Measurements</span>
    # </div>
    # """, unsafe_allow_html=True)

    # df = create_alerts_table(data["alerts"])
    # display_paginated_table(df)

if __name__ == "__main__":
    main()