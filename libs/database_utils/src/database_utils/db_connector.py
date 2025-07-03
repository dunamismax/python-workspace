# libs/database_utils/src/database_utils/db_connector.py

import sqlite3
from contextlib import contextmanager

from rich.console import Console

console = Console()


class DatabaseManager:
    """A robust context manager for SQLite database connections."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        """Opens the database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            console.log(
                f"[bold green]Database connection opened to:[/bold green] [cyan]{self.db_path}[/cyan]"
            )
            return self
        except sqlite3.Error as e:
            console.log(f"[bold red]Error connecting to database:[/bold red] {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            console.log("[bold green]Database connection closed.[/bold green]")

    def execute_query(self, query, params=()):
        """Executes a given SQL query (e.g., INSERT, UPDATE, DELETE)."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            console.log(f"[bold red]Query failed:[/bold red] {e}")
            self.conn.rollback()
            raise

    def fetchone(self, query, params=()):
        """Executes a query and fetches one result."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            console.log(f"[bold red]Fetch one failed:[/bold red] {e}")
            raise

    def fetchall(self, query, params=()):
        """Executes a query and fetches all results."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            console.log(f"[bold red]Fetch all failed:[/bold red] {e}")
            raise

    def create_table(self, table_name, schema):
        """Creates a table if it doesn't already exist."""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.execute_query(query)
        console.log(f"Table [bold cyan]'{table_name}'[/bold cyan] created or already exists.")


@contextmanager
def get_sqlite_connection(db_path):
    """
    A context manager for a simple, one-off SQLite database connection.

    This is suitable for simple scripts or functions where a full DatabaseManager
    class might be overkill.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        console.log(f"[bold red]Database error:[/bold red] {e}")
        raise
    finally:
        if conn:
            conn.close()
