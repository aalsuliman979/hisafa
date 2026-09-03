import sqlite3

connection = sqlite3.connect("hisafa.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM expenses")

rows = cursor.fetchall()

print("كل المصاريف المخزنة في قاعدة البيانات:")
for row in rows:
    print(row)

connection.close()