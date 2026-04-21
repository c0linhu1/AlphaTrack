
## `pages` Folder

This folder contains all of the Streamlit pages that make up the AlphaTrack application. Each page represents a specific feature or workflow tied to one of our four user personas:

- Portfolio Analyst (Bobby)
- Retail Investor (Mike)
- System Administrator (Gregory)
- Financial Advisor (James)

Navigation between these pages is controlled through the sidebar (`modules/nav.py`), which dynamically displays different pages depending on the user's role after logging in.



## How Pages Are Organized

Streamlit automatically orders pages based on the numeric prefixes in each filename. We use this system to group pages by persona:

- `00–02` → Portfolio Analyst
- `10–13` → Retail Investor
- `20–22` → System Administrator
- `30–33` → Financial Advisor
- `40` → About page

This structure keeps the app organized and ensures that each user only sees functionality relevant to their role.



## Page Breakdown

### Portfolio Analyst (Bobby)
These pages focus on portfolio analytics, risk insights, and asset relationships.

- **00_Analyst_Home.py**  
  Landing page for the Portfolio Analyst.

- **01_Risk_DashBoard.py**  
  Displays portfolio-level risk metrics such as volatility and overall risk scores.

- **02_Correlation_Watchlists.py**  
  Shows asset correlation matrices and allows users to create and manage watchlists.



### Retail Investor (Mike)
These pages focus on personal portfolio tracking and management.

- **10_Investor_Home.py**  
  Landing page for the Retail Investor.

- **11_Portfolio_Dashboard.py**  
  Provides an overview of portfolio performance and key metrics.

- **12_Holdings_Performance.py**  
  Displays detailed holdings and performance breakdowns.

- **13_Manage_Holdings.py**  
  Allows users to add, update, or remove holdings from their portfolio.



### System Administrator (Gregory)
These pages focus on system maintenance, user management, and monitoring.

- **20_Admin_Home.py**  
  Landing page for the System Administrator.

- **21_ML_Model_Mgmt.py**  
  Repurposed as an access control page for managing users and roles.

- **22_System_Monitoring.py**  
  Displays system activity logs, backups, and data integrity tools.



### Financial Advisor (James)
These pages support managing multiple client portfolios and advisory workflows.

- **30_Advisor_Home.py**  
  Landing page for the Financial Advisor.

- **31_Client_Overview.py**  
  Displays all clients and their portfolios.

- **32_Risk_Rebalancing.py**  
  Shows risk profiles and provides rebalancing insights.

- **33_Client_Management.py**  
  Allows the advisor to manage client accounts and portfolios.



### General

- **40_About.py**  
  Provides an overview of the AlphaTrack application and its purpose.



## Notes

- All pages rely on backend API routes defined in the `/api` folder.
- Role-based access is enforced using `st.session_state` and dynamic sidebar navigation.
- Several pages were adapted from the original project template and repurposed for AlphaTrack functionality.