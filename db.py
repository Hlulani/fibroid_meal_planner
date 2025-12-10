# db.py
import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib
from typing import Optional, Dict, Any

DB_PATH = Path("fibroid_meal_planner.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # Saved plans table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    conn.commit()
    conn.close()


def _hash_password(password: str) -> str:
    # simple hash; for a real public product use bcrypt / argon2
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(email: str, password: str) -> Dict[str, Any]:
    email = email.strip().lower()
    if not email or not password:
        raise ValueError("Email and password required")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing = cur.fetchone()
    if existing:
        conn.close()
        raise ValueError("User already exists")

    password_hash = _hash_password(password)
    now = datetime.utcnow().isoformat()

    cur.execute(
        "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
        (email, password_hash, now),
    )
    conn.commit()

    user_id = cur.lastrowid
    conn.close()
    return {"id": user_id, "email": email}


def authenticate(email: str, password: str) -> Optional[Dict[str, Any]]:
    email = email.strip().lower()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, email, password_hash FROM users WHERE email = ?",
        (email,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    if row["password_hash"] != _hash_password(password):
        return None

    return {"id": row["id"], "email": row["email"]}


def save_plan(user_id: int, plan_json: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()

    cur.execute(
        """
        INSERT INTO meal_plans (user_id, plan_json, created_at)
        VALUES (?, ?, ?)
        """,
        (user_id, plan_json, now),
    )
    conn.commit()
    conn.close()


def load_latest_plan(user_id: int) -> Optional[str]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT plan_json
        FROM meal_plans
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None
    return row["plan_json"]
