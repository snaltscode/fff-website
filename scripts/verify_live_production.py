import urllib.request
import urllib.parse
import json
import time

def verify_live():
    base = 'https://founderforfounder.in'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
    }

    print(f'Querying live production at {base}...')

    tests = [
        ('Homepage', f'{base}/', 200, ['Domine', 'Plus Jakarta Sans', '#003527', 'Beyond Networking']),
        ('Terms & Conditions', f'{base}/terms', 200, ['Terms', 'Domine']),
        ('Privacy Policy', f'{base}/privacy-policy', 200, ['Privacy', 'Domine']),
        ('Refund Policy', f'{base}/refund-policy', 200, ['Refund', 'Domine']),
        ('Community Guidelines', f'{base}/community-guidelines', 200, ['Guidelines', 'Domine']),
        ('Apply Standalone', f'{base}/apply', 200, ['Admissions Questionnaire', 'Domine']),
        ('API Health', f'{base}/api', 200, ['"status": "ok"']),
        ('API Public Content', f'{base}/api/public/content', 200, ['testimonials', 'faqs'])
    ]

    passed = 0
    for name, url, exp_status, checks in tests:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                code = resp.status
                body = resp.read().decode('utf-8', errors='ignore')
                missing = [c for c in checks if c not in body]
                if code == exp_status and not missing:
                    print(f'[PASS]: {name} ({code})')
                    passed += 1
                else:
                    print(f'[FAIL]: {name} (code: {code}, missing: {missing})')
        except Exception as e:
            print(f'[ERROR]: {name} -> {e}')

    print(f'\nLive Verification Score: {passed}/{len(tests)}')
    return passed == len(tests)

if __name__ == '__main__':
    verify_live()
