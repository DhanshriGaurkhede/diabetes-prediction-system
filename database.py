"""
database.py - SQLite Database Management Layer for Diabetes Prediction System
Provides secure, parameterized queries for user authentication, settings, and persistent prediction history.
"""

import sqlite3
from typing import Optional, Dict, Any, List
from datetime import datetime

DB_NAME = "diabetes_app.db"


def get_connection():
    """Create a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db():
    """Initialize SQLite database tables with appropriate schemas."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE COLLATE NOCASE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                theme TEXT DEFAULT 'light',
                notifications_enabled INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Prediction history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                patient_name TEXT DEFAULT 'Anonymous',
                pregnancies INTEGER NOT NULL,
                glucose REAL NOT NULL,
                blood_pressure REAL NOT NULL,
                skin_thickness REAL NOT NULL,
                insulin REAL NOT NULL,
                bmi REAL NOT NULL,
                diabetes_pedigree REAL NOT NULL,
                age INTEGER NOT NULL,
                prediction_result TEXT NOT NULL,
                prediction_probability REAL NOT NULL,
                notes TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()


# ==============================================================================
# USER MANAGEMENT FUNCTIONS
# ==============================================================================

def create_user(username: str, password_hash: str, full_name: str, email: Optional[str] = None) -> Optional[int]:
    """Register a new user and initialize their settings."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, full_name, email) VALUES (?, ?, ?, ?)",
                (username.strip(), password_hash, full_name.strip(), email.strip() if email else None)
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO user_settings (user_id, theme) VALUES (?, 'light')",
                (user_id,)
            )
            conn.commit()
            return user_id
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Retrieve user record by username."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user record by user ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def check_username_exists(username: str) -> bool:
    """Check if a username already exists in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username.strip(),))
        return cursor.fetchone() is not None


def check_email_exists(email: str) -> bool:
    """Check if an email already exists in the database."""
    if not email:
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email.strip(),))
        return cursor.fetchone() is not None


def update_user_profile(user_id: int, full_name: str, email: Optional[str] = None) -> bool:
    """Update a user's full name and email."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
                (full_name.strip(), email.strip() if email else None, user_id)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def update_user_password(user_id: int, new_password_hash: str) -> bool:
    """Update a user's password hash."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, user_id)
        )
        conn.commit()
        return True


# ==============================================================================
# USER SETTINGS FUNCTIONS
# ==============================================================================

def get_user_settings(user_id: int) -> Dict[str, Any]:
    """Fetch user settings (e.g. theme preference)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        # Create default if missing
        cursor.execute("INSERT OR IGNORE INTO user_settings (user_id, theme) VALUES (?, 'light')", (user_id,))
        conn.commit()
        return {"user_id": user_id, "theme": "light", "notifications_enabled": 1}


def update_user_theme(user_id: int, theme: str) -> bool:
    """Update the user's theme preference ('light' or 'dark')."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_settings SET theme = ? WHERE user_id = ?",
            (theme, user_id)
        )
        conn.commit()
        return True


# ==============================================================================
# PREDICTION HISTORY FUNCTIONS
# ==============================================================================

def add_prediction(
    user_id: int,
    pregnancies: int,
    glucose: float,
    blood_pressure: float,
    skin_thickness: float,
    insulin: float,
    bmi: float,
    diabetes_pedigree: float,
    age: int,
    prediction_result: str,
    prediction_probability: float,
    patient_name: str = "Anonymous",
    notes: str = ""
) -> int:
    """Save a clinical prediction record linked to a user account."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prediction_history (
                user_id, patient_name, pregnancies, glucose, blood_pressure,
                skin_thickness, insulin, bmi, diabetes_pedigree, age,
                prediction_result, prediction_probability, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, patient_name.strip() or "Anonymous", int(pregnancies),
            float(glucose), float(blood_pressure), float(skin_thickness),
            float(insulin), float(bmi), float(diabetes_pedigree), int(age),
            prediction_result, float(prediction_probability), notes
        ))
        conn.commit()
        return cursor.lastrowid


def get_user_history(
    user_id: int,
    search_query: Optional[str] = None,
    outcome_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve isolated prediction history for a specific user with optional filters."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM prediction_history WHERE user_id = ?"
        params: List[Any] = [user_id]

        if outcome_filter and outcome_filter != "All":
            query += " AND prediction_result = ?"
            params.append(outcome_filter)

        if search_query:
            query += " AND (patient_name LIKE ? OR notes LIKE ?)"
            wildcard = f"%{search_query.strip()}%"
            params.extend([wildcard, wildcard])

        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Compute summary metrics for a user's predictions."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) AS total,
                SUM(CASE WHEN prediction_result = 'Diabetes' THEN 1 ELSE 0 END) AS diabetes_count,
                SUM(CASE WHEN prediction_result != 'Diabetes' THEN 1 ELSE 0 END) AS no_diabetes_count,
                AVG(prediction_probability) AS avg_probability
            FROM prediction_history
            WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            total = row["total"] or 0
            diab = row["diabetes_count"] or 0
            no_diab = row["no_diabetes_count"] or 0
            avg_prob = row["avg_probability"] or 0.0
            return {
                "total": total,
                "diabetes_count": diab,
                "no_diabetes_count": no_diab,
                "avg_probability": avg_prob
            }
        return {"total": 0, "diabetes_count": 0, "no_diabetes_count": 0, "avg_probability": 0.0}


def clear_user_history(user_id: int) -> bool:
    """Delete all prediction history records for a specific user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prediction_history WHERE user_id = ?", (user_id,))
        conn.commit()
        return True


def delete_history_record(record_id: int, user_id: int) -> bool:
    """Delete a single prediction record, ensuring user ownership."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prediction_history WHERE id = ? AND user_id = ?", (record_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
