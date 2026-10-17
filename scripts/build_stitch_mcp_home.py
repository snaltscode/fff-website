import os
import re
import subprocess
from prepare_questionnaire import get_prepared_questionnaire

def build_home():
    # 1. Read Stitch MCP Home Desktop screen
    with open('stitch_mcp_export/html/b12ad31e7d8b4172af2f869e9eed8c5c_Founder for Founder _ Home _Desktop_.html', 'r', encoding='utf-8') as f:
        mcp_home = f.read()

    # 2. Get prepared Admissions Questionnaire HTML
    q_content = get_prepared_questionnaire()

    # 3. Read Authenticated Member Portal and other Modals from backup-stitch-redesign
    backup_index = subprocess.check_output(['git', 'show', 'backup-stitch-redesign:public/index.html']).decode('utf-8')

    portal_start = backup_index.find('<!-- AUTHENTICATED MEMBER PORTAL & DASHBOARD -->')
    if portal_start == -1:
        portal_start = backup_index.find('<div id="portalPage"')

    login_start = backup_index.find('<div class="modal-overlay" id="loginModal"')
    modals_end = backup_index.find('<!-- SCRIPTS -->')
    if modals_end == -1:
        modals_end = backup_index.find('<script src="/js/app.js')

    portal_html = backup_index[portal_start:login_start]
    other_modals = backup_index[login_start:modals_end]

    # 4. Enhance <head> with styles.css link and viewport fixes
    head_insertion = '''
  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/css/styles.css">
  <style>
    /* Executive Guild Overrides & Reset */
    .portal-container { display: none; }
    .portal-container.active { display: flex !important; }
    .modal-overlay { display: none; }
    .modal-overlay.active { display: flex !important; }
    /* Ensure Stitch fonts load cleanly */
    h1, h2, h3, .font-headline-hero, .font-headline-lg, .font-headline-md, .font-headline-sm {
      font-family: 'Domine', serif !important;
    }
    body, p, span, button, input, select, textarea, label {
      font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
  </style>
'''
    mcp_home = mcp_home.replace('</head>', head_insertion + '\n</head>')

    # 5. Enhance Navigation:
    # Wire Request Admissions CTA and Member Login
    # Wire section anchors: The Alliance -> #philosophy, Pillars -> #pillars, Gatherings -> #gatherings, FAQ -> #testimonials-faqs
    mcp_home = re.sub(r'data-path="show-interest"\s+href="#"', 'href="javascript:void(0)" onclick="openShowInterestModal()"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="show-interest"', 'href="javascript:void(0)" onclick="openShowInterestModal()"', mcp_home)
    mcp_home = re.sub(r'data-path="login"\s+href="#"', 'href="javascript:void(0)" onclick="openLoginModal()"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="login"', 'href="javascript:void(0)" onclick="openLoginModal()"', mcp_home)

    mcp_home = re.sub(r'data-path="about"\s+href="#"', 'href="#philosophy"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="about"', 'href="#philosophy"', mcp_home)
    mcp_home = re.sub(r'data-path="experiences"\s+href="#"', 'href="#pillars"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="experiences"', 'href="#pillars"', mcp_home)
    mcp_home = re.sub(r'data-path="directory"\s+href="#"', 'href="#gatherings"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="directory"', 'href="#gatherings"', mcp_home)
    mcp_home = re.sub(r'data-path="confidentiality"\s+href="#"', 'href="#testimonials-faqs"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="confidentiality"', 'href="#testimonials-faqs"', mcp_home)

    # Add section IDs
    mcp_home = mcp_home.replace('<!-- CORE PHILOSOPHY -->\n<section', '<!-- CORE PHILOSOPHY -->\n<section id="philosophy"')
    mcp_home = mcp_home.replace('<!-- THE 5 PILLARS OF PEER ENGAGEMENT -->\n<section', '<!-- THE 5 PILLARS OF PEER ENGAGEMENT -->\n<section id="pillars"')
    mcp_home = mcp_home.replace('<!-- MOMENTS OF LEVERAGE / CURATED GATHERINGS -->\n<section', '<!-- MOMENTS OF LEVERAGE / CURATED GATHERINGS -->\n<section id="gatherings"')

    # Inject authNavControls into header
    auth_nav_html = '''
      <!-- Authenticated User Controls -->
      <div id="authNavControls" class="hidden items-center gap-3">
        <span class="font-label-md text-label-md text-primary font-semibold hidden md:inline" id="navUserName">Welcome</span>
        <button class="px-4 py-2 rounded-[6px] bg-secondary-container text-on-secondary-container font-label-md text-label-md font-semibold hover:opacity-90 transition-all cursor-pointer" onclick="switchPortalTab('dashboard', this)">Portal</button>
        <button class="px-4 py-2 rounded-[6px] bg-surface-container-highest text-primary font-label-md text-label-md font-semibold hover:bg-surface-container transition-all cursor-pointer hidden" id="navAdminBtn" onclick="switchPortalTab('admin', this)">Admin</button>
        <button class="px-3 py-2 rounded-[6px] text-error font-label-md text-label-md font-medium hover:bg-error-container/30 transition-all cursor-pointer" onclick="logout()">Logout</button>
      </div>
'''
    # Find navigation actions container in header
    # Replace action block in header or append authNavControls
    mcp_home = mcp_home.replace('</header>', auth_nav_html + '\n    </div>\n  </header>')
    # Fix potential double closing div
    mcp_home = mcp_home.replace('    </div>\n  </header>', '  </header>')

    # Wrap public landing content with <div id="publicPage">
    # Starts right after <header ... </header>
    header_end_idx = mcp_home.find('</header>') + len('</header>')
    main_start = mcp_home.find('<main', header_end_idx)

    # 6. Insert Dynamic CMS Section (Counters, Testimonials, FAQs, Event Gallery)
    dynamic_cms_section = '''
<!-- DYNAMIC CMS SECTION: TESTIMONIALS & FAQS -->
<section class="w-full bg-surface-container-low py-20 lg:py-28" id="testimonials-faqs">
  <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop flex flex-col gap-space-xl">
    
    <!-- Dynamic Counters -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 w-full" id="countersGrid">
      <div class="flex flex-col items-center p-6 rounded-2xl bg-surface-container-lowest shadow-sm text-center">
        <span class="font-headline-lg text-headline-lg text-primary font-bold" id="statMembers">120+</span>
        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mt-1">Vetted Founders</span>
      </div>
      <div class="flex flex-col items-center p-6 rounded-2xl bg-surface-container-lowest shadow-sm text-center">
        <span class="font-headline-lg text-headline-lg text-primary font-bold" id="statCities">14</span>
        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mt-1">Metros & Hubs</span>
      </div>
      <div class="flex flex-col items-center p-6 rounded-2xl bg-surface-container-lowest shadow-sm text-center">
        <span class="font-headline-lg text-headline-lg text-primary font-bold" id="statGMV">₹450Cr+</span>
        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mt-1">Cumulative GMV</span>
      </div>
      <div class="flex flex-col items-center p-6 rounded-2xl bg-surface-container-lowest shadow-sm text-center">
        <span class="font-headline-lg text-headline-lg text-primary font-bold" id="statAttendance">94%</span>
        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mt-1">Gathering Presence</span>
      </div>
    </div>

    <!-- Testimonials Header -->
    <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-space-xs mt-8">
      <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
        PEER PERSPECTIVES
      </span>
      <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
        What Founders Say
      </h2>
      <p class="font-body-lg text-body-lg text-on-surface-variant">
        Authentic reflections from leaders scaling ventures inside the Founder for Founder network.
      </p>
    </div>

    <!-- Testimonials Container (Hydrated from CMS) -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter" id="testimonialsContainer">
      <div class="flex flex-col p-space-lg rounded-2xl bg-surface-container-lowest shadow-sm flex-1">
        <p class="font-body-md text-body-md text-on-surface leading-relaxed flex-1 italic mb-4">
          “Founder for Founder is completely different from noisy networking clubs. The intimate dinners and closed-door salons gave us direct access to high-integrity enterprise partners.”
        </p>
        <div class="flex items-center gap-3 pt-3 border-t border-surface-container">
          <div class="w-10 h-10 rounded-full bg-primary-fixed flex items-center justify-center font-bold text-on-primary-fixed">AK</div>
          <div class="flex flex-col">
            <span class="font-title-md text-title-md text-primary font-bold">Anand Krishnamurthy</span>
            <span class="font-label-md text-label-md text-on-surface-variant">Founder, QuantLogix</span>
          </div>
        </div>
      </div>
      <div class="flex flex-col p-space-lg rounded-2xl bg-surface-container-lowest shadow-sm flex-1">
        <p class="font-body-md text-body-md text-on-surface leading-relaxed flex-1 italic mb-4">
          “The sports meetups and weekend retreats create a level of camaraderie you just can't manufacture in conference ballrooms. Unmatched peer trust.”
        </p>
        <div class="flex items-center gap-3 pt-3 border-t border-surface-container">
          <div class="w-10 h-10 rounded-full bg-secondary-fixed flex items-center justify-center font-bold text-on-secondary-fixed">PS</div>
          <div class="flex flex-col">
            <span class="font-title-md text-title-md text-primary font-bold">Pooja Sharma</span>
            <span class="font-label-md text-label-md text-on-surface-variant">Co-Founder, BioVeda Labs</span>
          </div>
        </div>
      </div>
      <div class="flex flex-col p-space-lg rounded-2xl bg-surface-container-lowest shadow-sm flex-1">
        <p class="font-body-md text-body-md text-on-surface leading-relaxed flex-1 italic mb-4">
          “Through the Needs & Wants engine, we closed two key vendor partnerships within our first three weeks. High signal, zero spam.”
        </p>
        <div class="flex items-center gap-3 pt-3 border-t border-surface-container">
          <div class="w-10 h-10 rounded-full bg-primary-fixed-dim flex items-center justify-center font-bold text-on-primary-fixed">RV</div>
          <div class="flex flex-col">
            <span class="font-title-md text-title-md text-primary font-bold">Rohan Verma</span>
            <span class="font-label-md text-label-md text-on-surface-variant">CEO, UrbanScale Logistics</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Gallery Container (Hydrated from CMS) -->
    <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-space-xs mt-12">
      <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
        COMMUNITY ARCHIVE
      </span>
      <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
        Glimpses from Recent Gatherings
      </h2>
      <p class="font-body-lg text-body-lg text-on-surface-variant">
        Moments of candid exchange, executive roundtables, and sports sessions.
      </p>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="photoGalleryContainer">
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm">
        <img src="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80" alt="Executive Dinner" class="w-full h-full object-cover">
      </div>
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm">
        <img src="https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=600&q=80" alt="Founder Roundtable" class="w-full h-full object-cover">
      </div>
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm">
        <img src="https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=600&q=80" alt="Sports Meetup" class="w-full h-full object-cover">
      </div>
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm">
        <img src="https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=600&q=80" alt="Annual Retreat" class="w-full h-full object-cover">
      </div>
    </div>

    <!-- FAQs Section -->
    <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-space-xs mt-12">
      <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
        CLARITY & TRANSPARENCY
      </span>
      <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
        Frequently Asked Questions
      </h2>
      <p class="font-body-lg text-body-lg text-on-surface-variant">
        Everything you need to know about our community structure, admissions, and participation.
      </p>
    </div>

    <div class="max-w-3xl mx-auto w-full flex flex-col gap-3" id="faqsContainer">
      <details class="group bg-surface-container-lowest p-5 rounded-xl shadow-sm border border-surface-container">
        <summary class="font-title-md text-title-md text-primary font-bold cursor-pointer list-none flex justify-between items-center">
          <span>Who is eligible to join Founder for Founder?</span>
          <span class="material-symbols-outlined text-secondary transition-transform group-open:rotate-180">expand_more</span>
        </summary>
        <p class="font-body-md text-body-md text-on-surface-variant mt-3 leading-relaxed">
          Membership is strictly curated for active equity founders, co-founders, managing directors, and executive operators running registered businesses across India.
        </p>
      </details>
      <details class="group bg-surface-container-lowest p-5 rounded-xl shadow-sm border border-surface-container">
        <summary class="font-title-md text-title-md text-primary font-bold cursor-pointer list-none flex justify-between items-center">
          <span>How does the admissions review work?</span>
          <span class="material-symbols-outlined text-secondary transition-transform group-open:rotate-180">expand_more</span>
        </summary>
        <p class="font-body-md text-body-md text-on-surface-variant mt-3 leading-relaxed">
          Every application is reviewed on a rolling 72-hour window by our peer review committee to verify leadership track records, operational scale, and community alignment.
        </p>
      </details>
      <details class="group bg-surface-container-lowest p-5 rounded-xl shadow-sm border border-surface-container">
        <summary class="font-title-md text-title-md text-primary font-bold cursor-pointer list-none flex justify-between items-center">
          <span>What formats are included in membership?</span>
          <span class="material-symbols-outlined text-secondary transition-transform group-open:rotate-180">expand_more</span>
        </summary>
        <p class="font-body-md text-body-md text-on-surface-variant mt-3 leading-relaxed">
          Members gain access to sports & movement gatherings (pickleball, golf, badminton), intimate founder dinners, confidential advisory roundtables, retreats, and the digital portal.
        </p>
      </details>
      <details class="group bg-surface-container-lowest p-5 rounded-xl shadow-sm border border-surface-container">
        <summary class="font-title-md text-title-md text-primary font-bold cursor-pointer list-none flex justify-between items-center">
          <span>Is member information kept confidential?</span>
          <span class="material-symbols-outlined text-secondary transition-transform group-open:rotate-180">expand_more</span>
        </summary>
        <p class="font-body-md text-body-md text-on-surface-variant mt-3 leading-relaxed">
          Yes. All gatherings operate under strict Chatham House Rule and community non-solicitation guidelines. Private phone numbers and personal emails are never published publicly.
        </p>
      </details>
    </div>

  </div>
</section>
'''
    mcp_home = mcp_home.replace('<!-- FINAL CALL TO ACTION BANNER -->', dynamic_cms_section + '\n<!-- FINAL CALL TO ACTION BANNER -->')

    # Wrap main + footer in <div id="publicPage">
    # Locate where <main begins and where </footer> ends
    main_pos = mcp_home.find('<main')
    footer_end_pos = mcp_home.find('</footer>') + len('</footer>')

    public_content = mcp_home[main_pos:footer_end_pos]
    wrapped_public = f'<div id="publicPage">\n{public_content}\n</div>'

    # 7. Build Admissions Questionnaire Modal
    admissions_modal_html = f'''
<!-- STITCH ADMISSIONS QUESTIONNAIRE MODAL (Screen 975ae924) -->
<div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 bg-black/60 backdrop-blur-md overflow-y-auto" id="showInterestModal" style="display:none;">
  <div class="relative w-full max-w-5xl my-8 bg-surface rounded-2xl shadow-2xl overflow-hidden border border-surface-container">
    
    <!-- Close Button -->
    <button class="absolute top-4 right-4 z-50 w-10 h-10 rounded-full bg-surface-container-lowest/80 backdrop-blur-md flex items-center justify-center text-on-surface hover:bg-surface-container transition-colors shadow-sm cursor-pointer" onclick="closeModal('showInterestModal')" type="button">
      <span class="material-symbols-outlined text-2xl">close</span>
    </button>

    <!-- Modal Scrollable Content -->
    <div class="max-h-[85vh] overflow-y-auto p-4 sm:p-8">
      {q_content}
    </div>
  </div>
</div>
'''

    # 8. Dynamic Modal Control & Admissions Navigation Scripts
    scripts_html = '''
<!-- Dynamic Modal Control Helpers -->
<script>
function openShowInterestModal() {
  const m = document.getElementById('showInterestModal');
  if (m) {
    m.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    navigateToStep(1);
  }
}
function openLoginModal() {
  const m = document.getElementById('loginModal');
  if (m) {
    m.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}
function closeModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
}

// Multi-Step Admissions Wizard Engine
let currentStep = 1;
const totalSteps = 6;
const stepMeta = {
  1: { tracker: "SECTION 1 OF 6", title: "Founder Identity & Contact Anchor" },
  2: { tracker: "SECTION 2 OF 6", title: "Business Profile & Operating Scale" },
  3: { tracker: "SECTION 3 OF 6", title: "Digital Presence & Web Footprint" },
  4: { tracker: "SECTION 4 OF 6", title: "Community Contribution & Immediate Needs" },
  5: { tracker: "SECTION 5 OF 6", title: "Collaboration & Gathering Preferences" },
  6: { tracker: "SECTION 6 OF 6", title: "Confidentiality & Founder Affirmation" }
};

function updateStepUI() {
  for (let i = 1; i <= totalSteps; i++) {
    const stepElem = document.getElementById('form-step-' + i);
    if (stepElem) {
      if (i === currentStep) {
        stepElem.classList.remove('hidden');
        stepElem.classList.add('flex');
      } else {
        stepElem.classList.remove('flex');
        stepElem.classList.add('hidden');
      }
    }

    const bubble = document.getElementById('step-bubble-' + i);
    if (bubble) {
      if (i < currentStep) {
        bubble.className = "w-8 h-8 rounded-full bg-primary text-on-primary font-label-md text-label-md flex items-center justify-center transition-all";
        bubble.innerHTML = '<span class="material-symbols-outlined text-sm">check</span>';
      } else if (i === currentStep) {
        bubble.className = "w-8 h-8 rounded-full bg-primary-container text-on-primary font-label-md text-label-md flex items-center justify-center transition-all ring-2 ring-primary/20";
        bubble.innerText = i;
      } else {
        bubble.className = "w-8 h-8 rounded-full bg-surface-container text-on-surface font-label-md text-label-md flex items-center justify-center transition-all";
        bubble.innerText = i;
      }
    }

    if (i < totalSteps) {
      const line = document.getElementById('line-' + i);
      if (line) {
        line.className = (i < currentStep) ? "h-0.5 flex-1 min-w-4 bg-primary transition-colors" : "h-0.5 flex-1 min-w-4 bg-surface-container-high transition-colors";
      }
    }
  }

  const trackerLabel = document.getElementById('form-step-tracker');
  const titleLabel = document.getElementById('form-step-title');
  if (trackerLabel && titleLabel && stepMeta[currentStep]) {
    trackerLabel.innerText = stepMeta[currentStep].tracker;
    titleLabel.innerText = stepMeta[currentStep].title;
  }

  const prevBtn = document.getElementById('prev-step-btn');
  const nextBtn = document.getElementById('next-step-btn');
  const submitBtn = document.getElementById('submit-form-btn');

  if (prevBtn) {
    if (currentStep === 1) prevBtn.classList.add('hidden');
    else prevBtn.classList.remove('hidden');
  }

  if (nextBtn && submitBtn) {
    if (currentStep === totalSteps) {
      nextBtn.classList.add('hidden');
      submitBtn.classList.remove('hidden');
    } else {
      nextBtn.classList.remove('hidden');
      submitBtn.classList.add('hidden');
      nextBtn.innerText = "CONTINUE TO SECTION " + (currentStep + 1) + " →";
    }
  }

  const formCard = document.getElementById('showInterestForm');
  if (formCard) formCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function goToNextStep() {
  if (currentStep < totalSteps) {
    currentStep++;
    updateStepUI();
  }
}

function goToPreviousStep() {
  if (currentStep > 1) {
    currentStep--;
    updateStepUI();
  }
}

function navigateToStep(step) {
  if (step >= 1 && step <= totalSteps) {
    currentStep = step;
    updateStepUI();
  }
}

// Ensure first step is visible on page load
document.addEventListener('DOMContentLoaded', () => {
  navigateToStep(1);
});
</script>

<script src="/js/app.js?v=8.0" defer></script>
'''

    # Assemble final page:
    # head + header + wrapped_public + portal_html + admissions_modal_html + other_modals + scripts_html + </body></html>
    before_main = mcp_home[:main_pos]
    after_footer = mcp_home[footer_end_pos:]
    body_close_pos = after_footer.rfind('</body>')
    if body_close_pos == -1:
        body_close_pos = len(after_footer)

    final_html = (
        before_main +
        wrapped_public +
        '\n' +
        portal_html +
        '\n' +
        admissions_modal_html +
        '\n' +
        other_modals +
        '\n' +
        scripts_html +
        '\n' +
        after_footer[body_close_pos:]
    )

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f'Successfully built public/index.html ({len(final_html)} bytes)')

    # Also build standalone public/apply.html
    apply_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Admissions Questionnaire — Founder for Founder</title>
  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=Domine:wght@400..700&family=Plus+Jakarta+Sans:wght@300..800&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
  tailwind.config = {{"darkMode":"class","theme":{{"extend":{{"colors":{{"on-primary-fixed":"#002117","on-secondary-container":"#00714d","error":"#ba1a1a","on-background":"#131b2e","surface-container-low":"#f2f3ff","on-primary-fixed-variant":"#0b513d","secondary-fixed":"#6ffbbe","on-surface":"#131b2e","surface":"#faf8ff","tertiary":"#4a2400","on-secondary-fixed":"#002113","on-tertiary-fixed":"#2f1500","tertiary-fixed-dim":"#ffb77d","surface-tint":"#2b6954","surface-container-highest":"#dae2fd","error-container":"#ffdad6","surface-container":"#eaedff","background":"#faf8ff","secondary":"#006c49","secondary-container":"#6cf8bb","on-primary":"#ffffff","outline":"#707974","inverse-primary":"#95d3ba","on-error":"#ffffff","primary-fixed-dim":"#95d3ba","surface-container-lowest":"#ffffff","outline-variant":"#bfc9c3","inverse-on-surface":"#eef0ff","secondary-fixed-dim":"#4edea3","primary":"#003527","on-tertiary":"#ffffff","primary-fixed":"#b0f0d6","tertiary-container":"#6a3700","on-tertiary-container":"#ff9939","on-error-container":"#93000a","tertiary-fixed":"#ffdcc3","surface-variant":"#dae2fd","on-secondary-fixed-variant":"#005236","on-secondary":"#ffffff","surface-bright":"#faf8ff","primary-container":"#064e3b","on-surface-variant":"#404944","surface-container-high":"#e2e7ff","on-primary-container":"#80bea6","inverse-surface":"#283044","surface-dim":"#d2d9f4","on-tertiary-fixed-variant":"#6e3900"}}}}}}}};
  </script>
  <style>
    h1, h2, h3, .font-headline-hero, .font-headline-lg, .font-headline-md, .font-headline-sm {{
      font-family: 'Domine', serif !important;
    }}
    body, p, span, button, input, select, textarea, label {{
      font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
  </style>
</head>
<body class="bg-surface text-on-surface min-h-screen">
  <!-- Top Navigation -->
  <header class="w-full bg-surface-container-lowest border-b border-surface-container sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-3">
        <img src="/assets/logo.svg" alt="f4f Logo" class="h-8 w-8">
        <span class="font-headline-md text-primary font-bold tracking-tight text-lg">FOUNDER FOR FOUNDER</span>
      </a>
      <a href="/" class="text-sm font-semibold text-secondary hover:text-primary transition-colors flex items-center gap-1">
        ← Back to Homepage
      </a>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 py-8 sm:py-12">
    {q_content}
  </main>

  <footer class="w-full border-t border-surface-container py-8 text-center text-sm text-on-surface-variant">
    <p>© 2026 Founder for Founder Private Alliance. Strictly confidential and proprietary.</p>
  </footer>

  {scripts_html}
</body>
</html>
'''
    with open('public/apply.html', 'w', encoding='utf-8') as f:
        f.write(apply_html)

    print(f'Successfully built public/apply.html ({len(apply_html)} bytes)')

if __name__ == '__main__':
    build_home()
