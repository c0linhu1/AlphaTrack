import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Holdings & Performance")

API = "http://web-api:4000"
user_id = st.session_state.get("user_id", 2)

# get portfolios
portfolios = requests.get(f"{API}/p/portfolios/{user_id}").json()

if not portfolios:
    st.warning("No portfolios found.")
    st.stop()

names = {p["portfolio_id"]: p["portfolio_name"] for p in portfolios}

selected = st.selectbox(
    "Portfolio",
    options=list(names.keys()),
    format_func=lambda x: names[x]
)

# holdings
holdings = requests.get(f"{API}/i/portfolios/{selected}/holdings").json()

if holdings:
    df = pd.DataFrame(holdings)

    st.write("### Holdings")
    st.dataframe(df)

    # Compare stocks
    st.write("### Compare")

    tickers = df["ticker"].tolist()
    selected_tickers = st.multiselect("Stocks", tickers, default=tickers[:3])

    if selected_tickers:
        comp = df[df["ticker"].isin(selected_tickers)]

        col1, col2 = st.columns(2)
        col1.bar_chart(comp.set_index("ticker")["pct_return"])
        col2.bar_chart(comp.set_index("ticker")["current_value"])

# performance
st.write("### Performance")

perf = requests.get(f"{API}/i/portfolios/{selected}/performance").json()

if perf:
    df = pd.DataFrame(perf)
    st.dataframe(df)