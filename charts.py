import csv
from collections import defaultdict
import matplotlib.pyplot as plt


# Reads the processed receipt data from the csv file and creates a chart that shows how much money was spent in each category.
# In the full process, this is used after the receipt data has already been extracted and saved into structured form.
def generate_category_chart(csv_file: str, output_path: str) -> dict[str, float]:
    totals = defaultdict(float)

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row["Category"]
            total = float(row["Total"])
            totals[category] += total

    categories = list(totals.keys())
    values = list(totals.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, values)
    plt.xlabel("Category")
    plt.ylabel("Total (€)")
    plt.title("Expenses by Category")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return dict(totals)

# Same basic thing as the category chart function, but here the totals are grouped by store instead of category.
# It is part of the reporting side of the project, because it turns the collected receipt data into a more visual summary.
def generate_store_chart(csv_file: str, output_path: str) -> dict[str, float]:
    totals = defaultdict(float)

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            store = row["Store"]
            total = float(row["Total"])
            totals[store] += total

    stores = list(totals.keys())
    values = list(totals.values())

    plt.figure(figsize=(8, 5))
    plt.bar(stores, values)
    plt.xlabel("Store")
    plt.ylabel("Total (€)")
    plt.title("Expenses by Store")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return dict(totals)