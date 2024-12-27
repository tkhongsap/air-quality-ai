def get_tabs_style():
    return """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #5F6368;
        font-weight: 400;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #4285F4;
        font-weight: 500;
        border-bottom: 2px solid #4285F4;
    }
    </style>
    """

def get_dashboard_css():
    return """
    <style>
        .alert-section {
            padding: 1rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            color: #333;
            font-size: 1rem;
            font-weight: 600;
        }
        .action-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .action-title {
            display: flex;
            align-items: center;
        }
        .action-count {
            background: rgba(255, 75, 75, 0.1);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
        }
        .action-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 100%;
            margin-bottom: 1rem;
        }
        .action-content {
            flex-grow: 1;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .priority-badge {
            background: white;
            padding: 0.5rem 1.2rem;
            border-radius: 6px;
            font-size: 0.9rem;
            margin-left: 1rem;
            font-weight: 500;
        }
    </style>
    """

def get_priority_colors():
    return {
        "Immediate": {"bg": "rgba(255, 75, 75, 0.05)", "text": "#FF4B4B", "icon": ""},
        "Preventive": {"bg": "rgba(255, 193, 7, 0.05)", "text": "#FFC107", "icon": ""},
        "Long-Term": {"bg": "rgba(59, 130, 246, 0.05)", "text": "#3B82F6", "icon": ""}
    }
