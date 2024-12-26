# utils/html_components.py

from utils.html_styles import (
    get_content_container_style,
    get_content_style,
    get_copy_button_style,
    get_copy_button_svg
)
import html

def get_content_with_copy_button(content_id, button_id, content_html, title):
    # Escape the content for HTML display
    content_html_escaped = html.escape(content_html).replace('\n', '<br>')

    return f"""
    <div style="{get_content_container_style()}">
        <h4 style="margin: 0; color: #202124;">{title}</h4>
    </div>
    <div id="{content_id}" style="{get_content_style()}">
    {content_html_escaped}
    </div>
    <div style="text-align: right; margin-top: 10px;">
        <button id="{button_id}" style="{get_copy_button_style()}">
            {get_copy_button_svg()}
            Copy
        </button>
    </div>
    <script>
    function fallbackCopyTextToClipboard(text) {{
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.top = "0";
        textArea.style.left = "0";
        textArea.style.position = "fixed";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {{
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Fallback: Copying text command was ' + msg);
        }} catch (err) {{
            console.error('Fallback: Oops, unable to copy', err);
        }}
        document.body.removeChild(textArea);
    }}

    function copyTextToClipboard(text) {{
        if (!navigator.clipboard) {{
            fallbackCopyTextToClipboard(text);
            return;
        }}
        navigator.clipboard.writeText(text).then(function() {{
            console.log('Async: Copying to clipboard was successful!');
        }}, function(err) {{
            console.error('Async: Could not copy text: ', err);
            fallbackCopyTextToClipboard(text);
        }});
    }}

    const copyButton_{button_id} = document.getElementById('{button_id}');
    const content_{content_id} = document.getElementById('{content_id}');

    copyButton_{button_id}.addEventListener('click', function(event) {{
        event.preventDefault();
        const textToCopy = content_{content_id}.innerText;
        copyTextToClipboard(textToCopy);
        
        copyButton_{button_id}.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="#4285F4" style="margin-right: 4px;">
                <path d="M0 0h24v24H0z" fill="none"/>
                <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
            </svg>
            Copied!
        `;
        copyButton_{button_id}.style.backgroundColor = '#E8F0FE';
        copyButton_{button_id}.style.color = '#4285F4';

        setTimeout(() => {{
            copyButton_{button_id}.innerHTML = `
                {get_copy_button_svg()}
                Copy
            `;
            copyButton_{button_id}.style.backgroundColor = '#F1F3F4';
            copyButton_{button_id}.style.color = '#5F6368';
        }}, 2000);
    }});
    </script>
    """
