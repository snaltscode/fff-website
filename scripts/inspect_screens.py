import os, re

def inspect_screen(filename):
    filepath = os.path.join('stitch_imported_screens_v2', 'html', filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    print(f"\n==================== {filename} ({len(html)} bytes) ====================")
    headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.DOTALL)
    print("Headings:")
    for h in headings[:10]:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        clean = ' '.join(clean.split())
        print(f"  - {clean}")
    
    inputs = re.findall(r'<(input|select|textarea|button)[^>]+>', html)
    print(f"Inputs count: {len(inputs)}")
    
    # Check for labels or form groups
    labels = re.findall(r'<label[^>]*>(.*?)</label>', html, re.DOTALL)
    print("Sample labels:")
    for l in labels[:12]:
        clean = re.sub(r'<[^>]+>', '', l).strip()
        clean = ' '.join(clean.split())
        print(f"  * {clean}")

if __name__ == '__main__':
    for fname in [
        '07_Admissions_Questionnaire___Founder_for_Founder_975ae924.html',
        '11_Member_Portal___Founder_for_Founder_d8c04d20.html',
        '13_Admin_Console___Founder_for_Founder_80037861.html',
        '01_Terms___Conditions___f4f_4a4c7e2e.html',
        '06_Privacy_Policy___f4f_29e2e2d0.html',
        '03_Refund___Cancellation_Policy___f4f_b9f8844d.html',
        '15_Community_Guidelines___f4f_3422b12a.html',
        '04_404_Not_Found___f4f_e04be2a1.html'
    ]:
        inspect_screen(fname)
