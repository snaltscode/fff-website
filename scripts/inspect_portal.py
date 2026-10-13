with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = text.find('id="portalPage"')
if pos != -1:
    print("Found portalPage at", pos)
    portal_chunk = text[pos:pos+15000]
    tabs = re.findall(r'id=\"(tab-[^\"]+)\"', text)
    print("Tabs found:", tabs)
    
    # Check buttons or tab switching
    switchers = re.findall(r'switchPortalTab\([^\)]+\)', portal_chunk)
    print("Tab switch calls:", switchers[:15])
