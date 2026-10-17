import urllib.request
import urllib.parse
import json
import time
import subprocess
import sys
import os

def run_tests():
    # Start server in background
    proc = subprocess.Popen([sys.executable, 'server.py'], cwd=os.getcwd())
    print('Started server pid:', proc.pid)
    time.sleep(1.5)

    base = 'http://127.0.0.1:8000'
    tests_passed = 0
    total_tests = 0

    def check(name, url, expected_code=200, checks=None, method='GET', data=None, headers=None):
        nonlocal tests_passed, total_tests
        total_tests += 1
        req = urllib.request.Request(url, method=method, data=data, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as resp:
                code = resp.status
                body = resp.read().decode('utf-8', errors='ignore')
                if code != expected_code:
                    print(f'FAIL [{name}]: expected code {expected_code}, got {code}')
                    return False
                if checks:
                    for c in checks:
                        if c not in body:
                            print(f'FAIL [{name}]: missing check string: {c[:80]}')
                            return False
                print(f'PASS [{name}]: status {code}')
                tests_passed += 1
                return True
        except urllib.error.HTTPError as e:
            if e.code == expected_code:
                print(f'PASS [{name}]: status {e.code}')
                tests_passed += 1
                return True
            print(f'FAIL [{name}]: HTTPError {e.code}')
            return False
        except Exception as e:
            print(f'FAIL [{name}]: {e}')
            return False

    try:
        # 1. Homepage
        check('Home page', f'{base}/', 200, ['Domine', 'Plus Jakarta Sans', 'Beyond Networking', 'showInterestModal', 'portalPage'])

        # 2. Legal pages
        check('Terms', f'{base}/terms', 200, ['Terms', 'Domine'])
        check('Privacy Policy', f'{base}/privacy-policy', 200, ['Privacy', 'Domine'])
        check('Refund Policy', f'{base}/refund-policy', 200, ['Refund', 'Domine'])
        check('Community Guidelines', f'{base}/community-guidelines', 200, ['Guidelines', 'Domine'])
        check('Apply Standalone', f'{base}/apply', 200, ['Admissions Questionnaire', 'Domine'])

        # 3. API Health
        check('API Health Check', f'{base}/api', 200, ['"status": "ok"'])

        # 4. API Public Content
        check('API Public Content', f'{base}/api/public/content', 200, ['testimonials', 'faqs'])

        # 5. API Options CORS
        check('API Options CORS', f'{base}/api/public/show-interest', 204, method='OPTIONS')

        # 6. Test application submission
        payload = json.dumps({
            'full_name': 'Test Founder Automated',
            'email': f'test_{int(time.time())}@founderdomain.com',
            'phone': '9876543210',
            'whatsapp': '9876543210',
            'designation': 'Founder & CEO',
            'city': 'Bengaluru',
            'business_name': 'ScaleCorp Technologies',
            'firm_type': 'Private Limited (Pvt Ltd)',
            'business_model_category': 'Product Based (SaaS / DeepTech / Hardware)',
            'years_in_business': '3 to 5 Years',
            'team_size': '11 - 50 Members',
            'business_category': 'Technology & Scaled Ventures',
            'business_stage': 'Profitable',
            'business_description': 'Enterprise AI workflow automation infrastructure.',
            'website': 'https://scalecorp.ai',
            'linkedin': 'https://linkedin.com/in/testfounder',
            'what_offer': 'Cross-border B2B sales acceleration Playbook.',
            'what_need': 'US regulatory compliance guidance.',
            'collaboration_preferences': ['Curated Founder Dinners', 'Closed-Door Salons'],
            'why_join': 'High trust peer exchange.',
            'consent_given': True
        }).encode('utf-8')

        check('POST Show Interest', f'{base}/api/public/show-interest', 200, ['"success": true', 'Application received successfully'], method='POST', data=payload, headers={'Content-Type': 'application/json'})

    finally:
        proc.terminate()
        proc.wait()
        print(f'\nTEST RESULTS: {tests_passed}/{total_tests} passed.')

if __name__ == '__main__':
    run_tests()
