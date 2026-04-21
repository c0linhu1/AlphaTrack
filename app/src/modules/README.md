# `modules` Folder

This folder contains shared functionality used across the AlphaTrack Streamlit application.



## Navigation System (`nav.py`)

The `nav.py` file implements a custom sidebar navigation system with built-in Role-Based Access Control (RBAC).

Instead of using Streamlit’s default navigation, we dynamically generate sidebar links based on the currently selected user role.



## Role-Based Navigation

When a user selects a role on the Home page, their role is stored in:

```python
st.session_state["role"]
```

The `SideBarLinks()` function reads this value and conditionally renders the appropriate navigation links.

Supported roles:

- **Portfolio Analyst**
- **Retail Investor**
- **Financial Advisor**
- **System Administrator**

Each role is only shown the pages relevant to their responsibilities.



## How Navigation Works

- Sidebar links are created using `st.sidebar.page_link()`
- Pages are organized inside the `/pages` directory
- Navigation is dynamically controlled based on:
  - `authenticated` status
  - `role` stored in session state

If a user is not authenticated, they are automatically redirected to `Home.py`.



## Session Management

The navigation system also handles:

- User login state (`authenticated`)
- Role assignment
- Logout functionality (clears session state and redirects to Home)



## Purpose

This design ensures:

- Clean separation of functionality by user role  
- Controlled access to pages  
- A more realistic, application-like user experience  



## Notes

- All pages must exist in the `/pages` directory for navigation to work  
- Page paths must match exactly with those defined in `nav.py`  
- Navigation updates automatically when roles change  

