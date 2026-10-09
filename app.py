"""
app.py - Main Application Controller for DiabetesCare AI
Intelligent Diabetes Risk Prediction System.
ML Engine, feature ordering, and model calculations are strictly protected.
"""

import streamlit as st
import pandas as pd
import joblib

import database
import auth
import styles
from views.dashboard import render_dashboard
from views.prediction import render_prediction
from views.analytics import render_analytics
from views.history import render_history
from views.healthy_living import render_healthy_living
from views.model_info import render_model_info
from views.settings import render_settings

# Initialize SQLite database schema
database.init_db()

# Page Configuration
st.set_page_config(
    page_title="DiabetesCare AI - Intelligent Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load dataset and ML model (Random Forest)
@st.cache_resource
def load_ml_assets():
    data = pd.read_csv("Diabetes Dataset.csv")
    model = joblib.load("diabetes_random_forest_model.pkl")
    return data, model

data, model = load_ml_assets()

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# Inject Dynamic CSS Design System (Theme-aware)
styles.apply_theme()

# ==============================================================================
# AUTHENTICATION GATE
# ==============================================================================
if not st.session_state.authenticated:
    auth.render_auth_page()
else:
    # Authenticated User Session
    user = st.session_state.user or {}

    # Sidebar Navigation & Branding
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.3rem 0.2rem 1rem 0.2rem; border-bottom: 1px solid var(--border-subtle); margin-bottom: 1rem;">
            <div style="font-size: 1.22rem; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.35rem;">🩺</span> DiabetesCare AI
            </div>
            <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 3px; font-weight: 500;">
                Intelligent Diabetes Risk Prediction
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;'>Navigation</p>", unsafe_allow_html=True)
        
        nav_options = [
            "Dashboard",
            "Prediction",
            "Analytics",
            "Prediction History",
            "Healthy Living",
            "Model Information",
            "Settings"
        ]

        nav_icons = {
            "Dashboard": "🏠",
            "Prediction": "🔮",
            "Analytics": "📊",
            "Prediction History": "🕘",
            "Healthy Living": "❤️",
            "Model Information": "🤖",
            "Settings": "⚙️"
        }

        # Sync selection with current page state
        selected_index = 0
        if st.session_state.current_page in nav_options:
            selected_index = nav_options.index(st.session_state.current_page)

        page = st.radio(
            "Navigation Menu",
            nav_options,
            index=selected_index,
            format_func=lambda x: f"{nav_icons.get(x, '•')}  {x}",
            label_visibility="collapsed",
            key="app_nav_radio"
        )
        st.session_state.current_page = page

        # Sidebar Bottom Section: User Info & Logout
        user_name = user.get("full_name", user.get("username", "Clinician"))
        username = user.get("username", "")

        st.markdown(f"""
        <div class="sidebar-user-pill">
            <div class="sidebar-user-avatar">
                {user_name[0].upper() if user_name else 'U'}
            </div>
            <div style="overflow: hidden; flex-grow: 1;">
                <div style="font-weight: 700; font-size: 0.88rem; color: var(--text-primary); white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">
                    {user_name}
                </div>
                <div style="font-size: 0.74rem; color: var(--text-muted);">
                    @{username}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", use_container_width=True, key="btn_sidebar_logout"):
            auth.logout()

    # ==============================================================================
    # VIEW ROUTER (Strictly Preserved)
    # ==============================================================================
    if page == "Dashboard":
        render_dashboard(user)

    elif page == "Prediction":
        render_prediction(model, user)

    elif page == "Analytics":
        render_analytics(data, user)

    elif page == "Prediction History":
        render_history(user)

    elif page == "Healthy Living":
        render_healthy_living()

    elif page == "Model Information":
        render_model_info()

    elif page == "Settings":
        render_settings(user)