with open(r'stitch_imported_screens_v2\html\04_404_Not_Found___f4f_e04be2a1.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("404 Screen:")
for p in re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)[:5]:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    print(" P:", clean)
for h in re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', text, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', h).strip()
    print(" H:", clean)
