with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

p2 = text.find('<!-- TAB 9: ADMIN DASHBOARD & CMS')
end_portal = text.find('</div>\n  </div>', p2)
print(f"tab-admin starts at {p2}, ends at {end_portal} (length {end_portal - p2})")
print("First 800 chars of tab-admin:")
print(text[p2:p2+800])
