with open(r'stitch_imported_screens_v2\html\09_Founder_for_Founder___Home__Mobile_21aec84f.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
if m:
    lines = m.group(1).split('\n')
    print("Top of main in mobile Stitch:")
    for l in lines[:40]:
        print(l[:120])
