import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Correlation & Watchlists")

API = "http://web-api:4000"
user_id = st.session_state.get("user_id", 1)

# get portfolios
portfolios = requests.get(f"{API}/p/portfolios/{user_id}").json()
names = {p["portfolio_id"]: p["portfolio_name"] for p in portfolios}

selected = st.selectbox(
    "Portfolio",
    options=list(names.keys()),
    format_func=lambda x: names[x]
)

# correlation
st.write("### Correlation")

data = requests.get(f"{API}/p/portfolios/{selected}/correlation").json()

if data:
    df = pd.DataFrame(data)
    pivot = df.pivot_table(index="date", columns="ticker", values="closing_price")

    st.dataframe(pivot)

    if len(pivot.columns) > 1:
        corr = pivot.corr()
        st.write("#### Matrix")
        st.dataframe(corr)

# watchlists
st.write("### Watchlists")

watchlists = requests.get(f"{API}/p/watchlists/{user_id}").json()

if watchlists:
    for wl in watchlists:
        st.write(f"{wl['watchlist_name']}: {wl.get('tickers', 'None')}")

# create watchlist
name = st.text_input("New Watchlist Name")

if st.button("Create"):
    if name:
        requests.post(
            f"{API}/p/watchlists/{user_id}",
            json={"watchlist_name": name}
        )
        st.rerun()