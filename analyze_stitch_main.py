import re

with open('scratch_stitch_html.html', 'r', encoding='utf-8') as f:
    content = f.read()

main_start = content.find('<main')
main_end = content.find('</main>')
main = content[main_start:main_end]

ids = re.findall(r'id=["\']([^"\']+)["\']', main)
print('Count of IDs:', len(ids))
for i in ids:
    print(' - ID:', i)
