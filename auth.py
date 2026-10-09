"""
auth.py - Authentication & Session Management for DiabetesCare AI
Handles password hashing (PBKDF2-HMAC-SHA256), login, registration, and logout flows.
"""

import os
import hashlib
import binascii
import streamlit as st
from typing import Optional, Dict, Any, Tuple
import database


def hash_password(password: str) -> str:
    """Hash a password for storing using PBKDF2 HMAC SHA-256 with a random salt."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    if not stored_password or not provided_password:
        return False
    try:
        salt = stored_password[:64]
        stored_hash = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('ascii'),
            100000
        )
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_hash
    except Exception:
        return False


def register_user(username: str, password: str, confirm_password: str, full_name: str, email: str = "") -> Tuple[bool, str]:
    """Validate and register a new user."""
    username = username.strip()
    full_name = full_name.strip()
    email = email.strip()

    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not full_name:
        return False, "Please provide your full name."
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if password != confirm_password:
        return False, "Passwords do not match."
    
    if database.check_username_exists(username):
        return False, f"Username '{username}' is already taken."
    
    if email and database.check_email_exists(email):
        return False, f"Email '{email}' is already registered with another account."

    pwd_hash = hash_password(password)
    user_id = database.create_user(username, pwd_hash, full_name, email)
    if user_id:
        return True, "Account registered successfully! Please log in."
    return False, "Failed to create account. Please try again."


def login_user(username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Authenticate a user with username and password."""
    username = username.strip()
    if not username or not password:
        return False, None, "Please enter both username and password."
    
    user = database.get_user_by_username(username)
    if not user:
        return False, None, "Invalid username or password."
    
    if verify_password(user["password_hash"], password):
        # Fetch user settings (e.g. theme)
        settings = database.get_user_settings(user["id"])
        user_data = {
            "id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"] or "",
            "theme": settings.get("theme", "light")
        }
        return True, user_data, "Login successful!"
    
    return False, None, "Invalid username or password."


def logout():
    """Clear user session state and trigger rerun."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.current_page = "Dashboard"
    st.session_state.last_prediction = None
    st.rerun()


def render_auth_page():
    """Render the login/signup tabbed interface for unauthenticated visitors."""
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
        <div style="font-size: 2.8rem; margin-bottom: 0.3rem;">🩺</div>
        <h1 style="color: var(--text-primary); font-size: 2.2rem; font-weight: 800; margin: 0;">
            DiabetesCare AI
        </h1>
        <p style="color: var(--text-secondary); font-size: 1.05rem; margin-top: 0.3rem;">
            Intelligent Diabetes Risk Prediction
        </p>
    </div>
    """, unsafe_allow_html=True)

    auth_col1, auth_col2, auth_col3 = st.columns([1, 2, 1])

    with auth_col2:
        tab_login, tab_signup = st.tabs(["🔐 Sign In", "📝 Create Account"])

        with tab_login:
            st.markdown("<h3 style='color: var(--text-primary); margin-top: 0.5rem;'>Sign In</h3>", unsafe_allow_html=True)
            st.caption("Enter your clinician or user credentials to access personalized evaluations.")
            
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Sign In", use_container_width=True, key="btn_login"):
                success, user_data, msg = login_user(login_username, login_password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.session_state.theme = user_data.get("theme", "light")
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with tab_signup:
            st.markdown("<h3 style='color: var(--text-primary); margin-top: 0.5rem;'>Create Account</h3>", unsafe_allow_html=True)
            st.caption("Register for a secure account to track patient assessment records.")
            
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_username = st.text_input("Choose Username", key="reg_username")
            reg_email = st.text_input("Email (Optional)", key="reg_email")
            reg_password = st.text_input("Password (min 6 chars)", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

            if st.button("Create Account", use_container_width=True, key="btn_signup"):
                ok, msg = register_user(reg_username, reg_password, reg_confirm, reg_name, reg_email)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
