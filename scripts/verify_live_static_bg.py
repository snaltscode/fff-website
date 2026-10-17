import urllib.request
import time

routes = ["/", "/terms", "/privacy-policy", "/community-guidelines", "/refund-policy"]

for route in routes:
    url = f"https://founderforfounder.in{route}?cachebust={int(time.time())}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")
            has_bg = 'id="static-textured-bg"' in html
            has_trans = 'background-color: transparent !important' in html
            has_footer = 'background: #002117 !important' in html
            print(f"{route:<25} Status: {resp.status} | Static BG: {has_bg} | Transparent Body: {has_trans} | Footer White: {has_footer}")
    except Exception as e:
        print(f"Error checking {route}: {e}")
