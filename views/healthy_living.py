"""
views/healthy_living.py - Preventative Wellness & Diabetes Education Cards
"""

import streamlit as st


def render_healthy_living():
    """Render clinical lifestyle cards and wellness recommendations."""
    st.markdown("""
    <div class="view-header">
        <div class="view-badge">Preventative Wellness Guidance</div>
        <h1 class="view-title">🌱 Healthy Living & Diabetes Awareness</h1>
        <p class="view-subtitle">
            Evidence-informed lifestyle pillars and proactive health recommendations to support long-term metabolic health.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🥗 Balanced Nutrition</div>
            <p class="clinical-card-body">
                Emphasize whole, minimally processed foods such as non-starchy vegetables, 
                legumes, whole grains, and lean proteins. Reduce refined carbohydrates and 
                sugar-sweetened beverages to maintain steady glycemic control.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">💧 Optimal Daily Hydration</div>
            <p class="clinical-card-body">
                Drink adequate water throughout the day (approximately 2–3 liters). Proper hydration 
                supports cardiovascular circulation and assists renal filtration in eliminating excess glucose.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🩺 Regular Health Checkups</div>
            <p class="clinical-card-body">
                Schedule routine screenings including Fasting Blood Glucose (FBG), HbA1c tests, 
                blood pressure checks, and lipid panels. Early detection is pivotal in preventing complication onset.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">🏃 Regular Physical Activity</div>
            <p class="clinical-card-body">
                Strive for at least 150 minutes of moderate aerobic exercise per week 
                (such as brisk walking or swimming) paired with resistance training to improve insulin receptor sensitivity.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">😴 Quality Sleep & Recovery</div>
            <p class="clinical-card-body">
                Target 7 to 9 hours of uninterrupted sleep each night. Consistent sleep deprivation 
                and elevated chronic stress stimulate cortisol release, which can induce insulin resistance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="clinical-card">
            <div class="clinical-card-title">💙 Diabetes Management & Awareness</div>
            <p class="clinical-card-body">
                If you have been diagnosed with prediabetes or diabetes, follow your primary physician's 
                treatment recommendations, monitor blood sugar levels when advised, and stay informed on health trends.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Mandatory Medical Notice
    st.markdown("""
    <div class="notice-box">
        <strong>⚠️ Medical Disclaimer:</strong> The wellness advice above is for educational awareness and lifestyle enrichment only. 
        It does not replace individualized clinical diagnosis, medication adjustments, or therapy plans prescribed by your healthcare provider.
    </div>
    """, unsafe_allow_html=True)
