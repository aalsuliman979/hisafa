import sqlite3

def get_connection():
    connection = sqlite3.connect("hisafa.db")
    return connection

def get_all_expenses():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print("خطأ في جلب البيانات:", e)
        return []

def add_expense(amount, category, date, description):
    if not isinstance(amount, (int, float)) or amount <= 0:
        print("خطأ: المبلغ لازم يكون رقم أكبر من صفر")
        return False
    if not category or not date:
        print("خطأ: الفئة والتاريخ مطلوبين")
        return False

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
        """, (amount, category, date, description))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print("خطأ في إضافة المصروف:", e)
        return False

def get_expenses_by_category(category):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM expenses
        WHERE category = ?
        """, (category,))
        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print("خطأ في الفلترة:", e)
        return []

def update_expense_amount(category, new_amount):
    if not isinstance(new_amount, (int, float)) or new_amount <= 0:
        print("خطأ: المبلغ الجديد لازم يكون رقم أكبر من صفر")
        return False

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE expenses
        SET amount = ?
        WHERE category = ?
        """, (new_amount, category))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print("خطأ في التعديل:", e)
        return False

def delete_expense_by_category(category):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM expenses
        WHERE category = ?
        """, (category,))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print("خطأ في الحذف:", e)
        return False

def get_total_expenses():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses")
        result = cursor.fetchone()
        connection.close()
        return result[0] if result[0] else 0
    except sqlite3.Error as e:
        print("خطأ في حساب الإجمالي:", e)
        return 0

def get_totals_by_category():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        """)
        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print("خطأ في التجميع:", e)
        return []

def get_totals_by_month():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM expenses
        GROUP BY month
        """)
        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print("خطأ في التجميع الشهري:", e)
        return []