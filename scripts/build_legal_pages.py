import os, re, json

PAGES = [
    {
        'title': 'Terms & Conditions — Founder for Founder',
        'desc': 'Official Terms of Membership & Platform Governance for Founder for Founder, operated by SnaLts.co.',
        'src': 'stitch_imported_screens_v2/html/01_Terms___Conditions___f4f_4a4c7e2e.html',
        'targets': ['src/app/terms/page.tsx', 'src/app/terms-and-conditions/page.tsx'],
        'public_target': 'public/terms.html'
    },
    {
        'title': 'Privacy Policy — Founder for Founder',
        'desc': 'Official Privacy & Data Protection Policy for Founder for Founder members and applicants.',
        'src': 'stitch_imported_screens_v2/html/06_Privacy_Policy___f4f_29e2e2d0.html',
        'targets': ['src/app/privacy-policy/page.tsx'],
        'public_target': 'public/privacy-policy.html'
    },
    {
        'title': 'Refund & Cancellation Policy — Founder for Founder',
        'desc': 'Official Refund, Cancellation & Fee Disciplinary Policies for Founder for Founder membership and gatherings.',
        'src': 'stitch_imported_screens_v2/html/03_Refund___Cancellation_Policy___f4f_b9f8844d.html',
        'targets': ['src/app/refund-policy/page.tsx', 'src/app/refund-and-cancellation-policy/page.tsx'],
        'public_target': 'public/refund-policy.html'
    },
    {
        'title': 'Community Guidelines & Sovereign Charter — Founder for Founder',
        'desc': 'The Chatham House Rule, Non-Solicitation Code, and Peer Reciprocity Guidelines governing all Founder for Founder members.',
        'src': 'stitch_imported_screens_v2/html/15_Community_Guidelines___f4f_3422b12a.html',
        'targets': ['src/app/community-guidelines/page.tsx', 'src/app/guidelines/page.tsx'],
        'public_target': 'public/community-guidelines.html'
    }
]

def clean_body_html(html_str):
    # Ensure links to internal routes are clean
    html_str = re.sub(r'href=[\'"][^\'"]*terms[^\'"]*[\'"]', 'href="/terms"', html_str, flags=re.I)
    html_str = re.sub(r'href=[\'"][^\'"]*privacy[^\'"]*[\'"]', 'href="/privacy-policy"', html_str, flags=re.I)
    html_str = re.sub(r'href=[\'"][^\'"]*refund[^\'"]*[\'"]', 'href="/refund-policy"', html_str, flags=re.I)
    html_str = re.sub(r'href=[\'"][^\'"]*guidelines[^\'"]*[\'"]', 'href="/community-guidelines"', html_str, flags=re.I)
    # Fix home links
    html_str = re.sub(r'href=[\'"]#[\'"]\s+class=[\'"][^\'"]*flex items-center', 'href="/" class="flex items-center', html_str)
    html_str = re.sub(r'data-path=[\'"][^\'"]*[\'"]', '', html_str)
    return html_str

for item in PAGES:
    with open(item['src'], 'r', encoding='utf-8') as f:
        src_html = f.read()

    # Clean full html for public/ target
    cleaned_full_html = clean_body_html(src_html)
    if 'public_target' in item:
        with open(item['public_target'], 'w', encoding='utf-8') as pf:
            pf.write(cleaned_full_html)
        print(f"Updated public file {item['public_target']} ({len(cleaned_full_html)} bytes)")

    body_match = re.search(r'<body[^>]*>(.*?)</body>', src_html, re.DOTALL)
    if not body_match:
        print(f"Error: No body found in {item['src']}")
        continue

    body_content = clean_body_html(body_match.group(1).strip())
    # Escape for React dangerouslySetInnerHTML
    body_json = json.dumps(body_content)

    component_code = f'''import type {{ Metadata }} from 'next';
import Script from 'next/script';

export const metadata: Metadata = {{
  title: {json.dumps(item['title'])},
  description: {json.dumps(item['desc'])},
}};

export default function LegalDocPage() {{
  return (
    <>
      <Script src="https://cdn.tailwindcss.com" strategy="beforeInteractive" />
      <div 
        className="min-h-screen bg-[#FAF8F5] text-[#1A1A1A]" 
        style={{{{ fontStyle: 'normal' }}}}
        dangerouslySetInnerHTML={{{{ __html: {body_json} }}}} 
      />
      <Script id="reading-progress" strategy="afterInteractive" dangerouslySetInnerHTML={{{{ __html: `
        if (typeof window !== 'undefined') {{
          window.addEventListener('scroll', () => {{
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
            const bar = document.getElementById('progress-bar') || document.getElementById('scrollProgressBar');
            const pct = document.getElementById('read-pct');
            if (bar) bar.style.width = scrolled + '%';
            if (pct) pct.innerText = Math.round(scrolled) + '% read';
          }}, {{ passive: true }});
        }}
      ` }}}} />
    </>
  );
}}
'''

    for target in item['targets']:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'w', encoding='utf-8') as tf:
            tf.write(component_code)
        print(f"Saved {target} ({len(component_code)} bytes)")

print("\nAll legal pages generated successfully from Stitch source!")
