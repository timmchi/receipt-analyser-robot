import csv

def load_categories(file="categories.csv"):
    rules = {}

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules[row["keyword"]] = row["category"]

    return rules


def categorize(text, rules):
    text = text.lower()

    for keyword, category in rules.items():
        if keyword in text:
            return category

    return "other"