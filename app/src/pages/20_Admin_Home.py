import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

# Page header
st.title('System Administrator Home')
st.write(
    f"Welcome, {st.session_state.get('first_name', 'Administrator')}. "
    "Use this area to manage users, roles, backups, logs, and data integrity checks."
)

st.write("### Admin Tools")

# Quick explanation of what this role can do
st.info(
    "As the system administrator, you are responsible for managing platform access, "
    "monitoring activity, maintaining backups, and validating portfolio data."
)

# Create two columns to make the landing page feel more like a dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("Access & Permissions")
    st.write(
        "View users, create new users, create roles, and update user access levels."
    )

    if st.button(
        'Open Access Control',
        type='primary',
        use_container_width=True
    ):
        st.switch_page('pages/21_ML_Model_Mgmt.py')

with col2:
    st.subheader("System Responsibilities")
    st.write(
        "Monitor activity logs, manage backups, and recalculate portfolio totals "
        "when data needs to be validated."
    )

    st.success("Backend routes for logs, backups, and validation are available and ready to connect.")

# Small summary section at the bottom
st.write("### Available Admin Features")
st.markdown("""
- View and create users
- View and create roles
- Update a user's assigned role
- Deactivate inactive users
- View activity logs
- Create and delete backups
- Recalculate portfolio total values
""")