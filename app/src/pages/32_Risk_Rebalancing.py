import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()
API_BASE = "http://web-api:4000/ad"
st.title("Risk & Rebalancing")
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

seen = {}
for c in clients:
    cid = c.get("client_id")
    if cid not in seen:
        seen[cid] = c
unique_clients = list(seen.values())
client_names = [c.get("name", f"Client {c.get('client_id', '?')}") for c in unique_clients]
client_map = {name: c for name, c in zip(client_names, unique_clients)}

selected_name = st.selectbox("Select a client:", client_names)
selected_client = client_map[selected_name]
client_id = selected_client.get("client_id")

st.divider()
st.subheader("Current Risk Profile")
risk_profile = None
try:
    rp_response = requests.get(f"{API_BASE}/clients/{client_id}/risk-profile")
    if rp_response.status_code == 200:
        rp_data = rp_response.json()
        if isinstance(rp_data, list) and len(rp_data) > 0:
            risk_profile = rp_data[0]
except Exception as e:
    st.error(f"Error: {e}")

if risk_profile:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Risk Level", risk_profile.get("risk_level", "N/A"))
    with c2:
        st.metric("Threshold Min", risk_profile.get("threshold_min", "N/A"))
    with c3:
        st.metric("Threshold Max", risk_profile.get("threshold_max", "N/A"))
else:
    st.info("No risk profile found.")

st.divider()
st.subheader("Update Risk Tolerance Thresholds")
with st.form("update_risk_form"):
    risk_options = ["conservative", "moderate", "aggressive"]
    default_idx = 1
    if risk_profile and risk_profile.get("risk_level") in risk_options:
        default_idx = risk_options.index(risk_profile["risk_level"])
    new_risk_level = st.selectbox("Risk Level", risk_options, index=default_idx)
    new_min = st.number_input("Threshold Min", min_value=0.00, max_value=1.00,
        value=float(risk_profile.get("threshold_min", 0.05)) if risk_profile else 0.05,
        step=0.01, format="%.4f")
    new_max = st.number_input("Threshold Max", min_value=0.00, max_value=1.00,
        value=float(risk_profile.get("threshold_max", 0.15)) if risk_profile else 0.15,
        step=0.01, format="%.4f")
    submitted = st.form_submit_button("Update Risk Profile", type="primary")
    if submitted:
        payload = {"risk_level": new_risk_level, "threshold_min": new_min, "threshold_max": new_max}
        try:
            put_response = requests.put(f"{API_BASE}/clients/{client_id}/risk-profile", json=payload)
            if put_response.status_code == 200:
                st.success(f"Risk profile updated for {selected_name}!")
                st.rerun()
            else:
                st.error(f"Failed to update (status {put_response.status_code}): {put_response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.subheader("Rebalancing Suggestions")
if st.button("Get Rebalancing Suggestions", type="primary"):
    try:
        rebal_response = requests.get(f"{API_BASE}/clients/{client_id}/rebalance")
        if rebal_response.status_code == 200:
            suggestions = rebal_response.json()
            if isinstance(suggestions, list) and len(suggestions) > 0:
                for s in suggestions:
                    ticker = s.get("ticker", "N/A")
                    alloc = s.get("allocation_percent", 0)
                    t_max = s.get("threshold_max")
                    if t_max and alloc and float(alloc) > float(t_max) * 100:
                        st.warning(f"**{ticker}** ({s.get('asset_name','')}) — Allocation: {alloc}%, Threshold Max: {t_max} — **EXCEEDS THRESHOLD**")
                    else:
                        st.success(f"**{ticker}** ({s.get('asset_name','')}) — Allocation: {alloc}% — Within limits")
            else:
                st.success("No holdings found or all within thresholds.")
        else:
            st.warning(f"Could not fetch suggestions (status {rebal_response.status_code})")
    except Exception as e:
        st.error(f"Error: {e}")