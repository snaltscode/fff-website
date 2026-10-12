with open('stitch_sections/section5_cms.html', 'r', encoding='utf-8') as f:
    cms = f.read()

import re
matches = re.findall(r'<input[^>]*>|<button[^>]*>.*?</button>', cms)
for m in matches:
    print('ITEM:', m[:100].replace('\n', ' '))
