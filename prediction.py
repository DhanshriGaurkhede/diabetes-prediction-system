"""
views/prediction.py - Patient Data Collection & ML Inference
STRICTLY PROTECTED: ML prediction logic, feature order, and probability calculations are 100% preserved.
"""

import streamlit as st
import database


def render_prediction(model, user_data: dict):
    """Render patient input form and execute untouched ML prediction engine."""
    user_id = user_data.get("id")

    st.markdown("""
    <div class="view-header">
        <div class="view-badge">Predictive Diagnostic Engine</div>
        <h1 class="view-title">🤖 Diabetes Risk Assessment</h1>
        <p class="view-subtitle">
            Enter patient physiological measurements below to compute statistical risk probabilities using our trained Machine Learning classifier.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Optional Patient Name / Case Identifier
    patient_name = st.text_input(
        "Patient Identifier / Case ID (Optional)",
        value="",
        placeholder="e.g. Case #2041 or Jane Doe",
        help="Used to label the assessment record in your history archive."
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Structured 2-Column Clinical Input Form
    col_personal, col_clinical = st.columns([1, 1])

    with col_personal:
        st.markdown("""
        <div class="form-group-card">
            <div class="form-group-title">👤 Personal & Demographic Info</div>
        """, unsafe_allow_html=True)

        age = st.number_input(
            "Age (Years)",
            min_value=1,
            max_value=120,
            value=25,
            step=1,
            help="Patient's age in completed years."
        )

        pregnancies = st.number_input(
            "Pregnancies",
            min_value=0,
            max_value=20,
            value=1,
            step=1,
            help="Total number of times pregnant."
        )

        diabetes_pedigree = st.number_input(
            "Diabetes Pedigree Function",
            min_value=0.0,
            max_value=3.0,
            value=0.5,
            step=0.01,
            format="%.3f",
            help="Genetic scoring of diabetes prevalence in direct relatives."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col_clinical:
        st.markdown("""
        <div class="form-group-card">
            <div class="form-group-title">🧪 Clinical & Laboratory Panels</div>
        """, unsafe_allow_html=True)

        glucose = st.number_input(
            "Glucose (mg/dL)",
            min_value=0,
            max_value=300,
            value=100,
            step=1,
            help="Plasma glucose concentration (2 hours in oral glucose tolerance test)."
        )

        blood_pressure = st.number_input(
            "Blood Pressure (mm Hg)",
            min_value=0,
            max_value=200,
            value=70,
            step=1,
            help="Diastolic blood pressure in mm Hg."
        )

        skin_thickness = st.number_input(
            "Skin Thickness (mm)",
            min_value=0,
            max_value=100,
            value=20,
            step=1,
            help="Triceps skin fold thickness in mm."
        )

        insulin = st.number_input(
            "Insulin (μU/mL)",
            min_value=0,
            max_value=900,
            value=80,
            step=1,
            help="2-Hour serum insulin measurement."
        )

        bmi = st.number_input(
            "BMI (Body Mass Index)",
            min_value=0.0,
            max_value=70.0,
            value=25.0,
            step=0.1,
            format="%.1f",
            help="Body Mass Index: Weight in kg / (Height in m)²"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # ==========================================================================
    # PROTECTED ML INFERENCE ENGINE
    # ==========================================================================
    if st.button("🔍 Analyze Diabetes Risk", use_container_width=True, key="btn_run_pred"):
        # EXACT 8-FEATURE ORDER PRESERVED
        patient_data = [[
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age
        ]]

        prediction = model.predict(patient_data)[0]
        probability = model.predict_proba(patient_data)[0]

        if prediction == 1:
            result = "Higher Risk"
        else:
            result = "Lower Risk"

        diabetes_prob_pct = probability[1] * 100

        # Save to SQLite database
        if user_id:
            database.add_prediction(
                user_id=user_id,
                pregnancies=pregnancies,
                glucose=glucose,
                blood_pressure=blood_pressure,
                skin_thickness=skin_thickness,
                insulin=insulin,
                bmi=bmi,
                diabetes_pedigree=diabetes_pedigree,
                age=age,
                prediction_result="Diabetes" if prediction == 1 else "No Diabetes",
                prediction_probability=round(diabetes_prob_pct, 2),
                patient_name=patient_name or "Anonymous"
            )

        # Cache in session state
        st.session_state.last_prediction = {
            "prediction": prediction,
            "result_label": "Higher Diabetes Risk Prediction" if prediction == 1 else "Lower Diabetes Risk Prediction",
            "probability": diabetes_prob_pct,
            "patient_name": patient_name or "Anonymous"
        }

    # Display Prediction Result Card
    if "last_prediction" in st.session_state and st.session_state.last_prediction is not None:
        last = st.session_state.last_prediction
        pred = last["prediction"]
        prob_val = last["probability"]
        res_label = last["result_label"]

        if pred == 1:
            st.markdown(f"""
            <div class="result-box-positive">
                <div class="result-badge-high">⚠️ Assessment Alert</div>
                <h2 class="result-title" style="color: #ef4444;">{res_label}</h2>
                <p class="result-desc" style="color: var(--pos-text);">
                    The machine learning model evaluated the provided clinical markers and identified indicators 
                    consistent with elevated diabetes risk. A clinical consultation with a healthcare provider is recommended.
                </p>
                <div class="prob-meter-container">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.95rem; color: var(--text-primary);">
                        <span>Estimated Diabetes Probability</span>
                        <span style="color: #ef4444;">{prob_val:.2f}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill-high" style="width: {min(max(prob_val, 5), 100)}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">
                        <span>0% Low Risk</span>
                        <span>50% Threshold</span>
                        <span>100% High Risk</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-box-negative">
                <div class="result-badge-low">✓ Favorable Profile</div>
                <h2 class="result-title" style="color: #10b981;">{res_label}</h2>
                <p class="result-desc" style="color: var(--neg-text);">
                    The machine learning model indicates a low statistical likelihood of diabetes based on the provided metrics. 
                    Continue maintaining healthy dietary habits, regular physical exercise, and routine preventive screenings.
                </p>
                <div class="prob-meter-container">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.95rem; color: var(--text-primary);">
                        <span>Estimated Diabetes Probability</span>
                        <span style="color: #10b981;">{prob_val:.2f}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill-low" style="width: {min(max(prob_val, 5), 100)}%;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">
                        <span>0% Low Risk</span>
                        <span>50% Threshold</span>
                        <span>100% High Risk</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Mandatory Clinical Disclaimer
    st.markdown("""
    <div class="notice-box">
        <strong>⚠️ Clinical Screening Notice:</strong> This result is an ML-based risk prediction for educational purposes and should not be treated as a medical diagnosis.
    </div>
    """, unsafe_allow_html=True)
