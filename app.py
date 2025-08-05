import logging
from flask import Flask, request, jsonify, Response
from terra.base_client import Terra

import os
import json
import time
import datetime

# ----------------------
# Logging Setup
# ----------------------
logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("app")

# ----------------------
# Flask App Setup
# ----------------------
app = Flask(__name__)

# ----------------------
# Terra API Setup
# ----------------------
webhook_secret = "b214a3b61acf5505af1380d487d1a019fe3e503a3cf861e1"
dev_id = "kimba-testing-0QpIlNCqtV"
api_key = "ZsNPUMzN37eMQnjbuBN_MWrsgoRyeFD_"

terra = Terra(api_key=api_key, dev_id=dev_id, secret=webhook_secret)

# ----------------------
# Routes
# ----------------------
@app.route("/authenticate", methods=['GET'])
def authenticate(): 
    widget_response = terra.generate_widget_session(
        providers=['GARMIN'], 
        reference_id="224"
    )
    widget_url = widget_response.get_json()['url']
    
    html = f"""
    <html>
    <head><title>Authenticate</title></head>
    <body>
        <h2>Authenticate with Garmin</h2>
        <button onclick="window.location.href='{widget_url}'">Authenticate with GARMIN</button>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')

# ----------------------
# App Runner
# ----------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
