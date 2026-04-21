import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Portfolio Dashboard")

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

portfolio = next(p for p in portfolios if p["portfolio_id"] == selected)

# summary
col1, col2, col3 = st.columns(3)
col1.metric("Total Value", f"${float(portfolio.get('total_value', 0)):,.2f}")
col2.metric("Performance", f"{float(portfolio.get('performance_metric', 0)) * 100:.2f}%")
col3.metric("Benchmark", portfolio.get("benchmark_name", "N/A"))

# holdings
st.write("### Holdings")

holdings = requests.get(f"{API}/i/portfolios/{selected}/holdings").json()

if holdings:
    df = pd.DataFrame(holdings)
    st.dataframe(df)
    
    top = df[["ticker", "current_value"]].sort_values("current_value", ascending=False).head(10)
    st.bar_chart(top.set_index("ticker"))

# performance
st.write("### Performance")

perf = requests.get(f"{API}/i/portfolios/{selected}/performance").json()

if perf:
    df = pd.DataFrame(perf)
    st.line_chart(df.set_index("date")["portfolio_value"])
    st.bar_chart(df.set_index("date")["gain_loss"])