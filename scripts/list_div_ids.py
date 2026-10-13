with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sections = re.findall(r'<div[^>]+id=\"([^\"]+)\"[^>]*>', text)
print("All major top-level div IDs:")
for s in sections:
    if any(k in s.lower() for k in ['portal', 'admin', 'member', 'page', 'dashboard', 'public']):
        print(" - ", s)
