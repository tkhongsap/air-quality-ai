import folium
import json
from folium import plugins
import branca.colormap as cm
import os
import glob
from datetime import datetime
import streamlit as st
from streamlit_folium import st_folium

def create_aqi_map():
    # Get the latest JSON file from the hourly directory
    json_pattern = os.path.join('output', 'hourly', 'bangkok_aqi_data_*.json')
    list_of_files = glob.glob(json_pattern)
    latest_file = max(list_of_files, key=os.path.getctime)

    # Read the JSON file
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract timestamp from the data
    timestamp = data['query_timestamp']
    timestamp_formatted = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')

    # Center coordinates for One Bangkok Smart City
    one_bangkok_center = [13.7271, 100.5473]

    # Create a map centered on One Bangkok with increased zoom level
    m = folium.Map(location=one_bangkok_center, zoom_start=13)

    # Add a marker for One Bangkok
    folium.Marker(
        location=one_bangkok_center,
        popup="One Bangkok Smart City",
        icon=folium.Icon(color='blue', icon='info-sign'),
        tooltip="One Bangkok Smart City"
    ).add_to(m)

    # Create a color scale for AQI values
    colormap = cm.LinearColormap(
        colors=['green', 'yellow', 'orange', 'red', 'purple', 'maroon'],
        vmin=0,
        vmax=300,
        caption='Air Quality Index (AQI)'
    )
    colormap.add_to(m)

    # Prepare data for heatmap
    heat_data = []
    
    # Create feature groups for layers
    marker_group = folium.FeatureGroup(name='Station Markers')
    heatmap_group = folium.FeatureGroup(name='AQI Heatmap')

    # Add markers for each station
    for station in data['data']:
        # Skip if no AQI data or coordinates
        if not all([station.get('latitude'), station.get('longitude'), station.get('aqi')]):
            continue
            
        # Determine color based on AQI value
        aqi = station['aqi']
        color = colormap(aqi)
        
        # Add data point for heatmap (lat, lon, weight)
        heat_data.append([station['latitude'], station['longitude'], aqi])
        
        # Create popup content
        popup_content = f"""
            <b>{station['station_name']}</b><br>
            AQI: {aqi}<br>
            PM2.5: {station['pm25']}<br>
            PM10: {station['pm10']}<br>
            Temperature: {station['temperature']}°C<br>
            Humidity: {station['humidity']}%
        """
        
        # Add circle marker to marker group
        folium.CircleMarker(
            location=[station['latitude'], station['longitude']],
            radius=8,
            popup=folium.Popup(popup_content, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=2
        ).add_to(marker_group)

    # Add heatmap layer
    plugins.HeatMap(
        heat_data,
        min_opacity=0.4,
        radius=25,
        blur=15,
        gradient={
            '0': 'blue',
            '0.4': 'lime',
            '0.6': 'yellow',
            '0.8': 'orange',
            '1': 'red'
        }
    ).add_to(heatmap_group)

    # Add the feature groups to the map
    heatmap_group.add_to(m)
    marker_group.add_to(m)

    # Add fullscreen option
    plugins.Fullscreen().add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    return m, timestamp_formatted

def main():
    st.title("Bangkok Air Quality Map")
    
    # Create the map
    map_obj, timestamp = create_aqi_map()
    
    # Display the timestamp
    st.write(f"Last Updated: {timestamp}")
    
    # Display the map using streamlit_folium
    st_folium(map_obj, width=725, height=500)

if __name__ == "__main__":
    main()
