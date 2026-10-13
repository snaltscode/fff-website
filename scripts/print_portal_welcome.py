with open(r'stitch_imported_screens_v2\html\11_Member_Portal___Founder_for_Founder_d8c04d20.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
main = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
if main:
    main_html = main.group(1)
    # Let's inspect the hero banner / welcome area
    print("=== WELCOME / HEADER AREA ===")
    print(main_html[:2000])
