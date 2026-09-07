from db_helper import get_expenses_by_category

marketing_expenses = get_expenses_by_category("Marketing")

print("مصاريف Marketing فقط:")
for expense in marketing_expenses:
    print(expense)