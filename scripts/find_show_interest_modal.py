with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '<!-- MODAL 1: SHOW INTEREST APPLICATION -->'
end_marker = '<!-- MODAL 2:'

p1 = text.find(start_marker)
p2 = text.find(end_marker)

print(f"showInterestModal from {p1} to {p2} (length {p2 - p1})")
print(text[p1:p1+300])
print("...")
print(text[p2-200:p2])
