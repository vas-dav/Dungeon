#!/usr/bin/env python
# encoding: utf-8

'''
dungeon_db_cli.py is the module for managing teh Dungeon's database services.
'''

import json
import pymssql
import os

class DungeonDBClient:
    def __init__(self):
        self.db_server = os.environ.get('DB_SERVER')
        print(self.db_server)
        self.password = os.environ.get('DB_PASSWORD')
        print(self.password)
        self.database = 'dungeondev'

        self.connection = pymssql.connect(
            server=self.db_server,
            user='sa',
            password=self.password,
            as_dict=True,
            autocommit=True
        )

        self.cursor = self.connection.cursor()
        self.initialize_database()

    def create_database(self, db_name):
        query = f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name='{db_name}') CREATE DATABASE {db_name};"
        self.cursor.execute(query)

    def switch_database(self, db_name):
        self.cursor.execute(f"USE {db_name};")

    def initialize_database(self):
        self.create_database(self.database)
        self.switch_database(self.database)

    def query(self, query_str, quiet=False):
        self.cursor.execute(query_str)
        if quiet:
            return []
        return self.cursor.fetchall()

