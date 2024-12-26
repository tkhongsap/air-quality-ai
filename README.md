# Bangkok Air Quality Data Fetcher

This Python script fetches the last 6 hours of air quality data for Bangkok from the WAQI API.

## Requirements

- Python 3.7+
- Required packages are listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Simply run the script:
```bash
python get_bangkok_aqi.py
```

The script will:
1. Fetch the latest air quality data from Bangkok station (ID: 7398)
2. Process and display the data in a formatted table
3. Save the data to a CSV file named 'bangkok_aqi_data.csv'

## Output Format

The script outputs data with the following columns:
- timestamp: Date and time of measurement (YYYY-MM-DD HH:MM:SS)
- aqi: Air Quality Index
- pm25: PM2.5 concentration
- pm10: PM10 concentration
- temperature: Temperature in Celsius
- humidity: Relative humidity percentage

## Error Handling

The script includes error handling for:
- API connection failures
- Invalid API responses
- Missing data fields

If any errors occur, the script will display an appropriate error message and exit. 