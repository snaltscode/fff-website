import re

with open('scratch_stitch_html.html', 'r', encoding='utf-8') as f:
    content = f.read()

main_start = content.find('<main')
main_end = content.find('</main>')
main = content[main_start:main_end]

# Split by comments that mark sections
pattern = r'(<!-- (?:Top Context Ribbon|Header Banner|Section \d+:|Sub-panel \d+:|Quick Add|Existing Photo Cards Grid|Floating / Sticky).*?-->)'
parts = re.split(pattern, main)

print(f"Total parts: {len(parts)}")
for i, p in enumerate(parts):
    if p.startswith('<!--'):
        print(f"\n=== {p.strip()} ===")
    else:
        # Show first 200 chars of non-comment block
        snippet = ' '.join(p.split())[:180]
        print(f"    Snippet: {snippet}...")
