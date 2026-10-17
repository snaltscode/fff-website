import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('=== Verification for public/index.html ===')
print('Material Symbols rule present:', '.material-symbols-outlined' in text and "font-family: 'Material Symbols Outlined' !important" in text)
print('Span exclusion rule present:', 'span:not(.material-symbols-outlined):not(.material-symbols)' in text)
print('Old raw span override present:', 'body, p, span, button' in text)
print('Continuous marquee keyframe present:', '@keyframes continuousMarquee' in text)
print('Animate marquee infinite class present:', 'animate-marquee-infinite' in text)
print('Accordion keyframe present:', '@keyframes accordionFadeIn' in text)
print('Accordion rotate present:', 'transform: rotate(180deg)' in text)
print('Replacement characters count (should be 0):', text.count('\ufffd'))

symbols = re.findall(r'<span[^>]*class="[^"]*material-symbols[^"]*"[^>]*>([^<]+)</span>', text)
print(f'Total Material Symbol instances: {len(symbols)}')
print(f'Unique symbols: {len(set(symbols))}')
print('Sample symbols:', sorted(list(set(symbols)))[:10])

# Check all public HTML files
import glob
print('\n=== Verification across ALL public HTML files ===')
for fpath in glob.glob('public/*.html'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    has_ms_rule = '.material-symbols-outlined' in content and 'Material Symbols Outlined' in content
    has_bad_override = 'body, p, span' in content
    num_symbols = len(re.findall(r'material-symbols', content))
    print(f'{fpath}: symbols={num_symbols}, has_ms_protection={has_ms_rule}, bad_span_override={has_bad_override}')
