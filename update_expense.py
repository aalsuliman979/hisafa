import sqlite3

connection = sqlite3.connect("hisafa.db")
cursor = connection.cursor()

cursor.execute("""
UPDATE expenses
SET amount = ?
WHERE category = ?
""", (500, "Software"))

connection.commit()

print("تم تعديل المصروف")

connection.close()