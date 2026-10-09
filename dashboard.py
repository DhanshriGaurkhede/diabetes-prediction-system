"""
views/dashboard.py - Professional Clinical AI Dashboard
Displays personalized welcome, KPI metrics, quick actions, recent predictions, and model overview.
"""

import streamlit as st
import pandas as pd
import database


def render_dashboard(user_data: dict):
    """Render the primary dashboard for authenticated clinical users."""
    full_name = user_data.get("full_name", "Clinician")
    user_id = user_data.get("id")

    # Fetch personalized stats from SQLite
    user_stats = database.get_user_stats(user_id) if user_id else {"total": 0, "diabetes_count": 0, "no_diabetes_count": 0}
    recent_records = database.get_user_history(user_id)[:5] if user_id else []

    # 1. Welcome Header Banner
    st.markdown(f"""
    <div class="view-header">
        <div class="view-badge">Intelligent Clinical Intelligence</div>
        <h1 class="view-title">Welcome back, {full_name}</h1>
        <p class="view-subtitle">
            DiabetesCare AI combines physiological indicators and statistical machine learning 
            to estimate diabetes risk probability for screening awareness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. KPI Cards Row
    st.markdown('<div class="section-title">📊 Key Performance & Assessment Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📝</div>
            <div class="metric-value">{user_stats['total']}</div>
            <div class="metric-label">Total Predictions</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🔴</div>
            <div class="metric-value" style="color: #ef4444;">{user_stats['diabetes_count']}</div>
            <div class="metric-label">Higher Risk Cases</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🟢</div>
            <div class="metric-value" style="color: #10b981;">{user_stats['no_diabetes_count']}</div>
            <div class="metric-label">Lower Risk Cases</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-value" style="color: #0284c7;">86.36%</div>
            <div class="metric-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3. Quick Action Buttons
    st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("🤖 Start New Prediction", use_container_width=True, key="qa_pred"):
            st.session_state.current_page = "🤖 Prediction"
            st.rerun()

    with q2:
        if st.button("📋 View Prediction History", use_container_width=True, key="qa_hist"):
            st.session_state.current_page = "📋 Prediction History"
            st.rerun()

    with q3:
        if st.button("📊 Explore Analytics", use_container_width=True, key="qa_ana"):
            st.session_state.current_page = "📊 Analytics"
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 4. Recent Predictions Activity
    st.markdown('<div class="section-title">🕒 Recent Prediction Activity</div>', unsafe_allow_html=True)

    if not recent_records:
        st.markdown("""
        <div class="clinical-card" style="text-align: center; padding: 2rem 1rem;">
            <p style="color: var(--text-muted); margin: 0; font-size: 0.92rem;">
                No assessments recorded yet in your account. Click <strong>Start New Prediction</strong> above to evaluate patient data.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        recent_df = pd.DataFrame(recent_records)[["patient_name", "prediction_result", "prediction_probability", "created_at"]]
        recent_df = recent_df.rename(columns={
            "patient_name": "Patient",
            "prediction_result": "Assessment Result",
            "prediction_probability": "Diabetes Probability (%)",
            "created_at": "Timestamp"
        })
        st.dataframe(recent_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 5. Information Section: Model & Dataset Architecture
    st.markdown('<div class="section-title">ℹ️ System Architecture & Dataset Specifications</div>', unsafe_allow_html=True)
    info1, info2 = st.columns(2)

    with info1:
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🧪 Model Specifications</div>
            <p class="clinical-card-body">
                • <strong>Algorithm:</strong> Scikit-Learn Random Forest (Selected)<br>
                • <strong>Clinical Inputs:</strong> 8 physiological markers (Glucose, Insulin, BMI, etc.)<br>
                • <strong>Validation Split:</strong> 80% Training (614 rows), 20% Testing (154 rows)<br>
                • <strong>Evaluation Accuracy:</strong> 86.36% on unseen test records
            </p>
        </div>
        """, unsafe_allow_html=True)

    with info2:
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">📁 Training Dataset Overview</div>
            <p class="clinical-card-body">
                • <strong>Dataset:</strong> Pima Indians Diabetes Diagnostic Dataset<br>
                • <strong>Total Records:</strong> 768 patient clinical profiles<br>
                • <strong>Outcome Balance:</strong> 500 Non-Diabetic (65.1%) / 268 Diabetic (34.9%)<br>
                • <strong>Storage Engine:</strong> SQLite3 with user data isolation
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Clinical Disclaimer
    st.markdown("""
    <div class="notice-box">
        <strong>⚠️ Clinical Screening Notice:</strong> DiabetesCare AI predictions are generated for educational, 
        screening awareness, and research demonstration. They do not constitute a formal medical diagnosis. 
        Always consult a licensed medical professional for clinical decision-making.
    </div>
    """, unsafe_allow_html=True)
