with open(r'stitch_imported_screens_v2\html\11_Member_Portal___Founder_for_Founder_d8c04d20.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length:", len(text))
# Check header and top nav
header_match = re.search(r'<header[^>]*>(.*?)</header>', text, re.DOTALL)
if header_match:
    print("Header found:", header_match.group(0)[:400])

# Check main sections / cards
print("\nSections / Headings:")
for h in re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', text, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', h).strip()
    clean = ' '.join(clean.split())
    print(" - ", clean)

# Check buttons and tabs
print("\nButtons:")
for b in re.findall(r'<button[^>]*>(.*?)</button>', text, re.DOTALL)[:15]:
    clean = re.sub(r'<[^>]+>', '', b).strip()
    clean = ' '.join(clean.split())
    if clean:
        print(" [btn] ", clean[:50])
