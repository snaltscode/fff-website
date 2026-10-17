import re

def get_prepared_questionnaire():
    with open('stitch_mcp_export/html/975ae924d8524f40addf2a18a87c497a_Admissions Questionnaire _ Founder for Founder.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract main content
    q_main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    q_content = q_main_match.group(1) if q_main_match else html

    # Wire up form ID and onsubmit
    q_content = q_content.replace(
        '<form class="flex flex-col gap-8" id="f4f-application-form" onsubmit="handleFormSubmission(event)">',
        '<form class="flex flex-col gap-8" id="showInterestForm" onsubmit="handleShowInterestSubmit(event)">'
    )

    # 1. Full name input
    q_content = re.sub(
        r'(<label[^>]*>Full Name.*?</label>\s*<input\s+class="[^"]*"\s+placeholder="e\.g\.\s*Varun Krishnamurthy"[^>]*?)>',
        r'\1 id="app_full_name" name="full_name">',
        q_content, flags=re.DOTALL
    )

    # 2. Designation select
    q_content = re.sub(
        r'(<label[^>]*>Designation\s*/\s*Role.*?</label>\s*<select\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_designation" name="designation">',
        q_content, flags=re.DOTALL
    )

    # 3. Work email input
    q_content = re.sub(
        r'(<label[^>]*>Official Work Email.*?</label>\s*<input\s+class="[^"]*"\s+placeholder="name@yourcompany\.com"[^>]*?)>',
        r'\1 id="app_email" name="email">',
        q_content, flags=re.DOTALL
    )

    # 4. WhatsApp phone input
    q_content = re.sub(
        r'(<label[^>]*>Direct WhatsApp Number.*?</label>[\s\S]*?<input\s+class="[^"]*"\s+pattern="\[0-9\]\{10\}"[^>]*?)>',
        r'\1 id="app_phone" name="phone">',
        q_content
    )

    # 5. City Hub radio buttons
    # Add hidden input for app_city that syncs with radio or fallback
    city_hidden = '<input type="hidden" id="app_city" name="city" value="Bengaluru"/>\n'
    q_content = q_content.replace('<label class="font-label-lg text-label-lg text-on-surface">City Hub / Primary Base <span class="text-error">*</span></label>',
                                  '<label class="font-label-lg text-label-lg text-on-surface">City Hub / Primary Base <span class="text-error">*</span></label>\n' + city_hidden)
    # Give onchange to radio buttons to update app_city
    q_content = re.sub(
        r'<input([^>]*name="city_hub"[^>]*)>',
        r'<input\1 onchange="document.getElementById(\'app_city\').value = this.value">',
        q_content
    )

    # 6. Registered Entity Name
    q_content = re.sub(
        r'(<label[^>]*>Registered Entity\s*/\s*Company Name.*?</label>\s*<input\s+class="[^"]*"\s+placeholder="e\.g\.\s*Acme Technologies Solutions Pvt Ltd"[^>]*?)>',
        r'\1 id="app_business_name" name="business_name">',
        q_content, flags=re.DOTALL
    )

    # 7. Corporate Structure select
    q_content = re.sub(
        r'(<label[^>]*>Corporate Structure.*?</label>\s*<select\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_firm_type" name="firm_type">',
        q_content, flags=re.DOTALL
    )

    # 8. Business Archetype select
    q_content = re.sub(
        r'(<label[^>]*>Business Archetype.*?</label>\s*<select\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_business_model_category" name="business_model_category">',
        q_content, flags=re.DOTALL
    )

    # Add hidden app_business_category
    biz_cat_hidden = '<input type="hidden" id="app_business_category" name="business_category" value="Technology & Scaled Ventures"/>\n'
    q_content = q_content.replace('<label class="font-label-lg text-label-lg text-on-surface">Business Archetype',
                                  biz_cat_hidden + '<label class="font-label-lg text-label-lg text-on-surface">Business Archetype')

    # 9. Operating Vintage select
    q_content = re.sub(
        r'(<label[^>]*>Operating Vintage.*?</label>\s*<select\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_years_in_business" name="years_in_business">',
        q_content, flags=re.DOTALL
    )

    # 10. Active Team Size select
    q_content = re.sub(
        r'(<label[^>]*>Active Team Size.*?</label>\s*<select\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_team_size" name="team_size">',
        q_content, flags=re.DOTALL
    )

    # 11. Funding stage
    stage_hidden = '<input type="hidden" id="app_business_stage" name="business_stage" value="Bootstrapped"/>\n'
    q_content = q_content.replace('<label class="font-label-lg text-label-lg text-on-surface">Capital &amp; Profitability Trajectory',
                                  stage_hidden + '<label class="font-label-lg text-label-lg text-on-surface">Capital &amp; Profitability Trajectory')
    q_content = re.sub(
        r'<input([^>]*name="funding_stage"[^>]*)>',
        r'<input\1 onchange="document.getElementById(\'app_business_stage\').value = this.value">',
        q_content
    )

    # 12. Company Website
    q_content = re.sub(
        r'(<label[^>]*>Company Website URL.*?</label>\s*<input\s+class="[^"]*"\s+placeholder="https://yourbrand\.com"[^>]*?)>',
        r'\1 id="app_website" name="website">',
        q_content, flags=re.DOTALL
    )

    # 13. Founder LinkedIn
    q_content = re.sub(
        r'(<label[^>]*>Founder LinkedIn Profile.*?</label>\s*<input\s+class="[^"]*"\s+placeholder="https://linkedin\.com/in/founderhandle"[^>]*?)>',
        r'\1 id="app_linkedin" name="linkedin">',
        q_content, flags=re.DOTALL
    )

    # 14. Twitter / X Handle
    q_content = re.sub(
        r'(<label[^>]*>Twitter\s*/\s*X Handle.*?</label>\s*<input\s+class="[^"]*"\s+placeholder="@yourhandle"[^>]*?)>',
        r'\1 id="app_instagram" name="instagram">',
        q_content, flags=re.DOTALL
    )

    # 15. Short Executive Pitch
    q_content = re.sub(
        r'(<label[^>]*>Short Executive Pitch.*?</label>[\s\S]*?<textarea\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_business_description" name="business_description">',
        q_content
    )

    # 16. What offer
    q_content = re.sub(
        r'(<label[^>]*>What specific value or expertise can you contribute.*?</label>[\s\S]*?<textarea\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_what_offer" name="what_offer">',
        q_content
    )

    # 17. What need
    q_content = re.sub(
        r'(<label[^>]*>What are your most critical operational bottlenecks.*?</label>[\s\S]*?<textarea\s+class="[^"]*"[^>]*?)>',
        r'\1 id="app_what_need" name="what_need">',
        q_content
    )

    # 18. Collab preferences checkboxes: name="collab_pref"
    # Tag each checkbox with name="collab_pref" and values
    collab_cards = [
        ('Curated Founder Dinners', 'Curated Founder Dinners'),
        ('Closed-Door Salons', 'Closed-Door Salons'),
        ('Active Sports &amp; Movement', 'Active Sports & Movement'),
        ('Confidential Advisory Circles', 'Confidential Advisory Circles'),
        ('Annual Chapter Retreats', 'Annual Chapter Retreats')
    ]
    for label_txt, val in collab_cards:
        q_content = re.sub(
            rf'(<input[^>]*class="w-5 h-5[^>]*?)>\s*(<div[^>]*>[\s\S]*?{re.escape(label_txt)})',
            rf'\1 name="collab_pref" value="{val}">\2',
            q_content, count=1
        )

    # 19. Affirmation and Consent Checkboxes
    q_content = re.sub(
        r'(<input[^>]*class="w-5 h-5[^>]*?)(>\s*<div[^>]*>\s*<span[^>]*>I accept the Chatham House Rule)',
        r'\1 id="app_consent" name="consent_given"\2',
        q_content, count=1
    )

    # Default why_join hidden input
    why_join_hidden = '<input type="hidden" id="app_why_join" name="why_join" value="I seek high-trust peer exchange and strategic collaboration with vetted founders across India.">\n'
    q_content = why_join_hidden + q_content

    return q_content

if __name__ == '__main__':
    q = get_prepared_questionnaire()
    print('Length:', len(q))
    for check_id in ['app_full_name', 'app_email', 'app_phone', 'app_city', 'app_business_name', 'app_firm_type', 'app_business_model_category', 'app_years_in_business', 'app_team_size', 'app_business_stage', 'app_website', 'app_linkedin', 'app_business_description', 'app_what_offer', 'app_what_need', 'app_consent', 'app_why_join', 'showInterestForm']:
        print(f'{check_id}: {"FOUND" if check_id in q else "MISSING"}')
