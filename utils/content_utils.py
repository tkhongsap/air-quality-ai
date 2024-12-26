def create_content_with_copy_button(content_type, content_html):
    return f"""
    <div style="
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    ">
        <h4 style="margin: 0; color: #202124;">{content_type.capitalize()} Content</h4>
    </div>
    <div id="{content_type}-content" style="
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #E8EAED;
        padding: 15px;
        background-color: white;
        font-size: 14px;
        line-height: 1.6;
        border-radius: 4px;
    ">
    {content_html}
    </div>
    <div style="text-align: right; margin-top: 10px;">
        <button id="copy-{content_type}-button" style="
            background-color: #F1F3F4;
            color: #5F6368;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            font-size: 14px;
        ">
            <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#5F6368" style="margin-right: 4px;">
                <path d="M0 0h24v24H0z" fill="none"/>
                <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
            </svg>
            Copy
        </button>
    </div>
    <script>
    const copyButton_{content_type} = document.getElementById('copy-{content_type}-button');
    const content_{content_type} = document.getElementById('{content_type}-content');

    copyButton_{content_type}.addEventListener('click', () => {{
        const textToCopy = content_{content_type}.innerText;
        if (navigator.clipboard && window.isSecureContext) {{
            // navigator.clipboard API method
            navigator.clipboard.writeText(textToCopy).then(() => {{
                // Change button to indicate success
                copyButton_{content_type}.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#4285F4" style="margin-right: 4px;">
                        <path d="M0 0h24v24H0z" fill="none"/>
                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                    </svg>
                    Copied!
                `;
                copyButton_{content_type}.style.backgroundColor = '#E8F0FE';
                copyButton_{content_type}.style.color = '#4285F4';

                setTimeout(() => {{
                    copyButton_{content_type}.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#5F6368" style="margin-right: 4px;">
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                        </svg>
                        Copy
                    `;
                    copyButton_{content_type}.style.backgroundColor = '#F1F3F4';
                    copyButton_{content_type}.style.color = '#5F6368';
                }}, 2000);
            }})
            .catch(err => {{
                console.error('Failed to copy: ', err);
            }});
        }} else {{
            // Fallback method
            const textArea = document.createElement('textarea');
            textArea.value = textToCopy;
            document.body.appendChild(textArea);
            textArea.select();
            try {{
                document.execCommand('copy');
                // Change button to indicate success
                copyButton_{content_type}.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#4285F4" style="margin-right: 4px;">
                        <path d="M0 0h24v24H0z" fill="none"/>
                        <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                    </svg>
                    Copied!
                `;
                copyButton_{content_type}.style.backgroundColor = '#E8F0FE';
                copyButton_{content_type}.style.color = '#4285F4';

                setTimeout(() => {{
                    copyButton_{content_type}.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#5F6368" style="margin-right: 4px;">
                            <path d="M0 0h24v24H0z" fill="none"/>
                            <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                        </svg>
                        Copy
                    `;
                    copyButton_{content_type}.style.backgroundColor = '#F1F3F4';
                    copyButton_{content_type}.style.color = '#5F6368';
                }}, 2000);
            }} catch (err) {{
                console.error('Fallback: Oops, unable to copy', err);
            }}
            document.body.removeChild(textArea);
        }}
    }});
    </script>
    """
