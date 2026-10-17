import urllib.request, ssl, time, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sys.stdout.reconfigure(encoding='utf-8')

print("Checking https://founderforfounder.in...")
for attempt in range(1, 10):
    try:
        # Cache buster to bypass local/CDN intermediate cache
        url = f"https://founderforfounder.in/?_t={int(time.time())}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            headers = dict(resp.headers)
            body = resp.read().decode('utf-8', errors='ignore')
            age = headers.get('Age', '0')
            last_mod = headers.get('Last-Modified', 'N/A')
            etag = headers.get('Etag', 'N/A')
            has_playfair = 'Playfair Display' in body
            has_executive = 'Executive Guild' in body or '975ae924' in body or 'bg-surface-container-lowest' in body
            print(f"Attempt {attempt}: Status {resp.status}, Len: {len(body)}, Age: {age}, Last-Modified: {last_mod}")
            print(f"   Stitch detected: Playfair/Executive={has_playfair or has_executive}, ETag: {etag}")
            if has_playfair or has_executive:
                print(">>> LIVE SITE VERIFIED WITH NEW STITCH DESIGN! <<<")
                break
    except Exception as e:
        print(f"Attempt {attempt} Error:", e)
    if attempt < 9:
        time.sleep(10)
