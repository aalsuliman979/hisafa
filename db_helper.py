import sqlite3

def get_connection():
    connection = sqlite3.connect("hisafa.db")
    return connection
def get_all_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    connection.close()
    return rows
def add_expense(amount, category, date, description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO expenses (amount, category, date, description)
    VALUES (?, ?, ?, ?)
    """, (amount, category, date, description))

    connection.commit()
    connection.close()