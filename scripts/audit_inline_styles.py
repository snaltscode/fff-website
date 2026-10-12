import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

inline_styles = re.findall(r'style="([^"]*(?:min-width|width)\s*:\s*\d+px[^"]*)"', text)
print(f"Found {len(inline_styles)} inline styles with pixel widths:")
for s in sorted(set(inline_styles)):
    # Extract the width values
    widths = re.findall(r'(?:min-width|width)\s*:\s*(\d+)px', s)
    max_w = max(int(w) for w in widths) if widths else 0
    if max_w > 100:
        print(f"  [{max_w}px] {s[:110]}")
