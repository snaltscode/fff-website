with open(r'stitch_imported_screens_v2\html\09_Founder_for_Founder___Home__Mobile_21aec84f.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = text.find('CURATED')
if pos == -1:
    pos = text.find('Curated')
if pos != -1:
    print("Found around pos:", pos)
    print(text[pos-100:pos+200])
else:
    # search first 5 spans in main
    spans = re.findall(r'<span[^>]*>(.*?)</span>', text, re.DOTALL)
    for s in spans[:10]:
        print("Span:", re.sub(r'<[^>]+>', '', s).strip())
