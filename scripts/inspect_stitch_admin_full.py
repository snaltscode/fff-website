with open(r'stitch_imported_screens_v2\html\13_Admin_Console___Founder_for_Founder_80037861.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print(f"Stitch Admin Console length: {len(text)}")
sections = re.findall(r'<section[^>]*>(.*?)</section>', text, re.DOTALL)
print(f"Sections found ({len(sections)}):")
for i, s in enumerate(sections):
    h = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', s, re.DOTALL)
    h_clean = [re.sub(r'<[^>]+>', '', x).strip() for x in h]
    print(f"Section {i+1}:", h_clean)

# Also check forms, tables, buttons
tables = re.findall(r'<table[^>]*>', text)
print(f"Tables: {len(tables)}")
forms = re.findall(r'<form[^>]*>', text)
print(f"Forms: {len(forms)}")
