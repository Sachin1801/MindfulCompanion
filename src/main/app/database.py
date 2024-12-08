import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import json
from .models import UserProfile, ChatMessage

class Database:
    def __init__(self, db_path: str = "mindful_companion.db"):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age_category TEXT NOT NULL,
                    emotions TEXT NOT NULL,
                    therapy_status TEXT NOT NULL,
                    interaction_style TEXT NOT NULL,
                    stress_level TEXT NOT NULL,
                    goals TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    mood TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()

    def save_user_profile(self, profile: UserProfile) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO users (name, age_category, emotions, therapy_status, 
                                 interaction_style, stress_level, goals)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (profile.name, profile.age_category, json.dumps(profile.emotions),
                  profile.therapy_status, profile.interaction_style, 
                  profile.stress_level, profile.goals))
            conn.commit()
            return cursor.lastrowid

    def get_user_profile(self, user_id: int) -> Optional[UserProfile]:
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return UserProfile(
                    name=row['name'],
                    age_category=row['age_category'],
                    emotions=json.loads(row['emotions']),
                    therapy_status=row['therapy_status'],
                    interaction_style=row['interaction_style'],
                    stress_level=row['stress_level'],
                    goals=row['goals']
                )
            return None

    def save_chat_message(self, user_id: int, message: ChatMessage):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO chat_history (user_id, role, content, mood)
                VALUES (?, ?, ?, ?)
            ''', (user_id, message.role, message.content, message.mood))
            conn.commit()

    def get_chat_history(self, user_id: int, limit: int = 10) -> List[ChatMessage]:
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM chat_history 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_id, limit))
            rows = cursor.fetchall()
            return [
                ChatMessage(
                    role=row['role'],
                    content=row['content'],
                    mood=row['mood']
                ) for row in rows
            ]

    def get_mood_statistics(self, user_id: int) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT mood, COUNT(*) as count
                FROM chat_history
                WHERE user_id = ? AND mood IS NOT NULL
                GROUP BY mood
            ''', (user_id,))
            return dict(cursor.fetchall())