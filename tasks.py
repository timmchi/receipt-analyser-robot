from robocorp.tasks import task
from receipt_processor import process_all_receipts

@task
def process_receipts():
    process_all_receipts()
