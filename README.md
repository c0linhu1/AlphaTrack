AlphaTrack

AlphaTrack is a full-stack portfolio tracking and analytics platform designed to bridge the gap between basic retail tools and advanced institutional systems. It provides users with a centralized interface to manage portfolios, analyze risk, and make data-driven financial decisions.



Overview

AlphaTrack supports four primary user roles:
	•	Portfolio Analyst — analyzes risk, correlations, and market behavior
	•	Retail Investor — manages personal portfolios and holdings
	•	Financial Advisor — oversees multiple client portfolios and rebalancing
	•	System Administrator — manages users, roles, and system integrity

Each role is given a tailored interface and functionality through a role-based Streamlit frontend connected to a Flask REST API and MySQL database.



Tech Stack
	•	Frontend: Streamlit
	•	Backend: Flask (REST API with Blueprints)
	•	Database: MySQL
	•	Containerization: Docker + Docker Compose
	•	Development Environment: VS Code



Project Structure

AlphaTrack/
│
├── api/                # Flask backend (routes, DB connection, blueprints)
├── app/                # Streamlit frontend
│   └── src/
│       ├── pages/      # Role-based UI pages
│       └── modules/    # Navigation logic
├── database-files/     # SQL schema + mock data
├── docker-compose.yml  # Container orchestration
└── README.md




Setup Instructions

1. Clone the repository

git clone git@github.com:c0linhu1/AlphaTrack.git
cd AlphaTrack




2. Create a .env file

Inside the /api directory, create a .env file with the following:

SECRET_KEY=your_secret_key

DB_USER=root
MYSQL_ROOT_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=3306
DB_NAME=alphatrack

  Make sure:
	•	The password matches what MySQL expects
	•	Do NOT commit your .env file to GitHub



3. Start the application

Run the following from the root directory:

docker compose up --build

This will:
	•	Start the MySQL database
	•	Load all schema and mock data automatically
	•	Launch the Flask API on port 4000
	•	Launch the Streamlit app on port 8501



4. Access the app

Open your browser and go to:

http://localhost:8501




 Features

Portfolio Analytics
	•	Risk dashboards (volatility, metrics)
	•	Asset correlation matrices
	•	Watchlist creation and management

Portfolio Management
	•	Add, update, and delete holdings
	•	Track performance over time
	•	Portfolio-level summaries

Client & Advisor Tools
	•	Multi-client portfolio views
	•	Risk profiling and rebalancing insights
	•	Report generation

Admin Controls
	•	Create and manage users
	•	Assign roles dynamically
	•	View system logs and backups



API Design

The backend follows RESTful design principles and is organized into four Flask blueprints:
	•	/p → Portfolio routes
	•	/i → Investor routes
	•	/a → Admin routes
	•	/ad → Advisor routes

The system includes:
	•	GET routes for retrieval
	•	POST routes for creation
	•	PUT routes for updates
	•	DELETE routes for removal

All routes are mapped from a REST API matrix based on user stories.



Database
	•	Fully relational schema using MySQL
	•	Includes tables for users, roles, portfolios, holdings, clients, and logs
	•	Mock data is automatically loaded from /database-files/



Demo

A full demo of the application can be found here:

👉 https://www.youtube.com/watch?v=nG_PAb0or1k



👥 Team Members
	•	Devaj Desai
	•	Colin Hui
	•	Henry Wonsiewicz
	•	Max 



Notes
	•	The application is fully containerized and runs end-to-end using Docker
	•	All pages and routes are connected to real backend functionality
	•	Role-based navigation is dynamically generated from database data



Resources
	•	Streamlit Docs: https://docs.streamlit.io
	•	Flask Docs: https://flask.palletsprojects.com
	•	Docker Docs: https://docs.docker.com

⸻

Submission Checklist
	•	Docker runs successfully
	•	Database initializes with mock data
	•	API routes function correctly
	•	Frontend interacts with backend
	•	README is complete and professional
	•	Demo video recorded and linked