with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Peer Guild Codex')
print(text[pos-200:pos+100])
