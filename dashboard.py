from db_helper import get_total_expenses, get_totals_by_category

total = get_total_expenses()
print("إجمالي المصاريف:", total)

totals_by_category = get_totals_by_category()
print("\nالمصاريف حسب الفئة:")
for category, amount in totals_by_category:
    print(category, ":", amount)

from db_helper import get_totals_by_month

totals_by_month = get_totals_by_month()
print("\nالمصاريف حسب الشهر:")
for month, amount in totals_by_month:
    print(month, ":", amount)