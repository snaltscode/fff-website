with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="heroBadge"')
open_div = text.rfind('<div', 0, pos)
close_div = text.find('</div>', pos)
print("Tag block:\n", text[open_div:close_div+6])
