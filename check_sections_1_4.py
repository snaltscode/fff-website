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
    e = main.find(end_str, s + len(start_str)) if end_str else s + 2000
    sub = main[s:e]
    # find form inputs
    inputs = re.findall(r'<(?:input|select|textarea|button|table|tbody|form)[^>]*>', sub)
    print(f"Inputs/Controls ({len(inputs)}):")
    for inp in inputs[:15]:
        print("  ", inp[:120])
    print("\nText snippet (first 600 chars):")
    print(sub[:600])

print_section("Section 1: KPIs", "<!-- Section 1: Executive KPI Summary Strip", "<!-- Section 2:")
print_section("Section 2: Applications", "<!-- Section 2: Membership Application Management Table", "<!-- Section 3:")
print_section("Section 3: Audit Logs", "<!-- Section 3: System Audit & Security Logs", "<!-- Section 4:")
print_section("Section 4: Meeting Photos", "<!-- Section 4: 16:9 Meeting Photos Gallery Manager", "<!-- Section 5:")
