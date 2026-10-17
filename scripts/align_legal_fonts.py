import re

legal_files = [
    'public/terms.html',
    'public/terms-and-conditions.html',
    'public/privacy-policy.html',
    'public/refund-policy.html',
    'public/refund-and-cancellation-policy.html',
    'public/community-guidelines.html',
    'public/guidelines.html',
    'public/404.html'
]

domine_font_link = '<link href="https://fonts.googleapis.com/css2?family=Domine:wght@400..700&family=Plus+Jakarta+Sans:wght@300..800&display=swap" rel="stylesheet">'
font_override_style = '''
<style>
  h1, h2, h3, .font-headline-hero, .font-headline-lg, .font-headline-md, .font-headline-sm {
    font-family: 'Domine', serif !important;
  }
  body, p, span, button, input, select, textarea, label, td, th {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
  }
</style>
'''

for fpath in legal_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add domine font if not present
    if 'family=Domine' not in content:
        content = content.replace('</head>', f'  {domine_font_link}\n</head>')

    # Add font override style if not present
    if 'font-family: \'Domine\'' not in content and 'font-family: "Domine"' not in content:
        content = content.replace('</head>', f'  {font_override_style}\n</head>')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Aligned fonts for {fpath}')
