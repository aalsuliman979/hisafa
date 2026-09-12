# Hisafa — Financial Intelligence Platform

A platform that analyzes small business expenses and turns them into actionable insights for decision-making.

## Features
- Full expense management (add, view, update, delete)
- Filter expenses by category
- Dashboard showing:
  - Total expenses
  - Expenses grouped by category
  - Expenses grouped by month

## Tech Stack
- Python 3.12
- SQLite (embedded database)
- Git / GitHub

## Project Structure
```
hisafa/
├── db_helper.py        # All database operations (CRUD + aggregation)
├── database.py          # Database and table creation
├── dashboard.py          # Summary and statistics view
├── view_expenses.py      # View all expenses
├── filter_expenses.py    # Filter by category
├── update_expense.py     # Update an expense
├── delete_expense.py     # Delete an expense
└── cleanup.py            # Table cleanup utility
```

## Security
- Parameterized queries to prevent SQL Injection
- Input validation before saving data
- Error handling across all database operations

## Author
Ahmad Al Suliman 