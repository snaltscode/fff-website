with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="heroBadge"')
print("pos:", pos)
print(repr(text[pos-160:pos+80]))
