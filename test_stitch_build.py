import os
import re

# Read all extracted stitch sections
with open('stitch_sections/top_and_header.html', 'r', encoding='utf-8') as f:
    top_header = f.read()

with open('stitch_sections/section1_kpis.html', 'r', encoding='utf-8') as f:
    sec1 = f.read()

with open('stitch_sections/section2_apps.html', 'r', encoding='utf-8') as f:
    sec2 = f.read()

with open('stitch_sections/section3_audit.html', 'r', encoding='utf-8') as f:
    sec3 = f.read()

with open('stitch_sections/section4_photos.html', 'r', encoding='utf-8') as f:
    sec4 = f.read()

with open('stitch_sections/section5_cms.html', 'r', encoding='utf-8') as f:
    sec5 = f.read()

with open('stitch_sections/section6_events.html', 'r', encoding='utf-8') as f:
    sec6 = f.read()

print("All sections read successfully.")
print(f"Top header: {len(top_header)} chars")
print(f"Sec 1: {len(sec1)} chars")
print(f"Sec 2: {len(sec2)} chars")
print(f"Sec 3: {len(sec3)} chars")
print(f"Sec 4: {len(sec4)} chars")
print(f"Sec 5: {len(sec5)} chars")
print(f"Sec 6: {len(sec6)} chars")
