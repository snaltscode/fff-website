with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('spa')
print(text[pos-100:pos+200])
