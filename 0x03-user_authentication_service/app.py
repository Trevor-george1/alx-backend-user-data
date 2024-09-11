#!/usr/bin/env python3
"""flask basic app for authentiaction"""

from flask import jsonify, render_template
from flask import Flask
app = Flask(__name__)


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
