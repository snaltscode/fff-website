with open('public/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('openShowInterestModal')
if pos != -1:
    print(js[pos-50:pos+350])
else:
    print("openShowInterestModal not found")
