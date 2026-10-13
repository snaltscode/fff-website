with open(r'stitch_imported_screens_v2\html\13_Admin_Console___Founder_for_Founder_80037861.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length:", len(text))
for h in re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', text, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', h).strip()
    clean = ' '.join(clean.split())
    try:
        print(" - ", clean)
    except Exception:
        pass
