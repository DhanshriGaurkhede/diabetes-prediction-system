"""
views/analytics.py - User-Isolated Prediction Analytics & Clinical Intelligence
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import database


def render_analytics(dataset: pd.DataFrame, user_data: dict):
    """Render user-specific prediction charts and dataset distribution analytics."""
    user_id = user_data.get("id")
    if not user_id:
        st.warning("Please sign in to view analytics.")
        return

    st.markdown("""
    <div class="view-header">
        <div class="view-badge">Clinical Analytics Dashboard</div>
        <h1 class="view-title">📊 Assessment Trends & Data Analytics</h1>
        <p class="view-subtitle">
            Visual breakdown of your historical patient risk assessments and benchmark dataset characteristics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch user records
    user_records = database.get_user_history(user_id)
    user_stats = database.get_user_stats(user_id)

    # 1. Summary KPI Row
    st.markdown('<div class="section-title">📈 Your Assessment Summary</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📑</div>
            <div class="metric-value">{user_stats['total']}</div>
            <div class="metric-label">Assessments Run</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🔴</div>
            <div class="metric-value" style="color: #ef4444;">{user_stats['diabetes_count']}</div>
            <div class="metric-label">Higher Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🟢</div>
            <div class="metric-value" style="color: #10b981;">{user_stats['no_diabetes_count']}</div>
            <div class="metric-label">Lower Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        avg_prob = user_stats.get("avg_probability", 0.0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value" style="color: #0284c7;">{avg_prob:.1f}%</div>
            <div class="metric-label">Avg Probability</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 2. Charts Section
    if user_records:
        df_user = pd.DataFrame(user_records)
        df_user["created_at"] = pd.to_datetime(df_user["created_at"])

        c_col1, c_col2 = st.columns(2)

        # Chart 1: User Outcome Distribution
        with c_col1:
            st.markdown('<div class="section-title">🥧 Your Assessment Distribution</div>', unsafe_allow_html=True)
            outcome_counts = df_user["prediction_result"].value_counts()

            fig1, ax1 = plt.subplots(figsize=(5, 3.5), dpi=120)
            colors = ["#10b981" if label == "No Diabetes" else "#ef4444" for label in outcome_counts.index]
            
            wedges, texts, autotexts = ax1.pie(
                outcome_counts.values,
                labels=outcome_counts.index,
                autopct='%1.1f%%',
                colors=colors,
                startangle=140,
                wedgeprops=dict(width=0.45, edgecolor='#0f172a', linewidth=0.5)
            )
            for t in texts:
                t.set_fontsize(10)
                t.set_fontweight('bold')
            for at in autotexts:
                at.set_fontsize(9)
                at.set_color('white')
                at.set_fontweight('bold')

            fig1.patch.set_facecolor('none')
            ax1.set_facecolor('none')
            plt.tight_layout()
            st.pyplot(fig1)

        # Chart 2: Probability Timeline / Trend
        with c_col2:
            st.markdown('<div class="section-title">📈 Risk Probability Trend</div>', unsafe_allow_html=True)
            df_sorted = df_user.sort_values("created_at")

            fig2, ax2 = plt.subplots(figsize=(5.5, 3.5), dpi=120)
            ax2.plot(range(1, len(df_sorted) + 1), df_sorted["prediction_probability"], marker='o', color="#0284c7", linewidth=2, markersize=6)
            ax2.axhline(50, color='#ef4444', linestyle='--', alpha=0.7, label='50% Threshold')
            ax2.set_xlabel("Assessment Sequence", fontsize=9, fontweight="bold", color="#64748b")
            ax2.set_ylabel("Risk Probability (%)", fontsize=9, fontweight="bold", color="#64748b")
            ax2.set_ylim(0, 105)
            ax2.grid(True, linestyle=':', alpha=0.4)
            ax2.legend(loc='upper right', fontsize=8)

            for spine in ['top', 'right', 'left', 'bottom']:
                ax2.spines[spine].set_color('#cbd5e1')

            fig2.patch.set_facecolor('none')
            ax2.set_facecolor('#f8fafc')
            plt.tight_layout()
            st.pyplot(fig2)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 3. Benchmark Dataset Distribution
    st.markdown('<div class="section-title">🏛️ Population Training Dataset Reference (768 Records)</div>', unsafe_allow_html=True)
    d_col1, d_col2 = st.columns([3, 2])

    with d_col1:
        ds_counts = dataset["Outcome"].value_counts().sort_index()
        fig3, ax3 = plt.subplots(figsize=(6, 3.2), dpi=120)
        bars = ax3.bar(["No Diabetes (0)", "Diabetes (1)"], ds_counts.values, color=["#0284c7", "#ef4444"], width=0.45, edgecolor="#0f172a", linewidth=0.5)
        ax3.set_ylabel("Number of Patients", fontsize=9, fontweight="bold", color="#64748b")
        ax3.grid(axis='y', linestyle='--', alpha=0.3)
        ax3.set_axisbelow(True)

        for bar in bars:
            h = bar.get_height()
            ax3.annotate(f"{int(h)} ({h/len(dataset)*100:.1f}%)",
                         xy=(bar.get_x() + bar.get_width()/2, h),
                         xytext=(0, 3), textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, fontweight='bold', color="#0f172a")

        for spine in ['top', 'right', 'left', 'bottom']:
            ax3.spines[spine].set_color('#cbd5e1')

        fig3.patch.set_facecolor('none')
        ax3.set_facecolor('#f8fafc')
        plt.tight_layout()
        st.pyplot(fig3)

    with d_col2:
        st.markdown(f"""
        <div class="clinical-card" style="margin-top: 10px;">
            <div class="clinical-card-title">🔬 Clinical Dataset Insights</div>
            <p class="clinical-card-body">
                • <strong>Total Records:</strong> {len(dataset)} verified profiles<br>
                • <strong>Negative Cases (0):</strong> 500 patients (65.1%)<br>
                • <strong>Positive Cases (1):</strong> 268 patients (34.9%)<br><br>
                Our Logistic Regression algorithm is trained against this balanced distribution to deliver generalizable risk probabilities.
            </p>
        </div>
        """, unsafe_allow_html=True)
