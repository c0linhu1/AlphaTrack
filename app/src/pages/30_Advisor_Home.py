import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!")
st.subheader("Financial Advisor Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### Client Overview")
    st.write("View all your clients' portfolios, performance, and risk levels.")
    if st.button("View Clients", type="primary", use_container_width=True):
        st.switch_page("pages/31_Client_Overview.py")
with col2:
    st.markdown("#### Risk & Rebalancing")
    st.write("Monitor risk profiles, get rebalancing suggestions, update thresholds.")
    if st.button("Manage Risk", type="primary", use_container_width=True):
        st.switch_page("pages/32_Risk_Rebalancing.py")
with col3:
    st.markdown("#### Client Management")
    st.write("Add new client portfolios, generate reports, manage accounts.")
    if st.button("Manage Clients", type="primary", use_container_width=True):
        st.switch_page("pages/33_Client_Management.py")