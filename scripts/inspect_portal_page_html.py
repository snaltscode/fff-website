with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p1 = text.find('id="portalPage"')
p2 = text.find('<!-- FOOTER -->', p1)
print(f"portalPage length: {p2 - p1}")
print("Start:")
print(text[p1:p1+1200])
