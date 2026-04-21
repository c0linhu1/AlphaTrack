import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Use a wide layout
st.set_page_config(layout='wide')

# Show sidebar navigation
SideBarLinks()

# Base API route for advisor endpoints
API_BASE = "http://web-api:4000/ad"

# Page title
st.title("Client Management")

# Advisor user id from session state
advisor_user_id = st.session_state.get('user_id', 4)

# Helper function
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


# Load client data
clients = fetch_json(f"{API_BASE}/clients/{advisor_user_id}") or []

# Deduplicate clients
seen = {}
for c in clients:
    cid = c.get("client_id")
    if cid not in seen:
        seen[cid] = c

unique_clients = list(seen.values())

# Add new client portfolio
st.subheader("Add New Client Portfolio")

with st.form("add_client_form"):
    new_portfolio_name = st.text_input(
        "Portfolio Name",
        placeholder="e.g., Growth Portfolio"
    )

    new_portfolio_value = st.number_input(
        "Initial Portfolio Value ($)",
        min_value=0.00,
        value=50000.00,
        step=1000.00
    )

    benchmark_id = st.selectbox(
        "Benchmark",
        options=[1, 2],
        format_func=lambda x: "S&P 500" if x == 1 else "NASDAQ 100"
    )

    add_submitted = st.form_submit_button("Add Portfolio", type="primary")

    if add_submitted:
        if not new_portfolio_name:
            st.error("Please enter a portfolio name.")
        else:
            payload = {
                "benchmark_id": benchmark_id,
                "portfolio_name": new_portfolio_name,
                "total_value": new_portfolio_value
            }

            try:
                post_response = requests.post(
                    f"{API_BASE}/clients/{advisor_user_id}",
                    json=payload,
                    timeout=10
                )

                if post_response.status_code in [200, 201]:
                    st.success(f"Portfolio '{new_portfolio_name}' created successfully.")
                    st.rerun()
                else:
                    st.error(
                        f"Failed to create portfolio "
                        f"(status {post_response.status_code}): {post_response.text}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Error creating portfolio: {e}")

# Generate performance report
st.divider()
st.subheader("Generate Performance Report")

if unique_clients:
    client_names = [
        c.get("name", f"Client {c.get('client_id', '?')}")
        for c in unique_clients
    ]
    client_map = {name: c for name, c in zip(client_names, unique_clients)}

    with st.form("report_form"):
        report_client = st.selectbox("Select Client:", client_names, key="report_client")
        report_type = st.selectbox("Report Type:", ["monthly", "quarterly", "annual"])
        report_summary = st.text_area(
            "Report Summary (optional):",
            placeholder="e.g., Monthly report for April 2026"
        )

        report_submitted = st.form_submit_button("Generate Report", type="primary")

        if report_submitted:
            selected = client_map[report_client]
            cid = selected.get("client_id")

            payload = {
                "report_type": report_type,
                "summary": (
                    report_summary
                    if report_summary
                    else f"{report_type.capitalize()} report for {report_client}"
                )
            }

            try:
                report_response = requests.post(
                    f"{API_BASE}/clients/{cid}/reports",
                    json=payload,
                    timeout=10
                )

                if report_response.status_code in [200, 201]:
                    st.success(f"{report_type.capitalize()} report generated for {report_client}.")
                else:
                    st.error(
                        f"Failed to generate report "
                        f"(status {report_response.status_code}): {report_response.text}"
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Error generating report: {e}")
else:
    st.info("No clients available for reporting.")

# Close client account
st.divider()
st.subheader("Close Client Account")

active_clients = [c for c in unique_clients if c.get("account_status") == "active"]

if active_clients:
    active_names = [
        c.get("name", f"Client {c.get('client_id', '?')}")
        for c in active_clients
    ]
    active_map = {name: c for name, c in zip(active_names, active_clients)}

    with st.form("close_client_form"):
        close_client = st.selectbox(
            "Select Client to Close:",
            active_names,
            key="close_client"
        )

        confirm = st.checkbox("I confirm I want to close this client's account.")

        close_submitted = st.form_submit_button("Close Account", type="primary")

        if close_submitted:
            if not confirm:
                st.warning("Please confirm before closing the account.")
            else:
                selected = active_map[close_client]
                cid = selected.get("client_id")

                try:
                    close_response = requests.put(
                        f"{API_BASE}/clients/{cid}",
                        json={"account_status": "closed"},
                        timeout=10
                    )

                    if close_response.status_code == 200:
                        st.success(f"Account for {close_client} has been closed.")
                        st.rerun()
                    else:
                        st.error(
                            f"Failed to close account "
                            f"(status {close_response.status_code}): {close_response.text}"
                        )
                except requests.exceptions.RequestException as e:
                    st.error(f"Error closing account: {e}")
else:
    st.info("No active client accounts available to close.")

# Current clients list
st.divider()
st.subheader("Current Clients")

if unique_clients:
    table_data = []
    for c in unique_clients:
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