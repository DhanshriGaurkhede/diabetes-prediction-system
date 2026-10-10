"""
views/history.py - Patient Prediction Archive & Record Management
"""

import streamlit as st
import pandas as pd
import database


def render_history(user_data: dict):
    """Render the user-specific historical assessment archive."""
    user_id = user_data.get("id")
    if not user_id:
        st.warning("Please sign in to access your assessment history.")
        return

    st.markdown("""
    <div class="view-header">
        <div class="view-badge">Archived Clinical Evaluations</div>
        <h1 class="view-title">📋 Patient Prediction History</h1>
        <p class="view-subtitle">
            Search, filter, and inspect previously calculated diabetes risk evaluations associated with your account.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Search and Filter Toolbar
    f1, f2 = st.columns([2, 1])
    with f1:
        search_query = st.text_input("🔍 Search by Patient / Case ID", placeholder="Search records...", key="h_search")
    with f2:
        outcome_filter = st.selectbox("Outcome Filter", ["All", "Diabetes", "No Diabetes"], key="h_filter")

    # Fetch user records
    records = database.get_user_history(user_id, search_query=search_query, outcome_filter=outcome_filter)

    if not records:
        st.markdown("""
        <div class="clinical-card" style="text-align: center; padding: 2.5rem 1.5rem;">
            <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">📁</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary);">No Matching Records Found</div>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.3rem;">
                Perform patient assessments in the <strong>🤖 Prediction</strong> tab to populate this archive.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # History Stats Banner
        total_rec = len(records)
        diab_count = sum(1 for r in records if r["prediction_result"] == "Diabetes")
        no_diab_count = total_rec - diab_count

        st.markdown('<div class="section-title">📊 Filtered Archive Metrics</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📑</div>
                <div class="metric-value">{total_rec}</div>
                <div class="metric-label">Matching Cases</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🔴</div>
                <div class="metric-value" style="color: #ef4444;">{diab_count}</div>
                <div class="metric-label">Higher Risk</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🟢</div>
                <div class="metric-value" style="color: #10b981;">{no_diab_count}</div>
                <div class="metric-label">Lower Risk</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # DataFrame Formatting
        df_raw = pd.DataFrame(records)
        display_cols = [
            "patient_name", "glucose", "blood_pressure", "bmi", "age",
            "prediction_result", "prediction_probability", "created_at"
        ]
        rename_cols = {
            "patient_name": "Patient / Case ID",
            "glucose": "Glucose (mg/dL)",
            "blood_pressure": "BP (mm Hg)",
            "bmi": "BMI",
            "age": "Age",
            "prediction_result": "Result",
            "prediction_probability": "Probability (%)",
            "created_at": "Timestamp"
        }

        existing_cols = [c for c in display_cols if c in df_raw.columns]
        df_clean = df_raw[existing_cols].rename(columns=rename_cols)

        st.markdown('<div class="section-title">📋 Clinical Record Details</div>', unsafe_allow_html=True)
        st.dataframe(df_clean, use_container_width=True, hide_index=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Actions Toolbar: Export CSV & Clear History
        act_col1, act_col2, _ = st.columns([1.5, 1.5, 3])

        with act_col1:
            csv_data = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export to CSV",
                data=csv_data,
                file_name="diabetes_prediction_history.csv",
                mime="text/csv",
                use_container_width=True
            )

        with act_col2:
            if st.button("🗑️ Clear My History", use_container_width=True):
                database.clear_user_history(user_id)
                st.success("History successfully cleared.")
                st.rerun()
