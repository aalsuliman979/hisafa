from flask import Flask, request, redirect
from db_helper import get_connection, get_total_expenses, get_totals_by_category, get_totals_by_month, forecast_next_month, add_expense, get_smart_insights

app = Flask(__name__)

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
    forecast = forecast_next_month()
    insights = get_smart_insights()

    html = "<h1>حِصافة - Dashboard</h1>"
    html += f"<h2>إجمالي المصاريف: {total}</h2>"

    html += "<h3>حسب الفئة:</h3><ul>"
    for category, amount in by_category:
        html += f"<li>{category}: {amount}</li>"
    html += "</ul>"

    html += "<h3>حسب الشهر:</h3><ul>"
    for month, amount in by_month:
        html += f"<li>{month}: {amount}</li>"
    html += "</ul>"

    if forecast:
        html += f"<h3>توقع الشهر الجاي: {forecast}</h3>"

    html += "<h3>تحليل ذكي:</h3><ul>"
    for insight in insights:
        html += f"<li>{insight}</li>"
    html += "</ul>"

    html += """
    <hr>
    <h3>إضافة مصروف جديد</h3>
    <form method="POST" action="/add">
        المبلغ: <input type="number" step="0.01" name="amount" required><br><br>
        الفئة: <input type="text" name="category" required><br><br>
        التاريخ: <input type="date" name="date" required><br><br>
        الوصف: <input type="text" name="description"><br><br>
        <input type="submit" value="إضافة">
    </form>
    """

    return html

@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]
    description = request.form["description"]

    add_expense(amount, category, date, description)

    return redirect("/")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)