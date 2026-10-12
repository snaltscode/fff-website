
import re

with open('scratch_stitch_html.html', 'r', encoding='utf-8') as f:
    content = f.read()

body_start = content.find('<body')
body_end = content.find('</body>')
body = content[body_start:body_end]

# Let us see what direct child elements exist under body
# Look for <header, <main, <footer, <div
for tag in ['<header', '<main', '<footer', '<aside']:
    pos = 0
    while True:
        pos = body.find(tag, pos)
        if pos == -1: break
        print(f'Found {tag} at index {pos}: {body[pos:pos+120]}...')
        pos += len(tag)
