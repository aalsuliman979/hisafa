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

def get_expenses_by_category(category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM expenses
    WHERE category = ?
    """, (category,))

    rows = cursor.fetchall()
    connection.close()
    return rows

def update_expense_amount(category, new_amount):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE expenses
    SET amount = ?
    WHERE category = ?
    """, (new_amount, category))
    connection.commit()
    connection.close()

def delete_expense_by_category(category):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM expenses
    WHERE category = ?
    """, (category,))
    connection.commit()
    connection.close()