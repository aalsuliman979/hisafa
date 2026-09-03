import sqlite3

connection = sqlite3.connect("hisafa.db")
cursor = connection.cursor()

cursor.execute("DELETE FROM expenses")
connection.commit()
connection.close()

print("تم تنظيف الجدول بالكامل")