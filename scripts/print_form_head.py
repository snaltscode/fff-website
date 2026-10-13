with open(r'stitch_imported_screens_v2\html\07_Admissions_Questionnaire___Founder_for_Founder_975ae924.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
form_match = re.search(r'<form[^>]*>(.*?)</form>', text, re.DOTALL)
if form_match:
    lines = form_match.group(0).split('\n')
    print(f"Form has {len(lines)} lines")
    # Print the first 100 lines and some key parts
    for line in lines[:80]:
        print(line[:120])
