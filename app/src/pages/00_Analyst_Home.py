import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Analyst')}!")
st.write("### Portfolio Analyst Dashboard")
st.write("Use the sidebar to navigate to your tools:")

col1, col2 = st.columns(2)

with col1:
    st.info("📊 **Risk Dashboard** — View Sharpe ratio, volatility, max drawdown, and benchmark comparisons for any portfolio.")

with col2:
    st.info("🧩 **Correlation & Watchlists** — Analyze asset correlations and manage your custom watchlists.")