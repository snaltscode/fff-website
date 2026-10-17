import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/live_prod.html', 'r', encoding='utf-8') as f:
    c = f.read()

title_m = re.search(r'<title>(.*?)</title>', c)
print('Title:', title_m.group(1) if title_m else 'No title')

h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', c, re.DOTALL)
print('H1s:', [h.strip()[:60] for h in h1s])

print('Has Beyond Networking:', 'Beyond Networking' in c)
print('Has Playfair Display:', 'Playfair Display' in c)
print('Has tailwind.config:', 'tailwind.config' in c)
print('Has cdn.tailwindcss.com:', 'cdn.tailwindcss.com' in c)
print('Has showInterestModal:', 'showInterestModal' in c)
print('Has Executive Guild:', 'Executive Guild' in c)
print('Has Screen 975ae924:', '975ae924' in c)
print('Has 16:9 Meeting Photos Manager:', '16:9 Meeting Photos Manager' in c)
print('Has Domine:', 'Domine' in c)
print('Has styles.css?v=9.0:', 'styles.css?v=9.0' in c)

# Check script src tags
scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', c)
print('Scripts in live prod:', scripts)
