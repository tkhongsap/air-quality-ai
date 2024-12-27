import json
import os
from datetime import datetime
import glob
from openai import OpenAI
from utils.prompt_instructions import get_air_quality_system_prompt
from dotenv import load_dotenv

load_dotenv()

llm_model = os.getenv('OPENAI_MODEL')

def get_latest_aqi_data():
    """Get the latest AQI data file from the output/hourly directory"""
    files = glob.glob('output/hourly/bangkok_aqi_data_*.json')
    if not files:
        raise FileNotFoundError("No AQI data files found")
    
    latest_file = max(files, key=os.path.getctime)
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data, latest_file

def generate_alerts(aqi_data):
    """Generate alerts using OpenAI API"""
    client = OpenAI()
    
    # Prepare the system prompt
    system_prompt = get_air_quality_system_prompt()
    
    # Convert data to a clean string format
    data_str = json.dumps(aqi_data, ensure_ascii=False, indent=2)
    
    response = client.chat.completions.create(
        model=llm_model,  # Using the latest model that's good at JSON
        response_format={ "type": "json_object" },  # Enforce JSON output
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate air quality alerts from this data:\n{data_str}"}
        ],
        temperature=0.3  # Low temperature for consistent output
    )
    
    # Parse the response
    alerts = json.loads(response.choices[0].message.content)
    return alerts

def save_alerts(alerts, source_file):
    """Save alerts to a JSON file"""
    # Create alerts directory if it doesn't exist
    os.makedirs('output/alerts', exist_ok=True)
    
    # Extract timestamp from source file
    # Get just the filename without path
    source_filename = os.path.basename(source_file)
    timestamp = source_filename.replace('bangkok_aqi_data_', '').replace('.json', '')
    
    # Generate filename using the same timestamp as source
    filename = os.path.join('output', 'alerts', f'bangkok_aqi_alerts_{timestamp}.json')
    
    # Save alerts with metadata
    output = {
        "generated_at": datetime.now().isoformat(),
        "source_file": source_file,
        **alerts
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    return filename

def sort_and_save_alerts(filename):
    """Read the alerts file, sort by AQI, and save it back"""
    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sort the alerts by AQI in descending order
    data['alerts'] = sorted(data['alerts'], key=lambda x: x['aqi'], reverse=True)
    
    # Save the sorted data back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

def main():
    try:
        # Get latest AQI data
        print("Reading latest AQI data...")
        aqi_data, source_file = get_latest_aqi_data()
        
        # Generate alerts
        print("Generating alerts...")
        alerts = generate_alerts(aqi_data)
        
        # Save alerts
        print("Saving alerts...")
        output_file = save_alerts(alerts, source_file)
        
        # Sort alerts by AQI
        print("Sorting alerts by AQI...")
        sorted_data = sort_and_save_alerts(output_file)
        
        print(f"Alerts successfully generated, sorted, and saved to: {output_file}")
        print(f"Number of alerts: {len(sorted_data['alerts'])}")
        print("\nTop 5 highest AQI locations:")
        for alert in sorted_data['alerts'][:5]:
            print(f"- {alert['station_name']}: AQI {alert['aqi']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
