with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('tailwind.config =')
if pos != -1:
    print(text[pos:pos+2500])
