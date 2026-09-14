import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    connection = sqlite3.connect("hisafa.db")
    return connection

def init_tables():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        company_name TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    connection.commit()
    connection.close()

def create_user(username, password, company_name):
    if not username or not password:
        return False, "اسم المستخدم وكلمة المرور مطلوبين"
    if len(password) < 6:
        return False, "كلمة المرور لازم تكون 6 أحرف على الأقل"

    try:
        connection = get_connection()
        cursor = connection.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute("""
        INSERT INTO users (username, password_hash, company_name)
        VALUES (?, ?, ?)
        """, (username, password_hash, company_name))
        connection.commit()
        connection.close()
        return True, "تم إنشاء الحساب بنجاح"
    except sqlite3.IntegrityError:
        return False, "اسم المستخدم مستخدم من قبل"
    except sqlite3.Error as e:
        return False, f"خطأ: {e}"

def authenticate_user(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password_hash, company_name FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        connection.close()

        if user and check_password_hash(user[2], password):
            return {"id": user[0], "username": user[1], "company_name": user[3]}
        return None
    except sqlite3.Error:
        return None

def add_expense(user_id, amount, category, date, description):
    if not isinstance(amount, (int, float)) or amount <= 0:
        return False
    if not category or not date:
        return False

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, amount, category, date, description))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error:
        return False

def get_all_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_total_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result[0] else 0

def get_totals_by_category(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT category, SUM(amount) FROM expenses
    WHERE user_id = ?
    GROUP BY category
    """, (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_totals_by_month(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses
    WHERE user_id = ?
    GROUP BY month
    """, (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def forecast_next_month(user_id):
    monthly_totals = get_totals_by_month(user_id)
    if len(monthly_totals) < 2:
        return None
    last_month_amount = monthly_totals[-1][1]
    previous_month_amount = monthly_totals[-2][1]
    growth_rate = (last_month_amount - previous_month_amount) / previous_month_amount
    return round(last_month_amount * (1 + growth_rate), 2)

def get_smart_insights(user_id):
    monthly_totals = get_totals_by_month(user_id)
    if len(monthly_totals) < 2:
        return ["لسه ما فيه بيانات كافية لتحليل الاتجاه (تحتاج شهرين على الأقل)"]

    last_month, last_amount = monthly_totals[-1]
    previous_month, previous_amount = monthly_totals[-2]
    change = ((last_amount - previous_amount) / previous_amount) * 100

    insights = []
    if change > 15:
        insights.append(f"⚠️ مصاريف {last_month} زادت بنسبة {change:.1f}% مقارنة بـ{previous_month} - يستاهل مراجعة")
    elif change > 0:
        insights.append(f"مصاريف {last_month} زادت بنسبة طفيفة ({change:.1f}%) مقارنة بـ{previous_month}")
    elif change < -15:
        insights.append(f"✅ مصاريف {last_month} انخفضت بنسبة {abs(change):.1f}% مقارنة بـ{previous_month} - أداء ممتاز")
    else:
        insights.append(f"مصاريف {last_month} مستقرة نسبيًا مقارنة بـ{previous_month} ({change:.1f}%)")

    by_category = get_totals_by_category(user_id)
    if by_category:
        highest_category = max(by_category, key=lambda x: x[1])
        insights.append(f"أعلى فئة إنفاق: {highest_category[0]} بمبلغ {highest_category[1]}")

    return insights

def get_category_percentages(user_id):
    total = get_total_expenses(user_id)
    if total == 0:
        return []
    by_category = get_totals_by_category(user_id)
    return [(cat, amt, round((amt / total) * 100, 1)) for cat, amt in by_category]

def check_budget_alerts(user_id, budget_limits=None):
    if budget_limits is None:
        budget_limits = {"Marketing": 5000, "Salaries": 20000, "Software": 2000, "Utilities": 2000}

    by_category = get_totals_by_category(user_id)
    alerts = []
    for category, amount in by_category:
        limit = budget_limits.get(category, 3000)
        if amount > limit:
            over = ((amount - limit) / limit) * 100
            alerts.append(f"🔴 تجاوزت ميزانية {category} بنسبة {over:.0f}% (المصروف: {amount}, الحد المتوقع: {limit})")
        elif amount > limit * 0.85:
            alerts.append(f"🟡 اقتربت من حد ميزانية {category} ({amount} من أصل {limit})")
    return alerts

def get_recommendations(user_id):
    recommendations = []
    percentages = get_category_percentages(user_id)

    for category, amount, percentage in percentages:
        if percentage > 45:
            recommendations.append(f"💡 فئة {category} تستحوذ على {percentage}% من إجمالي مصاريفك — نسبة مرتفعة تستحق المراجعة")

    monthly_totals = get_totals_by_month(user_id)
    if len(monthly_totals) >= 2:
        last_month, last_amount = monthly_totals[-1]
        previous_month, previous_amount = monthly_totals[-2]
        change = ((last_amount - previous_amount) / previous_amount) * 100
        if change > 20:
            recommendations.append(f"💡 النمو المتسارع في المصاريف ({change:.1f}%) قد يشير لحاجتك لمراجعة الميزانية الشهرية")

    if not recommendations:
        recommendations.append("✅ لا توجد ملاحظات حرجة حاليًا — إنفاقك يبدو متوازنًا")

    return recommendations