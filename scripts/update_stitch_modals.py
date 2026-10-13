import os, re

def generate_admissions_modal():
    return '''<!-- MODAL 1: SHOW INTEREST APPLICATION (STITCH REVISED SCREEN 975ae924) -->
  <div class="modal-overlay" id="showInterestModal" style="display:none; align-items: flex-start; overflow-y: auto; padding: 2rem 1rem;">
    <div class="modal-content modal-content-lg" style="max-width: 860px; width: 100%; margin: auto; background: var(--canvas-cream, #FAF8F5); border: 1px solid var(--card-border, #E8E4DC); border-radius: 12px; box-shadow: 0 25px 50px -12px rgba(6, 78, 59, 0.15); overflow: hidden; padding: 0;">
      
      <!-- Top Admissions Header Banner -->
      <div style="background: linear-gradient(135deg, #003527 0%, #064E3B 100%); color: #FAF8F5; padding: 2rem 2.25rem; position: relative;">
        <button class="modal-close" onclick="closeModal('showInterestModal')" style="position: absolute; top: 1.25rem; right: 1.25rem; color: #FAF8F5; background: rgba(255,255,255,0.12); border: none; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.12)'">&times;</button>
        
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
          <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #10B981;"></span>
          <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #A7F3D0;">CONFIDENTIAL ADMISSIONS &bull; ROLLING 72H INTAKE</span>
        </div>
        
        <h2 style="font-family: 'Domine', serif; font-size: 1.85rem; font-weight: 700; letter-spacing: -0.02em; margin: 0 0 0.5rem 0; color: #FAF8F5;">
          Admissions Questionnaire &amp; Application
        </h2>
        
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.92rem; color: #D1FAE5; margin: 0; line-height: 1.5; max-width: 680px;">
          Founder for Founder is a strictly curated, peer-governed collective of founders, promoters, and scale operators. We review all applications within a rolling 72-hour vetting window.
        </p>

        <!-- 3 Feature Pillars -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid rgba(255,255,255,0.12);">
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span style="font-size: 0.78rem; color: #ECFDF5; font-weight: 600;">Rolling 72-Hour Intake</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span style="font-size: 0.78rem; color: #ECFDF5; font-weight: 600;">Zero Sales Sponsorships</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <span style="font-size: 0.78rem; color: #ECFDF5; font-weight: 600;">Chatham House Protocol</span>
          </div>
        </div>
      </div>

      <!-- Applicant Segment Selector -->
      <div style="padding: 1.25rem 2.25rem 0 2.25rem; background: var(--canvas-ivory, #FBF9F6); border-bottom: 1px solid var(--border-hairline, #EDE9E1);">
        <label style="display: block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted, #5A6260); margin-bottom: 0.5rem;">
          Select Your Executive Category <span style="color: #DC2626;">*</span>
        </label>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button type="button" class="segmented-option active" id="segFounder" onclick="setApplicantType('Founder')" style="flex: 1; min-width: 140px; padding: 0.65rem 1rem; border-radius: 6px; border: 1px solid var(--card-border, #E8E4DC); background: #FAF8F5; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; font-weight: 600; color: #1A1A1A; cursor: pointer; text-align: center; transition: all 0.2s;">
            Founder / Co-Founder
          </button>
          <button type="button" class="segmented-option" id="segBizOwner" onclick="setApplicantType('Business Owner')" style="flex: 1; min-width: 140px; padding: 0.65rem 1rem; border-radius: 6px; border: 1px solid var(--card-border, #E8E4DC); background: #FAF8F5; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; font-weight: 600; color: #1A1A1A; cursor: pointer; text-align: center; transition: all 0.2s;">
            Business Owner / MD
          </button>
          <button type="button" class="segmented-option" id="segProfessional" onclick="setApplicantType('Professional')" style="flex: 1; min-width: 140px; padding: 0.65rem 1rem; border-radius: 6px; border: 1px solid var(--card-border, #E8E4DC); background: #FAF8F5; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; font-weight: 600; color: #1A1A1A; cursor: pointer; text-align: center; transition: all 0.2s;">
            Founding Partner / Executive
          </button>
        </div>

        <!-- Stepper Indicator -->
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 1.25rem; overflow-x: auto; padding-bottom: 0.75rem; gap: 8px;">
          <div class="app-step-pill active" id="stepPill1" onclick="jumpToAppStep(1)" style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 700; color: #064E3B; white-space: nowrap;">
            <span style="width: 20px; height: 20px; border-radius: 50%; background: #064E3B; color: #FAF8F5; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">1</span>
            <span>Identity</span>
          </div>
          <span style="color: #D1D5DB; font-size: 0.8rem;">&rarr;</span>
          <div class="app-step-pill" id="stepPill2" onclick="jumpToAppStep(2)" style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 600; color: #6B7280; white-space: nowrap;">
            <span style="width: 20px; height: 20px; border-radius: 50%; background: #E5E7EB; color: #4B5563; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">2</span>
            <span>Entity</span>
          </div>
          <span style="color: #D1D5DB; font-size: 0.8rem;">&rarr;</span>
          <div class="app-step-pill" id="stepPill3" onclick="jumpToAppStep(3)" style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 600; color: #6B7280; white-space: nowrap;">
            <span style="width: 20px; height: 20px; border-radius: 50%; background: #E5E7EB; color: #4B5563; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">3</span>
            <span>Footprint</span>
          </div>
          <span style="color: #D1D5DB; font-size: 0.8rem;">&rarr;</span>
          <div class="app-step-pill" id="stepPill4" onclick="jumpToAppStep(4)" style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 600; color: #6B7280; white-space: nowrap;">
            <span style="width: 20px; height: 20px; border-radius: 50%; background: #E5E7EB; color: #4B5563; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">4</span>
            <span>Give &amp; Ask</span>
          </div>
          <span style="color: #D1D5DB; font-size: 0.8rem;">&rarr;</span>
          <div class="app-step-pill" id="stepPill5" onclick="jumpToAppStep(5)" style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 600; color: #6B7280; white-space: nowrap;">
            <span style="width: 20px; height: 20px; border-radius: 50%; background: #E5E7EB; color: #4B5563; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">5</span>
            <span>Formats</span>
          </div>
          <span style="color: #D1D5DB; font-size: 0.8rem;">&rarr;</span>
          <div class="app-step-pill" id="stepPill6" onclick="jumpToAppStep(6)" style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 600; color: #6B7280; white-space: nowrap;">
            <span style="width: 20px; height: 20px; border-radius: 50%; background: #E5E7EB; color: #4B5563; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem;">6</span>
            <span>Charter</span>
          </div>
        </div>
      </div>

      <!-- Main Application Form Body -->
      <form id="showInterestForm" onsubmit="handleShowInterestSubmit(event)" style="padding: 2rem 2.25rem;">
        <input type="hidden" id="app_applicant_type" value="Founder">

        <!-- =================== STEP 1: IDENTITY & ROLE =================== -->
        <div id="appStep1" class="app-step-content" style="display: block;">
          <div style="margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Domine', serif; font-size: 1.35rem; font-weight: 700; color: #064E3B; margin: 0 0 0.25rem 0;">Founder Identity &amp; Contact Anchor</h3>
            <p style="font-size: 0.85rem; color: #5A6260; margin: 0;">Direct personal details used by the admissions committee for verification.</p>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Full Legal Name <span style="color: #DC2626;">*</span></label>
              <input type="text" id="app_full_name" class="form-input" required placeholder="e.g. Siddharth Mehta" style="border-radius: 6px; height: 44px;">
              <span style="font-size: 0.72rem; color: #7E8784;">Legal name matching government identification</span>
            </div>

            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Designation / Executive Role <span style="color: #DC2626;">*</span></label>
              <input type="text" id="app_designation" class="form-input" required placeholder="e.g. Founder &amp; CEO" style="border-radius: 6px; height: 44px;">
              <span style="font-size: 0.72rem; color: #7E8784;">Restricted exclusively to equity founders &amp; promoters</span>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Official Work Email <span style="color: #DC2626;">*</span></label>
              <input type="email" id="app_email" class="form-input" required placeholder="name@yourcompany.com" style="border-radius: 6px; height: 44px;">
              <span style="font-size: 0.72rem; color: #7E8784;">Domain work email required for fast-track vetting</span>
            </div>

            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Direct WhatsApp Number <span style="color: #DC2626;">*</span></label>
              <div style="display: flex; gap: 8px;">
                <span style="height: 44px; padding: 0 12px; background: #EDE9E1; border: 1px solid #E8E4DC; border-radius: 6px; display: inline-flex; align-items: center; font-size: 0.85rem; font-weight: 700; color: #064E3B;">+91</span>
                <input type="tel" id="app_phone" class="form-input" required placeholder="9876543210" maxlength="10" style="border-radius: 6px; height: 44px; flex: 1;">
              </div>
              <input type="hidden" id="app_whatsapp">
              <span style="font-size: 0.72rem; color: #7E8784;">For confidential executive salon invites &amp; city circles</span>
            </div>
          </div>

          <div class="form-group" style="margin: 0;">
            <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">City Hub / Primary Base <span style="color: #DC2626;">*</span></label>
            <select id="app_city" class="form-select" required style="border-radius: 6px; height: 44px;">
              <option value="Bengaluru" selected>Bengaluru (Hub)</option>
              <option value="Mumbai MMR">Mumbai MMR</option>
              <option value="Delhi NCR">Delhi NCR</option>
              <option value="Hyderabad">Hyderabad</option>
              <option value="Pune">Pune</option>
              <option value="Chennai">Chennai</option>
              <option value="Ahmedabad">Ahmedabad</option>
              <option value="Other Metros">Other Metros / Global</option>
            </select>
          </div>

          <div style="display: flex; justify-content: flex-end; margin-top: 2rem;">
            <button type="button" class="btn btn-emerald" onclick="nextAppStep(1)" style="padding: 0.75rem 1.75rem; border-radius: 6px; font-weight: 700;">
              Next: Entity &amp; Scale &rarr;
            </button>
          </div>
        </div>

        <!-- =================== STEP 2: BUSINESS PROFILE & SCALE =================== -->
        <div id="appStep2" class="app-step-content" style="display: none;">
          <div style="margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Domine', serif; font-size: 1.35rem; font-weight: 700; color: #064E3B; margin: 0 0 0.25rem 0;">Entity Structure &amp; Scale Trajectory</h3>
            <p style="font-size: 0.85rem; color: #5A6260; margin: 0;">Information verifying your active venture footprint and operating model.</p>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Registered Entity / Brand Name <span style="color: #DC2626;">*</span></label>
              <input type="text" id="app_business_name" class="form-input" required placeholder="e.g. Apex Logix Private Limited" style="border-radius: 6px; height: 44px;">
            </div>

            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Corporate Structure</label>
              <select id="app_firm_type" class="form-select" style="border-radius: 6px; height: 44px;">
                <option value="Private Limited (Pvt Ltd)">Private Limited Company (Pvt Ltd)</option>
                <option value="Limited Liability Partnership (LLP)">Limited Liability Partnership (LLP)</option>
                <option value="Delaware C-Corp">Delaware C-Corp / Flip Entity</option>
                <option value="Public Limited">Public Limited Company</option>
                <option value="Partnership / Sole Prop">Partnership / Sole Proprietorship</option>
              </select>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Business Archetype <span style="color: #DC2626;">*</span></label>
              <select id="app_business_category" class="form-select" required style="border-radius: 6px; height: 44px;">
                <option value="Technology &amp; Software">B2B SaaS / Enterprise Software</option>
                <option value="Manufacturing &amp; Engineering">Precision Manufacturing &amp; Industrial</option>
                <option value="Retail &amp; E-commerce">D2C &amp; High-Growth Retail</option>
                <option value="Finance &amp; FinTech">Fintech, BFSI &amp; Capital Markets</option>
                <option value="Healthcare &amp; Pharma">HealthTech &amp; MedTech</option>
                <option value="Logistics &amp; Supply Chain">Supply Chain &amp; Logistics Infra</option>
                <option value="Professional Services">Specialized Tech Consulting &amp; Agency</option>
              </select>
            </div>

            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Operating Vintage</label>
              <select id="app_years_in_business" class="form-select" style="border-radius: 6px; height: 44px;">
                <option value="0 - 12 Months">&lt; 1 Year (Seed Genesis)</option>
                <option value="1 - 3 Years" selected>1 - 3 Years (PMR &amp; Initial Scale)</option>
                <option value="3 - 7 Years">3 - 7 Years (Mature Growth)</option>
                <option value="7+ Years">7+ Years (Established Scale)</option>
              </select>
            </div>

            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Active Team Size</label>
              <select id="app_team_size" class="form-select" style="border-radius: 6px; height: 44px;">
                <option value="1 - 10 Members">1 - 10 Full-time Operators</option>
                <option value="11 - 50 Members" selected>11 - 50 FTEs</option>
                <option value="51 - 200 Members">51 - 200 FTEs</option>
                <option value="200+ Members">200+ Team Members</option>
              </select>
            </div>
          </div>

          <div class="form-group" style="margin: 0;">
            <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Capital &amp; Profitability Trajectory</label>
            <select id="app_business_stage" class="form-select" style="border-radius: 6px; height: 44px;">
              <option value="Bootstrapped">Bootstrapped (Self-funded, Cash Flow Positive)</option>
              <option value="Seed Funded">Angel / Seed Funded</option>
              <option value="Venture Backed">Venture Backed (Series A+)</option>
              <option value="Established Scale" selected>Profitable Scale / Dividend Generating</option>
            </select>
          </div>

          <input type="hidden" id="app_business_model_category" value="Product Based">

          <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
            <button type="button" class="btn btn-secondary" onclick="prevAppStep(2)" style="padding: 0.75rem 1.5rem; border-radius: 6px;">&larr; Back</button>
            <button type="button" class="btn btn-emerald" onclick="nextAppStep(2)" style="padding: 0.75rem 1.75rem; border-radius: 6px; font-weight: 700;">Next: Digital Footprint &rarr;</button>
          </div>
        </div>

        <!-- =================== STEP 3: WEB & DIGITAL FOOTPRINT =================== -->
        <div id="appStep3" class="app-step-content" style="display: none;">
          <div style="margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Domine', serif; font-size: 1.35rem; font-weight: 700; color: #064E3B; margin: 0 0 0.25rem 0;">Web &amp; Digital Verification Footprint</h3>
            <p style="font-size: 0.85rem; color: #5A6260; margin: 0;">Our admissions committee conducts cross-checks against registered URLs and social profiles.</p>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Company Website URL <span style="color: #DC2626;">*</span></label>
              <input type="url" id="app_website" class="form-input" required placeholder="https://yourcompany.com" style="border-radius: 6px; height: 44px;">
            </div>

            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Founder LinkedIn Profile <span style="color: #DC2626;">*</span></label>
              <input type="url" id="app_linkedin" class="form-input" required placeholder="https://linkedin.com/in/yourprofile" style="border-radius: 6px; height: 44px;">
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Twitter / X Profile (Optional)</label>
              <input type="text" id="app_instagram" class="form-input" placeholder="https://x.com/yourhandle or @handle" style="border-radius: 6px; height: 44px;">
            </div>
            
            <div class="form-group" style="margin: 0;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Brief Core Pitch / Business Model</label>
              <input type="text" id="app_business_description" class="form-input" placeholder="One sentence summary of what your business solves" style="border-radius: 6px; height: 44px;">
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
            <button type="button" class="btn btn-secondary" onclick="prevAppStep(3)" style="padding: 0.75rem 1.5rem; border-radius: 6px;">&larr; Back</button>
            <button type="button" class="btn btn-emerald" onclick="nextAppStep(3)" style="padding: 0.75rem 1.75rem; border-radius: 6px; font-weight: 700;">Next: Value Exchange &rarr;</button>
          </div>
        </div>

        <!-- =================== STEP 4: VALUE CONTRIBUTION & BOTTLENECK =================== -->
        <div id="appStep4" class="app-step-content" style="display: none;">
          <div style="margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Domine', serif; font-size: 1.35rem; font-weight: 700; color: #064E3B; margin: 0 0 0.25rem 0;">Value Contribution &amp; Critical Bottlenecks</h3>
            <p style="font-size: 0.85rem; color: #5A6260; margin: 0;">The foundation of Founder for Founder is reciprocity: giving before taking.</p>
          </div>

          <div class="form-group" style="margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A; margin: 0;">What specific expertise or value can you contribute to fellow founders? <span style="color: #DC2626;">*</span></label>
              <span style="font-size: 0.68rem; font-weight: 700; color: #064E3B; background: #D1FAE5; padding: 2px 8px; border-radius: 4px;">CORE SELECTION METRIC</span>
            </div>
            <textarea id="app_what_offer" class="form-textarea" required rows="3" placeholder="e.g. Scaled B2B SaaS ARR from $0 to $3M, deep expertise in outbound enterprise sales cycles, UAE cross-border tax structuring, supply chain vendor contracts." style="border-radius: 6px;"></textarea>
            <span style="font-size: 0.72rem; color: #7E8784;">We prioritize high-give founders who actively share operational playbooks and hard-won lessons.</span>
          </div>

          <div class="form-group" style="margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A; margin: 0;">What are your most critical operational bottlenecks or immediate needs? <span style="color: #DC2626;">*</span></label>
              <span style="font-size: 0.68rem; font-weight: 700; color: #4B5563; background: #F3F4F6; padding: 2px 8px; border-radius: 4px;">CONFIDENTIAL</span>
            </div>
            <textarea id="app_what_need" class="form-textarea" required rows="3" placeholder="e.g. Seeking recommendations for trusted US patent attorney, introductions to growth-stage working capital lenders, hiring a VP of Engineering." style="border-radius: 6px;"></textarea>
            <span style="font-size: 0.72rem; color: #7E8784;">Used by the admissions team to immediately pair you with the right peer founders upon acceptance.</span>
          </div>

          <div class="form-group" style="margin: 0;">
            <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Why do you wish to join Founder for Founder? <span style="color: #DC2626;">*</span></label>
            <textarea id="app_why_join" class="form-textarea" required rows="2" placeholder="Your perspective on peer community, trust, and confidentiality." style="border-radius: 6px;"></textarea>
          </div>

          <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
            <button type="button" class="btn btn-secondary" onclick="prevAppStep(4)" style="padding: 0.75rem 1.5rem; border-radius: 6px;">&larr; Back</button>
            <button type="button" class="btn btn-emerald" onclick="nextAppStep(4)" style="padding: 0.75rem 1.75rem; border-radius: 6px; font-weight: 700;">Next: Formats &rarr;</button>
          </div>
        </div>

        <!-- =================== STEP 5: COLLABORATION PREFERENCES =================== -->
        <div id="appStep5" class="app-step-content" style="display: none;">
          <div style="margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Domine', serif; font-size: 1.35rem; font-weight: 700; color: #064E3B; margin: 0 0 0.25rem 0;">Active Collaboration Formats</h3>
            <p style="font-size: 0.85rem; color: #5A6260; margin: 0;">Select the intimate gatherings in which you are committed to actively participating.</p>
          </div>

          <div style="display: grid; grid-template-columns: 1fr; gap: 12px; margin-bottom: 1.5rem;">
            <label style="display: flex; align-items: flex-start; gap: 12px; padding: 1rem; background: #FAF8F5; border: 1px solid #E8E4DC; border-radius: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#064E3B'" onmouseout="this.style.borderColor='#E8E4DC'">
              <input type="checkbox" name="collab_pref" value="Curated Founder Dinners" checked style="margin-top: 4px; accent-color: #064E3B; width: 18px; height: 18px;">
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #1A1A1A;">Curated Founder Dinners</div>
                <div style="font-size: 0.78rem; color: #5A6260; margin-top: 2px;">Private 8-person dinners hosted bi-monthly at secluded private dining venues across Bengaluru, Mumbai, and Delhi NCR.</div>
              </div>
            </label>

            <label style="display: flex; align-items: flex-start; gap: 12px; padding: 1rem; background: #FAF8F5; border: 1px solid #E8E4DC; border-radius: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#064E3B'" onmouseout="this.style.borderColor='#E8E4DC'">
              <input type="checkbox" name="collab_pref" value="Closed-Door Salons" checked style="margin-top: 4px; accent-color: #064E3B; width: 18px; height: 18px;">
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #1A1A1A;">Closed-Door Salons</div>
                <div style="font-size: 0.78rem; color: #5A6260; margin-top: 2px;">Deep-dive confidential masterminds on tax structuring, secondary sales, debt syndication, and enterprise M&amp;A.</div>
              </div>
            </label>

            <label style="display: flex; align-items: flex-start; gap: 12px; padding: 1rem; background: #FAF8F5; border: 1px solid #E8E4DC; border-radius: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#064E3B'" onmouseout="this.style.borderColor='#E8E4DC'">
              <input type="checkbox" name="collab_pref" value="1:1 Coffee Matchups" checked style="margin-top: 4px; accent-color: #064E3B; width: 18px; height: 18px;">
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #1A1A1A;">1:1 High-Trust Coffee Matchups</div>
                <div style="font-size: 0.78rem; color: #5A6260; margin-top: 2px;">Direct peer introductions tailored around complementary operational expertise and shared business scale.</div>
              </div>
            </label>

            <label style="display: flex; align-items: flex-start; gap: 12px; padding: 1rem; background: #FAF8F5; border: 1px solid #E8E4DC; border-radius: 8px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#064E3B'" onmouseout="this.style.borderColor='#E8E4DC'">
              <input type="checkbox" name="collab_pref" value="Annual Founders Sanctuary" checked style="margin-top: 4px; accent-color: #064E3B; width: 18px; height: 18px;">
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #1A1A1A;">Annual Founders' Sanctuary</div>
                <div style="font-size: 0.78rem; color: #5A6260; margin-top: 2px;">An exclusive 3-day annual retreat gathering verified fellows in pristine wellness destinations (Goa / Coorg / Himachal).</div>
              </div>
            </label>
          </div>

          <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
            <button type="button" class="btn btn-secondary" onclick="prevAppStep(5)" style="padding: 0.75rem 1.5rem; border-radius: 6px;">&larr; Back</button>
            <button type="button" class="btn btn-emerald" onclick="nextAppStep(5)" style="padding: 0.75rem 1.75rem; border-radius: 6px; font-weight: 700;">Next: Charter &amp; Submit &rarr;</button>
          </div>
        </div>

        <!-- =================== STEP 6: CHARTER & SUBMISSION =================== -->
        <div id="appStep6" class="app-step-content" style="display: none;">
          <div style="margin-bottom: 1.5rem;">
            <h3 style="font-family: 'Domine', serif; font-size: 1.35rem; font-weight: 700; color: #064E3B; margin: 0 0 0.25rem 0;">Charter of Conduct &amp; Discretion</h3>
            <p style="font-size: 0.85rem; color: #5A6260; margin: 0;">Founder for Founder exists strictly as a safe haven. To preserve integrity, every applicant binds themselves to our core covenants.</p>
          </div>

          <div style="background: #F4FBF7; border: 1px solid #A7F3D0; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#064E3B" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span style="font-size: 0.88rem; font-weight: 700; color: #064E3B;">Guaranteed Sovereign Safe Space</span>
            </div>
            <ul style="margin: 0; padding-left: 1.25rem; font-size: 0.8rem; color: #064E3B; line-height: 1.6;">
              <li><strong>Chatham House Discretion:</strong> All discussions, revenue figures, and private vulnerabilities shared inside the collective remain strictly confidential.</li>
              <li><strong>Zero-Solicitation Code:</strong> Unsolicited sales pitches, mercenary cold messaging, or agency recruiting result in immediate, non-negotiable expulsion.</li>
              <li><strong>Radical Reciprocity:</strong> Members commit to being candid, supportive sounding boards for peers navigating scale inflection points.</li>
            </ul>
          </div>

          <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 1.5rem;">
            <label style="display: flex; align-items: flex-start; gap: 10px; cursor: pointer;">
              <input type="checkbox" id="app_consent" required checked style="margin-top: 3px; accent-color: #064E3B; width: 18px; height: 18px;">
              <span style="font-size: 0.82rem; color: #1A1A1A; line-height: 1.5;">
                I accept the Chatham House code of discretion and commit to active reciprocity. I understand that violating member confidentiality results in immediate expulsion and forfeiture. <span style="color: #DC2626;">*</span>
              </span>
            </label>

            <label style="display: flex; align-items: flex-start; gap: 10px; cursor: pointer;">
              <input type="checkbox" required checked style="margin-top: 3px; accent-color: #064E3B; width: 18px; height: 18px;">
              <span style="font-size: 0.82rem; color: #1A1A1A; line-height: 1.5;">
                I affirm that all business figures, domain credentials, and operational metrics provided are accurate and truthful to the best of my knowledge. <span style="color: #DC2626;">*</span>
              </span>
            </label>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 2rem; padding-top: 1.25rem; border-top: 1px solid #EDE9E1;">
            <button type="button" class="btn btn-secondary" onclick="prevAppStep(6)" style="padding: 0.75rem 1.5rem; border-radius: 6px;">&larr; Back</button>
            <button type="submit" class="btn btn-emerald" style="padding: 0.85rem 2.25rem; border-radius: 6px; font-weight: 700; font-size: 0.95rem; letter-spacing: 0.02em;">
              SUBMIT ADMISSIONS APPLICATION
            </button>
          </div>
        </div>

      </form>
    </div>
  </div>'''

