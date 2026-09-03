import sqlite3

connection = sqlite3.connect("hisafa.db")
cursor = connection.cursor()

cursor.execute("""
SELECT * FROM expenses
WHERE category = ?
""", ("Marketing",))

rows = cursor.fetchall()

print("مصاريف Marketing فقط:")
for row in rows:
    print(row)
cursor.execute("""
SELECT * FROM expenses
WHERE amount > ?
""", (1000,))

rows = cursor.fetchall()

print("\nالمصاريف الأكبر من 1000 ريال:")
for row in rows:
    print(row)

cursor.execute("""
SELECT * FROM expenses
WHERE category = ? AND amount > ?
""", ("Marketing", 1000))

rows = cursor.fetchall()

print("\nمصاريف Marketing الأكبر من 1000 ريال:")
for row in rows:
    print(row)
connection.close()