#!/usr/bin/env python
# encoding: utf-8

'''
auth.py is the functional api generator for users
'''

from flask import jsonify, make_response, request
import uuid
from argon2 import PasswordHasher, exceptions

USER_KEYS = ['email', 'password']
class User():
    def __init__(self, json):
        self.email = None
        self.password = None
        self.uid = None
        if all(key in json for key in USER_KEYS):
            self.email = json['email']
            self.password = json["password"]

    def hash_password(self):
        if self.password:
            ph = PasswordHasher()
            self.password = ph.hash(self.password)

    def set_uid(self, uid):
        if uid:
            self.uid = int(uid)


class AuthApi:
    def __init__(self, db_cli):
        self.db = db_cli

    def valid_user(self, user):
        return isinstance(user.email, str) and user.email.strip() != '' and \
               isinstance(user.password, str) and user.password.strip() != ''

    def email_exists(self, email):
        checkUserEmail = f"""
			SELECT *
			FROM users
			WHERE userEmail='{email}';
		"""
        return True if self.db.query(checkUserEmail) else False

    def verify_user(self, user):
        extractUserHash = f"""
            SELECT *
            FROM users
            WHERE userEmail='{user.email}';
        """
        db_user_object = self.db.query(extractUserHash)
        if not db_user_object:
            return False
        db_user_hash = db_user_object[0]['userPassword']
        user.set_uid(db_user_object[0]['UID'])
        if db_user_hash:
            ph = PasswordHasher()
            try:
                return ph.verify(db_user_hash, user.password)
            except exceptions.VerifyMismatchError as e:
                return False
        return False

    def generate_session_token(self, user):
        token = str(uuid.uuid4())
        createNewToken = f"""
        INSERT INTO sessions (sessionToken, userID)
        VALUES ('{token}', '{user.uid}')
        """
        print(self.db.query(createNewToken, quiet=True))
        return token

    def create_user(self, user):
        if not self.valid_user(user):
            return jsonify({"message": "Corrupted data supplied."}), 400
        if self.email_exists(user.email):
            return jsonify({"message": "Email already in use"}), 400
        user.hash_password()
        initialiseUser = f"""
           INSERT INTO users (userEmail, userPassword)
           VALUES ('{user.email}', '{user.password}');
        """
        print(self.db.query(initialiseUser, quiet=True))
        return jsonify({'message': 'User added successfully!'}), 201

    def create_session(self, user):
        if not self.valid_user(user):
            return jsonify({"message": "Corrupted data supplied."}), 400
        if self.verify_user(user):
            res = make_response(jsonify({'message': f'New session token generated for {user.email}'}), 201)
            res.set_cookie('SESSION_ID', self.generate_session_token(user))
            return res
        else:
            return jsonify({'message': 'Passwords don\'t match or user not found.'}), 400

    def delete_session(self):
        if "SESSION_ID" not in request.cookies:
            return jsonify({'message': "No session token provided."})

        deleteSession = f"""
            DELETE FROM sessions WHERE
            sessionToken = '{request.cookies.get("SESSION_ID")}'
        """
        self.db.query(deleteSession, quiet=True)
        res = make_response(jsonify({'message': 'Logout!'}))
        res.set_cookie('SESSION_ID', expires=0)
        return res
