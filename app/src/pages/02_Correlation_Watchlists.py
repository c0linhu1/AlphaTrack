import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Correlation & Watchlists")

# Base URL for the backend API
API = "http://web-api:4000"

# Use the logged-in user's ID, and fall back to Bobby's sample ID if needed
user_id = st.session_state.get("user_id", 1)

# Load the user's portfolios
try:
    portfolio_response = requests.get(f"{API}/p/portfolios/{user_id}", timeout=10)
    portfolio_response.raise_for_status()
    portfolios = portfolio_response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Could not load portfolios: {e}")
    st.stop()

if not portfolios:
    st.info("No portfolios were found for this user.")
    st.stop()

names = {p["portfolio_id"]: p["portfolio_name"] for p in portfolios}

selected = st.selectbox(
    "Portfolio",
    options=list(names.keys()),
    format_func=lambda x: names[x]
)

# Correlation section
st.write("### Correlation")

try:
    correlation_response = requests.get(
        f"{API}/p/portfolios/{selected}/correlation",
        timeout=10
    )
    correlation_response.raise_for_status()
    data = correlation_response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Could not load correlation data: {e}")
    data = []

if data:
    df = pd.DataFrame(data)

    # Convert fields to the right data types so pandas can build the pivot table
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["closing_price"] = pd.to_numeric(df["closing_price"], errors="coerce")

    # Drop rows missing the fields needed for the correlation view
    df = df.dropna(subset=["date", "ticker", "closing_price"])

    if df.empty:
        st.info("No valid price history was available for this portfolio.")
    else:
        # Build a date-by-ticker price table. We use the first value because each
        # date/ticker pair should represent a single closing price.
        pivot = df.pivot_table(
            index="date",
            columns="ticker",
            values="closing_price",
            aggfunc="first"
        ).sort_index()

        st.write("#### Price History")
        st.dataframe(pivot)

        if len(pivot.columns) > 1:
            corr = pivot.corr()
            st.write("#### Correlation Matrix")
            st.dataframe(corr)
        else:
            st.info("At least two assets are needed to calculate correlations.")
else:
    st.info("No correlation data was returned for this portfolio.")

# Watchlists section
st.write("### Watchlists")

try:
    watchlist_response = requests.get(f"{API}/p/watchlists/{user_id}", timeout=10)
    watchlist_response.raise_for_status()
    watchlists = watchlist_response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Could not load watchlists: {e}")
    watchlists = []

if watchlists:
    for wl in watchlists:
        st.write(f"{wl['watchlist_name']}: {wl.get('tickers', 'None')}")
else:
    st.info("No watchlists found yet.")

# Create a new watchlist
name = st.text_input("New Watchlist Name")

if st.button("Create"):
    if not name.strip():
        st.warning("Please enter a watchlist name.")
    else:
        try:
            create_response = requests.post(
                f"{API}/p/watchlists/{user_id}",
                json={"watchlist_name": name.strip()},
                timeout=10
            )
            create_response.raise_for_status()
            st.success("Watchlist created successfully.")
            st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Could not create watchlist: {e}")