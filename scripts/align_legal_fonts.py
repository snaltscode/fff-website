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

  /* Fixed Static Textured Background Layer (Stationary while text and tabs scroll) */
  #static-textured-bg {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: -10 !important;
    pointer-events: none !important;
    overflow: hidden !important;
    background-color: #faf8ff;
    will-change: transform;
  }
  body {
    background-color: transparent !important;
    position: relative !important;
  }
  main, section, .legal-container {
    position: relative;
    z-index: 1;
    background-color: rgba(255, 255, 255, 0.88) !important;
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
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

static_bg_html = '''<!-- Fixed Static Textured Background (Executive Alliance Theme) -->
<div id="static-textured-bg" class="fixed inset-0 pointer-events-none z-[-10] overflow-hidden" aria-hidden="true">
  <!-- Layer 1: Ambient Executive Mesh Gradients (Emerald, Mint blooms) -->
  <div class="absolute -top-[12%] -left-[10%] w-[50vw] h-[50vw] max-w-[700px] max-h-[700px] rounded-full bg-gradient-to-br from-emerald-500/12 via-[#006c49]/10 to-transparent blur-[110px] transform-gpu"></div>
  <div class="absolute top-[28%] -right-[12%] w-[55vw] h-[55vw] max-w-[750px] max-h-[750px] rounded-full bg-gradient-to-bl from-[#6ffbbe]/15 via-emerald-700/8 to-transparent blur-[130px] transform-gpu"></div>
  <div class="absolute top-[65%] -left-[10%] w-[45vw] h-[45vw] max-w-[650px] max-h-[650px] rounded-full bg-gradient-to-tr from-[#003527]/10 via-[#064e3b]/8 to-transparent blur-[120px] transform-gpu"></div>
  <div class="absolute -bottom-[15%] right-[10%] w-[60vw] h-[60vw] max-w-[800px] max-h-[800px] rounded-full bg-gradient-to-tl from-emerald-600/10 via-[#6ffbbe]/8 to-transparent blur-[140px] transform-gpu"></div>

  <!-- Layer 2: Theme-Relevant Geometric Network Matrix & Architectural Lattice (SVG) -->
  <div class="absolute inset-0 bg-repeat opacity-[0.035] mix-blend-multiply" style="background-image: url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2248%22%20height%3D%2248%22%20viewBox%3D%220%200%2048%2048%22%3E%0A%20%20%3Cpath%20d%3D%22M48%200L0%200%200%2048%22%20fill%3D%22none%22%20stroke%3D%22%23003527%22%20stroke-width%3D%220.6%22%20stroke-dasharray%3D%222%202%22%20stroke-opacity%3D%220.8%22/%3E%0A%20%20%3Cpath%20d%3D%22M24%2017L31%2024L24%2031L17%2024Z%22%20fill%3D%22none%22%20stroke%3D%22%23064e3b%22%20stroke-width%3D%220.75%22/%3E%0A%20%20%3Ccircle%20cx%3D%2224%22%20cy%3D%2224%22%20r%3D%221.75%22%20fill%3D%22%23006c49%22/%3E%0A%20%20%3Ccircle%20cx%3D%220%22%20cy%3D%220%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%20%20%3Ccircle%20cx%3D%2248%22%20cy%3D%220%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%20%20%3Ccircle%20cx%3D%220%22%20cy%3D%2248%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%20%20%3Ccircle%20cx%3D%2248%22%20cy%3D%2248%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%3C/svg%3E'); background-size: 48px 48px;"></div>
  
  <!-- Layer 3: Tactile Micro-Dot Mesh Texture -->
  <div class="absolute inset-0 opacity-[0.025] mix-blend-overlay" style="background-image: radial-gradient(#003527 0.75px, transparent 0.75px); background-size: 24px 24px;"></div>
</div>'''

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

    # Ensure static background layer is present right after body
    if 'id="static-textured-bg"' not in content:
        body_match = re.search(r'(<body[^>]*>)', content)
        if body_match:
            content = content[:body_match.end()] + '\n' + static_bg_html + content[body_match.end():]

    # Ensure footer in legal pages has dark background and white text classes
    content = re.sub(r'<footer[^>]*class="([^"]*)"', r'<footer class="\1 bg-[#002117] text-white border-t border-[#064e3b]/60"', content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Aligned fonts, symbols, and footer for {fpath}')
