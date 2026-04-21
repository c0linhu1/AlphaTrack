
# AlphaTrack main landing / mock login page


import logging
import streamlit as st
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

# Page content
logger.info("Loading AlphaTrack Home page")

st.title("AlphaTrack")
st.write("#### Portfolio tracking and analytics for analysts, investors, administrators, and advisors.")
st.write("Select a sample user below to enter the app as that persona.")


# Portfolio Analyst login
portfolio_analyst_user = st.selectbox(
    "Portfolio Analyst",
    options=["Bobby James"],
    index=None,
    placeholder="Select a portfolio analyst"
)
 
if st.button(
    "Log in as Portfolio Analyst",
    type="primary",
    use_container_width=True
):
    if portfolio_analyst_user is None:
        st.warning("Please select a portfolio analyst first.")
    else:
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'portfolio_analyst'
        st.session_state['first_name'] = 'Bobby'
        st.session_state['user_id'] = 1
        logger.info("Logging in as Portfolio Analyst")
        st.switch_page('pages/00_Analyst_Home.py')
 
 
# Retail Investor login
retail_investor_user = st.selectbox(
    "Retail Investor",
    options=["Mike Gasly"],
    index=None,
    placeholder="Select a retail investor"
)
 
if st.button(
    "Log in as Retail Investor",
    type="primary",
    use_container_width=True
):
    if retail_investor_user is None:
        st.warning("Please select a retail investor first.")
    else:
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'retail_investor'
        st.session_state['first_name'] = 'Mike'
        st.session_state['user_id'] = 2
        logger.info("Logging in as Retail Investor")
        st.switch_page('pages/10_Investor_Home.py')


# System Administrator login
admin_user = st.selectbox(
    "System Administrator",
    options=["Gregory Hilton"],
    index=None,
    placeholder="Select a system administrator"
)

if st.button(
    "Log in as System Administrator",
    type="primary",
    use_container_width=True
):
    if admin_user is None:
        st.warning("Please select a system administrator first.")
    else:
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'administrator'
        st.session_state['first_name'] = 'Gregory'
        st.session_state['user_id'] = 3
        logger.info("Logging in as System Administrator")
        st.switch_page('pages/20_Admin_Home.py')


# Financial Advisor login
advisor_user = st.selectbox(
    "Financial Advisor",
    options=["James Carter"],
    index=None,
    placeholder="Select a financial advisor"
)

if st.button(
    "Log in as Financial Advisor",
    type="primary",
    use_container_width=True
):
    if advisor_user is None:
        st.warning("Please select a financial advisor first.")
    else:
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'financial_advisor'
        st.session_state['first_name'] = 'James'
        st.session_state['user_id'] = 4
        logger.info("Logging in as Financial Advisor")
        st.switch_page('pages/30_Advisor_Home.py')