import re

target_files = [
    'public/terms.html',
    'public/terms-and-conditions.html',
    'public/privacy-policy.html',
    'public/refund-policy.html',
    'public/refund-and-cancellation-policy.html',
    'public/community-guidelines.html',
    'public/guidelines.html',
    'public/404.html',
    'public/apply.html'
]

font_links = '''  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=Domine:wght@400..700&family=Plus+Jakarta+Sans:wght@300..800&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">'''

font_override_style = '''
<style id="f4f-font-system">
  /* Google Material Symbols Font Protection */
  .material-symbols-outlined,
  .material-symbols {
    font-family: 'Material Symbols Outlined' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 24px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga' !important;
    font-feature-settings: 'liga' !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
    vertical-align: middle;
    user-select: none;
  }

  /* Stitch Executive Typography */
  h1, h2, h3, .font-headline-hero, .font-headline-lg, .font-headline-md, .font-headline-sm {
    font-family: 'Domine', serif !important;
  }
  body, p, button, input, select, textarea, label, td, th,
  span:not(.material-symbols-outlined):not(.material-symbols) {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
  }

  /* Executive Dark Footer with Pure White Text */
  footer {
    background: #002117 !important;
    color: #ffffff !important;
  }
  footer h1, footer h2, footer h3, footer h4,
  footer p, footer a, footer span, footer div, footer li {
    color: #ffffff !important;
  }
  footer a {
    color: rgba(255, 255, 255, 0.8) !important;
    transition: color 0.2s ease;
  }
  footer a:hover {
    color: #ffffff !important;
  }
  footer .text-secondary-fixed,
  footer .font-label-status {
    color: #6ffbbe !important;
  }

  /* Unblocked Natural Scrolling */
  html {
    overflow-x: hidden !important;
    overflow-y: auto !important;
    scroll-behavior: smooth !important;
    height: auto !important;
  }
  body {
    overflow-x: hidden !important;
    overflow-y: visible !important;
    min-height: 100vh !important;
  }
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  ::-webkit-scrollbar-track {
    background: #f2f3ff;
  }
  ::-webkit-scrollbar-thumb {
    background: #064e3b;
    border-radius: 4px;
  }
</style>
'''

for fpath in target_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up replacement characters
    content = content.replace('\ufffd', '•')

    # Remove any existing custom font override block
    content = re.sub(r'<style id="f4f-font-system">.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>\s*h1,\s*h2,\s*h3.*?font-family:\s*\'Plus Jakarta Sans\'.*?</style>', '', content, flags=re.DOTALL)

    # Ensure font links are present
    if 'family=Material+Symbols+Outlined' not in content:
        content = content.replace('</head>', f'{font_links}\n</head>')

    # Append our robust font override style to head
    content = content.replace('</head>', f'{font_override_style}\n</head>')

    # Ensure footer in legal pages has dark background and white text classes
    content = re.sub(r'<footer[^>]*class="([^"]*)"', r'<footer class="\1 bg-[#002117] text-white border-t border-[#064e3b]/60"', content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Aligned fonts, symbols, and footer for {fpath}')
