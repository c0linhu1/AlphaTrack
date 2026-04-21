import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Use a wide layout so tables and forms fit better
st.set_page_config(layout='wide')

# Show sidebar navigation
SideBarLinks()

# Base URL for the backend API
API_BASE_URL = "http://web-api:4000"

# Page header
st.title('Access Control & Admin Operations')
st.write(
    "Use this page to manage users, roles, and permissions. "
    "This page is connected to the real admin routes in the backend API."
)

# Helper function for GET requests
def get_data(endpoint):
    """
    Send a GET request to the backend and return parsed JSON if successful.
    If something goes wrong, show an error message and return None.
    """
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load data from {endpoint}: {e}")
        return None


# View all users
st.write("## Current Users")

if st.button("Load All Users", type='primary', use_container_width=True):
    users = get_data("/a/users")
    if users is not None:
        st.dataframe(users, use_container_width=True)


# View all roles
st.write("## Current Roles")

if st.button("Load All Roles", type='primary', use_container_width=True):
    roles = get_data("/a/roles")
    if roles is not None:
        st.dataframe(roles, use_container_width=True)


# Create a new user
st.write("## Create a New User")

with st.form("create_user_form"):
    # Basic user details required by the backend
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")

    create_user_submitted = st.form_submit_button("Create User")

    if create_user_submitted:
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/a/users",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            st.success("User created successfully.")
            st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Could not create user: {e}")


# Create a new role
st.write("## Create a New Role")

with st.form("create_role_form"):
    # Role name is required and description is optional
    role_name = st.text_input("Role Name")
    role_description = st.text_input("Role Description")

    create_role_submitted = st.form_submit_button("Create Role")

    if create_role_submitted:
        payload = {
            "role_name": role_name,
            "role_description": role_description
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/a/roles",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            st.success("Role created successfully.")
            st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Could not create role: {e}")


# Update a user's role
st.write("## Update a User's Role")

with st.form("update_role_form"):
    # The backend route expects a user_id in the path and a role_id in the JSON body
    user_id_for_role_update = st.number_input("User ID", min_value=1, step=1)
    new_role_id = st.number_input("New Role ID", min_value=1, step=1)

    update_role_submitted = st.form_submit_button("Update User Role")

    if update_role_submitted:
        payload = {
            "role_id": int(new_role_id)
        }

        try:
            response = requests.put(
                f"{API_BASE_URL}/a/users/{int(user_id_for_role_update)}/roles",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            st.success("User role updated successfully.")
            st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Could not update user role: {e}")


# Deactivate a user
st.write("## Deactivate a User")

with st.form("deactivate_user_form"):
    # This route marks the user as inactive
    user_id_to_deactivate = st.number_input("User ID to Deactivate", min_value=1, step=1)

    deactivate_user_submitted = st.form_submit_button("Deactivate User")

    if deactivate_user_submitted:
        try:
            response = requests.put(
                f"{API_BASE_URL}/a/users/{int(user_id_to_deactivate)}",
                timeout=10
            )
            response.raise_for_status()
            st.success("User deactivated successfully.")
            st.json(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Could not deactivate user: {e}")