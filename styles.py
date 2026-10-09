"""
styles.py - Unified Design System & Theme Engine for DiabetesCare AI
Provides clean, accessible, production-grade clinical styles for Light and Dark modes.
"""

import streamlit as st


def get_theme_css(theme: str = "light") -> str:
    """Generate CSS variables and component styles tailored to the active theme."""
    is_dark = theme.lower() == "dark"

    if is_dark:
        vars_css = """
        :root {
            --bg-page: #0a0f1d;
            --bg-surface: #111a2e;
            --bg-surface-hover: #16223b;
            --bg-surface-subtle: #0d1527;
            --bg-header: #111a2e;
            --border-subtle: #1e2d4a;
            --border-medium: #2a3d63;
            --border-focus: #0284c7;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --text-inverse: #0f172a;
            --accent-primary: #0284c7;
            --accent-primary-hover: #0369a1;
            --accent-teal: #0d9488;
            --accent-teal-light: #14b8a6;
            --pos-bg: #271217;
            --pos-border: #ef4444;
            --pos-text: #fca5a5;
            --pos-badge: #dc2626;
            --neg-bg: #0b291e;
            --neg-border: #10b981;
            --neg-text: #6ee7b7;
            --neg-badge: #059669;
            --notice-bg: #1e1e24;
            --notice-border: #f59e0b;
            --notice-text: #fbbf24;
            --shadow-card: 0 4px 12px rgba(0, 0, 0, 0.35);
            --shadow-card-hover: 0 8px 24px rgba(0, 0, 0, 0.45);
            --sidebar-bg: #0d1527;
            --sidebar-nav-hover-bg: #15223c;
            --sidebar-nav-active-bg: #172a4c;
            --sidebar-nav-active-border: #234173;
            --sidebar-nav-active-text: #38bdf8;
            --sidebar-user-bg: #111a2e;
            --sidebar-user-border: #1e2d4a;
        }
        """
    else:
        vars_css = """
        :root {
            --bg-page: #f8fafc;
            --bg-surface: #ffffff;
            --bg-surface-hover: #f1f5f9;
            --bg-surface-subtle: #f8fafc;
            --bg-header: #ffffff;
            --border-subtle: #e2e8f0;
            --border-medium: #cbd5e1;
            --border-focus: #0284c7;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --text-inverse: #ffffff;
            --accent-primary: #0284c7;
            --accent-primary-hover: #0369a1;
            --accent-teal: #0d9488;
            --accent-teal-light: #0f766e;
            --pos-bg: #fef2f2;
            --pos-border: #ef4444;
            --pos-text: #991b1b;
            --pos-badge: #dc2626;
            --neg-bg: #f0fdf4;
            --neg-border: #10b981;
            --neg-text: #065f46;
            --neg-badge: #059669;
            --notice-bg: #fffbeb;
            --notice-border: #f59e0b;
            --notice-text: #92400e;
            --shadow-card: 0 2px 8px rgba(15, 23, 42, 0.05);
            --shadow-card-hover: 0 6px 16px rgba(15, 23, 42, 0.08);
            --sidebar-bg: #f8fafc;
            --sidebar-nav-hover-bg: #f1f5f9;
            --sidebar-nav-active-bg: #e0f2fe;
            --sidebar-nav-active-border: #bae6fd;
            --sidebar-nav-active-text: #0284c7;
            --sidebar-user-bg: #ffffff;
            --sidebar-user-border: #e2e8f0;
        }
        """

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    {vars_css}

    /* Global Typography & Reset */
    html, body, [class*="css"], .stMarkdown, .stText {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}

    .stApp {{
        background-color: var(--bg-page);
        color: var(--text-primary);
    }}

    /* Container Spacing */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1180px !important;
    }}

    /* Main Page Header Banner */
    .view-header {{
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-left: 5px solid var(--accent-primary);
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-card);
    }}
    .view-badge {{
        display: inline-block;
        background-color: var(--bg-surface-subtle);
        border: 1px solid var(--border-medium);
        color: var(--accent-primary);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 3px 10px;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }}
    .view-title {{
        font-size: 1.7rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.25;
        letter-spacing: -0.3px;
    }}
    .view-subtitle {{
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
        margin-bottom: 0;
        line-height: 1.5;
    }}

    /* Section Titles */
    .section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 1.2rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Clinical Cards */
    .clinical-card {{
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-card);
        transition: all 0.2s ease;
    }}
    .clinical-card:hover {{
        border-color: var(--border-focus);
        box-shadow: var(--shadow-card-hover);
        transform: translateY(-1px);
    }}
    .clinical-card-title {{
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .clinical-card-body {{
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin: 0;
    }}

    /* KPI Metric Cards */
    .metric-card {{
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.2rem 1.1rem;
        box-shadow: var(--shadow-card);
        text-align: center;
        transition: all 0.2s ease;
    }}
    .metric-card:hover {{
        border-color: var(--accent-primary);
        box-shadow: var(--shadow-card-hover);
    }}
    .metric-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
    }}
    .metric-value {{
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0.15rem 0;
        letter-spacing: -0.5px;
    }}
    .metric-label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* Result Card Styles */
    .result-box-positive {{
        background-color: var(--pos-bg);
        border: 2px solid var(--pos-border);
        border-radius: 14px;
        padding: 1.6rem;
        text-align: center;
        margin-top: 1.2rem;
        box-shadow: var(--shadow-card);
    }}
    .result-box-negative {{
        background-color: var(--neg-bg);
        border: 2px solid var(--neg-border);
        border-radius: 14px;
        padding: 1.6rem;
        text-align: center;
        margin-top: 1.2rem;
        box-shadow: var(--shadow-card);
    }}
    .result-badge-high {{
        display: inline-block;
        background-color: var(--pos-badge);
        color: #ffffff !important;
        padding: 5px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        margin-bottom: 0.6rem;
    }}
    .result-badge-low {{
        display: inline-block;
        background-color: var(--neg-badge);
        color: #ffffff !important;
        padding: 5px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        margin-bottom: 0.6rem;
    }}
    .result-title {{
        font-size: 1.35rem;
        font-weight: 800;
        margin: 0.3rem 0;
    }}
    .result-desc {{
        font-size: 0.92rem;
        max-width: 620px;
        margin: 0 auto 1rem auto;
        line-height: 1.5;
    }}
    .prob-meter-container {{
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 1rem 1.4rem;
        max-width: 520px;
        margin: 0.8rem auto 0 auto;
    }}
    .prob-bar-track {{
        background-color: var(--border-subtle);
        height: 12px;
        border-radius: 6px;
        overflow: hidden;
        margin: 0.6rem 0 0.3rem 0;
    }}
    .prob-bar-fill-high {{
        height: 100%;
        background-color: var(--pos-border);
        border-radius: 6px;
        transition: width 0.5s ease;
    }}
    .prob-bar-fill-low {{
        height: 100%;
        background-color: var(--neg-border);
        border-radius: 6px;
        transition: width 0.5s ease;
    }}

    /* Clinical Disclaimer Box */
    .notice-box {{
        background-color: var(--notice-bg);
        border-left: 4px solid var(--notice-border);
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        margin-top: 1.2rem;
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }}

    /* ==========================================================================
       MODERN HEALTHCARE SAAS SIDEBAR NAVIGATION
       ========================================================================== */
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding: 1rem 0.85rem 1.2rem 0.85rem !important;
    }}
    [data-testid="stSidebar"] .block-container {{
        padding: 0 !important;
    }}

    /* Hide standard circular radio input button */
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"] > div:first-child {{
        display: none !important;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] input[type="radio"] {{
        display: none !important;
    }}

    /* Clean vertical stack */
    [data-testid="stSidebar"] [role="radiogroup"] {{
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    /* Navigation item row */
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"] {{
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 10px 14px !important;
        min-height: 42px !important;
        border-radius: 9px !important;
        margin: 0 !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
        background-color: transparent !important;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-sizing: border-box !important;
    }}

    /* Nav Item Typography */
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"] p,
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"] span,
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"] div {{
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        letter-spacing: -0.1px !important;
        line-height: 1.3 !important;
        transition: color 0.15s ease !important;
    }}

    /* Hover State */
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"]:hover {{
        background-color: var(--sidebar-nav-hover-bg) !important;
        border-color: var(--border-subtle) !important;
        transform: translateX(3px) !important;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"]:hover p,
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"]:hover span {{
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    /* Active / Selected Page Indicator */
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"]:has(input:checked),
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"][aria-checked="true"] {{
        background-color: var(--sidebar-nav-active-bg) !important;
        border: 1px solid var(--sidebar-nav-active-border) !important;
        border-left: 4px solid var(--accent-primary) !important;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.14) !important;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"]:has(input:checked) p,
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"]:has(input:checked) span,
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"][aria-checked="true"] p,
    [data-testid="stSidebar"] [role="radiogroup"] [data-baseweb="radio"][aria-checked="true"] span {{
        color: var(--sidebar-nav-active-text) !important;
        font-weight: 700 !important;
    }}

    /* Sidebar User Profile Card */
    .sidebar-user-pill {{
        background-color: var(--sidebar-user-bg);
        border: 1px solid var(--sidebar-user-border);
        border-radius: 11px;
        padding: 0.75rem 0.9rem;
        margin-top: 1.8rem;
        margin-bottom: 0.7rem;
        box-shadow: var(--shadow-card);
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.2s ease;
    }}
    .sidebar-user-avatar {{
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-primary-hover) 100%);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.92rem;
        box-shadow: 0 2px 5px rgba(2, 132, 199, 0.3);
        flex-shrink: 0;
    }}

    /* Sidebar Logout Button */
    [data-testid="stSidebar"] div.stButton > button {{
        background: transparent !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 1rem !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: all 0.18s ease !important;
    }}
    [data-testid="stSidebar"] div.stButton > button:hover {{
        background-color: #fee2e2 !important;
        border-color: #fca5a5 !important;
        color: #b91c1c !important;
        transform: translateY(-1px) !important;
    }}

    /* Custom Form Card Containers */
    .form-group-card {{
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-card);
    }}
    .form-group-title {{
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-primary);
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.9rem;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 0.4rem;
    }}

    /* Streamlit Primary Button (Main Views) */
    .stApp > div:not([data-testid="stSidebar"]) div.stButton > button:first-child,
    .block-container div.stButton > button:first-child {{
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-primary-hover) 100%) !important;
        color: #ffffff !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.5rem !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
        transition: all 0.2s ease !important;
    }}
    .stApp > div:not([data-testid="stSidebar"]) div.stButton > button:first-child:hover,
    .block-container div.stButton > button:first-child:hover {{
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35) !important;
        transform: translateY(-1px) !important;
        color: #ffffff !important;
    }}
    </style>
    """


def apply_theme():
    """Inject active theme CSS variables into the application."""
    theme = st.session_state.get("theme", "light")
    st.markdown(get_theme_css(theme), unsafe_allow_html=True)
