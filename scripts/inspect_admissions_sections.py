with open(r'stitch_imported_screens_v2\html\07_Admissions_Questionnaire___Founder_for_Founder_975ae924.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Look at the form cards and headlines
sections = re.findall(r'<section[^>]*>(.*?)</section>', text, re.DOTALL)
print(f"Total sections: {len(sections)}")
for i, s in enumerate(sections):
    h = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', s, re.DOTALL)
    h_text = [re.sub(r'<[^>]+>', '', x).strip() for x in h]
    print(f"Section {i+1}:", h_text)

# Also let's inspect the entire form wrapper
form_match = re.search(r'<form[^>]*>(.*?)</form>', text, re.DOTALL)
if form_match:
    print("\nForm tag found! Length:", len(form_match.group(1)))
    # print all field labels or titles
    for m in re.finditer(r'<h[3-5][^>]*>(.*?)</h[3-5]>', form_match.group(1), re.DOTALL):
        print("  - Field/Group:", re.sub(r'<[^>]+>', '', m.group(1)).strip())
else:
    print("No explicit <form> tag, searching container div...")
    main_match = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
    if main_match:
        print("Main tag length:", len(main_match.group(1)))
