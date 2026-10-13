import os, re

files = [
    ('Terms', '01_Terms___Conditions___f4f_4a4c7e2e.html', 'src/app/terms/page.tsx', 'src/app/terms-and-conditions/page.tsx'),
    ('Privacy', '06_Privacy_Policy___f4f_29e2e2d0.html', 'src/app/privacy-policy/page.tsx', None),
    ('Refund', '03_Refund___Cancellation_Policy___f4f_b9f8844d.html', 'src/app/refund-policy/page.tsx', 'src/app/refund-and-cancellation-policy/page.tsx'),
    ('Guidelines', '15_Community_Guidelines___f4f_3422b12a.html', 'src/app/community-guidelines/page.tsx', 'src/app/guidelines/page.tsx'),
]

for label, src_file, dest1, dest2 in files:
    src_path = os.path.join('stitch_imported_screens_v2', 'html', src_file)
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    body_m = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_m:
        print(f"[{label}] Found body: {len(body_m.group(1))} chars. Target: {dest1}")
    else:
        print(f"[{label}] NO body found in {src_file}")
