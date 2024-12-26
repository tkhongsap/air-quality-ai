import requests
import pandas as pd
import sys
import json
import os
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# API Configuration
API_TOKEN = "54cff9cde8d4d06de330c249aa0d09c9ab5a1372"
SEARCH_URL = "https://api.waqi.info/v2/map/bounds"
FEED_URL = "https://api.waqi.info/feed/@{}/"

# Output directory
OUTPUT_DIR = "output/hourly"

# Thailand's geographical bounds
# These coordinates cover the entire country of Thailand
THAILAND_BOUNDS = {
    'latlng': [5.612851, 97.343636, 20.463157, 105.639389]  # [south lat, west lng, north lat, east lng]
}

def ensure_output_dir():
    """
    Create output directory and subdirectories if they don't exist
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"{Fore.GREEN}Created output directory: {OUTPUT_DIR}{Style.RESET_ALL}")

def print_colored_json(data):
    """
    Print JSON with color formatting
    """
    def colorize(text):
        # Add colors based on data type
        if isinstance(text, str):
            return Fore.GREEN + f'"{text}"' + Style.RESET_ALL
        elif isinstance(text, (int, float)):
            return Fore.CYAN + str(text) + Style.RESET_ALL
        elif text is None:
            return Fore.RED + "null" + Style.RESET_ALL
        return str(text)

    # Convert to JSON string with indentation
    json_str = json.dumps(data, indent=2)
    
    # Add colors
    colored_lines = []
    for line in json_str.split('\n'):
        # Color the keys
        if ':' in line:
            key, value = line.split(':', 1)
            line = f"{Fore.YELLOW}{key}{Style.RESET_ALL}:{value}"
        
        # Color the values
        for old_value in ['"[^"]*"', r'\d+\.?\d*', 'null', 'true', 'false']:
            line = line.replace(old_value, colorize(old_value))
        
        colored_lines.append(line)
    
    print('\n'.join(colored_lines))

def fetch_thailand_stations():
    """
    Fetch all air quality monitoring stations in Thailand using geographical bounds
    """
    try:
        params = {
            "token": API_TOKEN,
            "latlng": f"{THAILAND_BOUNDS['latlng'][0]},{THAILAND_BOUNDS['latlng'][1]},{THAILAND_BOUNDS['latlng'][2]},{THAILAND_BOUNDS['latlng'][3]}"
        }
        
        response = requests.get(SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"API returned non-OK status: {data.get('status')}")
            sys.exit(1)
        
        # Get all stations within Thailand's bounds
        stations = data.get('data', [])
        
        # Filter stations to ensure they are in Thailand (additional verification)
        thailand_stations = []
        for station in stations:
            lat = float(station.get('lat', 0))
            lon = float(station.get('lon', 0))
            
            # Check if coordinates are within Thailand's bounds
            if (THAILAND_BOUNDS['latlng'][0] <= lat <= THAILAND_BOUNDS['latlng'][2] and
                THAILAND_BOUNDS['latlng'][1] <= lon <= THAILAND_BOUNDS['latlng'][3]):
                station_info = {
                    'uid': station.get('uid'),
                    'station': {
                        'name': station.get('station', {}).get('name', 'Unknown'),
                        'geo': [station.get('lat'), station.get('lon')]
                    }
                }
                thailand_stations.append(station_info)
            
        return thailand_stations
    except requests.RequestException as e:
        print(f"Error fetching stations data: {e}")
        sys.exit(1)

def fetch_station_data(station_id):
    """
    Fetch latest air quality data for a specific station
    """
    try:
        params = {
            "token": API_TOKEN
        }
        response = requests.get(FEED_URL.format(station_id), params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for station {station_id}: {e}")
        return None

def process_station_data(raw_data, station_info):
    """
    Process the raw API data and extract relevant information
    """
    try:
        if raw_data.get('status') != 'ok':
            return None
            
        data = raw_data['data']
        iaqi = data.get('iaqi', {})
        station_name = station_info.get('station', {}).get('name', 'Unknown')
        
        # Extract city name from station name
        city = station_name.split(',')[0].strip()
        if 'Thailand' in city:
            city = city.replace('Thailand', '').strip()
        
        # Create a record with the latest data
        record = {
            'station_name': station_name,
            'station_id': station_info.get('uid'),
            'city': city,
            'latitude': station_info.get('station', {}).get('geo', [None, None])[0],
            'longitude': station_info.get('station', {}).get('geo', [None, None])[1],
            'timestamp': data.get('time', {}).get('s'),
            'aqi': data.get('aqi'),
            'pm25': iaqi.get('pm25', {}).get('v'),
            'pm10': iaqi.get('pm10', {}).get('v'),
            'temperature': iaqi.get('t', {}).get('v'),
            'humidity': iaqi.get('h', {}).get('v')
        }
        return record
    
    except Exception as e:
        print(f"Error processing data for station {station_info.get('uid')}: {e}")
        return None

def get_rounded_hour_timestamp():
    """
    Get current timestamp rounded down to the nearest hour
    Returns format like '2024-03-21_1300' (without colon)
    """
    current = datetime.now()
    rounded = current.replace(minute=0, second=0, microsecond=0)
    return rounded.strftime('%Y-%m-%d_%H00')

def main():
    """
    Main function to fetch and process air quality data for all Thailand stations
    """
    # Ensure output directory exists
    ensure_output_dir()
    
    print(f"{Fore.CYAN}Fetching list of air quality monitoring stations in Thailand...{Style.RESET_ALL}")
    stations = fetch_thailand_stations()
    
    if not stations:
        print(f"{Fore.RED}No stations found in Thailand{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"\n{Fore.GREEN}Found {len(stations)} stations in Thailand{Style.RESET_ALL}")
    
    # Collect data from all stations
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
    
    # Get the current query time
    query_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create output dictionary
    output = {
        'query_timestamp': query_time,  # When we queried the API
        'country': 'Thailand',
        'total_stations': len(stations),
        'total_data_points': len(records),
        'data': records
    }
    
    # Print colored JSON output
    print(f"\n{Fore.CYAN}Latest air quality data for all Thailand stations (Query time: {query_time}):{Style.RESET_ALL}")
    print_colored_json(output)
    
    # Get rounded timestamp for filenames
    timestamp = get_rounded_hour_timestamp()
    
    # Save to JSON file in output directory
    output_file = os.path.join(OUTPUT_DIR, f'thailand_aqi_data_{timestamp}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n{Fore.GREEN}Data has been saved to '{output_file}'{Style.RESET_ALL}")
    
    # Calculate and print summary statistics
    df = pd.DataFrame(records)
    if not df.empty:
        print(f"\n{Fore.CYAN}Summary Statistics:{Style.RESET_ALL}")
        
        stats = {
            'AQI Statistics by City': df.groupby('city')['aqi'].describe().to_dict(),
            'PM2.5 Statistics by City': df.groupby('city')['pm25'].describe().to_dict()
        }
        print_colored_json(stats)
        
        # Save statistics to JSON file with timestamp
        stats_file = os.path.join(OUTPUT_DIR, f'thailand_aqi_stats_{timestamp}.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"\n{Fore.GREEN}Statistics have been saved to '{stats_file}'{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}No data available from any station{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 