with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p1 = text.find('<!-- MODAL 1: SHOW INTEREST APPLICATION -->')
p2 = text.find('id="appDetailModal"')
print("Distance:", p2 - p1)
print(text[p2-100:p2+100])
