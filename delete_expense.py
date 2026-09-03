import sqlite3

connection = sqlite3.connect("hisafa.db")
cursor = connection.cursor()

cursor.execute("""
DELETE FROM expenses
WHERE category = ?
""", ("Utilities",))

connection.commit()

print("تم حذف المصروف")

connection.close()