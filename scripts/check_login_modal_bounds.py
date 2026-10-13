with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lp1 = text.find('id="loginModal"')
print("loginModal at:", lp1)
print(text[lp1:lp1+2000])
