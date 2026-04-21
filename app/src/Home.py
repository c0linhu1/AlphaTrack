##################################################
# AlphaTrack main landing / mock login page
##################################################

import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up logging
logging.basicConfig(
    format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Use the wide layout
st.set_page_config(layout='wide')

# Visiting this page means the user is not currently logged in
st.session_state['authenticated'] = False

# Show sidebar navigation
SideBarLinks(show_home=True)

# Backend API base URL
API = "http://web-api:4000"

logger.info("Loading AlphaTrack Home page")

st.title("AlphaTrack")
st.write("#### Portfolio tracking and analytics for analysts, investors, administrators, and advisors.")
st.write("Select a user below to enter the app as that persona.")

# Load active users and their roles from the backend
try:
    response = requests.get(f"{API}/a/users/access", timeout=10)
    response.raise_for_status()
    users = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Could not load users from the backend: {e}")
    st.stop()

# Group users by role
portfolio_analysts = []
retail_investors = []
administrators = []
financial_advisors = []

for user in users:
    role_name = (user.get("role_name") or "").strip()

    entry = {
        "user_id": user["user_id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "full_name": f"{user['first_name']} {user['last_name']}"
    }

    if role_name == "Portfolio Analyst":
        portfolio_analysts.append(entry)
    elif role_name == "Retail Investor":
        retail_investors.append(entry)
    elif role_name == "System Admin":
        administrators.append(entry)
    elif role_name == "Financial Advisor":
        financial_advisors.append(entry)

# Helper function for selectbox labels
def format_user(user):
    return user["full_name"]

# Portfolio Analyst login
selected_analyst = st.selectbox(
    "Portfolio Analyst",
    options=portfolio_analysts,
    format_func=format_user,
    index=None,
    placeholder="Select a portfolio analyst"
)

if st.button(
    "Log in as Portfolio Analyst",
    type="primary",
    use_container_width=True
):
    if selected_analyst is None:
        st.warning("Please select a portfolio analyst first.")
    else:
        st.session_state["authenticated"] = True
        st.session_state["role"] = "portfolio_analyst"
        st.session_state["first_name"] = selected_analyst["first_name"]
        st.session_state["user_id"] = selected_analyst["user_id"]
        logger.info("Logging in as Portfolio Analyst")
        st.switch_page("pages/00_Analyst_Home.py")

# Retail Investor login
selected_investor = st.selectbox(
    "Retail Investor",
    options=retail_investors,
    format_func=format_user,
    index=None,
    placeholder="Select a retail investor"
)

if st.button(
    "Log in as Retail Investor",
    type="primary",
    use_container_width=True
):
    if selected_investor is None:
        st.warning("Please select a retail investor first.")
    else:
        st.session_state["authenticated"] = True
        st.session_state["role"] = "retail_investor"
        st.session_state["first_name"] = selected_investor["first_name"]
        st.session_state["user_id"] = selected_investor["user_id"]
        logger.info("Logging in as Retail Investor")
        st.switch_page("pages/10_Investor_Home.py")

# System Administrator login
selected_admin = st.selectbox(
    "System Administrator",
    options=administrators,
    format_func=format_user,
    index=None,
    placeholder="Select a system administrator"
)

if st.button(
    "Log in as System Administrator",
    type="primary",
    use_container_width=True
):
    if selected_admin is None:
        st.warning("Please select a system administrator first.")
    else:
        st.session_state["authenticated"] = True
        st.session_state["role"] = "administrator"
        st.session_state["first_name"] = selected_admin["first_name"]
        st.session_state["user_id"] = selected_admin["user_id"]
        logger.info("Logging in as System Administrator")
        st.switch_page("pages/20_Admin_Home.py")

# Financial Advisor login
selected_advisor = st.selectbox(
    "Financial Advisor",
    options=financial_advisors,
    format_func=format_user,
    index=None,
    placeholder="Select a financial advisor"
)

if st.button(
    "Log in as Financial Advisor",
    type="primary",
    use_container_width=True
):
    if selected_advisor is None:
        st.warning("Please select a financial advisor first.")
    else:
        st.session_state["authenticated"] = True
        st.session_state["role"] = "financial_advisor"
        st.session_state["first_name"] = selected_advisor["first_name"]
        st.session_state["user_id"] = selected_advisor["user_id"]
        logger.info("Logging in as Financial Advisor")
        st.switch_page("pages/30_Advisor_Home.py")