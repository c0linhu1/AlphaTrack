import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Manage Holdings")

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

# current holdings
holdings = requests.get(f"{API}/i/portfolios/{selected}/holdings").json()

if holdings:
    df = pd.DataFrame(holdings)
    st.write("### Holdings")
    st.dataframe(df)

# add holding
st.write("### Add")

asset_id = st.number_input("Asset ID", min_value=1, step=1)
qty = st.number_input("Quantity", min_value=0.01)
cost = st.number_input("Avg Cost", min_value=0.01)
alloc = st.number_input("Allocation %", min_value=0.0, max_value=100.0)

if st.button("Add Holding"):
    requests.post(
        f"{API}/i/portfolios/{selected}/holdings",
        json={
            "asset_id": int(asset_id),
            "quantity": float(qty),
            "avg_cost": float(cost),
            "allocation_percent": float(alloc),
            "weight": float(alloc) / 100
        }
    )
    st.rerun()

# edit holding
if holdings:
    st.write("### Edit")

    ticker_map = {h["ticker"]: h for h in holdings}
    ticker = st.selectbox("Ticker", options=list(ticker_map.keys()))

    h = ticker_map[ticker]

    new_qty = st.number_input("Quantity", value=float(h["quantity"]))
    new_cost = st.number_input("Avg Cost", value=float(h["avg_cost"]))
    new_val = st.number_input("Value", value=float(h["current_value"]))
    new_alloc = st.number_input("Allocation %", value=float(h["allocation_percent"]))

    if st.button("Update"):
        requests.put(
            f"{API}/i/holdings/{selected}/{h.get('asset_id', 0)}",
            json={
                "quantity": float(new_qty),
                "avg_cost": float(new_cost),
                "current_value": float(new_val),
                "allocation_percent": float(new_alloc)
            }
        )
        st.rerun()

    # remove holding
    st.write("### Remove")

    remove = st.selectbox("Remove Ticker", options=list(ticker_map.keys()), key="remove")

    if st.button("Delete"):
        h = ticker_map[remove]
        requests.delete(f"{API}/i/holdings/{selected}/{h.get('asset_id', 0)}")
        st.rerun()