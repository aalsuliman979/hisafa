from flask import Flask, request, redirect, session
from db_helper import (
    init_tables, create_user, authenticate_user, add_expense,
    get_total_expenses, get_totals_by_category, get_totals_by_month,
    forecast_next_month, get_smart_insights, check_budget_alerts, get_recommendations
)

app = Flask(__name__)
app.secret_key = "hisafa-secret-key-change-this-later"

init_tables()

def render_page(title, body):
    return f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, 'Segoe UI', system-ui, sans-serif;
            direction: rtl;
            background-color: #171b21;
            color: #e6e8eb;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .auth-card {{
            background: #1c2128;
            border: 1px solid #2b313a;
            border-radius: 14px;
            padding: 40px;
            width: 360px;
        }}
        .auth-card h1 {{
            font-size: 22px;
            margin-bottom: 24px;
            text-align: center;
        }}
        .field {{ margin-bottom: 16px; }}
        label {{
            display: block;
            font-size: 13px;
            color: #8b939d;
            margin-bottom: 6px;
        }}
        input {{
            background: #171b21;
            color: #e6e8eb;
            padding: 10px 12px;
            border: 1px solid #2b313a;
            border-radius: 8px;
            width: 100%;
            font-size: 14px;
        }}
        input:focus {{ outline: none; border-color: #2f81f7; }}
        input[type=submit] {{
            background: linear-gradient(135deg, #2f81f7, #388bfd);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 600;
            margin-top: 8px;
        }}
        .switch-link {{
            text-align: center;
            margin-top: 16px;
            font-size: 13px;
            color: #8b939d;
        }}
        .switch-link a {{ color: #58a6ff; text-decoration: none; }}
        .error {{
            background: #3a1d1d;
            border: 1px solid #6e2c2c;
            color: #ff8080;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 16px;
            font-size: 13px;
        }}
        .success {{
            background: #1d3a24;
            border: 1px solid #2c6e3d;
            color: #7ee787;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 16px;
            font-size: 13px;
        }}
    </style>
    </head>
    <body>
    <div class="auth-card">
        <h1>{title}</h1>
        {body}
    </div>
    </body>
    </html>
    """

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        company_name = request.form["company_name"]

        success, msg = create_user(username, password, company_name)
        if success:
            return redirect("/login")
        else:
            message = f'<div class="error">{msg}</div>'

    body = f"""
    {message}
    <form method="POST">
        <div class="field">
            <label>اسم الشركة</label>
            <input type="text" name="company_name" required>
        </div>
        <div class="field">
            <label>اسم المستخدم</label>
            <input type="text" name="username" required>
        </div>
        <div class="field">
            <label>كلمة المرور</label>
            <input type="password" name="password" required>
        </div>
        <input type="submit" value="إنشاء حساب">
    </form>
    <div class="switch-link">عندك حساب؟ <a href="/login">سجّل دخول</a></div>
    """
    return render_page("إنشاء حساب - حِصافة", body)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = authenticate_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["company_name"] = user["company_name"]
            return redirect("/dashboard")
        else:
            message = '<div class="error">اسم المستخدم أو كلمة المرور غلط</div>'

    body = f"""
    {message}
    <form method="POST">
        <div class="field">
            <label>اسم المستخدم</label>
            <input type="text" name="username" required>
        </div>
        <div class="field">
            <label>كلمة المرور</label>
            <input type="password" name="password" required>
        </div>
        <input type="submit" value="تسجيل الدخول">
    </form>
    <div class="switch-link">ما عندك حساب؟ <a href="/register">سوّي حساب جديد</a></div>
    """
    return render_page("تسجيل الدخول - حِصافة", body)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
def landing():
    html = """
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #161b22; --bg-secondary: #1c2128; --bg-glass: rgba(28, 33, 40, 0.65);
            --text-primary: #e6edf3; --text-secondary: #8b949e; --text-muted: #6e7681;
            --accent-blue: #388bfd; --accent-purple: #a371f7;
            --gradient-primary: linear-gradient(135deg, #1f6feb, #388bfd);
            --gradient-hero: linear-gradient(135deg, #1f6feb 0%, #a371f7 50%, #388bfd 100%);
            --gradient-card: linear-gradient(145deg, rgba(56,139,253,0.08), rgba(163,113,247,0.08));
            --border-color: #363c46; --border-glow: rgba(56, 139, 253, 0.4);
            --radius-sm: 8px; --radius-md: 14px; --radius-lg: 20px;
            --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.25); --shadow-hover: 0 8px 30px rgba(56, 139, 253, 0.25);
            --transition-fast: 0.2s ease; --transition-smooth: 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            --font-main: 'Inter', 'Cairo', -apple-system, sans-serif; --container-width: 1200px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: var(--font-main); background-color: var(--bg-primary); color: var(--text-primary); line-height: 1.6; direction: rtl; }
        a { text-decoration: none; color: inherit; }
        .container { max-width: var(--container-width); margin: 0 auto; padding: 0 24px; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }
        @keyframes logoPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .navbar { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: var(--bg-glass); backdrop-filter: blur(16px); border-bottom: 1px solid var(--border-color); animation: fadeIn 0.5s ease-out; }
        .navbar .container { display: flex; align-items: center; justify-content: space-between; padding-block: 14px; }
        .navbar-logo { display: flex; align-items: center; transition: transform 0.3s ease; }
        .navbar-logo:hover { transform: scale(1.05); }
        .navbar-logo img { height: 56px; display: block; }
        .navbar-links { display: flex; gap: 32px; align-items: center; }
        .navbar-links a { font-size: 14.5px; font-weight: 500; color: var(--text-secondary); transition: var(--transition-fast); }
        .navbar-links a:hover { color: var(--text-primary); }
        .navbar-cta { background: var(--gradient-primary); color: white !important; padding: 10px 22px; border-radius: var(--radius-sm); font-weight: 600; font-size: 14px; transition: var(--transition-fast); box-shadow: var(--shadow-soft); }
        .navbar-cta:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover); }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; padding: 120px 24px 80px; text-align: center; overflow: hidden; }
        .mouse-glow { position: absolute; width: 500px; height: 500px; background: radial-gradient(circle, rgba(56,139,253,0.25) 0%, rgba(163,113,247,0.12) 45%, transparent 70%); border-radius: 50%; pointer-events: none; z-index: 0; transform: translate(-50%, -50%); transition: left 0.15s ease-out, top 0.15s ease-out; }
        .hero-logo-wrapper { position: relative; z-index: 1; margin: 0 auto 36px auto; width: fit-content; animation: fadeIn 0.6s ease-out; }
        .hero-logo { width: 460px; display: block; animation: logoPulse 3s ease-in-out infinite; }
        .hero h1 { position: relative; z-index: 1; font-size: clamp(26px, 5vw, 52px); font-weight: 800; line-height: 1.3; margin-bottom: 20px; max-width: 900px; animation: fadeIn 0.6s ease-out 0.15s both; }
        .hero h1 .highlight { background: var(--gradient-hero); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: gradientShift 4s ease infinite; }
        .hero p { position: relative; z-index: 1; font-size: clamp(15px, 2vw, 18px); color: var(--text-secondary); max-width: 600px; margin-bottom: 36px; margin-inline: auto; animation: fadeIn 0.6s ease-out 0.3s both; }
        .hero-buttons { position: relative; z-index: 1; display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; animation: fadeIn 0.6s ease-out 0.45s both; }
        .btn { padding: 14px 32px; border-radius: var(--radius-sm); font-weight: 600; font-size: 15px; cursor: pointer; border: none; transition: var(--transition-smooth); }
        .btn-primary { background: var(--gradient-primary); background-size: 200% auto; color: white; box-shadow: var(--shadow-soft); animation: pulse 2.5s ease-in-out infinite; }
        .btn-primary:hover { transform: translateY(-3px) scale(1.03); box-shadow: var(--shadow-hover); }
        .btn-secondary { background: var(--bg-glass); backdrop-filter: blur(10px); color: var(--text-primary); border: 1px solid var(--border-color); }
        .btn-secondary:hover { background: var(--bg-secondary); border-color: var(--border-glow); transform: translateY(-3px); }
        .features { padding: 100px 24px; }
        .section-header { text-align: center; max-width: 600px; margin: 0 auto 60px; }
        .section-header span { color: var(--accent-blue); font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
        .section-header h2 { font-size: clamp(26px, 4vw, 40px); font-weight: 700; margin: 12px 0; }
        .section-header p { color: var(--text-secondary); font-size: 15.5px; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; max-width: var(--container-width); margin: 0 auto; }
        .feature-card { background: var(--gradient-card); backdrop-filter: blur(20px); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 32px; transition: var(--transition-smooth); animation: fadeIn 0.6s ease-out both; }
        .feature-card:nth-child(1) { animation-delay: 0.1s; }
        .feature-card:nth-child(2) { animation-delay: 0.25s; }
        .feature-card:nth-child(3) { animation-delay: 0.4s; }
        .feature-card:hover { transform: translateY(-10px) scale(1.02); border-color: var(--border-glow); box-shadow: var(--shadow-hover); }
        .feature-icon { width: 52px; height: 52px; background: var(--gradient-primary); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 20px; box-shadow: var(--shadow-soft); transition: transform 0.3s ease; }
        .feature-card:hover .feature-icon { transform: rotate(-8deg) scale(1.1); }
        .feature-card h3 { font-size: 19px; font-weight: 700; margin-bottom: 10px; }
        .feature-card p { color: var(--text-secondary); font-size: 14.5px; line-height: 1.7; }
        .footer { background: var(--bg-secondary); border-top: 1px solid var(--border-color); padding: 60px 24px 24px; }
        .footer-bottom { max-width: var(--container-width); margin: 0 auto; padding-top: 24px; display: flex; flex-direction: column; align-items: center; gap: 8px; }
        .footer-bottom p { color: var(--text-muted); font-size: 13px; }
        @media (max-width: 768px) { .navbar-links { display: none; } .hero { padding: 100px 20px 60px; } .features { padding: 70px 20px; } .hero-logo { width: 280px; } }
        @media (max-width: 480px) { .hero-buttons { flex-direction: column; width: 100%; } .btn { width: 100%; text-align: center; } }
    </style></head><body>
    <nav class="navbar"><div class="container">
        <div class="navbar-logo"><img src="/static/logo.png" alt="حِصافة"></div>
        <div class="navbar-links">
            <a href="#features">المميزات</a>
            <a href="mailto:aalsuliman979@gmail.com">تواصل</a>
            <a href="/login" class="navbar-cta">تسجيل الدخول</a>
        </div>
    </div></nav>
    <section class="hero" id="heroSection">
        <div class="mouse-glow" id="mouseGlow"></div>
        <div class="hero-logo-wrapper"><img src="/static/logo.png" alt="حِصافة" class="hero-logo"></div>
        <h1>حوّل مصاريفك إلى  <span class="highlight">قرارات ذكية</span></h1>
        <p>من إدخال المصروف إلى القرار النهائي — بخطوات بسيطة</p>
        <div class="hero-buttons">
            <a href="/register" class="btn btn-primary">جرّب الآن مجانًا</a>
            <a href="#features" class="btn btn-secondary">اعرف أكثر</a>
        </div>
    </section>
    <section class="features" id="features">
        <div class="section-header"><span>المميزات</span><h2>كل شي تحتاجه بمكان وحد</h2>
        <p>حِصافة تحلل مصاريف شركتك تلقائيًا وتطلع لك رؤى وتوقعات تساعدك تتخذ القرار الصح بدل ما تغرق بالأرقام.</p></div>
        <div class="features-grid">
            <div class="feature-card"><div class="feature-icon">📊</div><h3>لوحة تحكم حية</h3><p>شوف إجمالي مصاريفك، مجمّعة حسب الفئة والشهر، بتحديث فوري.</p></div>
            <div class="feature-card"><div class="feature-icon">📈</div><h3>توقع ذكي</h3><p>نتوقع مصاريف الشهر الجاي بناءً على نمط إنفاقك السابق.</p></div>
            <div class="feature-card"><div class="feature-icon">🧠</div><h3>تحليل تلقائي</h3><p>نطلع لك ملاحظات فورية عن أي تغيّر ملحوظ بمصاريفك.</p></div>
        </div>
    </section>
    <footer class="footer" id="footer"><div class="footer-bottom">
        <p>© 2026 حِصافة — Financial Intelligence Platform</p>
        <p>جميع الحقوق محفوظة لحصافة</p>
    </div></footer>
    <script>
        const heroSection = document.getElementById('heroSection');
        const mouseGlow = document.getElementById('mouseGlow');
        heroSection.addEventListener('mousemove', function(e) {
            const rect = heroSection.getBoundingClientRect();
            mouseGlow.style.left = (e.clientX - rect.left) + 'px';
            mouseGlow.style.top = (e.clientY - rect.top) + 'px';
        });
    </script>
    </body></html>
    """
    return html

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    company_name = session.get("company_name") or session.get("username")

    total = get_total_expenses(user_id)
    by_category = get_totals_by_category(user_id)
    by_month = get_totals_by_month(user_id)
    forecast = forecast_next_month(user_id)
    insights = get_smart_insights(user_id)
    budget_alerts = check_budget_alerts(user_id)
    recommendations = get_recommendations(user_id)

    html = f"""
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, 'Segoe UI', system-ui, sans-serif; direction: rtl; background-color: #171b21; color: #e6e8eb; min-height: 100vh; }}
        .topbar {{ background-color: #1c2128; border-bottom: 1px solid #2b313a; padding: 14px 40px; display: flex; align-items: center; justify-content: space-between; }}
        .topbar-left {{ display: flex; align-items: center; gap: 12px; }}
        .topbar-logo img {{ height: 52px; display: block; }}
        .topbar .subtitle {{ font-size: 12px; color: #8b939d; }}
        .logout-link {{ color: #8b939d; font-size: 13px; text-decoration: none; }}
        .logout-link:hover {{ color: #e6e8eb; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 32px 40px 60px; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .stat-card {{ background-color: #1c2128; border: 1px solid #2b313a; border-radius: 12px; padding: 20px; animation: fadeIn 0.45s ease-out; transition: border-color 0.15s, transform 0.15s; }}
        .stat-card:hover {{ border-color: #2f81f7; transform: translateY(-4px); }}
        .stat-label {{ font-size: 12px; color: #8b939d; display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }}
        .stat-value {{ font-size: 26px; font-weight: 700; color: #fff; }}
        .stat-value.green {{ color: #3fb950; }}
        .stat-value.blue {{ color: #58a6ff; }}
        .stat-value.orange {{ color: #d29922; }}
        .section {{ background-color: #1c2128; border: 1px solid #2b313a; border-radius: 12px; padding: 22px; margin-bottom: 20px; animation: fadeIn 0.45s ease-out; }}
        .section-title {{ font-size: 13px; font-weight: 600; color: #8b939d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 14px; }}
        .row {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #262c34; font-size: 14px; }}
        .row:last-child {{ border-bottom: none; }}
        .row .amount {{ font-weight: 600; background-color: #171b21; padding: 4px 10px; border-radius: 6px; font-size: 13px; }}
        .insight-badge {{ padding: 12px 14px; background-color: #171b21; border: 1px solid #2b313a; border-radius: 8px; margin-bottom: 10px; font-size: 13.5px; color: #c9d1d9; }}
        .insight-badge:last-child {{ margin-bottom: 0; }}
        label {{ display: block; font-size: 12.5px; color: #8b939d; margin-bottom: 6px; font-weight: 500; }}
        .field {{ margin-bottom: 16px; }}
        .form-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
        select, input[type=text], input[type=number], input[type=date] {{ background-color: #171b21; color: #e6e8eb; padding: 10px 12px; border: 1px solid #2b313a; border-radius: 8px; width: 100%; font-size: 14px; }}
        input:focus, select:focus {{ outline: none; border-color: #2f81f7; }}
        input[type=submit] {{ background: linear-gradient(135deg, #2f81f7, #388bfd); color: white; padding: 11px 26px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; margin-top: 8px; }}
        input[type=submit]:hover {{ opacity: 0.9; }}
    </style></head><body>
    <div class="topbar">
        <div class="topbar-left">
            <div class="topbar-logo"><img src="/static/logo.png" alt="حِصافة"></div>
            <div class="subtitle">{company_name}</div>
        </div>
        <a href="/logout" class="logout-link">تسجيل الخروج</a>
    </div>
    <div class="container">
    """

    html += f"""
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-label">💰 إجمالي المصاريف</div><div class="stat-value green">{total}</div></div>
    """
    if forecast:
        html += f'<div class="stat-card"><div class="stat-label">📈 توقع الشهر الجاي</div><div class="stat-value blue">{forecast}</div></div>'
    html += f'<div class="stat-card"><div class="stat-label">📊 عدد الفئات</div><div class="stat-value orange">{len(by_category)}</div></div></div>'

    html += '<div class="section"><div class="section-title">📂 حسب الفئة</div>'
    for category, amount in by_category:
        html += f'<div class="row"><span>{category}</span><span class="amount">{amount}</span></div>'
    html += "</div>"

    html += '<div class="section"><div class="section-title">🗓️ حسب الشهر</div>'
    for month, amount in by_month:
        html += f'<div class="row"><span>{month}</span><span class="amount">{amount}</span></div>'
    html += "</div>"

    html += '<div class="section"><div class="section-title">🧠 تحليل ذكي</div>'
    for insight in insights:
        html += f'<div class="insight-badge">{insight}</div>'
    html += "</div>"

    html += '<div class="section"><div class="section-title">💰 تنبيهات الميزانية</div>'
    if budget_alerts:
        for alert in budget_alerts:
            html += f'<div class="insight-badge">{alert}</div>'
    else:
        html += '<div class="insight-badge">✅ كل الفئات ضمن الميزانية المتوقعة</div>'
    html += "</div>"

    html += '<div class="section"><div class="section-title">💡 توصيات</div>'
    for rec in recommendations:
        html += f'<div class="insight-badge">{rec}</div>'
    html += "</div>"

    html += """
    <div class="section">
        <div class="section-title">➕ إضافة مصروف جديد</div>
        <form method="POST" action="/add">
            <div class="form-grid">
                <div class="field"><label>المبلغ</label><input type="number" step="0.01" name="amount" required></div>
                <div class="field"><label>الفئة</label>
                    <select name="category" required>
                        <option value="">اختر الفئة</option>
                        <option value="Marketing">Marketing</option>
                        <option value="Salaries">Salaries</option>
                        <option value="Software">Software</option>
                        <option value="Utilities">Utilities</option>
                        <option value="Rent">Rent</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="field"><label>التاريخ</label><input type="date" name="date" required></div>
                <div class="field"><label>الوصف</label><input type="text" name="description"></div>
            </div>
            <input type="submit" value="إضافة المصروف">
        </form>
    </div>
    """

    html += "</div></body></html>"
    return html

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]
    description = request.form["description"]

    add_expense(user_id, amount, category, date, description)
    return redirect("/dashboard")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)