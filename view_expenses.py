from db_helper import get_all_expenses

expenses = get_all_expenses()

print("كل المصاريف المخزنة في قاعدة البيانات:")
for expense in expenses:
    print(expense)