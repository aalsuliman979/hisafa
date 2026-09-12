from flask import Flask
from db_helper import get_total_expenses, get_totals_by_category, get_totals_by_month

app = Flask(__name__)
from db_helper import get_connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT
    )
    """)
    connection.commit()
    connection.close()

init_db()
@app.route("/")
def dashboard():
    total = get_total_expenses()
    by_category = get_totals_by_category()
    by_month = get_totals_by_month()

    html = f"<h1>حِصافة - Dashboard</h1>"
    html += f"<h2>إجمالي المصاريف: {total}</h2>"

    html += "<h3>حسب الفئة:</h3><ul>"
    for category, amount in by_category:
        html += f"<li>{category}: {amount}</li>"
    html += "</ul>"

    html += "<h3>حسب الشهر:</h3><ul>"
    for month, amount in by_month:
        html += f"<li>{month}: {amount}</li>"
    html += "</ul>"

    return html

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
