with open(r'stitch_imported_screens_v2\html\07_Admissions_Questionnaire___Founder_for_Founder_975ae924.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find form or card contents
blocks = re.findall(r'<div class="([^"]*rounded-[^"]*)"[^>]*>(.*?)</div>', html, re.DOTALL)
print(f"Found {len(blocks)} rounded blocks")
for cls, content in blocks[:8]:
    title = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', content)
    t_text = re.sub(r'<[^>]+>', '', title.group(1)).strip() if title else 'No heading'
    print(f"Block [{cls[:50]}]: {t_text}")

# Check specific questions or field groups
print("\nForm inputs and names:")
for m in re.finditer(r'<(input|select|textarea)[^>]+(placeholder|name|id)=\"([^\"]+)\"[^>]*>', html):
    print(m.group(0)[:120])
