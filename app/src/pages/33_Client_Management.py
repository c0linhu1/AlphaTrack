import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()
API_BASE = "http://web-api:4000/ad"
st.title("Client Management")
advisor_user_id = st.session_state.get('user_id', 4)

try:
    response = requests.get(f"{API_BASE}/clients/{advisor_user_id}")
    clients = response.json() if response.status_code == 200 else []
except Exception as e:
    clients = []
    st.error(f"Could not connect to API: {e}")

# Add New Client Portfolio (POST)
st.subheader("Add New Client Portfolio")
with st.form("add_client_form"):
    new_portfolio_name = st.text_input("Portfolio Name", placeholder="e.g., Growth Portfolio")
    new_portfolio_value = st.number_input("Initial Portfolio Value ($)", min_value=0.00, value=50000.00, step=1000.00)
    benchmark_id = st.selectbox("Benchmark", options=[1, 2], format_func=lambda x: "S&P 500" if x == 1 else "NASDAQ 100")
    add_submitted = st.form_submit_button("Add Portfolio", type="primary")
    if add_submitted:
        if not new_portfolio_name:
            st.error("Please enter a portfolio name.")
        else:
            payload = {"benchmark_id": benchmark_id, "portfolio_name": new_portfolio_name, "total_value": new_portfolio_value}
            try:
                post_response = requests.post(f"{API_BASE}/clients/{advisor_user_id}", json=payload)
                if post_response.status_code in [200, 201]:
                    st.success(f"Portfolio '{new_portfolio_name}' created!")
                    st.rerun()
                else:
                    st.error(f"Failed (status {post_response.status_code}): {post_response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# Generate Performance Report (POST)
st.divider()
st.subheader("Generate Performance Report")
if clients:
    seen = {}
    for c in clients:
        cid = c.get("client_id")
        if cid not in seen:
            seen[cid] = c
    unique_clients = list(seen.values())
    client_names = [c.get("name", f"Client {c.get('client_id', '?')}") for c in unique_clients]
    client_map = {name: c for name, c in zip(client_names, unique_clients)}

    with st.form("report_form"):
        report_client = st.selectbox("Select Client:", client_names, key="report_client")
        report_type = st.selectbox("Report Type:", ["monthly", "quarterly", "annual"])
        report_summary = st.text_area("Report Summary (optional):", placeholder="e.g., Monthly report for April 2026")
        report_submitted = st.form_submit_button("Generate Report", type="primary")
        if report_submitted:
            selected = client_map[report_client]
            cid = selected.get("client_id")
            payload = {"report_type": report_type, "summary": report_summary if report_summary else f"{report_type.capitalize()} report for {report_client}"}
            try:
                report_response = requests.post(f"{API_BASE}/clients/{cid}/reports", json=payload)
                if report_response.status_code in [200, 201]:
                    st.success(f"{report_type.capitalize()} report generated for {report_client}!")
                else:
                    st.error(f"Failed (status {report_response.status_code}): {report_response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("No clients available.")

# Close Client Account (PUT)
st.divider()
st.subheader("Close Client Account")
if clients:
    seen2 = {}
    for c in clients:
        cid = c.get("client_id")
        if cid not in seen2:
            seen2[cid] = c
    unique2 = list(seen2.values())
    active_clients = [c for c in unique2 if c.get("account_status") == "active"]
    if active_clients:
        active_names = [c.get("name", f"Client {c.get('client_id', '?')}") for c in active_clients]
        active_map = {name: c for name, c in zip(active_names, active_clients)}
        with st.form("close_client_form"):
            close_client = st.selectbox("Select Client to Close:", active_names, key="close_client")
            confirm = st.checkbox("I confirm I want to close this client's account.")
            close_submitted = st.form_submit_button("Close Account", type="primary")
            if close_submitted:
                if not confirm:
                    st.warning("Please confirm before closing.")
                else:
                    selected = active_map[close_client]
                    cid = selected.get("client_id")
                    try:
                        close_response = requests.put(f"{API_BASE}/clients/{cid}", json={"account_status": "closed"})
                        if close_response.status_code == 200:
                            st.success(f"Account for {close_client} has been closed.")
                            st.rerun()
                        else:
                            st.error(f"Failed (status {close_response.status_code}): {close_response.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
    else:
        st.info("No active client accounts to close.")

# Current Clients List
st.divider()
st.subheader("Current Clients")
if clients:
    seen3 = {}
    for c in clients:
        cid = c.get("client_id")
        if cid not in seen3:
            seen3[cid] = c
    unique3 = list(seen3.values())
    table_data = []
    for c in unique3:
        table_data.append({
            "Client ID": c.get("client_id", "N/A"),
            "Name": c.get("name", "N/A"),
            "Email": c.get("email", "N/A"),
            "Status": c.get("account_status", "N/A"),
            "Risk Tolerance": c.get("risk_tolerance", "N/A"),
        })
    st.dataframe(table_data, use_container_width=True)
else:
    st.info("No clients found.")