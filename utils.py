import re


def clean_lines(text):
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def normalize_store(store):
    s = store.lower()

    if "lidl" in s:
        return "Lidl"
    if "k-superm" in s or "k-supermarket" in s:
        return "K-Supermarket"
    if "ikea" in s:
        return "IKEA"

    return store


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