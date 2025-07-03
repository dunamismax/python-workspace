# apps/todo_api/src/todo_api/database.py

from database_utils.db_connector import DatabaseManager

DATABASE_FILE = "todo.db"
TABLE_NAME = "tasks"
TABLE_SCHEMA = """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0
"""

def get_db():
    """Returns a DatabaseManager instance for the To-Do app."""
    return DatabaseManager(DATABASE_FILE)

def initialize_database():
    """Initializes the database and creates the tasks table."""
    with get_db() as db:
        db.create_table(TABLE_NAME, TABLE_SCHEMA)
