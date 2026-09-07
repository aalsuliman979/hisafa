from db_helper import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("DELETE FROM expenses WHERE id IN (25, 26, 27)")

connection.commit()
connection.close()

print("تم حذف الصفوف المكررة")