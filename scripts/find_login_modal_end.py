with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lp1 = text.find('id="loginModal"')
end = text.find('</div>\n  </div>', lp1)
print("End of loginModal at:", end)
print(text[end:end+400])
