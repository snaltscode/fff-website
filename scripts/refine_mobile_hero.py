with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Refine hero pill badge
target_pill = '''<div class="hero-pill-badge">
                 <div class="inline-flex items-center gap-space-xs px-3 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-status text-label-status tracking-widest uppercase w-fit shadow-sm">
                  <span class="w-2 h-2 rounded-full bg-secondary inline-block animate-pulse"></span>
                  <span id="heroBadge">CURATED FOUNDER NETWORK • BY APPLICATION ONLY</span>
                </div>
              </div>'''

# Or find hero-pill-badge block flexibly
pos = text.find('class="hero-pill-badge"')
if pos != -1:
    end_pos = text.find('</div>\n              </div>', pos)
    if end_pos != -1:
        new_pill = '''<div class="hero-pill-badge">
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-primary-container font-label-status text-xs uppercase font-bold tracking-wider max-w-full">
                  <span class="w-2 h-2 rounded-full bg-secondary inline-block animate-pulse shrink-0"></span>
                  <span id="heroBadge" class="truncate">CURATED FOUNDER NETWORK &bull; BY APPLICATION ONLY</span>
                </div>
              </div>'''
        text = text[:pos] + new_pill + text[end_pos + len('</div>\n              </div>'):]
        print("Updated hero pill badge successfully!")

# Refine CTA buttons container
cta_old = '<div class="flex items-center gap-space-sm flex-wrap">'
cta_new = '<div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-space-sm max-w-md">'
if cta_old in text:
    text = text.replace(cta_old, cta_new, 1)
    print("Updated hero CTA buttons to flex-col sm:flex-row!")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("public/index.html refined successfully.")
