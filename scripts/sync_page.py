import json
import re

def sync_page():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not match:
        print("Could not find <body> tags in public/index.html")
        return

    body_content = match.group(1).strip()
    encoded_body = json.dumps(body_content)

    page_content = (
        "import type { Metadata } from 'next';\n"
        "import Script from 'next/script';\n\n"
        "export const metadata: Metadata = {\n"
        '  title: "Founder for Founder \u2014 Curated Business Network & Member Experience Platform",\n'
        "  description: 'A curated business network connecting founders, entrepreneurs, business owners, and professionals across India.',\n"
        "};\n\n"
        "export default function HomePage() {\n"
        "  return (\n"
        "    <>\n"
        "      <div dangerouslySetInnerHTML={{ __html: " + encoded_body + " }} />\n"
        '      <Script src="https://accounts.google.com/gsi/client" strategy="afterInteractive" />\n'
        '      <Script src="/js/app.js?v=9.0" strategy="afterInteractive" />\n'
        "    </>\n"
        "  );\n"
        "}\n"
    )
    with open('src/app/page.tsx', 'w', encoding='utf-8') as f:
        f.write(page_content)
    print("src/app/page.tsx successfully synchronized with public/index.html body!")

if __name__ == '__main__':
    sync_page()
