# Hisafa (حِصافة) — Financial Intelligence Platform

A multi-user web platform that analyzes small business expenses and turns them into actionable insights for decision-making.

🔗 **Live Demo:** https://hisafa.onrender.com

## Features

- **Multi-user authentication** — secure registration, login, and session management with hashed passwords
- **Data isolation** — each account only sees its own expense data
- **Interactive dashboard** showing:
  - Total expenses
  - Expenses grouped by category
  - Expenses grouped by month
  - Next month's spending forecast
- **Smart Insights** — automatic month-over-month trend analysis
- **Budget Alerts** — flags categories that exceed or approach preset spending limits
- **Recommendations** — rule-based suggestions when spending patterns look risky
- **Modern responsive UI** — dark theme, custom logo, animations, mouse-tracking glow effect
- **Expense management** — add expenses through a validated form with category dropdown

## Tech Stack

- **Backend:** Python 3.12, Flask
- **Database:** SQLite
- **Security:** Werkzeug password hashing, parameterized SQL queries, Flask sessions
- **Frontend:** HTML, CSS (custom, no framework), vanilla JavaScript
- **Deployment:** Render
- **Version Control:** Git / GitHub

## Project Structure

hisafa/
├── app.py            # Flask routes: landing page, auth, dashboard, expense form
├── db_helper.py       # All database logic (users, expenses, analytics)
├── static/
│   └── logo.png        # App logo
├── requirements.txt
└── README.md

## Security

- Passwords are hashed with Werkzeug (generate_password_hash / check_password_hash) — never stored in plain text
- All SQL queries use parameterized statements to prevent SQL Injection
- Server-side input validation on all forms
- Session-based route protection (/dashboard and /add require login)
- Each user's data is scoped by user_id at the database level

## How It Works

1. A business creates an account and logs in
2. They add their expenses (amount, category, date, description)
3. The dashboard aggregates this data using SQL (SUM, GROUP BY, strftime)
4. A simple forecasting model projects next month's spending based on recent growth rate
5. Rule-based logic flags budget overruns and generates written recommendations

## Author

Ahmad Al Suliman — built as a hands-on learning project while transitioning toward Data/Network Engineering.