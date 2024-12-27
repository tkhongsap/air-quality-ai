def get_chat_assistant_banner():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(to right, #f5f5f5, #e8e8e8);
        padding: 1.2rem 2.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.2rem;
        text-align: center;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(245, 245, 245, 0.5), rgba(232, 232, 232, 0.5));
        z-index: 1;
    }
    
    .main-header > * {
        position: relative;
        z-index: 2;
    }
    
    .main-header h1 {
        color: #333333;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        letter-spacing: 0.01em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .main-header p {
        color: #666666;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        text-align: left;
    }
    
    .benefit-pills {
        display: flex;
        gap: 2rem;
        margin-top: 0.8rem;
        justify-content: center;
    }
    
    .benefit-pill {
        color: #666666;
        font-weight: 500;
        font-size: 0.8rem;
        letter-spacing: 0.03em;
        display: flex;
        align-items: center;
        gap: 6px;
        position: relative;
        padding-bottom: 3px;
    }
    
    .benefit-pill:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 20px;
        height: 2px;
        background-color: #000000;
        opacity: 0.2;
    }
    </style>
    <div class="main-header">
        <h1>🌬️ <span>Air Quality Command Center</span></h1>
        <div class="benefit-pills">
            <span class="benefit-pill">🔍 Real-time Monitoring</span>
            <span class="benefit-pill">⚠️ Smart Alerts</span>
            <span class="benefit-pill">📊 Action Planning</span>
        </div>
    </div>
    """

def get_dashboard_banner():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(to right, #f5f5f5, #e8e8e8);
        padding: 1.2rem 2.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.2rem;
        text-align: center;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(245, 245, 245, 0.5), rgba(232, 232, 232, 0.5));
        z-index: 1;
    }
    
    .main-header > * {
        position: relative;
        z-index: 2;
    }
    
    .main-header h1 {
        color: #333333;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        letter-spacing: 0.01em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .main-header p {
        color: #666666;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        text-align: left;
    }
    
    .benefit-pills {
        display: flex;
        gap: 2rem;
        margin-top: 0.8rem;
        justify-content: center;
    }
    
    .benefit-pill {
        color: #666666;
        font-weight: 500;
        font-size: 0.8rem;
        letter-spacing: 0.03em;
        display: flex;
        align-items: center;
        gap: 6px;
        position: relative;
        padding-bottom: 3px;
    }
    
    .benefit-pill:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 20px;
        height: 2px;
        background-color: #000000;
        opacity: 0.2;
    }
    </style>
    <div class="main-header">
        <h1>🌬️ <span>Air Quality Dashboard</span></h1>
    </div>
    """