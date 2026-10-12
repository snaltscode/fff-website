with open('stitch_sections/section5_cms.html', 'r', encoding='utf-8') as f:
    cms = f.read()

import re
subpanels = re.split(r'<!-- Sub-panel \d+:', cms)
print(f"Total subpanels: {len(subpanels)-1}")
for i, sp in enumerate(subpanels[1:], 1):
    lines = sp.strip().split('\n')
    title = lines[0] if lines else ""
    print(f"\nSub-panel {i}: {title}")
    # find inputs and values
    inps = re.findall(r'<input[^>]*value="([^"]*)"[^>]*>|<input[^>]*placeholder="([^"]*)"[^>]*>', sp)
    for inp in inps:
        print("  input:", inp[0] or inp[1])
