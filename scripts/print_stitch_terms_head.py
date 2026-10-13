with open(r'stitch_imported_screens_v2\html\01_Terms___Conditions___f4f_4a4c7e2e.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
head = re.search(r'<head[^>]*>(.*?)</head>', text, re.DOTALL)
if head:
    for i, s in enumerate(re.findall(r'<style[^>]*>(.*?)</style>', head.group(1), re.DOTALL)):
        print(f"=== Style {i+1} ===")
        print(s[:300])
    for i, sc in enumerate(re.findall(r'<script[^>]*>(.*?)</script>', head.group(1), re.DOTALL)):
        print(f"=== Script {i+1} ===")
        print(sc[:300])
