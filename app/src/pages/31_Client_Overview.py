import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Use a wide layout for tables and metrics
st.set_page_config(layout='wide')

# Show sidebar navigation
SideBarLinks()

# Base API route for advisor endpoints
API_BASE = "http://web-api:4000/ad"

# Page title
st.title("Client Portfolio Overview")

# Use the advisor's user_id from session state
advisor_user_id = st.session_state.get('user_id', 4)

# Helper function
def fetch_json(url):
    """
    Send a GET request and return JSON if successful.
    If the request fails, show an error and return None.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")
        return None


# Load client data
clients = fetch_json(f"{API_BASE}/clients/{advisor_user_id}")

if not clients:
    st.info("No clients found.")
    st.stop()

# Remove duplicate client entries caused by multiple portfolios
seen = {}
for client in clients:
    cid = client.get("client_id")
    if cid not in seen:
        seen[cid] = client

unique_clients = list(seen.values())

# All clients table
st.subheader("All Clients")

table_data = []
for client in clients:
    row = {
        "Client Name": client.get("name", "N/A"),
        "Status": client.get("account_status", "N/A"),
        "Risk Tolerance": client.get("risk_tolerance", "N/A"),
        "Risk Level": client.get("risk_level", "N/A")
    }

    if client.get("portfolio_name"):
        row["Portfolio"] = client["portfolio_name"]

    if client.get("total_value") is not None:
        row["Total Value"] = f"${float(client['total_value']):,.2f}"

    if client.get("performance_metric") is not None:
        row["Performance"] = client["performance_metric"]

    table_data.append(row)

st.dataframe(table_data, use_container_width=True)

# Quick alerts
st.divider()
st.subheader("Advisor Alerts")

alerts_found = False

for client in unique_clients:
    name = client.get("name", "Unknown Client")
    performance = client.get("performance_metric")
    risk_level = client.get("risk_level")

    # Simple demo-friendly warning rules
    if performance is not None and float(performance) < 0:
        st.warning(f"{name} has negative recent performance and may need review.")
        alerts_found = True

    if risk_level is None:
        st.warning(f"{name} does not currently have a complete risk profile.")
        alerts_found = True

if not alerts_found:
    st.success("No major portfolio alerts found at this time.")

# ---------------------------------------------------
# Client detail view
# ---------------------------------------------------
st.divider()
st.subheader("Client Detail View")

client_names = [
    c.get("name", f"Client {c.get('client_id', '?')}")
    for c in unique_clients
]
client_map = {name: c for name, c in zip(client_names, unique_clients)}

selected_name = st.selectbox("Select a client:", client_names)

if selected_name:
    sel = client_map[selected_name]
    client_id = sel.get("client_id")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Client Info")
        st.write(f"**Name:** {sel.get('name', 'N/A')}")
        st.write(f"**Email:** {sel.get('email', 'N/A')}")
        st.write(f"**Status:** {sel.get('account_status', 'N/A')}")
        st.write(f"**Risk Tolerance:** {sel.get('risk_tolerance', 'N/A')}")

    with col2:
        st.markdown("#### Risk Profile")

        rp_data = fetch_json(f"{API_BASE}/clients/{client_id}/risk-profile")

        if isinstance(rp_data, list) and len(rp_data) > 0:
            rp = rp_data[0]
            st.write(f"**Risk Level:** {rp.get('risk_level', 'N/A')}")
            st.write(f"**Threshold Min:** {rp.get('threshold_min', 'N/A')}")
            st.write(f"**Threshold Max:** {rp.get('threshold_max', 'N/A')}")
        else:
            st.info("No risk profile data found.")

    st.markdown("#### Portfolio Summary")
    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric("Portfolio", sel.get("portfolio_name", "N/A"))

    with p2:
        total_value = sel.get("total_value")
        st.metric(
            "Total Value",
            f"${float(total_value):,.2f}" if total_value is not None else "N/A"
        )

    with p3:
        perf = sel.get("performance_metric")
        st.metric("Performance", f"{perf}" if perf is not None else "N/A")