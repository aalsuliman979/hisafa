expenses = [
    {
        "amount": 2500,
        "category": "Marketing",
        "date": "2026-08-19",
        "description": "Google Ads"
    },
    {
        "amount": 8500,
        "category": "Salaries",
        "date": "2026-08-01",
        "description": "August Salaries"
    },
    {
        "amount": 450,
        "category": "Software",
        "date": "2026-08-10",
        "description": "Adobe Subscription"
    }
]

print("كل المصاريف:")
for expense in expenses:
    print(expense)

# حساب المجموع الكلي
total = 0
for expense in expenses:
    total = total + expense["amount"]

print("\nإجمالي المصاريف:", total)

# حساب المجموع حسب كل فئة
totals_by_category = {}

for expense in expenses:
    category = expense["category"]
    amount = expense["amount"]

    if category in totals_by_category:
        totals_by_category[category] = totals_by_category[category] + amount
    else:
        totals_by_category[category] = amount

print("\nالمصاريف حسب الفئة:")
for category in totals_by_category:
    print(category, ":", totals_by_category[category])