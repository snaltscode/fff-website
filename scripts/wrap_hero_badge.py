with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="heroBadge"')
open_div = text.rfind('<div', 0, pos)
close_div = text.find('</div>', pos)

target = text[open_div:close_div+6]
inner = target.replace('hero-pill-badge ', '')
replacement = f'<div class="hero-pill-badge">\n                {inner}\n              </div>'

text = text[:open_div] + replacement + text[close_div+6:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: hero-pill-badge wrapped exactly.")
