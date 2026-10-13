with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="loginModal"')
if pos != -1:
    end = text.find('</div>\n  </div>', pos)
    print(text[pos:pos+1500])
