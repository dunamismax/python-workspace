# libs/database_utils/tests/test_db_connector.py

import unittest
import sqlite3
import os
from database_utils.db_connector import DatabaseManager, get_sqlite_connection

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.db_path = "test.db"
        # Ensure the db file does not exist before a test
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        # Clean up the created db file
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_context_manager(self):
        with DatabaseManager(self.db_path) as db:
            self.assertIsNotNone(db.conn)
        # Connection should be closed after exiting the context
        self.assertTrue(db.conn.close)

    def test_create_table(self):
        with DatabaseManager(self.db_path) as db:
            db.create_table("test_table", "id INTEGER, name TEXT")
            cursor = db.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';")
            self.assertIsNotNone(cursor.fetchone())

    def test_execute_query(self):
        with DatabaseManager(self.db_path) as db:
            db.create_table("users", "id INTEGER, name TEXT")
            db.execute_query("INSERT INTO users (name) VALUES (?)", ("test_user",))
            cursor = db.conn.cursor()
            cursor.execute("SELECT name FROM users WHERE name='test_user';")
            self.assertEqual(cursor.fetchone()[0], "test_user")

    def test_fetchone(self):
        with DatabaseManager(self.db_path) as db:
            db.create_table("users", "id INTEGER, name TEXT")
            db.execute_query("INSERT INTO users (name) VALUES (?)", ("test_user",))
            user = db.fetchone("SELECT * FROM users WHERE name=?", ("test_user",))
            self.assertEqual(user["name"], "test_user")

    def test_fetchall(self):
        with DatabaseManager(self.db_path) as db:
            db.create_table("users", "id INTEGER, name TEXT")
            db.execute_query("INSERT INTO users (name) VALUES (?), (?)", ("user1", "user2"))
            users = db.fetchall("SELECT * FROM users")
            self.assertEqual(len(users), 2)
            self.assertEqual(users[0]["name"], "user1")
            self.assertEqual(users[1]["name"], "user2")

class TestGetSqliteConnection(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_simple.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_simple_connection(self):
        with get_sqlite_connection(self.db_path) as conn:
            self.assertIsNotNone(conn)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER)")
            conn.commit()
        
        # Check if table was created
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test';")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

if __name__ == '__main__':
    unittest.main()
