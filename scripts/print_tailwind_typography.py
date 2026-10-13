with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('surface-container-highest')
if pos != -1:
    print(text[pos:pos+1500])
