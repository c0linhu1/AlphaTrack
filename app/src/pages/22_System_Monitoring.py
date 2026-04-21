import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Use a wide layout so tables have enough space
st.set_page_config(layout='wide')

# Show sidebar navigation
SideBarLinks()

# Base URL for the backend API
API_BASE_URL = "http://web-api:4000"

# Page header
st.title("System Monitoring & Recovery")
st.write(
    "Use this page to monitor activity logs, manage backups, and "
    "recalculate portfolio totals when data needs to be validated."
)

# Helper function for GET requests
def get_data(endpoint):
    """
    Send a GET request to the backend and return JSON if successful.
    Show an error in the UI if the request fails.
    """
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load data from {endpoint}: {e}")
        return None


# Activity logs
st.write("## Activity Logs")
st.write("View recent system events and user activity.")

if st.button("Load Activity Logs", type="primary", use_container_width=True):
    logs = get_data("/a/activity-logs")
    if logs is not None:
        st.dataframe(logs, use_container_width=True)


# Backups
st.write("## Existing Backups")
st.write("View all current backups stored in the system.")

if st.button("Load Backups", type="primary", use_container_width=True):
    backups = get_data("/a/backups")
    if backups is not None:
        st.dataframe(backups, use_container_width=True)


# Create a backup
st.write("## Create a New Backup")

with st.form("create_backup_form"):
    backup_name = st.text_input("Backup Name")
    storage_location = st.text_input("Storage Location")
    backup_size_gb = st.number_input("Backup Size (GB)", min_value=0.0, step=0.1)

    create_backup_submitted = st.form_submit_button("Create Backup")

    if create_backup_submitted:
        payload = {
            "backup_name": backup_name,
            "storage_location": storage_location,
            "backup_size_gb": backup_size_gb
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/a/backups",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            st.success("Backup created successfully.")
            st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Could not create backup: {e}")


# Delete a backup
st.write("## Delete a Backup")

with st.form("delete_backup_form"):
    backup_id_to_delete = st.number_input("Backup ID to Delete", min_value=1, step=1)
    confirm_delete_backup = st.checkbox("I understand this backup will be removed.")

    delete_backup_submitted = st.form_submit_button("Delete Backup")

    if delete_backup_submitted:
        if not confirm_delete_backup:
            st.warning("Please confirm that you want to delete this backup.")
        else:
            try:
                response = requests.delete(
                    f"{API_BASE_URL}/a/backups/{int(backup_id_to_delete)}",
                    timeout=10
                )
                response.raise_for_status()
                st.success("Backup deleted successfully.")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Could not delete backup: {e}")


# Portfolio validation
st.write("## Recalculate Portfolio Total Value")
st.write(
    "Use this tool to recalculate a portfolio's total value based on its current holdings."
)

with st.form("recalculate_portfolio_form"):
    portfolio_id = st.number_input("Portfolio ID", min_value=1, step=1)

    recalculate_submitted = st.form_submit_button("Recalculate Portfolio Total")

    if recalculate_submitted:
        try:
            response = requests.put(
                f"{API_BASE_URL}/a/portfolios/{int(portfolio_id)}/validation",
                timeout=10
            )
            response.raise_for_status()
            st.success("Portfolio total recalculated successfully.")
            st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Could not recalculate portfolio total: {e}")