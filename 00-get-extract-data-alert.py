import requests
import pandas as pd
import sys
import json
import os
from datetime import datetime
from colorama import init, Fore, Style
from dotenv import load_dotenv
from openai import OpenAI
from utils.prompt_instructions import get_air_quality_system_prompt

# Initialize
load_dotenv()
init()  # Initialize colorama

# Constants
API_TOKEN = os.getenv("AQI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

API_ENDPOINTS = {
    'search': "https://api.waqi.info/v2/map/bounds",
    'feed': "https://api.waqi.info/feed/@{}/"
}

DIRECTORIES = {
    'hourly': "output/hourly",
    'alerts': "output/alerts"
}

BANGKOK_BOUNDS = {
    'latlng': [13.4963, 100.3270, 13.9876, 100.9378]  # [south lat, west lng, north lat, east lng]
}

AQI_THRESHOLDS = {
    'Good': (0, 50),
    'Moderate': (51, 100),
    'Unhealthy for Sensitive Groups': (101, 150),
    'Unhealthy': (151, 200),
    'Very Unhealthy': (201, 300),
    'Hazardous': (301, float('inf'))
}

def ensure_directories():
    """Create necessary output directories if they don't exist"""
    for directory in DIRECTORIES.values():
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Fore.GREEN}Created directory: {directory}{Style.RESET_ALL}")

def get_aqi_category(aqi):
    """Determine AQI category based on value"""
    if aqi is None:
        return "Unknown"
    for category, (min_val, max_val) in AQI_THRESHOLDS.items():
        if min_val <= aqi <= max_val:
            return category
    return "Unknown"

def get_alert_level(aqi):
    """Determine alert level based on AQI value"""
    if aqi is None:
        return "unknown"
    if aqi <= 100:
        return "info"
    elif aqi <= 150:
        return "warning"
    return "danger"

