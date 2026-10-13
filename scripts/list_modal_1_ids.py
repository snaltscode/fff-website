with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '<!-- MODAL 1: SHOW INTEREST APPLICATION -->'
end_marker = '<!-- MODAL 2:'

p1 = text.find(start_marker)
p2 = text.find(end_marker)

modal_html = text[p1:p2]

import re
inputs = re.findall(r'id=\"([^\"]+)\"', modal_html)
print(f"IDs in modal 1: {inputs}")
forms = re.findall(r'<form[^>]*>', modal_html)
print(f"Forms: {forms}")
