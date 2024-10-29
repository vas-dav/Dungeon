#!/usr/bin/env python
# encoding: utf-8

'''
server.py is the main source file for the Dungeon's backend service.
'''

import json
from flask import Flask, redirect, url_for, request, jsonify
from auth.auth_api import User, AuthApi
from auth.middleware import AuthMiddleware
from dashboard_api import construct_dashboard
from database.dungeon_db_cli import DungeonDBClient

app = Flask(__name__)
database = DungeonDBClient()
auth_api = AuthApi(database)
middleware = AuthMiddleware(database)

@app.before_request
def validator():
    res = middleware.validate_request()
    if res:
        return res

@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        new_user = User(request.json)
        return auth_api.create_user(new_user)
    else:
        return jsonify({'error': 'Request must contain JSON data'}), 400

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        new_user = User(request.json)
        return auth_api.create_session(new_user)
    else:
        return jsonify({'error': 'Request must contain JSON data'}), 400

@app.route('/logout')
def logout():
    return auth_api.delete_session()

@app.route('/dashboard')
def dashboard():
    return jsonify(construct_dashboard())

@app.route('/projects')
def projects():
    return jsonify(construct_projects())

if __name__ == "__main__":
    app.run(debug=True)
