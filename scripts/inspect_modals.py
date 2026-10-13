with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for target in ['showInterestModal', 'loginModal', 'memberPortalSection', 'adminSection']:
    pos = text.find(target)
    if pos != -1:
        print(f"=== Found {target} at pos {pos} ===")
        print(text[pos-80:pos+350])
        print("...\n")
    else:
        print(f"NOT FOUND: {target}")
