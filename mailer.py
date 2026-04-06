import os
from RPA.Email.ImapSmtp import ImapSmtp

def send_report_email(
    attachments: list[str],
    subject: str = "Receipt Expense Report",
    body: str = "Attached are the generated receipt processing results.",
) -> None:
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_account = os.getenv("SMTP_ACCOUNT")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_SENDER")
    recipient = os.getenv("SMTP_RECIPIENT")

    if not all([smtp_server, smtp_account, smtp_password, sender, recipient]):
        raise ValueError(
            "Missing SMTP environment variables. "
            "Set SMTP_SERVER, SMTP_PORT, SMTP_ACCOUNT, SMTP_PASSWORD, "
            "SMTP_SENDER, and SMTP_RECIPIENT."
        )

    mail = ImapSmtp(smtp_server=smtp_server, smtp_port=smtp_port)
    mail.authorize(account=smtp_account, password=smtp_password)

    mail.send_message(
        sender=sender,
        recipients=recipient,
        subject=subject,
        body=body,
        attachments=attachments,
    )