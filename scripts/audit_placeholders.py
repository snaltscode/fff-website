import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

placeholders = re.findall(r'placeholder="([^"]+)"', text)
print("--- SUSPICIOUS PLACEHOLDERS IN index.html ---")
for p in sorted(set(placeholders)):
    if any(k in p.lower() for k in ['987', 'demo', 'example', 'john', 'admin', 'test', 'apex', 'sample', '+91']):
        print(f"  {p}")

print("\n--- ALL EMAIL MATCHES IN index.html ---")
emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
for e in sorted(set(emails)):
    print(f"  {e}")
