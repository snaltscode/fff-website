with open(r'stitch_imported_screens_v2\html\01_Terms___Conditions___f4f_4a4c7e2e.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
if m:
    lines = m.group(0).split('\n')
    print("Main has", len(lines), "lines")
    for line in lines[:30]:
        print(line[:120])
