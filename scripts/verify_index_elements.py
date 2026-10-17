with open('public/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    'publicPage',
    'portalPage',
    'showInterestModal',
    'showInterestForm',
    'loginModal',
    'otpModal',
    'activationModal',
    'tab-dashboard',
    'tab-needs',
    'tab-events',
    'tab-meetings',
    'tab-attendance',
    'tab-directory',
    'tab-chat',
    'tab-crm',
    'tab-challenge',
    'tab-account',
    'tab-admin',
    'app_full_name',
    'app_email',
    'app_phone',
    'app_city',
    'app_business_name',
    'app_firm_type',
    'app_business_model_category',
    'app_years_in_business',
    'app_team_size',
    'app_business_stage',
    'app_website',
    'app_linkedin',
    'app_business_description',
    'app_what_offer',
    'app_what_need',
    'app_consent',
    'app_why_join',
    'Domine',
    'Plus Jakarta Sans',
    '#003527',
    '#064e3b'
]

missing = []
for c in checks:
    if c not in text:
        missing.append(c)

if missing:
    print('FAILED! Missing checks:', missing)
else:
    print('ALL CHECKS PASSED!')
