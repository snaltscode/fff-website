import os

with open('scratch_stitch_html.html', 'r', encoding='utf-8') as f:
    content = f.read()

main_start = content.find('<main')
main_end = content.find('</main>')
main = content[main_start:main_end]

os.makedirs('stitch_sections', exist_ok=True)

markers = [
    ("top_and_header", "<!-- Top Context Ribbon & Master Utilities -->", "<!-- Section 1: Executive KPI Summary Strip"),
    ("section1_kpis", "<!-- Section 1: Executive KPI Summary Strip", "<!-- Section 2: Membership Application Management Table"),
    ("section2_apps", "<!-- Section 2: Membership Application Management Table", "<!-- Section 3: System Audit & Security Logs Table"),
    ("section3_audit", "<!-- Section 3: System Audit & Security Logs Table", "<!-- Section 4: 16:9 Meeting Photos Gallery Manager"),
    ("section4_photos", "<!-- Section 4: 16:9 Meeting Photos Gallery Manager", "<!-- Section 5: Dynamic Media & Website Images CMS"),
    ("section5_cms", "<!-- Section 5: Dynamic Media & Website Images CMS", "<!-- Section 6: Event Creation & Ticketing Publisher"),
    ("section6_events", "<!-- Section 6: Event Creation & Ticketing Publisher", "<script>"),
    ("scripts", "<script>", "</main>")
]

for name, start_m, end_m in markers:
    s = main.find(start_m)
    if s == -1:
        print(f"Marker not found: {start_m}")
        continue
    e = main.find(end_m, s + len(start_m)) if end_m != "</main>" else len(main)
    chunk = main[s:e]
    with open(f'stitch_sections/{name}.html', 'w', encoding='utf-8') as out:
        out.write(chunk)
    print(f"Wrote stitch_sections/{name}.html ({len(chunk)} bytes)")
