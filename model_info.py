"""
views/model_info.py - Machine Learning Model Architecture & Performance Evaluation
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def render_model_info():
    """Render technical performance metrics, confusion matrix, and model explanation."""
    st.markdown("""
    <div class="view-header">
        <div class="view-badge">Predictive ML Architecture</div>
        <h1 class="view-title">📈 Model Performance & Evaluation</h1>
        <p class="view-subtitle">
            Comprehensive evaluation metrics, model comparison benchmarks, and confusion matrix breakdown for the selected Random Forest classifier.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Model Comparison Benchmarks
    st.markdown('<div class="section-title">🏆 Model Evaluation & Selection Benchmarks</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)

    with b1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📉</div>
            <div class="metric-value" style="color: #64748b;">70.78%</div>
            <div class="metric-label">Logistic Regression</div>
        </div>
        """, unsafe_allow_html=True)

    with b2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🌲</div>
            <div class="metric-value" style="color: #0d9488;">82.47%</div>
            <div class="metric-label">Decision Tree</div>
        </div>
        """, unsafe_allow_html=True)

    with b3:
        st.markdown("""
        <div class="metric-card" style="border: 2px solid #0284c7; background-color: var(--bg-surface);">
            <div class="metric-icon">⭐</div>
            <div class="metric-value" style="color: #0284c7;">86.36%</div>
            <div class="metric-label">Random Forest (Selected)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 2. Key Performance Indicators (Random Forest)
    st.markdown('<div class="section-title">🎯 Random Forest Benchmark Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-value" style="color: #0284c7;">86.36%</div>
            <div class="metric-label">Overall Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🔬</div>
            <div class="metric-value" style="color: #0d9488;">85.0%</div>
            <div class="metric-label">Macro Precision</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📡</div>
            <div class="metric-value" style="color: #6366f1;">85.0%</div>
            <div class="metric-label">Macro Recall</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">⚖️</div>
            <div class="metric-value" style="color: #8b5cf6;">85.0%</div>
            <div class="metric-label">Macro F1-Score</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 3. Confusion Matrix & Classification Report Layout
    cm_col, cr_col = st.columns([1, 1])

    with cm_col:
        st.markdown('<div class="section-title">🔲 Random Forest Confusion Matrix</div>', unsafe_allow_html=True)

        cm = [[90, 10],
              [11, 43]]

        fig, ax = plt.subplots(figsize=(5.2, 4.2), dpi=120)
        cax = ax.imshow(cm, cmap="Blues", interpolation='nearest')

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["No Diabetes (0)", "Diabetes (1)"], fontsize=9, fontweight="bold", color="#334155")
        ax.set_yticklabels(["No Diabetes (0)", "Diabetes (1)"], fontsize=9, fontweight="bold", color="#334155")

        ax.set_xlabel("Predicted Class", fontsize=10, fontweight="bold", color="#0f172a", labelpad=8)
        ax.set_ylabel("Actual Ground Truth", fontsize=10, fontweight="bold", color="#0f172a", labelpad=8)
        ax.set_title("Test Sample Confusion Matrix (154 Cases)", fontsize=11, fontweight="bold", color="#0f172a", pad=10)

        # Annotations (TN=90, FP=10, FN=11, TP=43)
        for i in range(2):
            for j in range(2):
                val = cm[i][j]
                text_color = "white" if val > 45 else "#0f172a"
                ax.text(
                    j, i, f"{val}",
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=12,
                    fontweight="bold"
                )

        fig.patch.set_facecolor('none')
        ax.set_facecolor('#f8fafc')
        plt.tight_layout()
        st.pyplot(fig)

    with cr_col:
        st.markdown('<div class="section-title">📋 Detailed Classification Report</div>', unsafe_allow_html=True)

        report_data = {
            "Class": [
                "No Diabetes (Class 0)",
                "Diabetes (Class 1)",
                "Accuracy",
                "Macro Avg",
                "Weighted Avg"
            ],
            "Precision": ["0.89", "0.81", "-", "0.85", "0.86"],
            "Recall": ["0.90", "0.80", "-", "0.85", "0.86"],
            "F1-Score": ["0.90", "0.80", "0.86", "0.85", "0.86"],
            "Support": ["100", "54", "154", "154", "154"]
        }

        st.dataframe(pd.DataFrame(report_data), use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="clinical-card" style="margin-top: 15px;">
            <div class="clinical-card-title">💡 Metric Definitions</div>
            <p class="clinical-card-body">
                • <strong>Precision (81–89%):</strong> Proportion of positive predictions that were clinically accurate.<br>
                • <strong>Recall (80–90%):</strong> Proportion of actual cases correctly identified by the model.<br>
                • <strong>F1-Score (80–90%):</strong> Harmonic mean balancing precision and recall across classes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 4. Beginner-Friendly Explanation Cards
    st.markdown('<div class="section-title">🤖 How the Model Works (Beginner-Friendly Guide)</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)

    with e1:
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🧠 Random Forest in Plain Terms</div>
            <p class="clinical-card-body">
                Random Forest is an ensemble learning method that constructs a multitude of individual 
                decision trees during training. Each tree votes on the patient's risk classification based 
                on clinical features (such as Glucose, BMI, and Insulin), and the forest outputs the aggregated 
                majority vote and continuous class probability to minimize prediction error.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🔬 Dataset & Validation Protocol</div>
            <p class="clinical-card-body">
                • <strong>Dataset:</strong> 768 verified clinical patient profiles.<br>
                • <strong>Features:</strong> 8 diagnostic markers.<br>
                • <strong>80/20 Split:</strong> 614 profiles were used to train the models, while 154 unseen profiles were kept for validation.<br>
                • <strong>Benchmark:</strong> Random Forest achieved the highest test accuracy of 86.36%, outperforming Decision Tree (82.47%) and Logistic Regression (70.78%).
            </p>
        </div>
        """, unsafe_allow_html=True)
