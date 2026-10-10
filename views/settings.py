"""
views/settings.py - User Settings, Preferences & Security Management
"""

import streamlit as st
import database
import auth


def render_settings(user_data: dict):
    """Render profile management, theme selection, security settings, and app info."""
    user_id = user_data.get("id")
    if not user_id:
        st.warning("Please sign in to access settings.")
        return

    st.markdown("""
    <div class="view-header">
        <div class="view-badge">System Preferences</div>
        <h1 class="view-title">⚙️ Application Settings & Profile</h1>
        <p class="view-subtitle">
            Customize display preferences, update your personal clinician profile, and manage account security.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_profile, tab_theme, tab_security, tab_about = st.tabs([
        "👤 Profile", "🎨 Theme & Appearance", "🔒 Security", "ℹ️ About DiabetesCare AI"
    ])

    # 1. Profile Tab
    with tab_profile:
        st.markdown("<h4 style='color: var(--text-primary); margin-top: 0.5rem;'>Clinician Profile</h4>", unsafe_allow_html=True)
        st.caption("Update your display name and contact email for this account.")

        current_name = user_data.get("full_name", "")
        current_email = user_data.get("email", "")
        username = user_data.get("username", "")

        st.text_input("Username", value=username, disabled=True, help="Username is permanently assigned to your account.")
        new_name = st.text_input("Full Name", value=current_name)
        new_email = st.text_input("Contact Email", value=current_email)

        if st.button("Save Profile Updates", key="btn_save_prof"):
            if not new_name.strip():
                st.error("Full name cannot be empty.")
            else:
                ok = database.update_user_profile(user_id, new_name, new_email)
                if ok:
                    st.session_state.user["full_name"] = new_name.strip()
                    st.session_state.user["email"] = new_email.strip()
                    st.success("Profile updated successfully!")
                else:
                    st.error("Could not update profile (email might already be taken).")

    # 2. Theme Tab
    with tab_theme:
        st.markdown("<h4 style='color: var(--text-primary); margin-top: 0.5rem;'>Theme Configuration</h4>", unsafe_allow_html=True)
        st.caption("Switch between clean Clinical Light Mode and High-Contrast Dark Mode.")

        current_theme = st.session_state.get("theme", "light")
        theme_choice = st.radio(
            "Interface Color Theme",
            ["Light Mode (Clinical White & Slate)", "Dark Mode (Navy & Cyan Accent)"],
            index=0 if current_theme == "light" else 1
        )

        selected_theme = "light" if "Light Mode" in theme_choice else "dark"

        if selected_theme != current_theme:
            st.session_state.theme = selected_theme
            database.update_user_theme(user_id, selected_theme)
            st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        notif_toggle = st.toggle("Enable In-App Clinical Notifications", value=True)
        if notif_toggle:
            st.caption("Active: High-priority risk assessment alerts will be highlighted in tables.")

    # 3. Security Tab
    with tab_security:
        st.markdown("<h4 style='color: var(--text-primary); margin-top: 0.5rem;'>Account Security & Password</h4>", unsafe_allow_html=True)
        st.caption("Update your login password. Your password is encrypted with PBKDF2-HMAC-SHA256 salted hashing.")

        old_pwd = st.text_input("Current Password", type="password", key="s_old_pwd")
        new_pwd = st.text_input("New Password (min 6 characters)", type="password", key="s_new_pwd")
        confirm_pwd = st.text_input("Confirm New Password", type="password", key="s_conf_pwd")

        if st.button("Change Password", key="btn_change_pwd"):
            user_db = database.get_user_by_id(user_id)
            if not user_db or not auth.verify_password(user_db["password_hash"], old_pwd):
                st.error("Current password is incorrect.")
            elif len(new_pwd) < 6:
                st.error("New password must be at least 6 characters.")
            elif new_pwd != confirm_pwd:
                st.error("New passwords do not match.")
            else:
                new_hash = auth.hash_password(new_pwd)
                database.update_user_password(user_id, new_hash)
                st.success("Password changed successfully!")

    # 4. About Tab
    with tab_about:
        st.markdown("<h4 style='color: var(--text-primary); margin-top: 0.5rem;'>System Specifications</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🩺 DiabetesCare AI v2.0</div>
            <p class="clinical-card-body">
                • <strong>Core ML Classifier:</strong> Scikit-Learn Logistic Regression (max_iter=1000)<br>
                • <strong>Training Dataset:</strong> Pima Indians Diabetes Dataset (768 patient records)<br>
                • <strong>Model Accuracy:</strong> 77.27% on independent test data<br>
                • <strong>Database Architecture:</strong> SQLite3 with user account isolation and WAL logging<br>
                • <strong>Security Architecture:</strong> PBKDF2-HMAC-SHA256 cryptography<br>
                • <strong>Frontend:</strong> Streamlit Multi-Component Modular Architecture
            </p>
        </div>
        """, unsafe_allow_html=True)
