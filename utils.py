import re

# small cleaning step for the OCR text.
# It removes extra empty lines and whitespace so the later extraction functions have a cleaner version of the receipt text to work with.
def clean_lines(text):
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]

# Normalizes store names into one consistent form. In the full process, this is used so that small OCR differences don't create many different versions of the same store in the final output.
def normalize_store(store):
    s = store.lower()

    if "lidl" in s:
        return "Lidl"
    if "k-superm" in s or "k-supermarket" in s:
        return "K-Supermarket"
    if "ikea" in s:
        return "IKEA"

    return store

# Tries to find the store name from the OCR text.
#It checks the first part of the receipt text, because that is where the store name usually appears. If a known store is found, the value is normalized before it is returned.
def extract_store(text):
    lines = clean_lines(text)

    for line in lines[:12]:
        low = line.lower()

        if "lidl" in low:
            return normalize_store(line)

        if "k-superm" in low or "k-supermarket" in low:
            return normalize_store(line)

        if "ikea" in low:
            return normalize_store(line)

    joined = "\n".join(lines[:12]).lower()

    if "lidl" in joined:
        return "Lidl"
    if "k-superm" in joined or "k-supermarket" in joined:
        return "K-Supermarket"
    if "ikea" in joined:
        return "IKEA"

    return "unknown"

# Tries to extract the receipt date from the OCR text.
# It checks a few common date formats and returns the first match it finds.
# If no date is found, it returns "unknown" so the main process can continue.
def extract_date(text):
    patterns = [
        r"\b\d{1,2}\.\d{1,2}\.\d{4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return "unknown"

# Tries to find the total amount from the receipt text.
# It first looks for lines that usually appear near the total, and if that doesn't work, it falls back to the last matching amount in the text.
# This is part of the data extraction step before the values are written into the final csv output.
def extract_total(text):
    lines = clean_lines(text)

    for i, line in enumerate(lines):
        low = line.lower()
        if "yhteensä" in low or "debit" in low or "korttimaksu" in low:
            combined = line
            if i + 1 < len(lines):
                combined += " " + lines[i + 1]

            amounts = re.findall(r"\d+[.,]\d{2}", combined)
            if amounts:
                return amounts[-1].replace(",", ".")

    matches = re.findall(r"\d+[.,]\d{2}", text)
    if matches:
        return matches[-1].replace(",", ".")

    return "0.00"