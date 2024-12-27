import folium
import json
from folium import plugins
import branca.colormap as cm
import os
import glob
from datetime import datetime

# Create maps directory if it doesn't exist
maps_dir = os.path.join('output', 'maps')
os.makedirs(maps_dir, exist_ok=True)

# Get the latest JSON file from the hourly directory
json_pattern = os.path.join('output', 'hourly', 'bangkok_aqi_data_*.json')
list_of_files = glob.glob(json_pattern)
latest_file = max(list_of_files, key=os.path.getctime)

print(f"Reading data from: {latest_file}")

# Read the JSON file
with open(latest_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract timestamp from the data
timestamp = data['query_timestamp']
timestamp_formatted = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d_%H%M')

# Calculate center of Bangkok (approximate)
bangkok_center = [13.7563, 100.5018]

# Create a map centered on Bangkok
m = folium.Map(location=bangkok_center, zoom_start=11)

# Create a color scale for AQI values
colormap = cm.LinearColormap(
    colors=['green', 'yellow', 'orange', 'red', 'purple', 'maroon'],
    vmin=0,
    vmax=300,
    caption='Air Quality Index (AQI)'
)
colormap.add_to(m)

# Add markers for each station
for station in data['data']:
    # Skip if no AQI data or coordinates
    if not all([station.get('latitude'), station.get('longitude'), station.get('aqi')]):
        continue
        
    # Determine color based on AQI value
    aqi = station['aqi']
    color = colormap(aqi)
    
    # Create popup content
    popup_content = f"""
        <b>{station['station_name']}</b><br>
        AQI: {aqi}<br>
        PM2.5: {station['pm25']}<br>
        PM10: {station['pm10']}<br>
        Temperature: {station['temperature']}°C<br>
        Humidity: {station['humidity']}%
    """
    
    # Add circle marker
    folium.CircleMarker(
        location=[station['latitude'], station['longitude']],
        radius=8,
        popup=folium.Popup(popup_content, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        weight=2
    ).add_to(m)

# Add fullscreen option
plugins.Fullscreen().add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map with timestamp in filename
output_file = os.path.join(maps_dir, f'bangkok_aqi_map_{timestamp_formatted}.html')
m.save(output_file)
print(f"Map saved as: {output_file}")