def make_api_request(url, params):
    """Make API request with error handling"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{Fore.RED}API request failed: {e}{Style.RESET_ALL}")
        return None

def fetch_bangkok_stations():
    """Fetch all air quality monitoring stations in Bangkok"""
    params = {
        "token": API_TOKEN,
        "latlng": f"{BANGKOK_BOUNDS['latlng'][0]},{BANGKOK_BOUNDS['latlng'][1]},{BANGKOK_BOUNDS['latlng'][2]},{BANGKOK_BOUNDS['latlng'][3]}"
    }
    
    data = make_api_request(API_ENDPOINTS['search'], params)
    if not data or data.get('status') != 'ok':
        return []
    
    stations = []
    for station in data.get('data', []):
        lat, lon = float(station.get('lat', 0)), float(station.get('lon', 0))
        if (BANGKOK_BOUNDS['latlng'][0] <= lat <= BANGKOK_BOUNDS['latlng'][2] and
            BANGKOK_BOUNDS['latlng'][1] <= lon <= BANGKOK_BOUNDS['latlng'][3]):
            stations.append({
                'uid': station.get('uid'),
                'station': {
                    'name': station.get('station', {}).get('name', 'Unknown'),
                    'geo': [lat, lon]
                }
            })
    return stations

def fetch_station_data(station_id):
    """Fetch latest air quality data for a specific station"""
    return make_api_request(API_ENDPOINTS['feed'].format(station_id), {"token": API_TOKEN})

def process_station_data(raw_data, station_info):
    """Process the raw API data and extract relevant information"""
    if not raw_data or raw_data.get('status') != 'ok':
        return None
        
    try:
        data = raw_data['data']
        iaqi = data.get('iaqi', {})
        station_name = station_info.get('station', {}).get('name', 'Unknown')
        
        city = station_name.split(',')[0].strip()
        city = city.replace('Bangkok', '').strip() if 'Bangkok' in city else city
        
        # Convert AQI to float or None if invalid
        aqi = data.get('aqi')
        try:
            if aqi and str(aqi).strip() != '-':
                aqi = float(aqi)
            else:
                aqi = None
        except (ValueError, TypeError):
            aqi = None
        
        return {
            'station_name': station_name,
            'station_id': station_info.get('uid'),
            'city': city,
            'latitude': station_info.get('station', {}).get('geo', [None, None])[0],
            'longitude': station_info.get('station', {}).get('geo', [None, None])[1],
            'timestamp': data.get('time', {}).get('s'),
            'aqi': aqi,
            'pm25': iaqi.get('pm25', {}).get('v'),
            'pm10': iaqi.get('pm10', {}).get('v'),
            'temperature': iaqi.get('t', {}).get('v'),
            'humidity': iaqi.get('h', {}).get('v')
        }
    except Exception as e:
        print(f"{Fore.RED}Error processing data for station {station_info.get('uid')}: {e}{Style.RESET_ALL}")
        return None

def generate_alerts(records):
    """Generate alerts for stations with AQI >= 50"""
    # Filter records with valid AQI >= 50
    alert_worthy_records = []
    for record in records:
        try:
            aqi_value = record.get('aqi')
            if aqi_value and str(aqi_value).strip() != '-':  # Check for '-' string
                aqi_float = float(aqi_value)
                if aqi_float >= 50:
                    record['aqi'] = aqi_float  # Store as float
                    alert_worthy_records.append(record)
        except (ValueError, TypeError):
            continue
    
    # Sort by AQI value in descending order
    alert_worthy_records = sorted(
        alert_worthy_records, 
        key=lambda x: float(x['aqi']), 
        reverse=True
    )
    
    if not alert_worthy_records:
        print(f"{Fore.YELLOW}No stations found with valid AQI >= 50{Style.RESET_ALL}")
        return []

    print(f"{Fore.YELLOW}Generating alerts for {len(alert_worthy_records)} stations with AQI >= 50{Style.RESET_ALL}")
    
    client = OpenAI()
    
    aqi_data = {
        'query_timestamp': get_rounded_hour_timestamp(),
        'city': 'Bangkok',
        'total_stations': len(alert_worthy_records),
        'total_data_points': len(alert_worthy_records),
        'data': alert_worthy_records
    }
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": get_air_quality_system_prompt()},
                {"role": "user", "content": f"Generate air quality alerts from this data:\n{json.dumps(aqi_data, ensure_ascii=False, indent=2)}"}
            ],
            temperature=0.3
        )
        alerts = json.loads(response.choices[0].message.content)
        return alerts.get('alerts', [])
        
    except Exception as e:
        print(f"{Fore.RED}Error generating alerts with OpenAI: {e}{Style.RESET_ALL}")
        return generate_basic_alerts(alert_worthy_records)

def generate_basic_alerts(records):
    """Fallback function for basic alert generation without OpenAI"""
    alerts = []
    for record in records:
        if record['aqi'] is None:
            continue
            
        aqi = float(record['aqi'])
        aqi_category = get_aqi_category(aqi)
        alert_level = get_alert_level(aqi)
        
        alerts.append({
            'timestamp': record['timestamp'],
            'station_name': record['station_name'],
            'city': record['city'],
            'aqi': aqi,
            'pm25_level': record['pm25'],
            'pm25_type': 'Normal' if record['pm25'] <= 50 else 'Above Threshold',
            'pm10_level': record['pm10'],
            'pm10_type': 'Normal' if record['pm10'] <= 100 else 'Above Threshold',
            'temperature_level': record['temperature'],
            'temperature_type': 'Normal',
            'humidity_level': record['humidity'],
            'humidity_type': 'Normal',
            'latitude': record['latitude'],
            'longitude': record['longitude'],
            'aqi_level': aqi_category,
            'alert_type': f'Air Quality {alert_level.title()}',
            'health_implications': get_health_implications(aqi_category),
            'recommended_actions': get_recommended_actions(aqi_category)
        })
    return alerts

def get_health_implications(aqi_category):
    """Get health implications based on AQI category"""
    implications = {
        'Moderate': 'Air quality is acceptable; however, some pollutants may affect very sensitive individuals.',
        'Unhealthy for Sensitive Groups': 'Members of sensitive groups may experience health effects. General public is less likely to be affected.',
        'Unhealthy': 'Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.',
        'Very Unhealthy': 'Health alert: The risk of health effects is increased for everyone.',
        'Hazardous': 'Health warning of emergency conditions: everyone is more likely to be affected.'
    }
    return implications.get(aqi_category, 'Air quality is generally good.')

def get_recommended_actions(aqi_category):
    """Get recommended actions based on AQI category"""
    base_actions = [
        {'action': '😷 Wear masks when outdoors', 'priority': 'Immediate'},
        {'action': '🪟 Keep windows closed during peak pollution', 'priority': 'Preventive'}
    ]
    
    if aqi_category in ['Unhealthy', 'Very Unhealthy', 'Hazardous']:
        return [
            {'action': '🚫 Avoid outdoor activities', 'priority': 'Immediate'},
            {'action': '🏠 Stay indoors with air purifiers', 'priority': 'Immediate'},
            {'action': '😷 Wear N95 masks if outdoors', 'priority': 'Immediate'},
            {'action': '⚕️ Monitor health symptoms', 'priority': 'Immediate'}
        ]
    elif aqi_category == 'Unhealthy for Sensitive Groups':
        return [
            {'action': '🌳 Sensitive groups should limit outdoor exposure', 'priority': 'Immediate'},
            {'action': '🌬️ Use air purifiers indoors', 'priority': 'Preventive'}
        ] + base_actions
    else:
        return base_actions

def get_rounded_hour_timestamp():
    """Get current timestamp rounded down to the nearest hour"""
    rounded = datetime.now().replace(minute=0, second=0, microsecond=0)
    return rounded.strftime('%Y-%m-%d %H:%M:%S')

def get_filename_timestamp():
    """Get timestamp for filenames"""
    rounded = datetime.now().replace(minute=0, second=0, microsecond=0)
    return rounded.strftime('%Y-%m-%d_%H00')

def save_json_file(data, filepath):
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"{Fore.GREEN}Data saved to '{filepath}'{Style.RESET_ALL}")

def print_summary_statistics(df):
    """Print summary statistics of the collected data"""
    print(f"\n{Fore.CYAN}Summary Statistics:{Style.RESET_ALL}")
    print(f"{'='*50}")
    
    # Number of stations
    print(f"{Fore.YELLOW}Station Statistics:{Style.RESET_ALL}")
    print(f"Total Stations: {len(df['station_name'].unique())}")
    print(f"Cities Covered: {len(df['city'].unique())}")
    
    # Convert AQI and PM2.5 to numeric, dropping any non-numeric values
    df['aqi'] = pd.to_numeric(df['aqi'], errors='coerce')
    df['pm25'] = pd.to_numeric(df['pm25'], errors='coerce')
    
    # AQI Statistics
    print(f"\n{Fore.YELLOW}AQI Statistics:{Style.RESET_ALL}")
    aqi_stats = df['aqi'].dropna()
    if not aqi_stats.empty:
        print(f"Mean AQI: {aqi_stats.mean():.2f}")
        print(f"Max AQI: {aqi_stats.max():.2f}")
        print(f"Min AQI: {aqi_stats.min():.2f}")
        print(f"Median AQI: {aqi_stats.median():.2f}")
        print(f"Number of Stations with AQI data: {len(aqi_stats)}")
    else:
        print("No AQI data available")
    
    # PM2.5 Statistics
    print(f"\n{Fore.YELLOW}PM2.5 Statistics:{Style.RESET_ALL}")
    pm25_stats = df['pm25'].dropna()
    if not pm25_stats.empty:
        print(f"Mean PM2.5: {pm25_stats.mean():.2f}")
        print(f"Max PM2.5: {pm25_stats.max():.2f}")
        print(f"Min PM2.5: {pm25_stats.min():.2f}")
        print(f"Median PM2.5: {pm25_stats.median():.2f}")
        print(f"Number of Stations with PM2.5 data: {len(pm25_stats)}")
    else:
        print("No PM2.5 data available")
    
    # Air Quality Categories
    print(f"\n{Fore.YELLOW}Air Quality Categories Distribution:{Style.RESET_ALL}")
    categories = df['aqi'].dropna().apply(get_aqi_category).value_counts()
    if not categories.empty:
        for category, count in categories.items():
            print(f"{category}: {count} stations")
    else:
        print("No category data available")
    
    # Top 5 Highest AQI Locations
    print(f"\n{Fore.YELLOW}Top 5 Highest AQI Locations:{Style.RESET_ALL}")
    top_5 = df.dropna(subset=['aqi']).nlargest(5, 'aqi')[['station_name', 'city', 'aqi']]
    if not top_5.empty:
        for _, row in top_5.iterrows():
            print(f"- {row['station_name']} ({row['city']}): AQI {row['aqi']:.2f}")
    else:
        print("No location data available")
    
    print(f"{'='*50}")

def main():
    """Main function to fetch data and generate alerts"""
    ensure_directories()
    print(f"{Fore.CYAN}Fetching air quality data for Bangkok...{Style.RESET_ALL}")
    
    # Fetch and process AQI data
    stations = fetch_bangkok_stations()
    if not stations:
        print(f"{Fore.RED}No stations found in Bangkok{Style.RESET_ALL}")
        sys.exit(1)
    
    records = []
    for station in stations:
        station_id = station.get('uid')
        station_name = station.get('station', {}).get('name', 'Unknown')
        print(f"\n{Fore.YELLOW}Fetching data for station {station_id} ({station_name}){Style.RESET_ALL}")
        
        raw_data = fetch_station_data(station_id)
        if raw_data:
            record = process_station_data(raw_data, station)
            if record:
                records.append(record)
    
    # Generate and sort alerts
    alerts = generate_alerts(records)
    alerts = sorted(alerts, key=lambda x: x.get('aqi', 0), reverse=True)
    
    # Get timestamps
    timestamp = get_rounded_hour_timestamp()
    filename_timestamp = get_filename_timestamp()
    
    # Save files
    save_json_file({
        'query_timestamp': timestamp,
        'city': 'Bangkok',
        'total_stations': len(stations),
        'total_data_points': len(records),
        'data': records
    }, os.path.join(DIRECTORIES['hourly'], f'bangkok_aqi_data_{filename_timestamp}.json'))
    
    save_json_file({
        'timestamp': timestamp,
        'total_alerts': len(alerts),
        'alerts': alerts
    }, os.path.join(DIRECTORIES['alerts'], f'bangkok_alerts_{filename_timestamp}.json'))
    
    # Generate and save statistics
    df = pd.DataFrame(records)
    if not df.empty:
        save_json_file({
            'AQI Statistics by City': df.groupby('city')['aqi'].describe().to_dict(),
            'PM2.5 Statistics by City': df.groupby('city')['pm25'].describe().to_dict()
        }, os.path.join(DIRECTORIES['hourly'], f'bangkok_aqi_stats_{filename_timestamp}.json'))
        
        # Print summary statistics
        print_summary_statistics(df)
    
    print(f"\n{Fore.CYAN}Processing complete!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
