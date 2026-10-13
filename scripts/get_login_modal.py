with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p1 = text.find('<!-- MODAL 4: MEMBER LOGIN -->')
p2 = text.find('<!-- MODAL', p1 + 50)
print(f"loginModal from {p1} to {p2} (length {p2 - p1})")
print(text[p1:p2])
