# utils/html_styles.py

def get_tab_css():
    return """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
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

def get_content_container_style():
    return """
    background-color: #F8F9FA;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    """

def get_content_style():
    return """
    max-height: 450px;
    overflow-y: auto;
    border: 1px solid #E8EAED;
    padding: 15px;
    background-color: white;
    font-size: 14px;
    line-height: 1.6;
    border-radius: 4px;
    """

def get_copy_button_style():
    return """
    background-color: #F1F3F4;
    color: #5F6368;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    font-size: 14px;
    """

def get_copy_button_svg():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#5F6368" style="margin-right: 4px;">
        <path d="M0 0h24v24H0z" fill="none"/>
        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
    </svg>
    """
