import sqlite3

def get_sqlite_connection(db_path):
    """Establishes and returns a SQLite database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def create_table_if_not_exists(conn, table_name, schema):
    """Creates a table if it doesn't already exist."""
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
    conn.commit()

