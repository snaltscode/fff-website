with open('public/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if '<header' in l:
        print(f'header at line {i+1}: {l.strip()[:60]}')
    if 'id="publicPage"' in l:
        print(f'publicPage at line {i+1}: {l.strip()[:60]}')
    if 'id="portalPage"' in l:
        print(f'portalPage at line {i+1}: {l.strip()[:60]}')
