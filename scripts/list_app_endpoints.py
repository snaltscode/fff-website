import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

endpoints = set(re.findall(r"['\"`](/api/[^'\"`?]+)", js))
for ep in sorted(endpoints):
    print(ep)
