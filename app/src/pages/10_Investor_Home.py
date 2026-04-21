import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Investor')}!")
st.write("### Retail Investor Dashboard")
st.write("Use the sidebar to navigate to your tools:")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📉 **Portfolio Dashboard** — View your total portfolio value, daily changes, and performance over time.")

with col2:
    st.info("📋 **Holdings & Performance** — See all your holdings with returns and compare stock performance.")

with col3:
    st.info("✏️ **Manage Holdings** — Add new stocks, edit existing positions, or remove holdings you've sold.")