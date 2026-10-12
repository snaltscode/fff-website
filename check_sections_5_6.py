import re

with open('scratch_stitch_html.html', 'r', encoding='utf-8') as f:
    content = f.read()

main_start = content.find('<main')
main_end = content.find('</main>')
main = content[main_start:main_end]

def print_section(title, start_str, end_str):
    print(f"\n==================== {title} ====================")
    s = main.find(start_str)
    if s == -1:
        print("NOT FOUND:", start_str)
        return
    e = main.find(end_str, s + len(start_str)) if end_str else s + 4000
    sub = main[s:e]
    # find form inputs
    inputs = re.findall(r'<(?:input|select|textarea|button|table|tbody|form)[^>]*>', sub)
    print(f"Inputs/Controls ({len(inputs)}):")
    for inp in inputs[:25]:
        print("  ", inp[:120])

print_section("Section 5: Dynamic Media CMS", "<!-- Section 5: Dynamic Media & Website Images CMS", "<!-- Section 6:")
print_section("Section 6: Event Publisher", "<!-- Section 6: Event Creation & Ticketing Publisher", "</main>")
