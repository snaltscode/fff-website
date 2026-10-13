with open(r'stitch_imported_screens_v2\html\01_Terms___Conditions___f4f_4a4c7e2e.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length:", len(text))
body = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL)
if body:
    print("Body length:", len(body.group(1)))
    # Inspect header and main layout
    for tag in ['header', 'nav', 'main', 'footer']:
        m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', body.group(1), re.DOTALL)
        if m:
            print(f"Tag <{tag}> found: length {len(m.group(0))}")
