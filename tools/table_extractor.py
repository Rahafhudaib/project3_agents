import re


def extract_numbers(text):
    matches = re.findall(r"-?\d+\.?\d*%?", text)
    numbers = []
    for m in matches:
        try:
            numbers.append(float(m.replace("%", "")))
        except ValueError:
            continue
    return numbers


def extract_tables(text):
    lines = text.split("\n")
    tables = []
    current = []
    for line in lines:
        if "|" in line:
            row = [c.strip() for c in line.split("|") if c.strip()]
            if row:
                current.append(row)
        else:
            if current:
                tables.append(current)
                current = []
    if current:
        tables.append(current)
    return tables
