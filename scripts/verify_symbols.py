import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

symbols = re.findall(r'<span[^>]*class="[^"]*material-symbols[^"]*"[^>]*>([^<]+)</span>', html)
print(f'Total Material Symbol instances: {len(symbols)}')

unique_symbols = sorted(list(set(symbols)))
print(f'Unique symbols ({len(unique_symbols)}):')
for s in unique_symbols:
    count = symbols.count(s)
    print(f'  {s}: {count}')
