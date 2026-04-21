import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Use a wide layout for a cleaner dashboard view
st.set_page_config(layout='wide')

# Show the sidebar links for this role
SideBarLinks()

# Get the current user's first name from session state
advisor_name = st.session_state.get("first_name", "Advisor")

# Page header
st.title(f"Welcome, {advisor_name}!")
st.subheader("Financial Advisor Dashboard")

st.write(
    "Use this workspace to review client portfolios, monitor risk thresholds, "
    "generate reports, and manage client accounts."
)

# Create three columns for the three main advisor tools
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Client Overview")
    st.write(
        "View all client portfolios, account status, performance, and risk information."
    )
    if st.button("View Clients", type="primary", use_container_width=True):
        st.switch_page("pages/31_Client_Overview.py")

with col2:
    st.markdown("#### Risk & Rebalancing")
    st.write(
        "Review client risk profiles, update thresholds, and check rebalancing suggestions."
    )
    if st.button("Manage Risk", type="primary", use_container_width=True):
        st.switch_page("pages/32_Risk_Rebalancing.py")

with col3:
    st.markdown("#### Client Management")
    st.write(
        "Add new portfolios, generate reports, and close outdated client accounts."
    )
    if st.button("Manage Clients", type="primary", use_container_width=True):
        st.switch_page("pages/33_Client_Management.py")

st.divider()

st.write("### Advisor Responsibilities")
st.markdown("""
- Review all client portfolios in one place  
- Monitor client risk levels and threshold breaches  
- Generate client-ready performance reports  
- Add new client portfolios  
- Close outdated or inactive client accounts  
""")