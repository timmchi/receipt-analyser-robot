# gonna keep all main logic here

import csv
import os
from RPA.Archive import Archive

from ocr import extract_text
from utils import extract_store, extract_date, extract_total
from categorizer import load_categories, categorize
from charts import generate_category_chart, generate_store_chart
from report import create_pdf_report
from mailer import send_report_email


RECEIPTS_DIR = "receipts"
OUTPUT_DIR = "output"
EXPENSES_CSV = os.path.join(OUTPUT_DIR, "expenses.csv")
CATEGORY_CHART = os.path.join(OUTPUT_DIR, "category_chart.png")
STORE_CHART = os.path.join(OUTPUT_DIR, "store_chart.png")
REPORT_PDF = os.path.join(OUTPUT_DIR, "report.pdf")
ARCHIVE_ZIP = os.path.join(OUTPUT_DIR, "receipts.zip")


def process_all_receipts() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rules = load_categories()

    with open(EXPENSES_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Store", "Date", "Total", "Category"])

        for filename in os.listdir(RECEIPTS_DIR):
            path = os.path.join(RECEIPTS_DIR, filename)

            if not os.path.isfile(path):
                continue

            text = extract_text(path)
            store = extract_store(text)
            date = extract_date(text)
            total = extract_total(text)
            category = categorize(text, rules)

            writer.writerow([store, date, total, category])

    category_totals = generate_category_chart(EXPENSES_CSV, CATEGORY_CHART)
    store_totals = generate_store_chart(EXPENSES_CSV, STORE_CHART)

    create_pdf_report(
        category_totals=category_totals,
        store_totals=store_totals,
        chart_files=[CATEGORY_CHART, STORE_CHART],
        output_file=REPORT_PDF,
    )

    archive_receipts()
    email_outputs()


def archive_receipts() -> None:
    archive = Archive()
    archive.archive_folder_with_zip(
        folder=RECEIPTS_DIR,
        archive_name=ARCHIVE_ZIP,
        recursive=True,
    )


def email_outputs() -> None:
    send_report_email(
        attachments=[REPORT_PDF, EXPENSES_CSV, ARCHIVE_ZIP],
        subject="Automated Receipt Report",
        body="All of the required files are attached",
    )