import urllib.request
import time
import re

def verify_live():
    base = 'https://founderforfounder.in'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
    }

    print(f'Waiting for Vercel deployment to propagate at {base}...')
    
    # We will poll for up to 60 seconds until commit updates or passes
    for attempt in range(1, 13):
        try:
            req = urllib.request.Request(f'{base}/?t={int(time.time())}', headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read().decode('utf-8', errors='ignore')

            has_marquee = 'animate-marquee-infinite' in body
            has_ms_protection = "font-family: 'Material Symbols Outlined' !important" in body
            has_bad_span = 'body, p, span, button' in body

            print(f'Attempt {attempt}: has_marquee={has_marquee}, has_ms_protection={has_ms_protection}, has_bad_span={has_bad_span}')
            if has_marquee and has_ms_protection and not has_bad_span:
                print('\n>>> LIVE PRODUCTION CONFIRMED UPDATED TO LATEST DEPLOYMENT! <<<')
                break
        except Exception as e:
            print(f'Attempt {attempt}: {e}')
        time.sleep(5)

    # Now verify all pages
    pages = [
        ('/', 'Home', ['animate-marquee-infinite', 'continuousMarquee', 'Material Symbols Outlined']),
        ('/apply', 'Apply', ['Material Symbols Outlined', 'Domine']),
        ('/terms', 'Terms', ['Material Symbols Outlined', 'Domine']),
        ('/privacy-policy', 'Privacy', ['Material Symbols Outlined', 'Domine']),
        ('/refund-policy', 'Refund', ['Material Symbols Outlined', 'Domine']),
        ('/community-guidelines', 'Guidelines', ['Material Symbols Outlined', 'Domine'])
    ]

    all_passed = True
    print('\n=== Verifying All Live Routes ===')
    for route, label, expectations in pages:
        req = urllib.request.Request(f'{base}{route}?t={int(time.time())}', headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                code = resp.status
                body = resp.read().decode('utf-8', errors='ignore')
                missing = [e for e in expectations if e not in body]
                if code == 200 and not missing:
                    print(f'PASS: {label} ({route}) - 200 OK, verified {expectations}')
                else:
                    print(f'FAIL: {label} ({route}) - code={code}, missing={missing}')
                    all_passed = False
        except Exception as e:
            print(f'ERROR: {label} ({route}) - {e}')
            all_passed = False

    return all_passed

if __name__ == '__main__':
    verify_live()
