with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="heroTitle"')
if pos != -1:
    print(text[pos-400:pos+100])
