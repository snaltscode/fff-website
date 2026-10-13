import os, re

screens = {
    'Terms': '01_Terms___Conditions___f4f_4a4c7e2e.html',
    'Privacy': '06_Privacy_Policy___f4f_29e2e2d0.html',
    'Refund': '03_Refund___Cancellation_Policy___f4f_b9f8844d.html',
    'Guidelines': '15_Community_Guidelines___f4f_3422b12a.html',
    '404': '04_404_Not_Found___f4f_e04be2a1.html'
}

for name, fname in screens.items():
    path = os.path.join('stitch_imported_screens_v2', 'html', fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"\n================ {name} ({len(content)} bytes) ================")
    m = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
    if m:
        main_html = m.group(1)
        headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', main_html)
        for h in headings[:8]:
            clean = re.sub(r'<[^>]+>', '', h).strip()
            print(" - ", clean)
    else:
        print("No main tag found")
