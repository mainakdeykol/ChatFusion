import sqlite3
import uuid
from datetime import datetime


class MemoryDB:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions(
            session_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
        """)

        self.conn.commit()

    def create_session(self):
        session_id = str(uuid.uuid4())

        self.conn.execute(
            """
            INSERT INTO chat_sessions(session_id,title,created_at)
            VALUES(?,?,?)
            """,
            (
                session_id,
                "New Chat",
                datetime.now().isoformat()
            )
        )

        self.conn.commit()

        return session_id

    def get_sessions(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT session_id,title
        FROM chat_sessions
        ORDER BY created_at DESC
        """)

        return cursor.fetchall()

    def update_title(self, session_id, title):
        self.conn.execute(
            """
            UPDATE chat_sessions
            SET title=?
            WHERE session_id=?
            """,
            (title[:40], session_id)
        )

        self.conn.commit()

    def save_message(self, session_id, role, content):

        self.conn.execute(
            """
            INSERT INTO messages(
                session_id,
                role,
                content,
                created_at
            )
            VALUES(?,?,?,?)
            """,
            (
                session_id,
                role,
                content,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()

    def get_messages(self, session_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT role,content
            FROM messages
            WHERE session_id=?
            ORDER BY id
            """,
            (session_id,)
        )

        rows = cursor.fetchall()

        return [
            {
                "role": role,
                "content": content
            }
            for role, content in rows
        ]