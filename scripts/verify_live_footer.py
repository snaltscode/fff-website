import urllib.request
import time

def verify_live_footer():
    base = 'https://founderforfounder.in'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
    }

    print(f'Waiting for Vercel deployment of commit 31078de at {base}...')
    
    for attempt in range(1, 15):
        try:
            req = urllib.request.Request(f'{base}/?t={int(time.time())}', headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read().decode('utf-8', errors='ignore')

            # Check footer
            idx = body.find('<footer')
            if idx != -1:
                end_idx = body.find('</footer>', idx) + len('</footer>')
                footer_html = body[idx:end_idx]
                has_white = 'text-white' in footer_html
                has_bg_dark = 'bg-[#002117]' in footer_html
                has_old_dark_text = 'text-on-surface-variant' in footer_html
                print(f'Attempt {attempt}: has_white={has_white}, has_bg_dark={has_bg_dark}, has_old_dark_text={has_old_dark_text}')
                if has_white and has_bg_dark and not has_old_dark_text:
                    print('\n>>> LIVE PRODUCTION VERIFIED: FOOTER TEXT IS PURE WHITE! <<<')
                    return True
            else:
                print(f'Attempt {attempt}: No footer tag found in response')
        except Exception as e:
            print(f'Attempt {attempt}: {e}')
        time.sleep(4)

    return False

if __name__ == '__main__':
    verify_live_footer()
