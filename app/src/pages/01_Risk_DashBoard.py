import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Risk Dashboard")
st.write(f"### Hi, {st.session_state['first_name']}.")

API = "http://web-api:4000"
user_id = st.session_state.get("user_id", 1)

# get portfolios
portfolios = requests.get(f"{API}/p/portfolios/{user_id}").json()
names = {p["portfolio_id"]: p["portfolio_name"] for p in portfolios}
selected = st.selectbox("Portfolio", options=list(names.keys()), format_func=lambda x: names[x])

if selected is None:
    st.stop()

# show risk metrics
metrics = requests.get(f"{API}/p/portfolios/{selected}/risk-metrics").json()
if metrics:
    m = metrics[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Sharpe Ratio", m["sharpe_ratio"])
    col2.metric("Volatility", f"{float(m['volatility']) * 100:.1f}%")
    col3.metric("Max Drawdown", f"{float(m['max_drawdown']) * 100:.1f}%")

    st.dataframe(pd.DataFrame(metrics))