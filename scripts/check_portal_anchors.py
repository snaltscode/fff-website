with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_anchor = '<div id="portalPage" class="portal-container">'
end_anchor = '<!-- TAB 9: ADMIN DASHBOARD & CMS -->'
p1 = text.find(start_anchor)
p2 = text.find(end_anchor)
print(f"p1: {p1}, p2: {p2}")
if p1 != -1:
    print("Start context:", repr(text[p1:p1+100]))
if p2 != -1:
    print("End context:", repr(text[p2:p2+100]))
