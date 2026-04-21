import streamlit as st
from modules.nav import SideBarLinks

# Use wide layout for better readability
st.set_page_config(layout='wide')

# Render sidebar navigation
SideBarLinks()

# ---------------------------------------------------
# Page Title
# ---------------------------------------------------
st.title("About AlphaTrack")

st.write(
    "AlphaTrack is a portfolio tracking and analytics platform designed to bring "
    "institution-level insights to everyday investors and financial professionals."
)

# What the app does
st.subheader("What AlphaTrack Does")

st.markdown("""
AlphaTrack allows users to:

- Track and manage investment portfolios in one place  
- Monitor performance, risk levels, and asset allocations  
- Generate reports and insights for better decision-making  
- Perform system-level management such as user roles, backups, and data validation  
""")

# Personas
st.subheader("User Roles in AlphaTrack")

st.markdown("""
This application is built around four key user roles, each with different responsibilities:
""")

# Use columns for clean layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### System Administrator (Gregory)")
    st.write(
        "Manages system-level operations including user accounts, roles, backups, "
        "and data validation to ensure platform reliability and security."
    )

    st.markdown("#### Financial Advisor (James)")
    st.write(
        "Oversees multiple client portfolios, monitors risk profiles, generates reports, "
        "and provides rebalancing insights to improve performance."
    )

with col2:
    st.markdown("#### Portfolio Analyst (Bobby)")
    st.write(
        "Analyzes portfolio performance, compares against benchmarks, and evaluates "
        "risk metrics to support investment decision-making."
    )

    st.markdown("#### Retail Investor (Mike)")
    st.write(
        "Tracks personal investments, monitors gains and losses, and compares assets "
        "to make informed financial decisions."
    )

# Tech Stack
st.subheader("Technology Stack")

st.markdown("""
- **Frontend:** Streamlit  
- **Backend:** Flask (REST API with Blueprints)  
- **Database:** MySQL  
- **Infrastructure:** Docker (multi-container setup)  
""")

# Closing
st.divider()

st.write(
    "AlphaTrack demonstrates how a full-stack application can integrate data management, "
    "analytics, and user-specific workflows into a unified platform."
)

# Button to return to home
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")