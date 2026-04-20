import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()
API_BASE = "http://web-api:4000/ad"
st.title("Client Portfolio Overview")
advisor_user_id = st.session_state.get('user_id', 4)

try:
    response = requests.get(f"{API_BASE}/clients/{advisor_user_id}")
    clients = response.json() if response.status_code == 200 else []
except Exception as e:
    clients = []
    st.error(f"Could not connect to API: {e}")

if not clients:
    st.info("No clients found.")
    st.stop()

st.subheader("All Clients")
table_data = []
for client in clients:
    row = {
        "Client Name": client.get("name", "N/A"),
        "Status": client.get("account_status", "N/A"),
        "Risk Tolerance": client.get("risk_tolerance", "N/A"),
    }
    if client.get("portfolio_name"):
        row["Portfolio"] = client["portfolio_name"]
    if client.get("total_value") is not None:
        row["Total Value"] = f"${float(client['total_value']):,.2f}"
    if client.get("risk_level"):
        row["Risk Level"] = client["risk_level"]
    table_data.append(row)
st.dataframe(table_data, use_container_width=True)

st.divider()
st.subheader("Client Detail View")

seen = {}
for c in clients:
    cid = c.get("client_id")
    if cid not in seen:
        seen[cid] = c
unique_clients = list(seen.values())
client_names = [c.get("name", f"Client {c.get('client_id', '?')}") for c in unique_clients]
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
        try:
            rp_resp = requests.get(f"{API_BASE}/clients/{client_id}/risk-profile")
            if rp_resp.status_code == 200:
                rp_data = rp_resp.json()
                rp = rp_data[0] if isinstance(rp_data, list) and len(rp_data) > 0 else None
                if rp:
                    st.write(f"**Risk Level:** {rp.get('risk_level', 'N/A')}")
                    st.write(f"**Threshold Min:** {rp.get('threshold_min', 'N/A')}")
                    st.write(f"**Threshold Max:** {rp.get('threshold_max', 'N/A')}")
                else:
                    st.info("No risk profile data.")
            else:
                st.warning("Could not load risk profile.")
        except Exception as e:
            st.error(f"Error: {e}")

    if sel.get("total_value") is not None:
        st.markdown("#### Portfolio Summary")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric("Portfolio", sel.get("portfolio_name", "N/A"))
        with p2:
            st.metric("Total Value", f"${float(sel.get('total_value', 0)):,.2f}")
        with p3:
            perf = sel.get("performance_metric")
            st.metric("Performance", f"{perf}" if perf else "N/A")