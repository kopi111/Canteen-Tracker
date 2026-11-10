def is_number(value):
    # True for 1200 or 2.5. False for None, text like "J$1,200", and True/False.
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# add_totals(orders, order_row_numbers):
# Calculates the total for each order by multiplying Price by Quantity.
# Skips rows with invalid data and records the reason why each row was skipped.
def add_totals(orders, order_row_numbers):
    good_orders = []
    skipped_rows = []

    for index in range(len(orders)):
        order = orders[index]
        row_number = order_row_numbers[index]
        price = order["Price"]
        quantity = order["Quantity"]

        reasons = []
        if price is None:
            reasons.append("Price is missing")
        elif not is_number(price):
            reasons.append("Price is not a number")
        if quantity is None:
            reasons.append("Quantity is missing")
        elif not is_number(quantity):
            reasons.append("Quantity is not a number")

        if len(reasons) == 0:
            order["Total"] = price * quantity
            good_orders.append(order)
        else:
            skipped_rows.append({"Row": row_number, "Reason": " and ".join(reasons)})

    return good_orders, skipped_rows


# calculate_summary(shown):
# Calculates and returns the total sales, number of orders,
# and average order value from the displayed orders.
def calculate_summary(shown):
    total_sales = 0
    for order in shown:
        total_sales = total_sales + order["Total"]

    number_of_orders = len(shown)
    if number_of_orders > 0:
        average_order = total_sales / number_of_orders
    else:
        average_order = 0

    return total_sales, number_of_orders, average_order


# add_up_by(shown, group_column, amount_column):
# Groups the data using a dictionary and adds up the values
# for each group.
# Used to calculate sales by item, identify best sellers,
# and prepare data for the daily sales chart.
def add_up_by(shown, group_column, amount_column):
    totals = {}
    for order in shown:
        group = order[group_column]
        if group in totals:
            totals[group] = totals[group] + order[amount_column]
        else:
            totals[group] = order[amount_column]
    return totals


# find_best_seller(shown):
# Finds and returns the item with the highest total quantity sold.
def find_best_seller(shown):
    quantity_by_item = add_up_by(shown, "Item", "Quantity")

    best_item = None
    best_quantity = 0
    for item in quantity_by_item:
        if quantity_by_item[item] > best_quantity:
            best_item = item
            best_quantity = quantity_by_item[item]

    return best_item, best_quantity


# count_orders_per_range(shown):
# Counts the number of orders within each J$500 price range.
# Used to create the order value histogram.
def count_orders_per_range(shown):
    range_counts = {}
    for order in shown:
        range_start = int((order["Total"] // 500) * 500)
        if range_start in range_counts:
            range_counts[range_start] = range_counts[range_start] + 1
        else:
            range_counts[range_start] = 1

    # Fill empty ranges with 0 so the histogram has no gaps
    if len(range_counts) > 0:
        for start in range(0, max(range_counts) + 500, 500):
            if start not in range_counts:
                range_counts[start] = 0

    return range_counts