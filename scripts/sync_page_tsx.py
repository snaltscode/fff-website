import re
import json

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract inner HTML of <body>
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
if not body_match:
    raise Exception("Could not find <body> tags in public/index.html")

body_html = body_match.group(1)

# Remove script tags that are handled by Next.js <Script> in page.tsx
body_html = re.sub(r'<script\s+src="https://accounts\.google\.com/gsi/client"[^>]*></script>', '', body_html)
body_html = re.sub(r'<script\s+src="/js/app\.js[^"]*"[^>]*></script>', '', body_html)

# Clean trailing whitespace
body_html = body_html.strip()

# Generate Next.js page.tsx
page_tsx = '''import type { Metadata } from 'next';
import Script from 'next/script';

export const metadata: Metadata = {
  title: "Founder for Founder \\u2014 Curated Business Network & Member Experience Platform",
  description: 'A curated business network connecting founders, entrepreneurs, business owners, and professionals across India.',
};

export default function HomePage() {
  return (
    <>
      <div dangerouslySetInnerHTML={{ __html: ''' + json.dumps(body_html) + ''' }} />
      <Script src="https://accounts.google.com/gsi/client" strategy="afterInteractive" />
      <Script src="/js/app.js?v=9.0" strategy="afterInteractive" />
    </>
  );
}
'''

with open('src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(page_tsx)

print(f"Successfully synced src/app/page.tsx ({len(page_tsx)} bytes) from public/index.html!")
