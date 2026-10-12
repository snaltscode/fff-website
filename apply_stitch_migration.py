import re
from generate_final_stitch_admin import generate_stitch_admin_markup

def main():
    print("Reading public/index.html...")
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update <head>
    font_target = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap">'
    font_replacement = '''<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap">
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
    tailwind.config = {
      corePlugins: { preflight: false },
      darkMode: "class",
      theme: {
        extend: {
          "colors": {
            "on-primary-container": "#80bea6",
            "background": "#fff8f5",
            "surface-container": "#f4ece8",
            "tertiary-fixed-dim": "#4edea3",
            "on-secondary": "#ffffff",
            "secondary-container": "#fed488",
            "error-container": "#ffdad6",
            "primary-fixed": "#b0f0d6",
            "on-error-container": "#93000a",
            "on-secondary-container": "#785a1a",
            "on-background": "#1e1b19",
            "on-primary-fixed": "#002117",
            "gold-light": "#F5EFEB",
            "surface-container-high": "#eee7e3",
            "inverse-on-surface": "#f7efeb",
            "surface-tint": "#2b6954",
            "inverse-surface": "#33302d",
            "secondary": "#775a19",
            "on-surface": "#1e1b19",
            "inverse-primary": "#95d3ba",
            "tertiary-container": "#004f34",
            "surface": "#fff8f5",
            "error": "#ba1a1a",
            "on-surface-variant": "#404944",
            "surface-bright": "#fff8f5",
            "outline-variant": "#bfc9c3",
            "primary-container": "#064e3b",
            "tertiary": "#003623",
            "surface-dim": "#e0d8d5",
            "text-tertiary": "#6B7280",
            "canvas-ivory": "#FBFBFA",
            "surface-variant": "#e9e1dd",
            "secondary-fixed": "#ffdea5",
            "primary": "#003527",
            "primary-fixed-dim": "#95d3ba",
            "on-primary": "#ffffff",
            "text-primary": "#111827",
            "surface-card": "#FFFFFF",
            "surface-container-low": "#faf2ee",
            "outline": "#707974",
            "border-strong": "#D5D2CB",
            "surface-subtle": "#F4F3F0",
            "on-secondary-fixed-variant": "#5d4201",
            "surface-container-lowest": "#ffffff",
            "on-primary-fixed-variant": "#0b513d",
            "border-hairline": "#EAE8E4",
            "emerald-deep": "#043E2E",
            "surface-container-highest": "#e9e1dd",
            "on-error": "#ffffff",
            "on-tertiary": "#ffffff",
            "on-tertiary-fixed": "#002113",
            "text-secondary": "#4B5563",
            "on-tertiary-container": "#31c98f",
            "on-secondary-fixed": "#261900",
            "tertiary-fixed": "#6ffbbe",
            "on-tertiary-fixed-variant": "#005236",
            "secondary-fixed-dim": "#e9c176"
          },
          "borderRadius": {
            "DEFAULT": "0.125rem",
            "lg": "0.25rem",
            "xl": "0.5rem",
            "full": "0.75rem"
          },
          "spacing": {
            "gutter": "1.5rem",
            "margin-md": "3rem",
            "space-xs": "0.25rem",
            "space-lg": "1.75rem",
            "space-xl": "3rem",
            "space-md": "1rem",
            "gutter-lg": "2.5rem",
            "space-sm": "0.5rem",
            "margin-lg": "6rem",
            "margin": "1.5rem"
          },
          "fontFamily": {
            "headline-lg-mobile": [ "Playfair Display", "serif" ],
            "body-lg": [ "Plus Jakarta Sans", "sans-serif" ],
            "label-caps": [ "Plus Jakarta Sans", "sans-serif" ],
            "numeric-stat": [ "Playfair Display", "serif" ],
            "headline-md": [ "Playfair Display", "serif" ],
            "body-md": [ "Plus Jakarta Sans", "sans-serif" ],
            "body-sm": [ "Plus Jakarta Sans", "sans-serif" ],
            "display-hero": [ "Playfair Display", "serif" ],
            "label-md": [ "Plus Jakarta Sans", "sans-serif" ],
            "subhead-lg": [ "Plus Jakarta Sans", "sans-serif" ],
            "headline-sm": [ "Playfair Display", "serif" ],
            "headline-lg": [ "Playfair Display", "serif" ],
            "display-hero-mobile": [ "Playfair Display", "serif" ]
          },
          "fontSize": {
            "headline-lg-mobile": [ "32px", { "lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600" } ],
            "body-lg": [ "17px", { "lineHeight": "28px", "letterSpacing": "0em", "fontWeight": "400" } ],
            "label-caps": [ "11px", { "lineHeight": "16px", "letterSpacing": "0.12em", "fontWeight": "700" } ],
            "numeric-stat": [ "48px", { "lineHeight": "52px", "letterSpacing": "-0.02em", "fontWeight": "700" } ],
            "headline-md": [ "28px", { "lineHeight": "36px", "letterSpacing": "-0.01em", "fontWeight": "600" } ],
            "body-md": [ "15px", { "lineHeight": "24px", "letterSpacing": "0em", "fontWeight": "400" } ],
            "body-sm": [ "13px", { "lineHeight": "20px", "letterSpacing": "0.005em", "fontWeight": "400" } ],
            "display-hero": [ "64px", { "lineHeight": "72px", "letterSpacing": "-0.02em", "fontWeight": "600" } ],
            "label-md": [ "14px", { "lineHeight": "20px", "letterSpacing": "0.01em", "fontWeight": "600" } ],
            "subhead-lg": [ "20px", { "lineHeight": "30px", "letterSpacing": "-0.01em", "fontWeight": "400" } ],
            "headline-sm": [ "22px", { "lineHeight": "30px", "letterSpacing": "0em", "fontWeight": "500" } ],
            "headline-lg": [ "44px", { "lineHeight": "52px", "letterSpacing": "-0.02em", "fontWeight": "600" } ],
            "display-hero-mobile": [ "40px", { "lineHeight": "48px", "letterSpacing": "-0.015em", "fontWeight": "600" } ]
          }
        }
      }
    };
  </script>'''
    
    if font_target in html:
        html = html.replace(font_target, font_replacement)
        print("Updated <head> with fonts and Tailwind config.")
    else:
        print("WARNING: font_target not found in public/index.html")

    # 2. Locate and replace <div id="tab-admin" ...> ... </div>
    tab_admin_start = html.find('<div id="tab-admin"')
    if tab_admin_start == -1:
        raise Exception("Could not find <div id=\"tab-admin\" in public/index.html")

    # Find the matching closing </div>
    # In public/index.html, tab-admin was lines 892 to 1540
    # The next tab or section is <!-- MODAL 1: SHOW INTEREST APPLICATION -->
    # which is right after </div>\n\n    </div>\n  </div>\n\n  <!-- MODAL 1:
    modal1_pos = html.find('<!-- MODAL 1: SHOW INTEREST APPLICATION -->')
    if modal1_pos == -1:
        raise Exception("Could not find MODAL 1 marker in public/index.html")

    # Find the closing </div> of tab-admin right before the closing tags of portal-main and portal-container
    # Let's inspect the chunk between tab_admin_start and modal1_pos
    chunk = html[tab_admin_start:modal1_pos]
    # The end of tab-admin is the last </div> before the two closing </div>s of portal-main and portal-container
    div_closes = [m.start() for m in re.finditer(r'</div>', chunk)]
    # The last 3 </div>s in chunk are:
    # 1. closing of tab-admin
    # 2. closing of portal-main
    # 3. closing of portal-container
    tab_admin_close_idx = div_closes[-3]
    tab_admin_end = tab_admin_start + tab_admin_close_idx + len('</div>')

    old_tab_admin = html[tab_admin_start:tab_admin_end]
    print(f"Old tab-admin length: {len(old_tab_admin)} chars")

    new_tab_admin = generate_stitch_admin_markup().strip()
    html = html[:tab_admin_start] + new_tab_admin + html[tab_admin_end:]
    print("Replaced tab-admin with Stitch Admin Console markup.")

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved public/index.html successfully!")

if __name__ == '__main__':
    main()
