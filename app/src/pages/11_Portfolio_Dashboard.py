import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Portfolio Dashboard")

API = "http://web-api:4000"
user_id = st.session_state.get("user_id", 2)

# Helper function for safe GET requests
def fetch_json(url):
    """
    Send a GET request and return JSON if successful.
    Show an error and return None if the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")
        return None


# Load portfolios for the current user
portfolios = fetch_json(f"{API}/p/portfolios/{user_id}")

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

# Safely handle possibly missing numeric values
total_value = portfolio.get("total_value")
safe_total_value = float(total_value) if total_value is not None else 0.0

performance_metric = portfolio.get("performance_metric")
safe_performance_metric = float(performance_metric) if performance_metric is not None else 0.0

benchmark_name = portfolio.get("benchmark_name", "N/A")

# Portfolio summary
col1, col2, col3 = st.columns(3)
col1.metric("Total Value", f"${safe_total_value:,.2f}")
col2.metric("Performance", f"{safe_performance_metric * 100:.2f}%")
col3.metric("Benchmark", benchmark_name)

# Holdings section
st.write("### Holdings")

holdings = fetch_json(f"{API}/i/portfolios/{selected}/holdings")

if holdings:
    df = pd.DataFrame(holdings)
    st.dataframe(df, use_container_width=True)

    # Only build the bar chart if the expected columns exist
    if "ticker" in df.columns and "current_value" in df.columns:
        top = df[["ticker", "current_value"]].sort_values(
            "current_value",
            ascending=False
        ).head(10)
        st.bar_chart(top.set_index("ticker"))
else:
    st.info("No holdings found for this portfolio.")

# Performance history section
st.write("### Performance")

perf = fetch_json(f"{API}/i/portfolios/{selected}/performance")

if perf:
    df = pd.DataFrame(perf)

    if "date" in df.columns and "portfolio_value" in df.columns:
        st.line_chart(df.set_index("date")["portfolio_value"])

    if "date" in df.columns and "gain_loss" in df.columns:
        st.bar_chart(df.set_index("date")["gain_loss"])
else:
    st.info("No performance history found for this portfolio.")