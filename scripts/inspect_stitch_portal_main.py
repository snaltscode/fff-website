with open(r'stitch_imported_screens_v2\html\11_Member_Portal___Founder_for_Founder_d8c04d20.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Look at the main container
main = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
if main:
    main_html = main.group(1)
    print("Main tag found, length:", len(main_html))
    # print section tags and classes
    sections = re.findall(r'<section[^>]+class=\"([^\"]+)\"[^>]*>', main_html)
    print(f"Sections in Member Portal ({len(sections)}):")
    for s in sections:
        print("  - ", s[:80])
    
    # check headings inside main
    headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', main_html)
    print("\nHeadings in Member Portal:")
    for h in headings:
        print("  *", re.sub(r'<[^>]+>', '', h).strip())
