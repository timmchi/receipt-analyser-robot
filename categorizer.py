import csv


def load_categories(file="categories.csv"):
    rules = []

    with open(file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append(
                (row["keyword"].strip().lower(), row["category"].strip().lower())
            )

    return rules


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