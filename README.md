# Air Quality Command Center

A real-time air quality monitoring and alert system for Bangkok with AI-powered chat assistance.

## Features

- Real-time air quality monitoring for Bangkok stations
- AI-powered alerts and recommendations
- Interactive chat assistant for air quality inquiries
- Automated data collection and analysis
- Health implications and recommended actions

## Requirements

- Python 3.7+
- OpenAI API key
- Required packages in `requirements.txt`
- Streamlit for dashboard interface

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Set up environment:
   - Create `.env` file with your OpenAI API key
   - Configure `.streamlit/secrets.toml` for Streamlit

## Project Structure

```
.
├── main.py                     # Main Streamlit dashboard
├── utils/
│   ├── message_utils.py        # Chat message formatting utilities
│   └── prompt_instructions.py  # AI prompt templates
├── scripts/
│   ├── 00-get_bangkok_aqi.py  # Data collection script
│   ├── 01-extract-alerts-actions.py  # Alert generation
│   └── 04-chat-assistant.py   # Chat assistant implementation
└── output/
    ├── hourly/                # Raw AQI data storage
    └── alerts/                # Processed alerts
```

## Usage

1. Start data collection:
```bash
python scripts/00-get_bangkok_aqi.py
```

2. Generate alerts:
```bash
python scripts/01-extract-alerts-actions.py
```

3. Launch dashboard:
```bash
streamlit run main.py
```

## Data Processing Pipeline

1. **Data Collection**: Fetches real-time AQI data from Bangkok stations
2. **Alert Generation**: AI processes data to generate alerts and recommendations
3. **Dashboard Display**: Shows current metrics and chat interface
4. **Chat Assistance**: Provides interactive air quality guidance

## Output Format

The system processes and displays:
- AQI (Air Quality Index)
- PM2.5 Levels
- Temperature
- Humidity
- Health Implications
- Recommended Actions

## Files and Directories

- `main.py`: Streamlit dashboard with real-time metrics and chat
- `utils/message_utils.py`: Chat interface formatting
- `utils/prompt_instructions.py`: AI prompt templates
- `output/hourly/`: Raw AQI data storage
- `output/alerts/`: Processed alerts and recommendations

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Add your license information here] 