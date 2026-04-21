# This file controls the sidebar navigation shown to each user role.

import streamlit as st


# ---- General 

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# ---- Role: Portfolio Analyst 

def analyst_home_nav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py",
        label="Analyst Home",
        icon="📈"
    )


def risk_dashboard_nav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py",
        label="Risk Dashboard",
        icon="📊"
    )


def correlation_watchlist_nav():
    st.sidebar.page_link(
        "pages/02_Map_Demo.py",
        label="Correlation & Watchlists",
        icon="🧩"
    )


# ---- Role: Retail Investor 

def investor_home_nav():
    st.sidebar.page_link(
        "pages/10_USAID_Worker_Home.py",
        label="Investor Home",
        icon="💰"
    )


def portfolio_dashboard_nav():
    st.sidebar.page_link(
        "pages/11_Prediction.py",
        label="Portfolio Dashboard",
        icon="📉"
    )


def holdings_nav():
    st.sidebar.page_link(
        "pages/12_API_Test.py",
        label="Holdings & Performance",
        icon="📋"
    )


def manage_holdings_nav():
    st.sidebar.page_link(
        "pages/13_Classification.py",
        label="Manage Holdings",
        icon="✏️"
    )


# ---- Role: Administrator 

def admin_home_nav():
    st.sidebar.page_link(
        "pages/20_Admin_Home.py",
        label="Admin Home",
        icon="🖥️"
    )


def access_control_nav():
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py",
        label="Access Control",
        icon="🔐"
    )

def system_monitoring_nav():
    st.sidebar.page_link(
        "pages/22_System_Monitoring.py",
        label="System Monitoring",
        icon="🛠️"
    )

# ---- Role: Financial Advisor 

def advisor_home_nav():
    st.sidebar.page_link(
        "pages/30_Advisor_Home.py",
        label="Advisor Home",
        icon="💼"
    )


def client_overview_nav():
    st.sidebar.page_link(
        "pages/31_Client_Overview.py",
        label="Client Overview",
        icon="📊"
    )


def risk_rebalancing_nav():
    st.sidebar.page_link(
        "pages/32_Risk_Rebalancing.py",
        label="Risk & Rebalancing",
        icon="⚖️"
    )


def client_management_nav():
    st.sidebar.page_link(
        "pages/33_Client_Management.py",
        label="Client Management",
        icon="👥"
    )


# ---- Sidebar assembly 

def SideBarLinks(show_home=False):
    """
    Render sidebar links based on the current user's role.
    The role is stored in st.session_state after the user selects a persona on Home.py.
    """

    # Show the AlphaTrack logo on every page
    st.sidebar.image("assets/logo.png", width=150)

    # If the user is not authenticated, send them back to Home
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "portfolio_analyst":
            analyst_home_nav()
            risk_dashboard_nav()
            correlation_watchlist_nav()

        if st.session_state["role"] == "retail_investor":
            investor_home_nav()
            portfolio_dashboard_nav()
            holdings_nav()
            manage_holdings_nav()

        if st.session_state["role"] == "administrator":
            admin_home_nav()
            access_control_nav()
            system_monitoring_nav()

        if st.session_state["role"] == "financial_advisor":
            advisor_home_nav()
            client_overview_nav()
            risk_rebalancing_nav()
            client_management_nav()

    # Always show the About page
    about_page_nav()

    # Logout button for authenticated users
    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            if "first_name" in st.session_state:
                del st.session_state["first_name"]
            if "user_id" in st.session_state:
                del st.session_state["user_id"]
            st.switch_page("Home.py")