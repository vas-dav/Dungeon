#!/usr/bin/env python
# encoding: utf-8

'''
middleware.py is the module for user auth middleware
'''

from flask import Flask, request, make_response, g

class AuthMiddleware:
    def __init__(self, db_cli):
        self.db = db_cli

    def extract_user_from_token(self, token):
        tokenIsPresent = f"""
            SELECT *
            FROM sessions
            WHERE sessionToken ='{token}'
        """
        data = self.db.query(tokenIsPresent)
        return data[0]['userID']

    def validate_request(self):
        if request.path == '/register' or request.path == '/login':
            return None
        session_token = request.cookies.get('SESSION_ID')
        if not session_token:
            return make_response('Unauthorized: Missing session_token cookie', 401)
        userID = self.extract_user_from_token(session_token)
        if not userID:
            return make_response('Unauthorized: corrupted session_token cookie', 401)

        # Flask's global object for custom data
        g.user_info = {'id': userID}
        return None
