#!/usr/bin/env python3
"""flask basic app for authentiaction"""

from auth import Auth
from flask import jsonify, request, abort, redirect
from flask import Flask
app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
        registers a user if the email doesnot already exists
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = AUTH.register_user(email, password)
            return jsonify({"email": user.email, "message": "user created"})
        except Exception:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
        logs in a user and creates a session
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.valid_login(email, password):
            sessionID = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', sessionID)

            return response
        else:
            abort(401)

@app.route('/sessions', methods=['DELETE'])
def logout():
    """deletes a session from user and logs out"""
    if request.method == 'DELETE':
        session_ID = request.cookies.get('session_id')

        user = AUTH.get_user_from_session_id(session_ID)
        if not user:
            abort(403)
        AUTH.destroy_session(user.session_id)
        return redirect('/')
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
