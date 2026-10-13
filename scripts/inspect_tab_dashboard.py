with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="tab-dashboard"')
if pos != -1:
    end = text.find('id="tab-directory"', pos)
    print("tab-dashboard length:", end - pos)
    print(text[pos:pos+1500])
