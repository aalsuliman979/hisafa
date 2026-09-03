import sqlite3

connection = sqlite3.connect("hisafa.db")
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

cursor.execute("""
INSERT INTO expenses (amount, category, date, description)
VALUES (?, ?, ?, ?)
""", (2500, "Marketing", "2026-08-19", "Google Ads"))

new_expenses = [
    (8500, "Salaries", "2026-08-01", "August Salaries"),
    (450, "Software", "2026-08-10", "Adobe Subscription"),
    (1200, "Utilities", "2026-08-15", "Electricity Bill")
]

for expense in new_expenses:
    cursor.execute("""
    INSERT INTO expenses (amount, category, date, description)
    VALUES (?, ?, ?, ?)
    """, expense)

connection.commit()
connection.close()

print("تم إنشاء قاعدة البيانات والجدول بنجاح")
print("تم إضافة مصاريف جديدة")