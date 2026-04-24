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