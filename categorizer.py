import csv

# Loads the category rules from the categories.csv file.
# This is used later when deciding what kind of purchase a receipt seems to contain.
def load_categories(file="categories.csv"):
    rules = []

    with open(file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append(
                (row["keyword"].strip().lower(), row["category"].strip().lower())
            )

    return rules


# Decides the category for one receipt based on its OCR text.
# In the full process, this is used after the receipt text has already been extracted and cleaned.
# The function first checks a few simple store-based rules, and if those do not match, it falls back to the keyword rules loaded from the csv file.
def categorize(text, rules):
    text = text.lower()

    if "lidl" in text or "k-superm" in text or "k-supermarket" in text:
        return "groceries"

    if "ikea" in text:
        return "household"

    for keyword, category in rules:
        if keyword in text:
            return category

    return "other"