def generate_login_modal():
    return '''<!-- MODAL 4: MEMBER LOGIN (STITCH REVISED EXECUTIVE GUILD) -->
  <div class="modal-overlay" id="loginModal" style="display:none; align-items: center; justify-content: center; padding: 1.5rem 1rem;">
    <div class="modal-content" style="max-width: 460px; width: 100%; margin: auto; background: var(--canvas-cream, #FAF8F5); border: 1px solid var(--card-border, #E8E4DC); border-radius: 12px; box-shadow: 0 20px 40px -10px rgba(6, 78, 59, 0.2); overflow: hidden; padding: 0;">
      
      <!-- Modal Header -->
      <div style="background: linear-gradient(135deg, #003527 0%, #064E3B 100%); color: #FAF8F5; padding: 1.75rem 2rem; position: relative; text-align: center;">
        <button class="modal-close" onclick="closeModal('loginModal')" style="position: absolute; top: 1rem; right: 1rem; color: #FAF8F5; background: rgba(255,255,255,0.12); border: none; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; cursor: pointer; transition: all 0.2s;">&times;</button>
        
        <div style="width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); display: flex; align-items: center; justify-content: center; margin: 0 auto 0.75rem auto;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
        </div>
        
        <h2 style="font-family: 'Domine', serif; font-size: 1.6rem; font-weight: 700; color: #FAF8F5; margin: 0 0 0.35rem 0;">
          Member Access
        </h2>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #D1FAE5; margin: 0;">
          Sign in to the Founder for Founder member portal.
        </p>
      </div>

      <!-- Modal Body -->
      <div style="padding: 1.75rem 2rem;">
        <!-- GOOGLE AUTHENTICATION SECTION -->
        <div style="margin-bottom: 1.25rem;">
          <div id="googleSignInBtn" style="display: flex; justify-content: center; margin-bottom: 0.5rem; min-height: 44px;"></div>
          <button type="button" class="btn-google-auth" id="customGoogleAuthBtn" onclick="initiateGoogleLogin()" style="width: 100%; height: 44px; border-radius: 6px; border: 1px solid #E8E4DC; background: #FFFFFF; font-weight: 600; font-size: 0.88rem; color: #1A1A1A; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; transition: all 0.2s;">
            <svg class="google-logo-svg" width="18" height="18" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            <span>Continue with Google</span>
          </button>
        </div>

        <!-- SEPARATOR -->
        <div class="auth-divider" style="display: flex; align-items: center; text-align: center; margin: 1.25rem 0;">
          <span style="flex: 1; border-bottom: 1px solid #EDE9E1;"></span>
          <span style="padding: 0 10px; font-size: 0.75rem; font-weight: 600; color: #7E8784; text-transform: uppercase;">or sign in with credentials</span>
          <span style="flex: 1; border-bottom: 1px solid #EDE9E1;"></span>
        </div>

        <form id="loginForm" onsubmit="handleLoginSubmit(event)">
          <div class="form-group" style="margin-bottom: 1rem;">
            <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A;">Email Address</label>
            <input type="email" id="login_email" class="form-input" required placeholder="Enter your registered email address" style="border-radius: 6px; height: 44px;">
          </div>
          
          <div class="form-group" style="margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <label class="form-label" style="font-size: 0.82rem; font-weight: 700; color: #1A1A1A; margin: 0;">Password</label>
              <button type="button" onclick="handleSendLoginOtp()" style="background: none; border: none; padding: 0; font-size: 0.78rem; color: #064E3B; font-weight: 700; cursor: pointer; text-decoration: underline;">Sign in with Email OTP</button>
            </div>
            <input type="password" id="login_password" class="form-input" placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;" style="border-radius: 6px; height: 44px;">
          </div>

          <!-- EMAIL OTP VERIFICATION SECTION -->
          <div id="loginOtpSection" style="display: none; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 12px; border-radius: 6px; margin-bottom: 1.25rem;">
            <label class="form-label" style="font-size: 0.8rem; font-weight: 700; color: #064E3B; margin-bottom: 4px;">Enter Verification OTP</label>
            <div style="display: flex; gap: 8px;">
              <input type="text" id="login_otp" class="form-input" placeholder="6-digit code" maxlength="6" style="letter-spacing: 3px; font-weight: 700; text-align: center; border-radius: 6px; height: 40px;">
              <button type="button" class="btn btn-emerald" style="padding: 0 1.25rem; font-size: 0.82rem; white-space: nowrap; border-radius: 6px; height: 40px; font-weight: 700;" onclick="handleVerifyLoginOtp()">Verify &amp; Enter</button>
            </div>
            <div style="font-size: 0.72rem; color: #065F46; margin-top: 6px;">A one-time login code will be sent to your registered email.</div>
          </div>

          <button type="submit" class="btn btn-emerald" style="width: 100%; justify-content: center; height: 44px; border-radius: 6px; font-weight: 700; font-size: 0.9rem; letter-spacing: 0.04em;">
            LOGIN TO PORTAL
          </button>
        </form>

        <div style="margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border-hairline, #EDE9E1); text-align: center; font-size: 0.82rem; color: var(--text-muted, #5A6260);">
          Looking to join? <a href="javascript:void(0)" onclick="closeModal('loginModal'); openShowInterestModal();" style="color: #064E3B; font-weight: 700; text-decoration: underline;">Apply for Membership</a>
        </div>
      </div>
    </div>
  </div>'''

def apply_modals_update():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace showInterestModal
    p1 = html.find('<!-- MODAL 1: SHOW INTEREST APPLICATION -->')
    p2 = html.find('<!-- MODAL: APPLICATION DETAIL')
    if p1 != -1 and p2 != -1:
        new_app_modal = generate_admissions_modal() + '\n\n  '
        html = html[:p1] + new_app_modal + html[p2:]
        print("Updated showInterestModal successfully!")
    else:
        print("Failed to locate showInterestModal boundaries:", p1, p2)

    # Replace loginModal
    lp1 = html.find('<!-- MODAL 4: MEMBER LOGIN -->')
    lp2 = html.find('<!-- MODAL 5: PAYMENT CONFIRMATION -->')
    if lp1 != -1 and lp2 != -1:
        new_login_modal = generate_login_modal() + '\n\n  '
        html = html[:lp1] + new_login_modal + html[lp2:]
        print("Updated loginModal successfully!")
    else:
        print("Failed to locate loginModal boundaries:", lp1, lp2)

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("public/index.html saved successfully.")

if __name__ == '__main__':
    apply_modals_update()
