import csv
from collections import defaultdict
import matplotlib.pyplot as plt


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