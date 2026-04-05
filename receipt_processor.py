# gonna keep all main logic here

import os
import csv
from ocr import extract_text
from categorizer import load_categories, categorize
from utils import extract_date, extract_store, extract_total
from RPA.Archive import Archive

OUTPUT_FILE = "output/expenses.csv"
RECEIPTS_DIR = "receipts"

def process_all_receipts():
    rules = load_categories()

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Store", "Date", "Total", "Category"])

        for filename in os.listdir(RECEIPTS_DIR):
            path = os.path.join(RECEIPTS_DIR, filename)

            text = extract_text(path)

            store = extract_store(text)
            date = extract_date(text)
            total = extract_total(text)
            category = categorize(text, rules)

            writer.writerow([store, date, total, category])

    archive_receipts()

def archive_receipts():
    archive = Archive()
    archive.archive_folder_with_zip(
        folder=RECEIPTS_DIR,
        archive_name="output/receipts.zip",
        recursive=True
    )