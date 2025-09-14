import logging
from flask import Flask, request, jsonify, Response, redirect, url_for
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
@app.route("/authenticate", methods=["GET"])
def authenticate():
    """
    Landing page with two buttons. Each button calls /start-auth/<provider>
    to create a Terra widget session and redirect the user to the widget.
    """
    html = """
    <html>
    <head><title>Authenticate</title></head>
    <body>
        <h2>Connect a Provider</h2>

        <div style="margin-bottom: 12px;">
            <h3>Garmin</h3>
            <button onclick="window.location.href='/start-auth/GARMIN'">Authenticate with GARMIN</button>
        </div>

        <div>
            <h3>Oura</h3>
            <button onclick="window.location.href='/start-auth/OURA'">Authenticate with OURA</button>
        </div>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


@app.route("/start-auth/<provider>", methods=["GET"])
def start_auth(provider: str):
    """
    Creates a Terra widget session for the requested provider and redirects.
    Supported examples: GARMIN, OURA
    """
    provider = provider.upper().strip()
    # Optional: make the reference id unique per attempt
    reference_id = f"ref-{provider}-{int(time.time())}"

    try:
        widget_response = terra.generate_widget_session(
            providers=[provider],
            reference_id=reference_id
        )
        widget_url = widget_response.get_json()["url"]
        return redirect(widget_url, code=302)
    except Exception as e:
        _LOGGER.exception("Failed to create widget session for %s", provider)
        return jsonify({"error": f"Could not start auth for {provider}", "details": str(e)}), 400


# ----------------------
# App Runner
# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


# import logging
# from flask import Flask, request, jsonify, Response
# from terra.base_client import Terra

# import os
# import json
# import time
# import datetime

# # ----------------------
# # Logging Setup
# # ----------------------
# logging.basicConfig(level=logging.INFO)
# _LOGGER = logging.getLogger("app")

# # ----------------------
# # Flask App Setup
# # ----------------------
# app = Flask(__name__)

# # ----------------------
# # Terra API Setup
# # ----------------------
# webhook_secret = "b214a3b61acf5505af1380d487d1a019fe3e503a3cf861e1"
# dev_id = "kimba-testing-0QpIlNCqtV"
# api_key = "ZsNPUMzN37eMQnjbuBN_MWrsgoRyeFD_"

# terra = Terra(api_key=api_key, dev_id=dev_id, secret=webhook_secret)

# # ----------------------
# # Routes
# # ----------------------
# @app.route("/authenticate", methods=['GET'])
# def authenticate(): 
#     widget_response = terra.generate_widget_session(
#         providers=['GARMIN'], 
#         reference_id="224"
#     )
#     widget_url = widget_response.get_json()['url']
    
#     html = f"""
#     <html>
#     <head><title>Authenticate</title></head>
#     <body>
#         <h2>Authenticate with Garmin</h2>
#         <button onclick="window.location.href='{widget_url}'">Authenticate with GARMIN</button>
#     </body>
#     </html>
#     """
#     return Response(html, mimetype='text/html')

# # ----------------------
# # App Runner
# # ----------------------
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
