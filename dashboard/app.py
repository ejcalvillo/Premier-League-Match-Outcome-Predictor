"""
Premier League Match Outcome Predictor
Main Streamlit Application
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import from project root
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Page configuration
st.set_page_config(
    page_title="Premier League Match Outcome Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #1f77b4;
        text-align: center;
        padding: 0.75rem 0 0.25rem 0;
    }
    .app-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.25rem;
    }
    .sub-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2d2d2d;
        margin-bottom: 0.75rem;
    }
    .metric-card {
        background-color: #f8f9fb;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 0.6rem;
        margin: 0.5rem 0;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fb;
        border: 1px solid #e5e7eb;
        border-radius: 0.6rem;
        padding: 0.9rem 1rem;
    }
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }
    .footer-note {
        text-align: center;
        color: #9ca3af;
        font-size: 0.85rem;
        padding: 0.75rem 0 0.25rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">Premier League Match Outcome Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Random Forest predictions from historical Premier League match data</div>',
    unsafe_allow_html=True
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Match Predictor", "Model Performance"],
    label_visibility="collapsed",
)
st.sidebar.caption("Match Predictor forecasts upcoming fixtures. Model Performance reports held-out accuracy.")

# Import page modules
try:
    if page == "Match Predictor":
        from views import predictor
        predictor.show()
    elif page == "Model Performance":
        from views import performance
        performance.show()
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer-note">Premier League Match Outcome Predictor</div>',
    unsafe_allow_html=True
)
