with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<h[1-3][^>]+class=\"([^\"]*text-headline-[^\"]*)\"[^>]*>', text)
print(f"Found {len(matches)} headline classes:")
for m in set(matches):
    print(" - ", m)
