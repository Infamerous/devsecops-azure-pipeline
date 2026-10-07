from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "dev")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "unknown")


@app.route("/")
def index():
    return jsonify(
        message="MIDSEM Data Center Project — sample app",
        environment=ENVIRONMENT,
        version=APP_VERSION,
        host=socket.gethostname(),
    )


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    # Binding to all interfaces is required here: the app runs inside a
    # Docker container and must be reachable via the host's published port.
    app.run(host="0.0.0.0", port=8080)  # nosec B104
