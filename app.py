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

    html = """
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, 'Segoe UI', system-ui, sans-serif;
            direction: rtl;
            background-color: #0e1116;
            color: #e6e8eb;
            min-height: 100vh;
        }
        .topbar {
            background-color: #14181f;
            border-bottom: 1px solid #23272f;
            padding: 18px 40px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .topbar .icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #1f6feb, #3fb950);
            border-radius: 9px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 7px;
        }
        .topbar .icon svg {
            width: 100%;
            height: 100%;
        }
        .topbar .title {
            font-size: 17px;
            font-weight: 700;
            color: #fff;
        }
        .topbar .subtitle {
            font-size: 12px;
            color: #7d8590;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 32px 40px 60px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        .stat-card {
            background-color: #161b22;
            border: 1px solid #23272f;
            border-radius: 12px;
            padding: 20px;
            animation: fadeIn 0.45s ease-out;
            transition: border-color 0.15s;
        }
        .stat-card:hover {
            border-color: #2f81f7;
        }
        .stat-label {
            font-size: 12px;
            color: #7d8590;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 10px;
        }
        .stat-value {
            font-size: 26px;
            font-weight: 700;
            color: #fff;
        }
        .stat-value.green { color: #3fb950; }
        .stat-value.blue { color: #58a6ff; }
        .stat-value.orange { color: #d29922; }
        .section {
            background-color: #161b22;
            border: 1px solid #23272f;
            border-radius: 12px;
            padding: 22px;
            margin-bottom: 20px;
            animation: fadeIn 0.45s ease-out;
        }
        .section-title {
            font-size: 13px;
            font-weight: 600;
            color: #7d8590;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #21262d;
            font-size: 14px;
        }
        .row:last-child { border-bottom: none; }
        .row .name { color: #c9d1d9; }
        .row .amount {
            font-weight: 600;
            color: #e6e8eb;
            background-color: #0e1116;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 13px;
        }
        .insight-badge {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 12px 14px;
            background-color: #0e1116;
            border: 1px solid #23272f;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 13.5px;
            color: #c9d1d9;
        }
        .insight-badge:last-child { margin-bottom: 0; }
        label {
            display: block;
            font-size: 12.5px;
            color: #7d8590;
            margin-bottom: 6px;
            font-weight: 500;
        }
        .field { margin-bottom: 16px; }
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        input[type=text], input[type=number], input[type=date] {
            background-color: #0e1116;
            color: #e6e8eb;
            padding: 10px 12px;
            border: 1px solid #23272f;
            border-radius: 8px;
            width: 100%;
            font-size: 14px;
        }
        input:focus {
            outline: none;
            border-color: #2f81f7;
        }
        input[type=submit] {
            background: linear-gradient(135deg, #2f81f7, #388bfd);
            color: white;
            padding: 11px 26px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            margin-top: 8px;
            transition: opacity 0.15s, transform 0.1s;
        }
        input[type=submit]:hover { opacity: 0.9; }
        input[type=submit]:active { transform: scale(0.97); }
    </style>
    </head>
    <body>

    <div class="topbar">
        <div class="icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 17L9 11L13 15L21 7" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M15 7H21V13" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div>
            <div class="title">حِصافة</div>
            <div class="subtitle">Financial Intelligence Platform</div>
        </div>
    </div>

    <div class="container">
    """

    html += f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">💰 إجمالي المصاريف</div>
            <div class="stat-value green">{total}</div>
        </div>
    """

    if forecast:
        html += f"""
        <div class="stat-card">
            <div class="stat-label">📈 توقع الشهر الجاي</div>
            <div class="stat-value blue">{forecast}</div>
        </div>
        """

    html += f"""
        <div class="stat-card">
            <div class="stat-label">📊 عدد الفئات</div>
            <div class="stat-value orange">{len(by_category)}</div>
        </div>
    </div>
    """

    html += '<div class="section"><div class="section-title">📂 حسب الفئة</div>'
    for category, amount in by_category:
        html += f'<div class="row"><span class="name">{category}</span><span class="amount">{amount}</span></div>'
    html += "</div>"

    html += '<div class="section"><div class="section-title">🗓️ حسب الشهر</div>'
    for month, amount in by_month:
        html += f'<div class="row"><span class="name">{month}</span><span class="amount">{amount}</span></div>'
    html += "</div>"

    html += '<div class="section"><div class="section-title">🧠 تحليل ذكي</div>'
    for insight in insights:
        html += f'<div class="insight-badge">{insight}</div>'
    html += "</div>"

    html += """
    <div class="section">
        <div class="section-title">➕ إضافة مصروف جديد</div>
        <form method="POST" action="/add">
            <div class="form-grid">
                <div class="field">
                    <label>المبلغ</label>
                    <input type="number" step="0.01" name="amount" required>
                </div>
                <div class="field">
                    <label>الفئة</label>
                    <input type="text" name="category" required>
                </div>
                <div class="field">
                    <label>التاريخ</label>
                    <input type="date" name="date" required>
                </div>
                <div class="field">
                    <label>الوصف</label>
                    <input type="text" name="description">
                </div>
            </div>
            <input type="submit" value="إضافة المصروف">
        </form>
    </div>
    """

    html += "</div></body></html>"
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