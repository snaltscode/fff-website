with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p2 = text.find('id="tab-admin"')
p3 = text.find('<!-- MODAL 1:', p2)
print("tab-admin from", p2, "to", p3, "length:", p3 - p2)
