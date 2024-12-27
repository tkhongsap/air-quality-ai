import streamlit as st
import json

from datetime import datetime
from pathlib import Path
from utils.custom_css_banner import get_chat_assistant_banner

# Set page config
st.set_page_config(page_title="📊 Dashboard", page_icon="", layout="wide")

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
    """Get the most recent alert file from the output/alerts directory"""
    alerts_dir = Path("output/alerts")
    # Change the pattern to match your actual file naming
    alert_files = list(alerts_dir.glob("bangkok_alerts_*.json"))
    
    if not alert_files:
        print("No alert files found matching pattern 'bangkok_alerts_*.json'")
        # List all files in the directory for debugging
        all_files = list(alerts_dir.glob("*.json"))
        if all_files:
            print(f"Files found in directory: {[f.name for f in all_files]}")
        return None
    
    latest_file = max(alert_files, key=lambda x: x.stat().st_mtime)
    print(f"Found latest alert file: {latest_file}")
    return latest_file

def load_alerts():
    """Load the latest alert data"""
    latest_file = get_latest_alert_file()
    if not latest_file:
        st.warning("No alert files found in output/alerts directory")
        return None
    
    print(f"Loading alerts from: {latest_file}")  # Debug print
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Loaded data structure: {list(data.keys())}")  # Debug print
            
            if data and "alerts" in data and data["alerts"]:
                alerts = data["alerts"]
                if alerts:
                    first_alert = alerts[0]
                    
                    # Handle empty city name
                    if not first_alert.get("city"):
                        first_alert["city"] = first_alert.get("station_name", "Bangkok")
                    
                    print(f"Found {len(alerts)} alerts")
                    print(f"First alert AQI: {first_alert.get('aqi')}")
                    return first_alert
            else:
                st.warning("No alerts found in the data file")
                print(f"Alert data structure: {data}")
                return None
    except Exception as e:
        st.error(f"Error loading alerts: {str(e)}")
        print(f"Exception details: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

# Load and display alert information
alert_data = load_alerts()
if alert_data:
    # Alert and Health Implications in two columns
    col_alert, col_health = st.columns([1, 1])
    
    # Alert Card (Left Column)
    with col_alert:
        location_name = alert_data.get("city") or alert_data.get("station_name", "Bangkok")
        alert_type = alert_data.get("alert_type", "Air Quality Warning")
        
        st.markdown(f"""
        <div style="background: linear-gradient(to bottom, rgba(255, 75, 75, 0.1), rgba(255, 75, 75, 0.05)); 
                    padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;">
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

    # After the Required Actions section and before the Chat Assistant section
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed Measurements Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 1.4rem; margin-right: 0.5rem;">📊</span>
            <span style="font-weight: 700; color: #3B82F6; font-size: 1.2rem;">Detailed Measurements</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load all alerts from the file
    latest_file = get_latest_alert_file()
    if latest_file:
        with open(latest_file, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            alerts_data = all_data.get("alerts", [])

            if alerts_data:
                # Create a list of dictionaries for the table
                table_data = []
                for index, alert in enumerate(alerts_data, 1):
                    table_data.append({
                        "No.": index,
                        # Location Information
                        "Station": alert.get("station_name", ""),
                        "City": alert.get("city", ""),
                        # "Latitude": alert.get("latitude", ""),
                        # "Longitude": alert.get("longitude", ""),
                        # Air Quality Metrics
                        "AQI": alert.get("aqi", ""),
                        "AQI Level": alert.get("aqi_level", ""),
                        "PM2.5 (μg/m³)": alert.get("pm25_level", ""),
                        # "PM2.5 Status": alert.get("pm25_type", ""),
                        # "PM10 (μg/m³)": alert.get("pm10_level", ""),
                        # "PM10 Status": alert.get("pm10_type", ""),
                        # Environmental Conditions
                        "Temperature (°C)": alert.get("temperature_level", ""),
                        # "Temperature Status": alert.get("temperature_type", ""),
                        "Humidity (%)": alert.get("humidity_level", ""),
                        # "Humidity Status": alert.get("humidity_type", ""),
                        # Alert Information
                        "Alert Type": alert.get("alert_type", ""),
                        "Timestamp": datetime.fromisoformat(alert.get("timestamp", "").replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
                    })

                # Convert to DataFrame
                import pandas as pd
                df = pd.DataFrame(table_data)

                # Calculate number of pages
                rows_per_page = 20
                total_rows = len(df)
                total_pages = (total_rows + rows_per_page - 1) // rows_per_page

                # Add page selector to session state if not exists
                if "current_page" not in st.session_state:
                    st.session_state.current_page = 0

                # Calculate start and end indices for current page
                start_idx = st.session_state.current_page * rows_per_page
                end_idx = min(start_idx + rows_per_page, total_rows)

                # Pagination controls with better styling
                col1, col2, col3 = st.columns([2, 3, 2])

                with col2:
                    if total_pages > 1:
                        st.markdown("""
                        <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin: 1rem 0;">
                        """, unsafe_allow_html=True)
                        
                        pagination = st.columns([1, 2, 1])
                        
                        with pagination[0]:
                            if st.button("← Previous", 
                                       disabled=st.session_state.current_page == 0,
                                       use_container_width=True):
                                st.session_state.current_page -= 1
                                st.rerun()

                        with pagination[1]:
                            st.markdown(f"""
                            <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 0.5rem;">
                                Page {st.session_state.current_page + 1} of {total_pages}
                            </div>
                            """, unsafe_allow_html=True)

                        with pagination[2]:
                            if st.button("Next →", 
                                       disabled=st.session_state.current_page == total_pages - 1,
                                       use_container_width=True):
                                st.session_state.current_page += 1
                                st.rerun()

                # Calculate appropriate height for the table
                row_height = 35  # approximate height per row in pixels
                header_height = 38  # height for the header
                padding = 10  # extra padding
                num_rows = len(df.iloc[start_idx:end_idx])
                calculated_height = (num_rows * row_height) + header_height + padding

                # Style the dataframe with Excel-like appearance and calculated height
                st.data_editor(
                    df.iloc[start_idx:end_idx],
                    hide_index=True,
                    use_container_width=True,
                    height=calculated_height,  # Dynamic height based on content
                    column_config={
                        # Row Number
                        "No.": st.column_config.NumberColumn(
                            "No.",
                            help="Record number",
                            format="%d"
                        ),
                        # Location Information
                        "Station": st.column_config.TextColumn(
                            "Station",
                            help="Monitoring station name"
                        ),
                        "City": st.column_config.TextColumn(
                            "City",
                            help="City name"
                        ),
                        "Latitude": st.column_config.NumberColumn(
                            "Latitude",
                            help="Station latitude",
                            format="%.4f"
                        ),
                        "Longitude": st.column_config.NumberColumn(
                            "Longitude",
                            help="Station longitude",
                            format="%.4f"
                        ),
                        # Air Quality Metrics
                        "AQI": st.column_config.NumberColumn(
                            "AQI",
                            help="Air Quality Index",
                            format="%d"
                        ),
                        "AQI Level": st.column_config.TextColumn(
                            "AQI Level",
                            help="AQI severity level"
                        ),
                        # ... rest of your column configs ...
                    },
                    disabled=True  # Makes it read-only like a regular table
                )

else:
    st.warning("No alert data available")
    # Debug information
    latest_file = get_latest_alert_file()
    if latest_file:
        st.info(f"Latest alert file found: {latest_file}")
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                st.code(json.dumps(data, indent=2), language='json')
        except Exception as e:
            st.error(f"Error reading alert file: {str(e)}")
    else:
        st.error("No alert files found in output/alerts directory")