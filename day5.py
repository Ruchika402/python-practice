# ===== REGULAR EXPRESSIONS =====
import re

# 1. Basic patterns: search, match, findall, fullmatch
text = "Contact us at support@example.com or sales@company.org for help."

# re.search — find first match anywhere in string
match = re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text)
if match:
    print(f"First email: {match.group()}")    # support@example.com
    print(f"Start:End  : {match.start()}:{match.end()}")

# re.findall — find ALL non-overlapping matches
emails = re.findall(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text)
print(f"All emails: {emails}")   # ['support@example.com', 'sales@company.org']

# re.match — only matches at BEGINNING of string
print(re.match(r'Contact', text))     # Match object
print(re.match(r'support', text))     # None — not at start

# re.fullmatch — entire string must match
print(re.fullmatch(r'\d{4}', '2024'))    # Match
print(re.fullmatch(r'\d{4}', '20245'))   # None





# Common regex patterns
patterns = {
    "phone_IN"  : r'[6-9]\d{9}',                     # Indian mobile
    "pin_code"  : r'\b[1-9][0-9]{5}\b',              # Indian PIN
    "url"       : r'https?://[\w./-]+',
    "date_dmy"  : r'\b\d{1,2}/\d{1,2}/\d{4}\b',
    "ipv4"      : r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "username"  : r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$',
}

test_cases = {
    "phone_IN"  : "Call 9876543210 now",
    "url"       : "Visit https://docs.python.org/3/library/re.html",
    "ipv4"      : "Server at 192.168.1.100",
    "username"  : "dev_user123",
}

for key, test in test_cases.items():
    m = re.search(patterns[key], test)
    print(f"{key:12}: {m.group() if m else 'no match'}")