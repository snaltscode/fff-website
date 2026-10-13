with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
p1 = text.find('id="portalPage"')
p2 = text.find('<!-- FOOTER', p1) if text.find('<!-- FOOTER', p1) != -1 else text.find('id="adminSection"', p1)
if p2 == -1:
    p2 = text.find('id="showInterestModal"', p1)

portal_html = text[p1:p2]
ids = re.findall(r'id=\"([^\"]+)\"', portal_html)
print(f"Total IDs in portalPage ({len(ids)}):")
for i in ids:
    print(" - ", i)
