with open('public/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.terms-[^\{]+\{[^\}]+\})', css)
print(f"Found {len(matches)} .terms- rules in styles.css")
for m in matches[:8]:
    print(m[:100])
