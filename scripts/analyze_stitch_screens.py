import re
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def analyze(filename, label):
    with open(f'stitch_imported_screens/html/{filename}', 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"\n========================================================")
    print(f"=== {label} ({filename}) ===")
    print(f"========================================================")
    
    headings = re.findall(r'<h([1-4])[^>]*>(.*?)</h\1>', html, re.DOTALL)
    print("Headings:")
    for level, h in headings[:15]:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        clean = ' '.join(clean.split())
        if clean:
            print(f"  [H{level}] {clean}")

    nav_links = re.findall(r'<a[^>]*class=[\'"][^\'"]*[\'"][^>]*>(.*?)</a>', html, re.DOTALL)
    print("\nSample Anchor Links:")
    for a in nav_links[:10]:
        clean = re.sub(r'<[^>]+>', '', a).strip()
        clean = ' '.join(clean.split())
        if clean:
            print(f"  - {clean}")

if __name__ == '__main__':
    analyze('02_Founder_for_Founder___Home__Editorial_Edition_5755021a.html', 'HOME EDITORIAL EDITION')
    analyze('03_Founder_for_Founder___Payment_Gateway___Checkout_5c0b6d39.html', 'PAYMENT GATEWAY & CHECKOUT')
    analyze('08_Founder_for_Founder___404_Page_Not_Found_fad01702.html', '404 PAGE NOT FOUND')
    analyze('07_Founder_for_Founder___Community_Guidelines_86d7ad6c.html', 'COMMUNITY GUIDELINES')
