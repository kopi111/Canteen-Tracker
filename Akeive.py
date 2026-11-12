# -----------------------------------------
# FILTERING FUNCTIONS
# -----------------------------------------

# build_choices(orders, column, first_choice):
# Builds a list of choices for a filter box using the values
# found in the specified column.
# Includes a first choice such as "All campuses" to allow
# users to view all available options.
# Requirement: R4.
def build_choices(orders, column, first_choice):
    choices = []
    for order in orders:
        value = order.get(column)
        if value is not None and value != "" and value not in choices:
            choices.append(value)
    choices.sort()
    return [first_choice] + choices


# filter_orders(orders, chosen_campus, chosen_category):
# Filters the orders based on the selected campus and category.
# Returns only orders that match both selected filter choices.
# Requirement: R4.
def filter_orders(orders, chosen_campus, chosen_category):
    shown = []
    for order in orders:
        campus_match = (
            chosen_campus in ("All campuses", "All Campuses", "All")
            or order.get("Campus") == chosen_campus
        )
        category_match = (
            chosen_category in ("All categories", "All Categories", "All")
            or order.get("Category") == chosen_category
        )
        if campus_match and category_match:
            shown.append(order)
    return shown


# -----------------------------------------
# EXPORT FUNCTION
# -----------------------------------------

# build_csv_text(shown):
# Converts the displayed orders into CSV (Comma-Separated Values) text.
# Allows users to download their filtered order data as a CSV file.
# Stretch Requirement.
def build_csv_text(shown):
    if not shown:
        return ""

    headers = list(shown[0].keys())
    lines = [",".join(str(header) for header in headers)]

    for order in shown:
        row_values = []
        for header in headers:
            value = str(order.get(header, ""))
            if "," in value or '"' in value:
                value = '"' + value.replace('"', '""') + '"'
            row_values.append(value)
        lines.append(",".join(row_values))

    return "\n".join(lines) + "\n"

