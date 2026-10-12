with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="tab-admin"')
print('Found tab-admin at char:', pos)
print('Snippet:\n', html[pos-80:pos+300])

modal_pos = html.find('<!-- MODAL 1: SHOW INTEREST APPLICATION -->')
print('\nSnippet before MODAL 1:\n', html[modal_pos-300:modal_pos+50])
