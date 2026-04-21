# AlphaTrack — Pages Directory

This folder contains all Streamlit pages that make up the AlphaTrack 
application's front-end user interface. Each page is tied to one of 
four user personas and represents a specific feature or workflow within 
the platform.

---

## User Personas

| Persona | Name | Role |
|---|---|---|
| Portfolio Analyst | Bobby | Analyzes portfolio risk and performance metrics |
| Retail Investor | Mike | Manages and monitors personal investment portfolio |
| System Administrator | Gregory | Manages users, roles, and system health |
| Financial Advisor | James | Oversees multiple client portfolios and risk profiles |

---

## Navigation & Role-Based Access

Navigation is controlled dynamically through `modules/nav.py`. When a 
user logs in from the Home page, their role is stored in 
`st.session_state`. The sidebar then renders only the pages relevant 
to that role, ensuring each persona sees only their own functionality.

Pages are ordered using numeric filename prefixes, which Streamlit uses 
to determine sidebar ordering:

| Prefix Range | Persona |
|---|---|
| `00–02` | Portfolio Analyst (Bobby) |
| `10–13` | Retail Investor (Mike) |
| `20–22` | System Administrator (Gregory) |
| `30–33` | Financial Advisor (James) |
| `40` | General / About |

---

## Page Breakdown

### Portfolio Analyst — Bobby (`00–02`)
Pages focused on portfolio analytics, risk metrics, and asset 
correlation insights.

| File | Description |
|---|---|
| `00_Analyst_Home.py` | Landing page for the Portfolio Analyst persona |
| `01_Risk_Dashboard.py` | Displays portfolio-level risk metrics including volatility and overall risk scores |
| `02_Correlation_Watchlists.py` | Shows asset correlation matrices and allows users to create and manage watchlists |

**User Stories Covered:** View risk metrics dashboard, visualize 
correlation matrix, save custom watchlists.

---

### Retail Investor — Mike (`10–13`)
Pages focused on personal portfolio tracking, performance monitoring, 
and holdings management.

| File | Description |
|---|---|
| `10_Investor_Home.py` | Landing page for the Retail Investor persona |
| `11_Portfolio_Dashboard.py` | Overview of portfolio value, total return, performance chart, and holdings breakdown |
| `12_Holdings_Performance.py` | Detailed view of individual holdings with gain/loss metrics |
| `13_Manage_Holdings.py` | Add, edit, or remove holdings from the portfolio |

**User Stories Covered:** View all investments in one dashboard, track 
gains and losses over time, compare individual stocks, add/edit/remove 
holdings.

**API Routes Used:**
- `GET /i/portfolios/{id}/holdings`
- `GET /i/portfolios/{id}/performance`
- `POST /i/portfolios/{id}/holdings`
- `PUT /i/holdings/{portfolioId}/{assetId}`
- `DELETE /i/holdings/{portfolioId}/{assetId}`

---

### System Administrator — Gregory (`20–22`)
Pages focused on platform maintenance, user and role management, and 
system monitoring.

| File | Description |
|---|---|
| `20_Admin_Home.py` | Landing page for the System Administrator persona |
| `21_ML_Model_Mgmt.py` | Repurposed as an access control page for managing users and roles |
| `22_System_Monitoring.py` | Displays system activity logs, backup records, and data integrity tools |

**User Stories Covered:** Add/update user roles and permissions, 
deactivate users, monitor system activity logs, manage backups.

---

### Financial Advisor — James (`30–33`)
Pages focused on client portfolio oversight, risk profiling, and 
advisory workflow management.

| File | Description |
|---|---|
| `30_Advisor_Home.py` | Landing page for the Financial Advisor persona |
| `31_Client_Overview.py` | Displays all clients and a high-level summary of their portfolios |
| `32_Risk_Rebalancing.py` | Shows individual client risk profiles and rebalancing suggestions |
| `33_Client_Management.py` | Allows the advisor to add, update, or close client accounts |

**User Stories Covered:** View all client portfolios in one dashboard, 
generate performance reports, set and monitor risk thresholds, 
add/remove client accounts.

---

### General (`40`)

| File | Description |
|---|---|
| `40_About.py` | Overview of the AlphaTrack application, its purpose, and the tech stack |

---

## Technical Notes

- All pages communicate with the Flask REST API running at 
`http://web-api:4000` inside the Docker network.
- Role-based access is enforced using `st.session_state['role']` 
set at login on `Home.py`.
- The sidebar is rendered by calling `SideBarLinks()` from 
`modules/nav.py` at the top of every page.
- Pages were built using the Streamlit framework and follow the 
project's three-tier architecture: MySQL → Flask API → Streamlit UI.