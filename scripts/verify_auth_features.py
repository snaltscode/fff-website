with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = {
    'GSI Client Script': 'https://accounts.google.com/gsi/client' in text,
    'Google Sign In Container': 'id="googleSignInBtn"' in text,
    'Custom Google Auth Button': 'id="customGoogleAuthBtn"' in text,
    'Member Login Section': 'id="memberLoginSection"' in text,
    'Admin Login Section': 'id="adminLoginSection"' in text,
    'Admin Login Form': 'id="adminLoginForm"' in text,
    'Quick Fill Admin Credentials': 'quickFillAdminCredentials()' in text,
    'Google Demo Modal': 'id="googleDemoModal"' in text,
    'Open Admin Login in Header': 'openAdminLoginModal()' in text,
    'Admin Console Link in Footer': 'Admin Console' in text,
    'Static Textured Background': 'id="static-textured-bg"' in text,
    'White Footer Text': 'background: #002117 !important' in text
}

print("=== VERIFICATION OF AUTH & ADMIN FEATURES IN public/index.html ===")
all_pass = True
for name, passed in checks.items():
    print(f"  {name:<32}: {'PASS' if passed else 'FAIL'}")
    if not passed:
        all_pass = False

print("\nALL AUTH & ADMIN CHECKS PASSED:", all_pass)
