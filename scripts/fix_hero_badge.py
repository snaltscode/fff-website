with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<div class="inline-flex items-center gap-space-xs px-3 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-caps text-label-caps uppercase w-fit shadow-sm">'
replacement = '<div class="hero-pill-badge"><div class="inline-flex items-center gap-space-xs px-3 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-caps text-label-caps uppercase w-fit shadow-sm">'

if target in text:
    # close the wrapper div
    old_block = target + '\n                  <span class="w-2 h-2 rounded-full bg-secondary inline-block animate-pulse"></span>\n                  <span id="heroBadge">CURATED FOUNDER NETWORK • BY APPLICATION ONLY</span>\n                </div>'
    new_block = replacement + '\n                  <span class="w-2 h-2 rounded-full bg-secondary inline-block animate-pulse"></span>\n                  <span id="heroBadge">CURATED FOUNDER NETWORK • BY APPLICATION ONLY</span>\n                </div></div>'
    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('public/index.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Updated hero badge with .hero-pill-badge successfully!")
    else:
        # Fallback to replacing target
        pos = text.find(target)
        end_d = text.find('</div>', pos)
        text = text[:pos] + '<div class="hero-pill-badge">' + text[pos:end_d+6] + '</div>' + text[end_d+6:]
        with open('public/index.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Wrapped target in hero-pill-badge successfully!")
else:
    print("Target not found!")
