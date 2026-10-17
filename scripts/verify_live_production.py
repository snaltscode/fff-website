import urllib.request
import ssl

ctx = ssl.create_default_context()

url = 'https://founderforfounder.in'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        html = resp.read().decode('utf-8')

    checks = {
        'GSI Script': 'https://accounts.google.com/gsi/client' in html,
        'Google Sign-In Container': 'id="googleSignInBtn"' in html,
        'Google Custom Button': 'id="customGoogleAuthBtn"' in html,
        'Admin Login Section': 'id="adminLoginSection"' in html,
        'Admin Tab Button': 'id="tabBtnAdmin"' in html,
        'Member Tab Button': 'id="tabBtnMember"' in html,
        'Admin Quick Fill Button': 'quickFillAdminCredentials()' in html,
        'Admin Nav Header Link': 'openAdminLoginModal()' in html,
        'Admin Footer Link': 'adminConsoleFooterLink' in html or 'openAdminLoginModal();' in html,
        'Google Demo Fallback Modal': 'id="googleDemoModal"' in html,
        'Static Textured Background': 'id="static-textured-bg"' in html,
        'White Footer Text': 'color: #ffffff' in html
    }

    print('=== LIVE PRODUCTION VERIFICATION (https://founderforfounder.in) ===')
    all_passed = True
    for name, passed in checks.items():
        print(f'  {name:<32}: {"PASS" if passed else "FAIL"}')
        if not passed:
            all_passed = False

    print(f'\nALL LIVE PRODUCTION CHECKS PASSED: {all_passed}')

    # Also test app.js live bundle
    js_url = 'https://founderforfounder.in/js/app.js'
    req_js = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req_js, context=ctx, timeout=20) as resp_js:
        js = resp_js.read().decode('utf-8')

    js_checks = {
        'openAdminLoginModal in app.js': 'openAdminLoginModal' in js,
        'switchLoginModalTab in app.js': 'switchLoginModalTab' in js,
        'quickFillAdminCredentials in app.js': 'quickFillAdminCredentials' in js,
        'handleAdminLoginSubmit in app.js': 'handleAdminLoginSubmit' in js,
        'auto redirect to admin tab in app.js': 'switchPortalTab(\'admin\'' in js or 'switchPortalTab("admin"' in js,
    }

    print('\n=== LIVE APP.JS ASSET VERIFICATION (https://founderforfounder.in/js/app.js) ===')
    for name, passed in js_checks.items():
        print(f'  {name:<36}: {"PASS" if passed else "FAIL"}')
        if not passed:
            all_passed = False

    print(f'\nALL APP.JS CHECKS PASSED: {all_passed}')

except Exception as e:
    print('Verification failed with error:', e)
