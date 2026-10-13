with open('public/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.portal-[^\{]+\{[^\}]+\})', css)
print(f"Portal CSS classes ({len(matches)}):")
for m in matches[:10]:
    print(m[:100])
