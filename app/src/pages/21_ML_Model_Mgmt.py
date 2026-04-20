import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set the layout to wide so the page uses more screen space
st.set_page_config(layout='wide')

# Render the sidebar navigation (based on user role)
SideBarLinks()

# Page title and section header
st.title('App Administration Page')
st.write('## Model 1 Maintenance')

# Base URL for the backend API
API_BASE_URL = "http://web-api:4000"

# Button: Train Model
if st.button("Train Model 01", type='primary', use_container_width=True):
    # Eventually this should call a POST route on your backend
    st.info("Training route not yet implemented.")

# Button: Test Model
if st.button('Test Model 01', type='primary', use_container_width=True):
    # This should eventually call a test endpoint on the backend
    st.info("Testing route not yet implemented.")

# Button: Get Prediction
if st.button(
    'Model 1 - get predicted value for 10, 25',
    type='primary',
    use_container_width=True
):
    try:
        # Send a GET request to the backend API
        response = requests.get(f"{API_BASE_URL}/prediction/10/25", timeout=10)

        # Show status code so we know if the request succeeded (200) or failed (404/500)
        st.write("Status code:", response.status_code)

        # Show raw response text for debugging
        st.write("Raw response text:", response.text)

        # Raise an error if the request failed (like 404 or 500)
        response.raise_for_status()

        try:
            # Try to convert the response into JSON
            results = response.json()

            # Display the results depending on their format
            if isinstance(results, list):
                # If it's a list, show it as a table
                st.dataframe(results)
            elif isinstance(results, dict):
                # If it's a dictionary, show it as JSON
                st.json(results)
            else:
                # Fallback if it's something unexpected
                st.write(results)

        except requests.exceptions.JSONDecodeError:
            # This happens if the backend did not return valid JSON
            st.error("The API responded, but it did not return valid JSON.")

    except requests.exceptions.RequestException as e:
        # This catches connection errors, timeouts, etc.
        st.error(f"Could not connect to the API: {e}")