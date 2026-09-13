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
def landing():
    html = """
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-glass: rgba(22, 27, 34, 0.65);
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent-blue: #388bfd;
            --accent-purple: #a371f7;
            --gradient-primary: linear-gradient(135deg, #1f6feb, #388bfd);
            --gradient-hero: linear-gradient(135deg, #1f6feb 0%, #a371f7 50%, #388bfd 100%);
            --gradient-card: linear-gradient(145deg, rgba(56,139,253,0.08), rgba(163,113,247,0.08));
            --border-color: #30363d;
            --border-glow: rgba(56, 139, 253, 0.4);
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
            --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.25);
            --shadow-hover: 0 8px 30px rgba(56, 139, 253, 0.25);
            --transition-fast: 0.2s ease;
            --transition-smooth: 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            --font-main: 'Inter', 'Cairo', -apple-system, sans-serif;
            --container-width: 1200px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
            font-family: var(--font-main);
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            direction: rtl;
        }
        a { text-decoration: none; color: inherit; }
        ul { list-style: none; }
        .container { max-width: var(--container-width); margin: 0 auto; padding: 0 24px; }

        .navbar {
            position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
            background: var(--bg-glass);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
        }
        .navbar .container {
            display: flex; align-items: center; justify-content: space-between; padding-block: 16px;
        }
        .navbar-logo {
            font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 8px;
            background: var(--gradient-primary);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }
        .navbar-links { display: flex; gap: 32px; align-items: center; }
        .navbar-links a {
            font-size: 14.5px; font-weight: 500; color: var(--text-secondary);
            transition: var(--transition-fast); position: relative;
        }
        .navbar-links a:hover { color: var(--text-primary); }
        .navbar-cta {
            background: var(--gradient-primary); color: white !important;
            padding: 10px 22px; border-radius: var(--radius-sm);
            font-weight: 600; font-size: 14px; transition: var(--transition-fast);
            box-shadow: var(--shadow-soft);
        }
        .navbar-cta:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover); }

        .hero {
            min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;
            position: relative; padding: 120px 24px 80px; text-align: center; overflow: hidden;
        }
        .hero::after {
            content: ''; position: absolute; bottom: -20%; left: -10%;
            width: 400px; height: 400px; background: var(--accent-purple);
            filter: blur(140px); opacity: 0.15; z-index: -1; border-radius: 50%;
        }
        .hero-badge {
            display: flex; align-items: center; justify-content: center; gap: 8px;
            background: var(--bg-glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            padding: 10px 28px;
            border-radius: 50px; font-size: 18px; font-weight: 600;
            color: var(--text-primary); margin: 0 auto 28px auto;
            width: fit-content;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        .hero-badge:hover {
            border-color: var(--border-glow);
            background: var(--bg-secondary);
        }
        .hero h1 {
            font-size: clamp(26px, 5vw, 52px); font-weight: 800; line-height: 1.3;
            margin-bottom: 20px; max-width: 900px;
        }
        .hero h1 .highlight {
            background: var(--gradient-hero);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        }
        .hero p {
            font-size: clamp(15px, 2vw, 18px); color: var(--text-secondary);
            max-width: 600px; margin-bottom: 36px; margin-inline: auto;
        }
        .hero-buttons { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; }
        .btn {
            padding: 14px 32px; border-radius: var(--radius-sm); font-weight: 600;
            font-size: 15px; cursor: pointer; border: none; transition: var(--transition-smooth);
        }
        .btn-primary { background: var(--gradient-primary); color: white; box-shadow: var(--shadow-soft); }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: var(--shadow-hover); }
        .btn-secondary {
            background: var(--bg-glass); backdrop-filter: blur(10px); color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        .btn-secondary:hover { background: var(--bg-secondary); border-color: var(--border-glow); }

        .features { padding: 100px 24px; }
        .section-header { text-align: center; max-width: 600px; margin: 0 auto 60px; }
        .section-header span {
            color: var(--accent-blue); font-size: 13px; font-weight: 700;
            text-transform: uppercase; letter-spacing: 1.5px;
        }
        .section-header h2 { font-size: clamp(26px, 4vw, 40px); font-weight: 700; margin: 12px 0; }
        .section-header p { color: var(--text-secondary); font-size: 15.5px; }
        .features-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px; max-width: var(--container-width); margin: 0 auto;
        }
        .feature-card {
            background: var(--gradient-card); backdrop-filter: blur(20px);
            border: 1px solid var(--border-color); border-radius: var(--radius-lg);
            padding: 32px; transition: var(--transition-smooth);
        }
        .feature-card:hover {
            transform: translateY(-8px); border-color: var(--border-glow); box-shadow: var(--shadow-hover);
        }
        .feature-icon {
            width: 52px; height: 52px; background: var(--gradient-primary);
            border-radius: var(--radius-md); display: flex; align-items: center;
            justify-content: center; font-size: 24px; margin-bottom: 20px; box-shadow: var(--shadow-soft);
        }
        .feature-card h3 { font-size: 19px; font-weight: 700; margin-bottom: 10px; }
        .feature-card p { color: var(--text-secondary); font-size: 14.5px; line-height: 1.7; }

        .footer {
            background: var(--bg-secondary); border-top: 1px solid var(--border-color);
            padding: 60px 24px 24px;
        }
        .footer-bottom {
            max-width: var(--container-width); margin: 0 auto; padding-top: 24px;
            display: flex; flex-direction: column; align-items: center; gap: 8px;
        }
        .footer-bottom p { color: var(--text-muted); font-size: 13px; }

        @media (max-width: 768px) {
            .navbar-links { display: none; }
            .hero { padding: 100px 20px 60px; }
            .features { padding: 70px 20px; }
        }
        @media (max-width: 480px) {
            .hero-buttons { flex-direction: column; width: 100%; }
            .btn { width: 100%; text-align: center; }
        }
    </style>
    </head>
    <body>

    <nav class="navbar">
        <div class="container">
            <div class="navbar-logo">حِصافة</div>
            <div class="navbar-links">
                <a href="#features">المميزات</a>
                <a href="mailto:aalsuliman979@gmail.com">تواصل</a>
                <a href="/dashboard" class="navbar-cta">فتح Dashboard</a>
            </div>
        </div>
    </nav>

    <section class="hero">
        <a href="#features" class="hero-badge">حِصافة</a>
        <h1>حوّل مصاريفك إلى  <span class="highlight">قرارات ذكية</span></h1>
        <p>من إدخال المصروف إلى القرار النهائي — بخطوات بسيطة</p>

        <div class="hero-buttons">
            <a href="/dashboard" class="btn btn-primary">جرّب الآن مجانًا</a>
            <a href="#features" class="btn btn-secondary">اعرف أكثر</a>
        </div>
    </section>

    <section class="features" id="features">
        <div class="section-header">
            <span>المميزات</span>
            <h2>كل شي تحتاجه بمكان وحد</h2>
            <p>حِصافة تحلل مصاريف شركتك تلقائيًا وتطلع لك رؤى وتوقعات تساعدك تتخذ القرار الصح بدل ما تغرق بالأرقام.</p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>لوحة تحكم حية</h3>
                <p>شوف إجمالي مصاريفك، مجمّعة حسب الفئة والشهر، بتحديث فوري.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <h3>توقع ذكي</h3>
                <p>نتوقع مصاريف الشهر الجاي بناءً على نمط إنفاقك السابق.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3>تحليل تلقائي</h3>
                <p>نطلع لك ملاحظات فورية عن أي تغيّر ملحوظ بمصاريفك.</p>
            </div>
        </div>
    </section>

    <footer class="footer" id="footer">
        <div class="footer-bottom">
            <p>© 2026 حِصافة — Financial Intelligence Platform</p>
            <p>جميع الحقوق محفوظة لحصافة</p>
        </div>
    </footer>

    </body>
    </html>
    """
    return html

@app.route("/dashboard")
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

    return redirect("/dashboard")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)