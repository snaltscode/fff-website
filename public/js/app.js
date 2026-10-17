/* Founder for Founder Master Build Script v4.0 */

let state = {
  user: null,
  token: localStorage.getItem('f4f_token') || null,
  pendingEmail: '',
  pendingAppData: null,
  cooldownTimer: null,
  cooldownSeconds: 30,
  applicantType: 'Founder',
  invitationToken: null,
  googleClientId: null
};

// Feature tab data repository
const featureTabsData = {
  network: {
    title: 'Curated Founder Network',
    text: 'Connect with verified founders and decision-makers in a high-trust, clutter-free environment designed for meaningful business growth.',
    image: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80'
  },
  needs: {
    title: 'Needs & Wants Engine',
    text: 'A structured post engine allowing members to list explicit commercial requirements or high-value business offerings.',
    image: 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80'
  },
  crm: {
    title: 'Leads & Referrals CRM',
    text: 'Record peer introductions, manage client deal pipelines, and track administrator-verified business generated.',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80'
  },
  meetings: {
    title: 'Founder Experiences',
    text: 'Activities spanning Play, Explore, Dine, Build, and Celebrate—from closed-door roundtables to sunrise trails and dinners.',
    image: 'https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=800&q=80'
  },
  collaborations: {
    title: 'Business Collaborations',
    text: 'Work alongside peers on strategic joint ventures, supplier partnerships, co-marketing, and co-founder alliances.',
    image: 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=800&q=80'
  },
  challenges: {
    title: 'Monthly Challenges',
    text: 'Participate in community milestone challenges focused on business growth, peer referrals, and introductions.',
    image: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80'
  }
};

// Initialize App on DOM Loaded
document.addEventListener('DOMContentLoaded', () => {
  fetchAuthConfig();
  fetchPublicContent();
  initScrollListeners();
  initVisibilityObservers();
  checkURLHash();
  if (state.token) {
    checkAuthSession();
  }
});

function checkURLHash() {
  const hash = window.location.hash;
  if (hash.includes('activate')) {
    const params = new URLSearchParams(hash.split('?')[1] || '');
    const token = params.get('token');
    if (token) {
      state.invitationToken = token;
      openActivationModalWithToken(token);
    }
  }
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('admin') === '1' || urlParams.get('login') === 'admin') {
    setTimeout(openAdminLoginModal, 300);
  } else if (urlParams.get('login') === '1' || urlParams.get('login') === 'member') {
    setTimeout(openLoginModal, 300);
  }
}

// Throttled Scroll Event Listeners for 60/120fps Smooth Scrolling
let isScrollTicking = false;
function initScrollListeners() {
  window.addEventListener('scroll', () => {
    if (!isScrollTicking) {
      window.requestAnimationFrame(() => {
        updateScrollProgress();
        updateTimelineProgress();
        handleNavbarScroll();
        isScrollTicking = false;
      });
      isScrollTicking = true;
    }
  }, { passive: true });
}

// Pause offscreen infinite animations to conserve GPU/CPU & battery
function initVisibilityObservers() {
  if (!('IntersectionObserver' in window)) return;

  const sliderTrack = document.getElementById('meetingPhotosTrack');
  const sliderSection = document.getElementById('meetingPhotosSection');
  if (sliderTrack && sliderSection) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        sliderTrack.style.animationPlayState = entry.isIntersecting ? 'running' : 'paused';
      });
    }, { rootMargin: '200px 0px', threshold: 0 });
    observer.observe(sliderSection);
  }

  const marqueeContent = document.querySelector('.marquee-content');
  const marqueeWrapper = document.querySelector('.marquee-wrapper');
  if (marqueeContent && marqueeWrapper) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        marqueeContent.style.animationPlayState = entry.isIntersecting ? 'running' : 'paused';
      });
    }, { rootMargin: '200px 0px', threshold: 0 });
    observer.observe(marqueeWrapper);
  }
}

function updateScrollProgress() {
  const bar = document.getElementById('scrollProgressBar');
  if (!bar) return;
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  bar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
}

let isNavbarScrolled = false;
function handleNavbarScroll() {
  const nav = document.getElementById('mainNavbar');
  if (!nav) return;
  const shouldBeScrolled = window.scrollY > 40;
  if (shouldBeScrolled !== isNavbarScrolled) {
    isNavbarScrolled = shouldBeScrolled;
    if (isNavbarScrolled) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }
}

function updateTimelineProgress() {
  const bar = document.getElementById('timelineProgressBar');
  const container = document.getElementById('how-it-works');
  if (!bar || !container) return;

  const rect = container.getBoundingClientRect();
  const windowHeight = window.innerHeight;
  if (rect.top < windowHeight && rect.bottom > 0) {
    const total = rect.height;
    const current = windowHeight - rect.top;
    const pct = Math.min(100, Math.max(0, (current / total) * 100));
    bar.style.width = `${pct}%`;
  }
}

// Feature Tabs Switcher
function switchFeatureTab(key, btnEl) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btnEl.classList.add('active');

  const data = featureTabsData[key];
  if (!data) return;

  const img = document.getElementById('featureTabImage');
  const title = document.getElementById('featureTabTitle');
  const text = document.getElementById('featureTabText');

  if (img) {
    img.style.opacity = '0.3';
    setTimeout(() => {
      img.src = data.image;
      img.style.opacity = '1';
    }, 200);
  }
  if (title) title.innerText = data.title;
  if (text) text.innerText = data.text;
}

// Modal Controls
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add('active');
}
function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove('active');
}
function openShowInterestModal() { openModal('showInterestModal'); }
function openLoginModal() { openModal('loginModal'); }
function openPostNeedModal() { openModal('postNeedModal'); }

// Segmented Choice Input for Application Modal
function setApplicantType(type) {
  state.applicantType = type;
  document.getElementById('app_applicant_type').value = type;
  document.querySelectorAll('.segmented-option').forEach(opt => opt.classList.remove('active'));

  if (type === 'Founder') document.getElementById('segFounder').classList.add('active');
  else if (type === 'Business Owner') document.getElementById('segBizOwner').classList.add('active');
  else if (type === 'Professional') document.getElementById('segProfessional').classList.add('active');
}

// Fetch & Render Public Content with 60s Client-Side Cache
let cachedPublicData = null;
let cachedPublicTimestamp = 0;

async function fetchPublicContent(force = false) {
  try {
    let data;
    if (!force && cachedPublicData && (Date.now() - cachedPublicTimestamp < 60000)) {
      data = cachedPublicData;
    } else {
      const res = await fetch('/api/public/content');
      data = await res.json();
      cachedPublicData = data;
      cachedPublicTimestamp = Date.now();
    }

    // Dynamic Branding & Settings
    if (data.settings) {
      if (data.settings.club_tagline && document.getElementById('navSubtitle')) {
        document.getElementById('navSubtitle').innerText = data.settings.club_tagline;
      }
      if (data.settings.logo_url) {
        if (document.getElementById('navLogo')) document.getElementById('navLogo').src = data.settings.logo_url;
        if (document.getElementById('footerLogo')) document.getElementById('footerLogo').src = data.settings.logo_url;
      }
      const heroUrl = data.settings.hero_banner_url || '/assets/hero_banner.jpg';
      const heroEl = document.getElementById('home');
      if (heroEl) {
        heroEl.style.backgroundImage = `linear-gradient(to right, rgba(243, 251, 247, 0.94) 0%, rgba(243, 251, 247, 0.78) 42%, rgba(243, 251, 247, 0.35) 75%, rgba(243, 251, 247, 0.08) 100%), url('${heroUrl}')`;
        heroEl.style.backgroundSize = 'cover';
        heroEl.style.backgroundPosition = 'center right';
        heroEl.style.backgroundRepeat = 'no-repeat';
      }
      if (data.settings.terms_policy && document.getElementById('termsModalContent')) document.getElementById('termsModalContent').innerText = data.settings.terms_policy;
      if (data.settings.privacy_policy && document.getElementById('privacyModalContent')) document.getElementById('privacyModalContent').innerText = data.settings.privacy_policy;
      if (data.settings.refund_policy && document.getElementById('refundModalContent')) document.getElementById('refundModalContent').innerText = data.settings.refund_policy;
      if (data.settings.community_guidelines && document.getElementById('guidelinesModalContent')) document.getElementById('guidelinesModalContent').innerText = data.settings.community_guidelines;

      // Dynamic Hero Collage Capsules
      if (data.settings.hero_capsule_1_url && document.getElementById('heroCapsule1')) {
        document.getElementById('heroCapsule1').src = data.settings.hero_capsule_1_url;
      }
      if (data.settings.hero_capsule_2_url && document.getElementById('heroCapsule2')) {
        document.getElementById('heroCapsule2').src = data.settings.hero_capsule_2_url;
      }
      if (data.settings.hero_capsule_3_url && document.getElementById('heroCapsule3')) {
        document.getElementById('heroCapsule3').src = data.settings.hero_capsule_3_url;
      }

      // Dynamic Core Philosophy Images (4 Cards)
      if (data.settings.philosophy_img_1 && document.getElementById('philosophyImg1')) {
        document.getElementById('philosophyImg1').src = data.settings.philosophy_img_1;
      }
      if (data.settings.philosophy_img_2 && document.getElementById('philosophyImg2')) {
        document.getElementById('philosophyImg2').src = data.settings.philosophy_img_2;
      }
      if (data.settings.philosophy_img_3 && document.getElementById('philosophyImg3')) {
        document.getElementById('philosophyImg3').src = data.settings.philosophy_img_3;
      }
      if (data.settings.philosophy_img_4 && document.getElementById('philosophyImg4')) {
        document.getElementById('philosophyImg4').src = data.settings.philosophy_img_4;
      }

      // Dynamic Ways We Connect and Collaborate Images (5 Pillars)
      if (data.settings.format_img_play && document.getElementById('formatImgPlay')) {
        document.getElementById('formatImgPlay').src = data.settings.format_img_play;
      }
      if (data.settings.format_img_explore && document.getElementById('formatImgExplore')) {
        document.getElementById('formatImgExplore').src = data.settings.format_img_explore;
      }
      if (data.settings.format_img_dine && document.getElementById('formatImgDine')) {
        document.getElementById('formatImgDine').src = data.settings.format_img_dine;
      }
      if (data.settings.format_img_build && document.getElementById('formatImgBuild')) {
        document.getElementById('formatImgBuild').src = data.settings.format_img_build;
      }
      if (data.settings.format_img_celebrate && document.getElementById('formatImgCelebrate')) {
        document.getElementById('formatImgCelebrate').src = data.settings.format_img_celebrate;
      }

      // Dynamic Platform Feature Showcase Images
      if (data.settings.feature_img_network) featureTabsData.network.image = data.settings.feature_img_network;
      if (data.settings.feature_img_needs) featureTabsData.needs.image = data.settings.feature_img_needs;
      if (data.settings.feature_img_crm) featureTabsData.crm.image = data.settings.feature_img_crm;
      if (data.settings.feature_img_meetings) featureTabsData.meetings.image = data.settings.feature_img_meetings;
      if (data.settings.feature_img_collaborations) featureTabsData.collaborations.image = data.settings.feature_img_collaborations;
      if (data.settings.feature_img_challenges) featureTabsData.challenges.image = data.settings.feature_img_challenges;

      const activeTabImg = document.getElementById('featureTabImage');
      if (activeTabImg && data.settings.feature_img_network) {
        const activeTabBtn = document.querySelector('.tabs-list .tab-btn.active');
        if (!activeTabBtn || activeTabBtn.textContent.includes('Curated Founder Network')) {
          activeTabImg.src = data.settings.feature_img_network;
        }
      }
    }

    // Hero Copy
    if (data.hero) {
      if (document.getElementById('heroTitle')) {
        let h = data.hero.heading;
        if (h.includes('Real Connections')) h = h.replace('Real Connections', '<span class="text-emerald">Real Connections</span>');
        document.getElementById('heroTitle').innerHTML = h;
      }
      if (document.getElementById('heroSubtitle')) document.getElementById('heroSubtitle').innerText = data.hero.subheading;
    }

    // Live Database Counters
    if (data.counters) {
      const activeMembersTotal = 1528 + (data.counters.active_members || 0);
      if (document.getElementById('counterMembers')) {
        document.getElementById('counterMembers').innerText = `${activeMembersTotal}+`;
      }
      const eventsTotal = Math.max(27, data.counters.published_events || 27);
      if (document.getElementById('counterEvents')) {
        document.getElementById('counterEvents').innerText = `${eventsTotal}`;
      }
    }

    // Upcoming Experiences Showcase
    const eventsGrid = document.getElementById('upcomingEventsGrid');
    if (eventsGrid && data.upcoming_events) {
      eventsGrid.innerHTML = '';
      data.upcoming_events.forEach(evt => {
        const card = document.createElement('div');
        card.className = 'card';
          const price = Number(evt.price_amount || 0);
          const priceBadge = price > 0
            ? `<span class="badge" style="background: rgba(212,175,55,0.15); color: var(--gold-600); border: 1px solid rgba(212,175,55,0.3); font-weight: 800;">₹${price.toLocaleString('en-IN')} ENTRY FEE</span>`
            : `<span class="badge badge-active" style="font-size: 0.72rem;">FREE FOR MEMBERS</span>`;

            const mapUrl = evt.google_maps_url || (evt.venue ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((evt.venue || '') + ' ' + (evt.city || ''))}` : null);
            const mapLink = mapUrl ? `<a href="${mapUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--emerald-700); font-size: 0.76rem; font-weight: 700; text-decoration: underline; margin-left: 6px; display: inline-flex; align-items: center; gap: 3px;" title="View Venue on Google Maps"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> Google Maps</a>` : '';

            card.innerHTML = `
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                  <span class="badge badge-verified">${evt.category || 'FOUNDER EXPERIENCE'}</span>
                  ${priceBadge}
                </div>
                <span style="font-size: 0.78rem; font-weight: 800; color: var(--gold-500); text-transform: uppercase;">${evt.signature_format || 'Signature Event'}</span>
              </div>
              <h3 class="card-title" style="font-size: 1.3rem; margin-bottom: 8px;">${evt.title}</h3>
              <p class="card-text" style="font-size: 0.88rem; color: var(--emerald-900); font-weight: 700; margin-bottom: 4px;">
                <span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span> 
                ${evt.venue} (${evt.city})${mapLink}
              </p>
              <p class="card-text" style="font-size: 0.85rem; color: var(--grey-500); margin-bottom: 12px;"><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></span> ${evt.event_date} | ${evt.time_str}</p>
              <p class="card-text" style="font-size: 0.9rem; margin-bottom: 16px;">${evt.description}</p>
              <button class="btn btn-emerald" style="width: 100%; font-size: 0.82rem; padding: 0.6rem 1rem; border-radius: 6px !important;" onclick="openShowInterestModal()">RSVP / SHOW INTEREST <span class="btn-circle-icon">→</span></button>
            `;
        eventsGrid.appendChild(card);
      });
    }

    // FAQ Accordion
    const faqContainer = document.getElementById('faqContainer');
    if (faqContainer && data.faqs) {
      faqContainer.innerHTML = '';
      data.faqs.forEach((faq, idx) => {
        const div = document.createElement('div');
        div.style.cssText = 'background: var(--mint-50); border: 1px solid var(--mint-200); border-radius: var(--radius-md); padding: 1.25rem; transition: all 0.2s ease; cursor: pointer;';
        div.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center; font-weight: 700; font-size: 1.05rem; color: var(--ink-primary);" onclick="toggleFAQ(${idx})">
            <span>${faq.question}</span>
            <span id="faqIcon-${idx}" style="color: var(--emerald-700); font-size: 1.2rem; font-weight: 800;">+</span>
          </div>
          <div id="faqBody-${idx}" style="display: none; margin-top: 10px; font-size: 0.92rem; color: var(--grey-500); line-height: 1.6;">
            ${faq.answer}
          </div>
        `;
        faqContainer.appendChild(div);
      });
    }

    // Curated Meeting Photos Slider (16:9 Continuous Steady Slide from Right to Left)
    const meetingPhotosTrack = document.getElementById('meetingPhotosTrack');
    if (meetingPhotosTrack && (data.meeting_photos || data.gallery)) {
      renderMeetingPhotosSlider(data.meeting_photos || data.gallery);
    }

    // Testimonials
    const testimonialsContainer = document.getElementById('testimonialsContainer');
    if (testimonialsContainer && data.testimonials) {
      testimonialsContainer.innerHTML = '';
      data.testimonials.forEach(t => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div style="font-size: 1.6rem; color: var(--emerald-700); margin-bottom: 8px;">“</div>
          <p class="card-text" style="font-size: 0.95rem; margin-bottom: 16px;">${t.quote}</p>
          <div style="border-top: 1px solid var(--border-hairline); padding-top: 12px; display: flex; align-items: center; justify-content: space-between;">
            <div>
              <h4 style="font-size: 0.95rem; color: var(--ink-primary); margin: 0;">${t.author_name}</h4>
              <span style="font-size: 0.8rem; color: var(--emerald-700); font-weight: 700;">${t.author_title} • ${t.business_name}</span>
            </div>
            <span class="badge badge-verified">VERIFIED</span>
          </div>
        `;
        testimonialsContainer.appendChild(card);
      });
    }

  } catch (err) {
    console.error("Error loading public content:", err);
  }
}

function toggleFAQ(idx) {
  const body = document.getElementById(`faqBody-${idx}`);
  const icon = document.getElementById(`faqIcon-${idx}`);
  if (!body) return;
  if (body.style.display === 'none') {
    body.style.display = 'block';
    if (icon) icon.innerText = '−';
  } else {
    body.style.display = 'none';
    if (icon) icon.innerText = '+';
  }
}

// Show Interest Form Direct Submit (With Comprehensive Business & Collaboration Data)
async function handleShowInterestSubmit(event) {
  event.preventDefault();
  const email = document.getElementById('app_email').value.trim().toLowerCase();
  
  // Collect selected collaboration preferences
  const collabChecked = Array.from(document.querySelectorAll('input[name="collab_pref"]:checked')).map(el => el.value);

  const payload = {
    full_name: document.getElementById('app_full_name').value.trim(),
    email: email,
    phone: document.getElementById('app_phone').value.trim(),
    whatsapp: document.getElementById('app_whatsapp') ? document.getElementById('app_whatsapp').value.trim() : document.getElementById('app_phone').value.trim(),
    applicant_type: state.applicantType || 'Founder',
    designation: document.getElementById('app_designation').value.trim(),
    city: (document.getElementById('app_city') ? document.getElementById('app_city').value.trim() : 'Pan India'),
    
    // Business questions
    business_name: document.getElementById('app_business_name').value.trim(),
    business_model_category: document.getElementById('app_business_model_category') ? document.getElementById('app_business_model_category').value : 'Product Based',
    firm_type: document.getElementById('app_firm_type') ? document.getElementById('app_firm_type').value : 'Private Limited (Pvt Ltd)',
    years_in_business: document.getElementById('app_years_in_business') ? document.getElementById('app_years_in_business').value : '3 to 5 Years',
    team_size: document.getElementById('app_team_size') ? document.getElementById('app_team_size').value : '2 - 10 Members',
    business_category: document.getElementById('app_business_category').value,
    business_stage: document.getElementById('app_business_stage').value,
    business_description: document.getElementById('app_business_description').value.trim(),
    
    // Social / Digital links (optional)
    website: document.getElementById('app_website') ? document.getElementById('app_website').value.trim() : '',
    linkedin: document.getElementById('app_linkedin') ? document.getElementById('app_linkedin').value.trim() : '',
    instagram: document.getElementById('app_instagram') ? document.getElementById('app_instagram').value.trim() : '',
    
    // Community Value Exchange
    what_offer: document.getElementById('app_what_offer') ? document.getElementById('app_what_offer').value.trim() : '',
    what_need: document.getElementById('app_what_need') ? document.getElementById('app_what_need').value.trim() : '',
    
    // Collaboration preferences
    collaboration_preferences: collabChecked,
    
    // Goals & Consent
    why_join: document.getElementById('app_why_join').value.trim(),
    consent_given: document.getElementById('app_consent').checked
  };

  try {
    const res = await fetch('/api/public/show-interest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    closeModal('showInterestModal');
    document.getElementById('showInterestForm').reset();
    alert("Thank you for showing interest! Your application with complete business details has been successfully submitted to the Founder for Founder admissions committee. We will review your profile and reach out shortly.");
  } catch (err) {
    alert("Network error submitting application. Please try again.");
  }
}

// Open Invitation Checkout Modal
async function openActivationModalWithToken(token) {
  try {
    const res = await fetch(`/api/public/invitation/${token}`);
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    openModal('activationModal');
  } catch (err) {
    alert("Failed to load invitation details.");
  }
}

async function handleProceedActivationPayment() {
  try {
    const res = await fetch('/api/payments/activate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
      body: JSON.stringify({ invitation_token: state.invitationToken })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    closeModal('activationModal');
    alert(`Payment Confirmed! Transaction ID: ${data.transaction_id}. Your Founder Membership is now ACTIVE.`);
    checkAuthSession();
  } catch (err) {
    alert("Payment activation failed.");
  }
}

// Auth Configuration & Google OAuth Client Setup
async function fetchAuthConfig() {
  try {
    const res = await fetch('/api/auth/config');
    if (res.ok) {
      const data = await res.json();
      state.googleClientId = data.google_client_id;
      if (state.googleClientId && state.googleClientId.trim() !== '') {
        setupGoogleAuth(state.googleClientId.trim());
      }
    }
  } catch (err) {
    console.warn("Could not load auth configuration:", err);
  }
}

function setupGoogleAuth(clientId) {
  if (!clientId) return;
  if (!window.google || !window.google.accounts || !window.google.accounts.id) {
    setTimeout(() => setupGoogleAuth(clientId), 400);
    return;
  }
  try {
    window.google.accounts.id.initialize({
      client_id: clientId,
      callback: handleGoogleCredentialResponse,
      auto_select: false,
      cancel_on_tap_outside: true
    });
    const container = document.getElementById('googleSignInBtn');
    if (container) {
      window.google.accounts.id.renderButton(container, {
        theme: 'outline',
        size: 'large',
        type: 'standard',
        shape: 'rectangular',
        text: 'continue_with',
        logo_alignment: 'left',
        width: 320
      });
      const customBtn = document.getElementById('customGoogleAuthBtn');
      if (customBtn) customBtn.style.display = 'none';
    }
  } catch (err) {
    console.error("Error initializing Google Identity Services:", err);
  }
}

function initiateGoogleLogin() {
  if (state.googleClientId && state.googleClientId.trim() !== '') {
    if (window.google && window.google.accounts && window.google.accounts.id) {
      window.google.accounts.id.prompt();
      return;
    }
  }
  openGoogleDemoModal();
}

function openGoogleDemoModal() {
  const input = document.getElementById('modal_google_client_id');
  if (input && state.googleClientId) input.value = state.googleClientId;
  const badge = document.getElementById('googleClientIdBadge');
  if (badge) {
    if (state.googleClientId) {
      badge.className = 'badge badge-verified';
      badge.innerText = 'Connected';
    } else {
      badge.className = 'badge badge-active';
      badge.innerText = 'Not Configured';
    }
  }
  openModal('googleDemoModal');
}

async function handleGoogleCredentialResponse(response) {
  if (!response || !response.credential) {
    alert("Google authentication was cancelled or returned no credentials.");
    return;
  }
  try {
    const res = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: response.credential })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    state.token = data.token;
    state.user = data.user;
    localStorage.setItem('f4f_token', data.token);
    closeModal('loginModal');
    closeModal('googleDemoModal');
    renderAuthenticatedUI(data);

    if (data.user && (data.user.role === 'ADMIN' || data.user.role === 'SUPER_ADMIN')) {
      setTimeout(() => {
        const navAdminBtn = document.getElementById('navAdminBtn');
        switchPortalTab('admin', navAdminBtn);
      }, 120);
    }
  } catch (err) {
    alert("Google authentication request failed. Please check your network connection.");
  }
}

async function handleDemoGoogleLogin(event) {
  event.preventDefault();
  const name = document.getElementById('demo_google_name').value.trim();
  const email = document.getElementById('demo_google_email').value.trim();
  if (!email || !email.includes('@')) {
    alert("Please enter a valid Google email address.");
    return;
  }
  try {
    const res = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email,
        name: name,
        sub: 'demo_google_' + Date.now()
      })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    state.token = data.token;
    state.user = data.user;
    localStorage.setItem('f4f_token', data.token);
    closeModal('loginModal');
    closeModal('googleDemoModal');
    renderAuthenticatedUI(data);

    if (data.user && (data.user.role === 'ADMIN' || data.user.role === 'SUPER_ADMIN')) {
      setTimeout(() => {
        const navAdminBtn = document.getElementById('navAdminBtn');
        switchPortalTab('admin', navAdminBtn);
      }, 120);
    }
  } catch (err) {
    alert("Failed to complete Google sign-in.");
  }
}

async function saveGoogleClientIdFromModal() {
  const val = document.getElementById('modal_google_client_id').value.trim();
  if (!val) {
    alert("Please enter a valid Google Client ID.");
    return;
  }
  try {
    await fetch('/api/admin/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(state.token ? { 'Authorization': `Bearer ${state.token}` } : {})
      },
      body: JSON.stringify({ google_client_id: val })
    });
    state.googleClientId = val;
    alert("Google Client ID saved successfully! Initializing Google Sign-In button...");
    setupGoogleAuth(val);
    closeModal('googleDemoModal');
  } catch (err) {
    state.googleClientId = val;
    setupGoogleAuth(val);
    closeModal('googleDemoModal');
  }
}

// Admin Login Modal Switching & Quick-Fill Helpers
function openAdminLoginModal() {
  if (typeof closeMobileMenu === 'function') closeMobileMenu();
  openLoginModal();
  switchLoginModalTab('admin');
}

function switchLoginModalTab(tab) {
  const btnMember = document.getElementById('tabBtnMember');
  const btnAdmin = document.getElementById('tabBtnAdmin');
  const sectionMember = document.getElementById('memberLoginSection');
  const sectionAdmin = document.getElementById('adminLoginSection');
  const title = document.getElementById('loginModalTitle');
  const subtitle = document.getElementById('loginModalSubtitle');

  if (tab === 'admin') {
    if (btnMember) {
      btnMember.style.background = 'transparent';
      btnMember.style.color = '#5A6260';
    }
    if (btnAdmin) {
      btnAdmin.style.background = '#003527';
      btnAdmin.style.color = '#FFFFFF';
    }
    if (sectionMember) sectionMember.style.display = 'none';
    if (sectionAdmin) sectionAdmin.style.display = 'block';
    if (title) title.innerText = 'Administrator Console';
    if (subtitle) subtitle.innerText = 'Secure access for Founder for Founder leadership and operators.';
  } else {
    if (btnMember) {
      btnMember.style.background = '#003527';
      btnMember.style.color = '#FFFFFF';
    }
    if (btnAdmin) {
      btnAdmin.style.background = 'transparent';
      btnAdmin.style.color = '#5A6260';
    }
    if (sectionMember) sectionMember.style.display = 'block';
    if (sectionAdmin) sectionAdmin.style.display = 'none';
    if (title) title.innerText = 'Executive Member Access';
    if (subtitle) subtitle.innerText = 'Sign in with your verified Google account or credentials.';
  }
}

function quickFillAdminCredentials() {
  const emailInput = document.getElementById('admin_login_email');
  const pwdInput = document.getElementById('admin_login_password');
  if (emailInput) emailInput.value = 'admin@founderforfounder.in';
  if (pwdInput) pwdInput.value = 'Admin@123';
}

async function handleAdminLoginSubmit(event) {
  event.preventDefault();
  const emailInput = document.getElementById('admin_login_email');
  const pwdInput = document.getElementById('admin_login_password');
  const email = (emailInput ? emailInput.value : 'admin@founderforfounder.in').trim();
  const password = pwdInput ? pwdInput.value : 'Admin@123';

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    state.token = data.token;
    state.user = data.user;
    localStorage.setItem('f4f_token', data.token);

    closeModal('loginModal');
    renderAuthenticatedUI(data);

    // Auto-navigate to Admin Console Tab
    setTimeout(() => {
      const navAdminBtn = document.getElementById('navAdminBtn');
      switchPortalTab('admin', navAdminBtn);
    }, 120);
  } catch (err) {
    alert("Admin login failed. Please verify credentials.");
  }
}

// Member Login
async function handleLoginSubmit(event) {
  event.preventDefault();
  const email = document.getElementById('login_email').value.trim();
  const password = document.getElementById('login_password').value;

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();

    if (data.error) { alert(data.error); return; }

    state.token = data.token;
    state.user = data.user;
    localStorage.setItem('f4f_token', data.token);

    closeModal('loginModal');
    renderAuthenticatedUI(data);

    if (data.user && (data.user.role === 'ADMIN' || data.user.role === 'SUPER_ADMIN')) {
      setTimeout(() => {
        const navAdminBtn = document.getElementById('navAdminBtn');
        switchPortalTab('admin', navAdminBtn);
      }, 120);
    }
  } catch (err) {
    alert("Login failed.");
  }
}

// Auth Session Check
async function checkAuthSession() {
  try {
    const res = await fetch('/api/auth/me', {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) { handleLogout(); return; }
    const data = await res.json();
    state.user = data.user;
    renderAuthenticatedUI(data);
  } catch (err) {
    handleLogout();
  }
}

function handleLogout() {
  state.token = null;
  state.user = null;
  localStorage.removeItem('f4f_token');
  document.getElementById('publicPage').style.display = 'block';
  document.getElementById('portalPage').classList.remove('active');
  document.getElementById('publicNav').style.display = 'flex';
  document.getElementById('authNavControls').style.display = 'none';
}

function renderAuthenticatedUI(data) {
  document.getElementById('publicPage').style.display = 'none';
  document.getElementById('portalPage').classList.add('active');
  document.getElementById('publicNav').style.display = 'none';
  document.getElementById('authNavControls').style.display = 'flex';

  const name = data.profile ? data.profile.full_name : data.user.email;
  if (document.getElementById('navUserName')) document.getElementById('navUserName').innerText = `Welcome, ${name}`;
  if (document.getElementById('dashboardWelcome')) document.getElementById('dashboardWelcome').innerText = `Welcome, ${name}`;

  const isAdmin = data.user && (data.user.role === 'ADMIN' || data.user.role === 'SUPER_ADMIN');
  if (document.getElementById('adminTabLink')) document.getElementById('adminTabLink').style.display = isAdmin ? 'flex' : 'none';
  if (document.getElementById('navAdminBtn')) document.getElementById('navAdminBtn').style.display = isAdmin ? 'inline-flex' : 'none';

  loadDashboardTab();
  loadDirectoryTab();
  loadNeedsTab();
  loadCRMTab();
  loadEventsTab();
  loadChallengeTab();

  if (isAdmin) {
    loadAdminTab();
  }
}

// Mobile Navigation Drawer Toggle Handlers
function toggleMobileNav() {
  const drawer = document.getElementById('navDrawer');
  const toggle = document.getElementById('mobileNavToggle');
  const backdrop = document.getElementById('navDrawerBackdrop');
  if (!drawer || !toggle) return;
  const isOpen = drawer.classList.toggle('active');
  toggle.classList.toggle('active', isOpen);
  toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  if (backdrop) backdrop.classList.toggle('active', isOpen);
  if (isOpen) {
    document.body.classList.add('mobile-nav-open');
  } else {
    document.body.classList.remove('mobile-nav-open');
  }
}

function closeMobileNav() {
  const drawer = document.getElementById('navDrawer');
  const toggle = document.getElementById('mobileNavToggle');
  const backdrop = document.getElementById('navDrawerBackdrop');
  if (drawer && drawer.classList.contains('active')) {
    drawer.classList.remove('active');
    if (toggle) {
      toggle.classList.remove('active');
      toggle.setAttribute('aria-expanded', 'false');
    }
    if (backdrop) backdrop.classList.remove('active');
    document.body.classList.remove('mobile-nav-open');
  }
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeMobileNav();
});

function switchPortalTab(tabName, el) {
  closeMobileNav();
  document.getElementById('publicPage').style.display = 'none';
  document.getElementById('portalPage').classList.add('active');

  document.querySelectorAll('.portal-tab').forEach(t => t.style.display = 'none');
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));

  const tab = document.getElementById(`tab-${tabName}`);
  if (tab) {
    tab.style.display = 'block';
  } else {
    console.error("Portal tab not found:", tabName);
  }

  let activeEl = el;
  if (!activeEl) {
    activeEl = Array.from(document.querySelectorAll('.sidebar-item')).find(item => item.getAttribute('onclick')?.includes(`'${tabName}'`));
  }
  if (activeEl) {
    activeEl.classList.add('active');
    if (window.innerWidth < 992) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (tabName === 'admin') loadAdminTab();
  else if (tabName === 'dashboard') loadDashboardTab();
  else if (tabName === 'directory') loadDirectoryTab();
  else if (tabName === 'needs') loadNeedsTab();
  else if (tabName === 'crm') loadCRMTab();
  else if (tabName === 'attendance') loadAttendanceTab();
  else if (tabName === 'meetings') loadMeetingsTab();
  else if (tabName === 'chat') loadChatMessages();
  else if (tabName === 'events') loadEventsTab();
  else if (tabName === 'challenge') loadChallengeTab();
}

// Dashboard Tab Loader
async function loadDashboardTab() {
  try {
    const res = await fetch('/api/crm/metrics', { headers: { 'Authorization': `Bearer ${state.token}` } });
    const metrics = await res.json();

    if (document.getElementById('dashBizGenerated')) {
      document.getElementById('dashBizGenerated').innerText = `${metrics.referrals_received || 0} Deals`;
    }
    if (document.getElementById('dashLeadsWon')) {
      document.getElementById('dashLeadsWon').innerText = metrics.leads_won || 0;
    }

    // Attendance summary for dashboard
    fetch('/api/attendance/summary', { headers: { 'Authorization': `Bearer ${state.token}` } })
      .then(r => r.json())
      .then(d => {
        if (d && !d.error && document.getElementById('dashAttendanceRate')) {
          document.getElementById('dashAttendanceRate').innerHTML = `${d.attendance_rate}% Event Presence <span class="badge-pulse-green" style="font-size: 0.78rem; background: #A7F3D0; color: #064E3B; padding: 2px 8px; border-radius: 12px; font-weight: 800;">Streak: ${d.attendance_streak} Gatherings</span>`;
        }
      })
      .catch(() => {});

    // Meetings summary for dashboard
    fetch('/api/founder-meetings', { headers: { 'Authorization': `Bearer ${state.token}` } })
      .then(r => r.json())
      .then(d => {
        if (d && d.stats && document.getElementById('dashMeetingsStat')) {
          document.getElementById('dashMeetingsStat').innerText = `${d.stats.this_month} 1-to-1 Founder Meetings logged in ${d.stats.current_month_name}`;
        }
      })
      .catch(() => {});
  } catch (err) {
    console.error("Dashboard metrics error:", err);
  }
}

// Directory Loader
async function loadDirectoryTab() {
  const res = await fetch('/api/members', { headers: { 'Authorization': `Bearer ${state.token}` } });
  const data = await res.json();
  renderMembers(data.members || []);
}

function filterDirectory() {
  const query = document.getElementById('dirSearchInput').value.toLowerCase();
  const stage = document.getElementById('dirStageFilter').value;
  fetch(`/api/members?q=${encodeURIComponent(query)}&stage=${encodeURIComponent(stage)}`, { headers: { 'Authorization': `Bearer ${state.token}` } })
    .then(r => r.json())
    .then(d => renderMembers(d.members || []));
}

function renderMembers(members) {
  const container = document.getElementById('directoryContainer');
  if (!container) return;
  container.innerHTML = '';
  members.forEach(m => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
        <img src="${m.profile_photo || '/assets/logo.svg'}" alt="${m.full_name || 'Member'}" loading="lazy" decoding="async" width="52" height="52" style="width: 52px; height: 52px; border-radius: 12px; border: 1px solid var(--mint-200); object-fit: cover;">
        <div>
          <h3 class="card-title" style="font-size: 1.15rem; margin: 0;">${m.full_name}</h3>
          <span style="font-size: 0.85rem; color: var(--emerald-700); font-weight: 700;">${m.designation} at ${m.business_name}</span>
        </div>
      </div>
      <p class="card-text" style="font-size: 0.85rem; margin-bottom: 8px;"><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span> ${m.city} | Stage: ${m.business_stage || 'Established'}</p>
      <p class="card-text" style="font-size: 0.9rem;">${m.business_description}</p>
      ${m.what_i_can_offer ? `<p style="font-size: 0.82rem; color: var(--emerald-900); font-weight: 700; margin-top: 8px;">Can Help With: ${m.what_i_can_offer}</p>` : ''}
    `;
    container.appendChild(card);
  });
}

// Needs Loader
async function loadNeedsTab() {
  const res = await fetch('/api/needs', { headers: { 'Authorization': `Bearer ${state.token}` } });
  const data = await res.json();
  const container = document.getElementById('needsContainer');
  if (!container) return;
  container.innerHTML = '';

  (data.needs || []).forEach(n => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span class="badge ${n.type === 'NEED' ? 'badge-pending' : 'badge-active'}">${n.type}</span>
        <span style="font-size: 0.78rem; color: var(--grey-500); font-weight: 700;">Urgency: ${n.urgency || 'Medium'}</span>
      </div>
      <h3 class="card-title" style="font-size: 1.2rem; margin-bottom: 8px;">${n.title}</h3>
      <p class="card-text" style="font-size: 0.9rem;">${n.description}</p>
      <p style="font-size: 0.85rem; color: var(--emerald-700); font-weight: 700; margin-top: 12px;">By: ${n.creator_name} (${n.business_name})</p>
    `;
    container.appendChild(card);
  });
}

async function handlePostNeedSubmit(e) {
  e.preventDefault();
  const body = {
    type: document.getElementById('need_type').value,
    title: document.getElementById('need_title').value,
    category: document.getElementById('need_category').value,
    budget: document.getElementById('need_budget').value,
    description: document.getElementById('need_description').value
  };

  const res = await fetch('/api/needs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
    body: JSON.stringify(body)
  });
  if (res.ok) {
    closeModal('postNeedModal');
    loadNeedsTab();
  }
}

// CRM Loader
async function loadCRMTab() {
  const res = await fetch('/api/crm/metrics', { headers: { 'Authorization': `Bearer ${state.token}` } });
  const data = await res.json();
  const list = document.getElementById('leadsList');
  if (!list) return;
  list.innerHTML = '';

  (data.leads || []).forEach(l => {
    const div = document.createElement('div');
    div.style.cssText = 'padding: 12px; background: var(--mint-50); border: 1px solid var(--mint-200); border-radius: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;';
    div.innerHTML = `
      <div>
        <div style="font-weight: 700; color: var(--ink-primary);">${l.lead_name} (${l.company || 'Direct'})</div>
        <div style="font-size: 0.85rem; color: var(--grey-500);">${l.requirement}</div>
      </div>
      <div>
        <span class="badge badge-active">${l.status}</span>
        <span style="font-weight: 800; margin-left: 10px; color: var(--emerald-700);">₹${(l.estimated_value || 0).toLocaleString('en-IN')}</span>
      </div>
    `;
    list.appendChild(div);
  });
}

// Events Loader
async function loadEventsTab() {
  const res = await fetch('/api/events', { headers: { 'Authorization': `Bearer ${state.token}` } });
  const data = await res.json();
  const container = document.getElementById('eventsContainer');
  if (!container) return;
  container.innerHTML = '';

  state.eventsList = data.events || [];

  state.eventsList.forEach(evt => {
    const card = document.createElement('div');
    card.className = 'card';

    const price = Number(evt.price_amount || 0);
    const hasPaid = evt.user_payment_status === 'PAID';
    const isAttending = evt.user_rsvp === 'ATTENDING';

    // Pricing & inclusions badge
    let priceBadge = '';
    if (price > 0) {
      priceBadge = `<span class="badge" style="background: rgba(212,175,55,0.15); color: var(--gold-600); border: 1px solid rgba(212,175,55,0.3); font-weight: 800;">₹${price.toLocaleString('en-IN')} REGISTRATION FEE</span>`;
    } else {
      priceBadge = `<span class="badge badge-verified">FREE FOR MEMBERS</span>`;
    }

    // Action button
    let actionBtnHtml = '';
    if (isAttending) {
      if (hasPaid) {
        actionBtnHtml = `<button class="btn btn-outline-emerald" style="padding: 6px 14px; font-size: 0.8rem; cursor: default; border-radius: 6px !important;"><svg class="icon-inline" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> SEAT CONFIRMED (PAID)</button>`;
      } else {
        actionBtnHtml = `<button class="btn btn-outline-emerald" style="padding: 6px 14px; font-size: 0.8rem; cursor: default; border-radius: 6px !important;"><svg class="icon-inline" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> RSVP CONFIRMED</button>`;
      }
    } else {
      if (price > 0) {
        actionBtnHtml = `<button class="btn btn-emerald" style="padding: 6px 16px; font-size: 0.8rem; border-radius: 6px !important;" onclick="openEventPaymentModal('${evt.id}')">PAY & REGISTER (₹${price.toLocaleString('en-IN')})</button>`;
      } else {
        actionBtnHtml = `<button class="btn btn-emerald" style="padding: 6px 16px; font-size: 0.8rem; border-radius: 6px !important;" onclick="handleRSVP('${evt.id}')">RSVP FOR EVENT (FREE)</button>`;
      }
    }

    const inclusionsHtml = evt.what_is_included ? `
      <div style="background: var(--mint-50); border: 1px solid var(--mint-100); border-radius: 6px; padding: 6px 10px; margin-top: 8px; font-size: 0.78rem; color: var(--emerald-900); display: flex; align-items: center; gap: 6px;">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        <span><strong>Included:</strong> ${evt.what_is_included}</span>
      </div>
    ` : '';

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
          <span class="badge badge-verified">${evt.category}</span>
          ${priceBadge}
        </div>
        <span style="font-size: 0.8rem; font-weight: 800; color: var(--gold-500);">${evt.signature_format}</span>
      </div>
      <h3 class="card-title">${evt.title}</h3>
      <p class="card-text">
        <span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span> 
        <strong>${evt.venue}</strong> (${evt.city})
        ${(() => {
          const mapUrl = evt.google_maps_url || (evt.venue ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((evt.venue || '') + ' ' + (evt.city || ''))}` : null);
          return mapUrl ? `<a href="${mapUrl}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 3px; margin-left: 6px; font-size: 0.78rem; color: var(--emerald-700); font-weight: 700; text-decoration: underline;" title="View Venue on Google Maps"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> Google Maps</a>` : '';
        })()}
        | <span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></span> ${evt.event_date} (${evt.time_str})
      </p>
      <p class="card-text">${evt.description}</p>
      ${inclusionsHtml}
      <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <span style="font-size: 0.85rem; color: var(--emerald-700); font-weight: 700;">Host: ${evt.host_name}</span>
        ${actionBtnHtml}
      </div>
    `;
    container.appendChild(card);
  });
}

async function handleRSVP(eventId) {
  const res = await fetch('/api/events/rsvp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
    body: JSON.stringify({ event_id: eventId, status: 'ATTENDING' })
  });
  const data = await res.json();
  if (data.requires_payment) {
    openEventPaymentModal(eventId);
    return;
  }
  if (res.ok) {
    alert("RSVP Confirmed! Your seat has been reserved.");
    loadEventsTab();
  } else {
    alert(data.error || "Failed to confirm RSVP.");
  }
}

async function openEventPaymentModal(eventId) {
  let evt = (state.eventsList || []).find(e => String(e.id) === String(eventId));
  if (!evt) {
    try {
      const res = await fetch('/api/events', { headers: { 'Authorization': `Bearer ${state.token}` } });
      const data = await res.json();
      state.eventsList = data.events || [];
      evt = state.eventsList.find(e => String(e.id) === String(eventId));
    } catch (err) {
      console.error(err);
    }
  }

  if (!evt) {
    alert("Event details not found. Please refresh and try again.");
    return;
  }

  const subtotal = Number(evt.price_amount || 0);
  const gst = Math.round(subtotal * 0.18 * 100) / 100;
  const total = Math.round((subtotal + gst) * 100) / 100;

  document.getElementById('evtPayEventId').value = evt.id;
  document.getElementById('evtPayTitle').textContent = evt.title;
  document.getElementById('evtPayFormatBadge').textContent = evt.signature_format || 'Signature Gathering';
  document.getElementById('evtPayDateTimeText').textContent = `${evt.event_date} (${evt.time_str || ''})`;
  document.getElementById('evtPayVenueText').textContent = `${evt.venue} (${evt.city || 'Pan India'})`;
  const mapUrl = evt.google_maps_url || (evt.venue ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((evt.venue || '') + ' ' + (evt.city || ''))}` : null);
  const mapLinkEl = document.getElementById('evtPayMapLink');
  if (mapLinkEl) {
    if (mapUrl) {
      mapLinkEl.href = mapUrl;
      mapLinkEl.style.display = 'inline-block';
    } else {
      mapLinkEl.style.display = 'none';
    }
  }
  document.getElementById('evtPayInclusions').textContent = evt.what_is_included || 'Full session access, curated networking, refreshments';

  document.getElementById('evtPaySubtotal').textContent = `₹${subtotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  document.getElementById('evtPayGst').textContent = `₹${gst.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  document.getElementById('evtPayTotal').textContent = `₹${total.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  
  const submitBtn = document.getElementById('evtPaySubmitBtn');
  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.innerHTML = `COMPLETE PAYMENT (₹${total.toLocaleString('en-IN', { minimumFractionDigits: 2 })}) &rarr;`;
  }

  document.getElementById('eventPaymentCheckoutView').style.display = 'block';
  document.getElementById('eventPaymentSuccessView').style.display = 'none';

  openModal('eventPaymentModal');
}

async function handleEventPaymentSubmit() {
  const eventId = document.getElementById('evtPayEventId').value;
  if (!eventId) {
    alert("Missing event reference.");
    return;
  }

  const selectedMethodRadio = document.querySelector('input[name="evt_payment_method"]:checked');
  const paymentMethod = selectedMethodRadio ? selectedMethodRadio.value : 'UPI';
  const submitBtn = document.getElementById('evtPaySubmitBtn');

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `Verifying payment with gateway...`;
  }

  try {
    const res = await fetch('/api/events/pay', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.token}`
      },
      body: JSON.stringify({
        event_id: eventId,
        payment_gateway: 'RAZORPAY',
        payment_method: paymentMethod
      })
    });

    const data = await res.json();

    if (res.ok && data.success) {
      document.getElementById('eventPaymentCheckoutView').style.display = 'none';
      document.getElementById('eventPaymentSuccessView').style.display = 'block';

      document.getElementById('evtPaySuccessTitle').textContent = `Seat Confirmed for "${data.event_title || 'Gathering'}"`;
      document.getElementById('evtPaySuccessInvoice').textContent = data.invoice_number || 'INV-EVT-CONFIRMED';
      document.getElementById('evtPaySuccessTxId').textContent = data.transaction_id || 'PAY-VERIFIED';
      document.getElementById('evtPaySuccessAmount').textContent = `₹${Number(data.amount_paid || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;

      loadEventsTab();
    } else {
      alert(data.error || "Payment verification failed. Please try again or select another payment method.");
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `TRY PAYMENT AGAIN &rarr;`;
      }
    }
  } catch (err) {
    console.error(err);
    alert("Network error connecting to payment gateway.");
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `TRY PAYMENT AGAIN &rarr;`;
    }
  }
}

// Challenge Loader
async function loadChallengeTab() {
  const res = await fetch('/api/challenges/current', { headers: { 'Authorization': `Bearer ${state.token}` } });
  const data = await res.json();

  if (data.challenge && document.getElementById('challengeDetailsCard')) {
    document.getElementById('challengeDetailsCard').innerHTML = `
      <span class="badge badge-verified">ACTIVE CHALLENGE</span>
      <h3 class="card-title" style="font-size: 1.6rem; margin: 8px 0;">${data.challenge.title}</h3>
      <p class="card-text">${data.challenge.description}</p>
      <p style="color: var(--emerald-700); font-weight: 700; margin-top: 12px;">Target: ₹${(data.challenge.target_value || 0).toLocaleString('en-IN')} | Reward: ${data.challenge.reward}</p>
    `;
  }
}

// Admin CMS Loader
async function loadAdminTab() {
  try {
    const res = await fetch('/api/admin/overview', { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (!res.ok) {
      console.error("Forbidden or error fetching admin overview");
      return;
    }
    const data = await res.json();

    if (document.getElementById('adminMetricsGrid') && data.metrics) {
      document.getElementById('adminMetricsGrid').innerHTML = `
        <div class="card"><div style="color:var(--grey-500); font-weight:700; font-size:0.8rem; text-transform:uppercase;">Total Members</div><div style="font-size:1.8rem; font-weight:800; color:var(--ink-primary); margin-top:4px;">${data.metrics.total_members}</div></div>
        <div class="card"><div style="color:var(--grey-500); font-weight:700; font-size:0.8rem; text-transform:uppercase;">Active MRR</div><div style="font-size:1.8rem; font-weight:800; color:var(--emerald-700); margin-top:4px;">₹${(data.metrics.mrr || 0).toLocaleString('en-IN')}</div></div>
        <div class="card"><div style="color:var(--grey-500); font-weight:700; font-size:0.8rem; text-transform:uppercase;">New Applications</div><div style="font-size:1.8rem; font-weight:800; color:var(--emerald-700); margin-top:4px;">${data.metrics.new_applications}</div></div>
      `;
    }

    // Applications Table
    if (document.getElementById('applicationsTable')) {
      state.adminApplications = data.recent_applications || [];
      let html = `<table style="width:100%; text-align:left; border-collapse:collapse; color:var(--ink-primary);">
        <thead>
          <tr style="border-bottom:1px solid var(--mint-200); font-size:0.82rem; text-transform:uppercase; color:var(--grey-500);">
            <th style="padding:10px;">Applicant</th>
            <th>Type / Role</th>
            <th>Business & Model</th>
            <th>Contact</th>
            <th>Status</th>
            <th>Update Status</th>
            <th>Inspection & Actions</th>
          </tr>
        </thead>
        <tbody>`;

      (data.recent_applications || []).forEach(app => {
        const inviteLink = app.invitation_token ? `${window.location.origin}/#activate?token=${app.invitation_token}` : '';
        const badgeClass = app.status === 'APPROVED' || app.status === 'INVITED' || app.status === 'CONVERTED' ? 'badge-verified' : (app.status === 'DECLINED' ? 'badge-pending' : 'badge-active');

        html += `<tr style="border-bottom:1px solid var(--border-hairline); font-size:0.88rem;">
          <td style="padding:10px; font-weight:700;">${app.full_name}</td>
          <td><span class="badge badge-active">${app.applicant_type || 'Founder'}</span><br><span style="font-size:0.75rem; color:var(--grey-500);">${app.designation || ''}</span></td>
          <td>${app.business_name || 'N/A'}<br><span style="font-size:0.75rem; color:var(--emerald-700); font-weight:600;">${app.business_model_category || 'Product Based'}</span> • <span style="font-size:0.75rem; color:var(--grey-500);">${app.city || 'Pan India'}</span></td>
          <td>${app.email}<br><span style="font-size:0.75rem; color:var(--grey-500);">${app.phone}</span></td>
          <td><span class="badge ${badgeClass}">${app.status}</span></td>
          <td>
            <select class="form-select" style="padding:4px 8px; font-size:0.78rem; min-width:130px;" onchange="updateAppStatus('${app.id}', this.value)">
              <option value="SUBMITTED" ${app.status === 'SUBMITTED' ? 'selected' : ''}>SUBMITTED</option>
              <option value="UNDER_REVIEW" ${app.status === 'UNDER_REVIEW' ? 'selected' : ''}>UNDER_REVIEW</option>
              <option value="APPROVED" ${app.status === 'APPROVED' ? 'selected' : ''}>APPROVED</option>
              <option value="INVITED" ${app.status === 'INVITED' ? 'selected' : ''}>INVITED</option>
              <option value="WAITLISTED" ${app.status === 'WAITLISTED' ? 'selected' : ''}>WAITLISTED</option>
              <option value="DECLINED" ${app.status === 'DECLINED' ? 'selected' : ''}>DECLINED</option>
            </select>
          </td>
          <td>
            <div style="display:flex; gap:6px; align-items:center;">
              <button class="btn btn-outline-emerald" style="padding:4px 8px; font-size:0.75rem;" onclick="openViewApplicationModal('${app.id}')">View Details</button>
              ${inviteLink ? `
                <button class="btn btn-outline-emerald" style="padding:4px 8px; font-size:0.75rem;" onclick="navigator.clipboard.writeText('${inviteLink}'); alert('Invitation Link Copied:\\n${inviteLink}');">Copy Link</button>
              ` : `
                <button class="btn btn-emerald" style="padding:4px 8px; font-size:0.75rem;" onclick="updateAppStatus('${app.id}', 'APPROVED')">Approve</button>
              `}
            </div>
          </td>
        </tr>`;
      });
      html += `</tbody></table>`;
      document.getElementById('applicationsTable').innerHTML = html;
    }

    // Load Audit Logs
    try {
      const auditRes = await fetch('/api/admin/audit-logs', { headers: { 'Authorization': `Bearer ${state.token}` } });
      if (auditRes.ok) {
        const auditData = await auditRes.json();
        if (document.getElementById('auditLogsTable')) {
          let auditHtml = `<table style="width:100%; text-align:left; border-collapse:collapse; color:var(--ink-primary);">
            <thead>
              <tr style="border-bottom:1px solid var(--mint-200); font-size:0.82rem; text-transform:uppercase; color:var(--grey-500);">
                <th style="padding:8px;">Timestamp</th>
                <th>Action</th>
                <th>User / Entity</th>
                <th>IP Address</th>
              </tr>
            </thead>
            <tbody>`;
          (auditData.audit_logs || []).forEach(log => {
            auditHtml += `<tr style="border-bottom:1px solid var(--border-hairline); font-size:0.82rem;">
              <td style="padding:8px; color:var(--grey-500);">${log.created_at || ''}</td>
              <td style="font-weight:700; color:var(--emerald-900);">${log.action_type || ''}</td>
              <td>${log.entity_type || ''} (${log.user_id || 'System'})</td>
              <td style="color:var(--grey-500);">${log.ip_address || '127.0.0.1'}</td>
            </tr>`;
          });
          auditHtml += `</tbody></table>`;
          document.getElementById('auditLogsTable').innerHTML = auditHtml;
        }
      }
    } catch (err) {
      console.error("Error loading audit logs:", err);
    }

    // Pre-fill Site Settings Customizer
    try {
      const setRes = await fetch('/api/admin/settings', { headers: { 'Authorization': `Bearer ${state.token}` } });
      if (setRes.ok) {
        const setData = await setRes.json();
        if (setData.settings) {
          setData.settings.forEach(s => {
            const input = document.getElementById(`set_${s.key_name}`);
            if (input) input.value = s.key_value || '';
            const prev = document.getElementById(`prev_${s.key_name}`);
            if (prev && s.key_value) prev.src = s.key_value;
          });
        }
      }
    } catch (err) {
      console.error("Error pre-filling settings:", err);
    }

    // Load Admin Meeting Photos Gallery (16:9)
    loadAdminMeetingPhotos();

  } catch (err) {
    console.error("Error loading admin tab:", err);
  }
}

async function updateAppStatus(appId, status) {
  const res = await fetch(`/api/admin/applications/${appId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
    body: JSON.stringify({ status })
  });
  const data = await res.json();
  if (data.invitation_token) {
    alert(`Applicant Approved! Invitation link generated:\nhttp://localhost:8000/#activate?token=${data.invitation_token}`);
  }
  loadAdminTab();
}

function openViewApplicationModal(appId) {
  const app = (state.adminApplications || []).find(a => a.id === appId);
  if (!app) {
    alert("Application details not found.");
    return;
  }

  document.getElementById('detail_app_status').innerText = app.status || 'SUBMITTED';
  document.getElementById('detail_app_status').className = `badge ${app.status === 'APPROVED' || app.status === 'INVITED' || app.status === 'CONVERTED' ? 'badge-verified' : 'badge-active'}`;
  document.getElementById('detail_app_date').innerText = `Applied: ${app.created_at || 'Recently'}`;
  document.getElementById('detail_app_name').innerText = app.full_name || 'Founder';
  document.getElementById('detail_app_headline').innerText = `${app.designation || 'Leader'} at ${app.business_name || 'Business'} • ${app.city || 'Pan India'}`;

  // Build collaboration preferences tags
  const rawPrefs = app.collaboration_preferences || '';
  const prefs = rawPrefs.split(',').map(p => p.trim()).filter(Boolean);
  const prefsHtml = prefs.length > 0
    ? prefs.map(p => `<span class="badge badge-active" style="margin-right: 6px; margin-bottom: 6px; font-size: 0.78rem;">${p}</span>`).join('')
    : '<span style="color: var(--grey-500); font-size: 0.85rem;">None specified</span>';

  // Social links
  const webLink = app.website ? `<a href="${app.website}" target="_blank" rel="noopener noreferrer" style="color: var(--emerald-700); font-weight: 700; text-decoration: underline;">${app.website}</a>` : '<span style="color: var(--grey-500);">Not provided</span>';
  const linkedinLink = app.linkedin ? `<a href="${app.linkedin}" target="_blank" rel="noopener noreferrer" style="color: var(--emerald-700); font-weight: 700; text-decoration: underline;">${app.linkedin}</a>` : '<span style="color: var(--grey-500);">Not provided</span>';
  const instaLink = app.instagram ? `<a href="${app.instagram}" target="_blank" rel="noopener noreferrer" style="color: var(--emerald-700); font-weight: 700; text-decoration: underline;">${app.instagram}</a>` : '<span style="color: var(--grey-500);">Not provided</span>';

  document.getElementById('detail_app_body').innerHTML = `
    <!-- Contact Info -->
    <div style="background: var(--mint-50); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 12px 16px;">
      <h5 style="color: var(--emerald-900); margin: 0 0 8px 0; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">Contact Information</h5>
      <div class="form-row-3" style="font-size: 0.88rem;">
        <div><strong>Email:</strong><br>${app.email}</div>
        <div><strong>Phone:</strong><br>${app.phone}</div>
        <div><strong>WhatsApp:</strong><br>${app.whatsapp || app.phone}</div>
      </div>
    </div>

    <!-- Business Details -->
    <div style="background: var(--mint-50); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 12px 16px;">
      <h5 style="color: var(--emerald-900); margin: 0 0 8px 0; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">Business Profile & Foundation</h5>
      <div class="form-row-2" style="font-size: 0.88rem; margin-bottom: 8px;">
        <div><strong>Business Name:</strong> ${app.business_name || 'N/A'}</div>
        <div><strong>Category of Business:</strong> <span class="badge badge-active">${app.business_model_category || 'Product Based'}</span></div>
      </div>
      <div class="form-row-3" style="font-size: 0.88rem; margin-bottom: 8px;">
        <div><strong>Type of Firm:</strong> ${app.firm_type || 'Private Limited (Pvt Ltd)'}</div>
        <div><strong>Years in Business:</strong> ${app.years_in_business || 'N/A'}</div>
        <div><strong>Team Size:</strong> ${app.team_size || 'N/A'}</div>
      </div>
      <div class="form-row-2" style="font-size: 0.88rem; margin-bottom: 10px;">
        <div><strong>Industry Sector:</strong> ${app.business_category || 'N/A'}</div>
        <div><strong>Growth Stage:</strong> ${app.business_stage || 'N/A'}</div>
      </div>
      <div style="font-size: 0.88rem; border-top: 1px dashed var(--mint-200); padding-top: 8px;">
        <strong>Brief About Business:</strong>
        <p style="margin: 4px 0 0 0; color: var(--ink-primary); line-height: 1.5; white-space: pre-wrap;">${app.business_description || 'N/A'}</p>
      </div>
    </div>

    <!-- Web & Social Links -->
    <div style="background: var(--mint-50); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 12px 16px;">
      <h5 style="color: var(--emerald-900); margin: 0 0 8px 0; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">Digital Presence & Profiles</h5>
      <div class="form-row-3" style="font-size: 0.88rem;">
        <div><strong>Business Website:</strong><br>${webLink}</div>
        <div><strong>Founder LinkedIn:</strong><br>${linkedinLink}</div>
        <div><strong>Business Instagram:</strong><br>${instaLink}</div>
      </div>
    </div>

    <!-- Community Exchange -->
    <div style="background: var(--mint-50); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 12px 16px;">
      <h5 style="color: var(--emerald-900); margin: 0 0 8px 0; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">Community Exchange (Give & Ask)</h5>
      <div style="font-size: 0.88rem; margin-bottom: 8px;">
        <strong style="color: var(--emerald-800);">What They Can Contribute:</strong>
        <p style="margin: 4px 0 0 0; color: var(--ink-primary); line-height: 1.5; white-space: pre-wrap;">${app.what_offer || 'N/A'}</p>
      </div>
      <div style="font-size: 0.88rem; border-top: 1px dashed var(--mint-200); padding-top: 8px;">
        <strong style="color: var(--emerald-800);">What They Are Looking For:</strong>
        <p style="margin: 4px 0 0 0; color: var(--ink-primary); line-height: 1.5; white-space: pre-wrap;">${app.what_need || 'N/A'}</p>
      </div>
    </div>

    <!-- Collaboration Preferences -->
    <div style="background: var(--mint-50); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 12px 16px;">
      <h5 style="color: var(--emerald-900); margin: 0 0 8px 0; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">Collaboration & Connection Preferences</h5>
      <div style="margin-top: 6px;">
        ${prefsHtml}
      </div>
    </div>

    <!-- Why Join -->
    <div style="background: var(--mint-50); border: 1px solid var(--border-hairline); border-radius: var(--radius-md); padding: 12px 16px;">
      <h5 style="color: var(--emerald-900); margin: 0 0 8px 0; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">Why Join Founder for Founder</h5>
      <p style="margin: 4px 0 0 0; color: var(--ink-primary); font-size: 0.88rem; line-height: 1.5; white-space: pre-wrap;">${app.why_join || 'N/A'}</p>
    </div>
  `;

  const inviteLink = app.invitation_token ? `${window.location.origin}/#activate?token=${app.invitation_token}` : '';
  document.getElementById('detail_app_actions').innerHTML = `
    <button class="btn btn-outline-emerald" onclick="closeModal('appDetailModal')">Close</button>
    ${inviteLink ? `
      <button class="btn btn-outline-emerald" onclick="navigator.clipboard.writeText('${inviteLink}'); alert('Invitation Link Copied:\\n${inviteLink}');">Copy Invite Link</button>
    ` : `
      <button class="btn btn-emerald" onclick="closeModal('appDetailModal'); updateAppStatus('${app.id}', 'APPROVED')">Approve & Generate Invite</button>
    `}
  `;

  openModal('appDetailModal');
}

async function handleCancelAutoRenew() {
  if (!confirm("Are you sure you want to cancel auto-renewal? Your membership will remain active until the end of your current billing period.")) return;
  const res = await fetch('/api/memberships/cancel-autorenew', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${state.token}` }
  });
  const data = await res.json();
  alert(data.message || "Auto-renewal cancelled.");
  checkAuthSession();
}

async function handleSaveSettings(e) {
  e.preventDefault();
  const keys = [
    'logo_url', 'hero_banner_url', 'hero_heading', 'hero_subheading',
    'hero_capsule_1_url', 'hero_capsule_2_url', 'hero_capsule_3_url',
    'philosophy_img_1', 'philosophy_img_2', 'philosophy_img_3', 'philosophy_img_4',
    'format_img_play', 'format_img_explore', 'format_img_dine', 'format_img_build', 'format_img_celebrate',
    'feature_img_network', 'feature_img_needs', 'feature_img_crm', 'feature_img_meetings', 'feature_img_collaborations', 'feature_img_challenges',
    'google_client_id'
  ];
  const body = {};
  keys.forEach(k => {
    const el = document.getElementById(`set_${k}`);
    if (el) body[k] = el.value.trim();
  });

  const res = await fetch('/api/admin/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
    body: JSON.stringify(body)
  });
  if (res.ok) {
    alert("Website Media & CMS Settings saved successfully!");
    fetchPublicContent();
    loadAdminTab();
  } else {
    alert("Failed to save settings. Please verify admin permissions.");
  }
}

// Media Upload & Preview Helpers
function previewImageInput(url, previewImgId) {
  const img = document.getElementById(previewImgId);
  if (img && url) {
    img.src = url;
  }
}

async function handleAdminFileUpload(fileInput, targetInputId, previewImgId, statusId) {
  const file = fileInput.files && fileInput.files[0];
  if (!file) return;

  const statusEl = document.getElementById(statusId);
  if (statusEl) {
    statusEl.innerText = 'Uploading...';
    statusEl.style.color = 'var(--gold-500)';
  }

  const reader = new FileReader();
  reader.onload = async (e) => {
    try {
      const base64Data = e.target.result;
      const res = await fetch('/api/admin/upload-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.token}`
        },
        body: JSON.stringify({
          filename: file.name,
          data: base64Data
        })
      });

      const data = await res.json();
      if (res.ok && data.url) {
        const input = document.getElementById(targetInputId);
        if (input) input.value = data.url;
        const prev = document.getElementById(previewImgId);
        if (prev) prev.src = data.url;
        if (statusEl) {
          statusEl.innerText = 'Uploaded';
          statusEl.style.color = 'var(--emerald-600)';
          setTimeout(() => { statusEl.innerText = ''; }, 3000);
        }
      } else {
        alert(data.error || 'Upload failed');
        if (statusEl) {
          statusEl.innerText = 'Failed';
          statusEl.style.color = '#dc2626';
        }
      }
    } catch (err) {
      console.error('File upload error:', err);
      alert('Error uploading image file: ' + err.message);
      if (statusEl) {
        statusEl.innerText = 'Error';
        statusEl.style.color = '#dc2626';
      }
    }
  };
  reader.readAsDataURL(file);
}

function toggleEventPricingFields(isPaid) {
  const container = document.getElementById('evt_paid_fields_container');
  const priceInput = document.getElementById('evt_price_amount');
  if (container) {
    container.style.display = isPaid ? 'grid' : 'none';
  }
  if (!isPaid && priceInput) {
    priceInput.value = '0';
  } else if (isPaid && priceInput && (!priceInput.value || Number(priceInput.value) <= 0)) {
    priceInput.value = '1499';
  }
}

function generateMapLinkFromVenue() {
  const venue = (document.getElementById('evt_venue')?.value || '').trim();
  const city = (document.getElementById('evt_city')?.value || '').trim();
  const mapInput = document.getElementById('evt_google_maps_url');
  if (!venue) {
    alert("Please enter a Venue or Meeting Address first.");
    return;
  }
  const searchQuery = encodeURIComponent(`${venue} ${city}`.trim());
  const mapUrl = `https://www.google.com/maps/search/?api=1&query=${searchQuery}`;
  if (mapInput) {
    mapInput.value = mapUrl;
    updateMapPreview(mapUrl);
  }
}

function autoSuggestMapUrl() {
  const mapInput = document.getElementById('evt_google_maps_url');
  if (!mapInput || mapInput.dataset.manualEdited === 'true') return;
  const venue = (document.getElementById('evt_venue')?.value || '').trim();
  const city = (document.getElementById('evt_city')?.value || '').trim();
  if (venue) {
    const searchQuery = encodeURIComponent(`${venue} ${city}`.trim());
    const mapUrl = `https://www.google.com/maps/search/?api=1&query=${searchQuery}`;
    mapInput.value = mapUrl;
    updateMapPreview(mapUrl);
  } else {
    mapInput.value = '';
    updateMapPreview('');
  }
}

function updateMapPreview(url) {
  const btn = document.getElementById('evt_map_preview_btn');
  const mapInput = document.getElementById('evt_google_maps_url');
  if (mapInput && window.event && window.event.type === 'input') {
    mapInput.dataset.manualEdited = 'true';
  }
  if (!btn) return;
  if (url && (url.startsWith('http://') || url.startsWith('https://'))) {
    btn.href = url;
    btn.style.display = 'inline-flex';
  } else {
    btn.style.display = 'none';
  }
}

async function handleAdminCreateEvent(e) {
  e.preventDefault();
  const venue = (document.getElementById('evt_venue')?.value || '').trim();
  const city = (document.getElementById('evt_city')?.value || 'Pan India').trim();
  let googleMapsUrl = (document.getElementById('evt_google_maps_url')?.value || '').trim();
  if (!googleMapsUrl && venue) {
    googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((venue + ' ' + city).trim())}`;
  }

  const priceAmount = parseFloat(document.getElementById('evt_price_amount')?.value || 0);
  const whatIncluded = (document.getElementById('evt_what_is_included')?.value || '').trim() || 'Included in Gathering Ticket';

  const body = {
    title: document.getElementById('evt_title').value,
    category: document.getElementById('evt_category').value,
    signature_format: document.getElementById('evt_signature_format').value,
    event_date: document.getElementById('evt_date').value,
    time_str: document.getElementById('evt_time_str').value,
    venue: venue,
    city: city,
    google_maps_url: googleMapsUrl,
    description: document.getElementById('evt_description').value,
    price_amount: priceAmount,
    what_is_included: whatIncluded
  };

  const res = await fetch('/api/admin/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
    body: JSON.stringify(body)
  });
  if (res.ok) {
    alert("New Event published successfully!");
    document.getElementById('adminCreateEventForm').reset();
    toggleEventPricingFields(false);
    updateMapPreview('');
    const mapInput = document.getElementById('evt_google_maps_url');
    if (mapInput) delete mapInput.dataset.manualEdited;
    fetchPublicContent();
    loadEventsTab();
    loadAdminTab();
  } else {
    alert("Failed to create event.");
  }
}

// ==========================================================================
// ATTENDANCE TRACKER & PRESENCE ENGINE
// ==========================================================================
let currentAttendanceData = null;

async function loadAttendanceTab(selectedMonth) {
  try {
    const url = selectedMonth ? `/api/attendance/summary?month=${encodeURIComponent(selectedMonth)}` : '/api/attendance/summary';
    const res = await fetch(url, { headers: { 'Authorization': `Bearer ${state.token}` } });
    const data = await res.json();
    if (data.error) {
      console.error("Attendance fetch error:", data.error);
      return;
    }
    currentAttendanceData = data;

    // Populate month select if options changed
    const sel = document.getElementById('attendanceMonthSelect');
    if (sel && data.available_months && data.available_months.length > 0) {
      sel.innerHTML = data.available_months.map(m => {
        let label = m;
        try {
          const parts = m.split('-');
          const d = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, 1);
          label = d.toLocaleString('default', { month: 'long', year: 'numeric' });
        } catch (e) {}
        return `<option value="${m}" ${m === data.selected_month ? 'selected' : ''}>${label}</option>`;
      }).join('');
    }

    // Update KPI metrics
    if (document.getElementById('attRateValue')) document.getElementById('attRateValue').innerText = `${data.attendance_rate}%`;
    if (document.getElementById('attEventsAttendedRatio')) document.getElementById('attEventsAttendedRatio').innerText = `(${data.events_attended}/${data.completed_events || data.total_events} Attended)`;
    if (document.getElementById('attRateBar')) document.getElementById('attRateBar').style.width = `${data.attendance_rate}%`;
    if (document.getElementById('attTotalEvents')) document.getElementById('attTotalEvents').innerText = data.total_events;
    if (document.getElementById('attStreakValue')) document.getElementById('attStreakValue').innerText = `Streak: ${data.attendance_streak} Gatherings`;
    if (document.getElementById('attStandingTier')) document.getElementById('attStandingTier').innerText = `<svg class="icon-inline" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> ${data.accountability_tier}`;
    if (document.getElementById('attendanceListTitle')) document.getElementById('attendanceListTitle').innerText = `Gatherings Hosted in ${data.month_name}`;

    // Render Events List
    const container = document.getElementById('attendanceEventsList');
    if (!container) return;

    if (!data.events || data.events.length === 0) {
      container.innerHTML = `<div style="text-align: center; padding: 2rem; color: var(--grey-500);">No gatherings scheduled or hosted for ${data.month_name}.</div>`;
      return;
    }

    container.innerHTML = data.events.map(ev => {
      let badgeHtml = '';
      let actionBtnHtml = '';

      if (ev.calculated_status === 'PRESENT') {
        badgeHtml = `<span class="badge-status-present"><svg class="icon-inline" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Attended &amp; Verified</span>`;
        actionBtnHtml = `<span style="font-size: 0.82rem; color: var(--emerald-700); font-weight: 700;">Check-in Confirmed</span>`;
      } else if (ev.calculated_status === 'MISSED') {
        badgeHtml = `<span class="badge-status-missed">Missed Gathering</span>`;
        actionBtnHtml = `<span style="font-size: 0.82rem; color: #b45309; font-weight: 600;">Absent</span>`;
      } else if (ev.calculated_status === 'RSVP_CONFIRMED') {
        badgeHtml = `<span class="badge-status-rsvp"><svg class="icon-inline" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> RSVP Confirmed</span>`;
        actionBtnHtml = `<button class="btn btn-emerald" style="padding: 0.45rem 0.95rem; font-size: 0.82rem;" onclick="openCheckinModal('${ev.id}')">Check In Now</button>`;
      } else {
        badgeHtml = `<span class="badge-status-upcoming">Upcoming Event</span>`;
        actionBtnHtml = `<button class="btn btn-outline-emerald" style="padding: 0.45rem 0.95rem; font-size: 0.82rem;" onclick="openCheckinModal('${ev.id}')">Check In</button>`;
      }

      return `
        <div class="meeting-item-card" style="border-left: 4px solid ${ev.calculated_status === 'PRESENT' ? 'var(--emerald-500)' : 'var(--mint-200)'};">
          <div style="flex: 2; min-width: 260px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap;">
              <span style="font-size: 0.78rem; font-weight: 800; background: var(--mint-100); color: var(--emerald-900); padding: 3px 8px; border-radius: 4px;">${ev.event_date.split(' ')[0]}</span>
              <span style="font-size: 0.78rem; font-weight: 700; color: var(--grey-500);">${ev.time_str || ''}</span>
              <span style="font-size: 0.78rem; font-weight: 700; color: var(--gold-500);">${ev.signature_format || 'Gathering'}</span>
              ${badgeHtml}
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: var(--ink-primary); margin-bottom: 4px;">${ev.title}</div>
            <div style="font-size: 0.85rem; color: var(--grey-600); display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
              <span><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span> ${ev.venue || 'Private Location'}, ${ev.city || 'Pan India'}</span>
              <span><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span> Host: ${ev.host_name || 'Community Team'}</span>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            ${actionBtnHtml}
          </div>
        </div>
      `;
    }).join('');

  } catch (err) {
    console.error("loadAttendanceTab error:", err);
  }
}

function filterAttendanceMonth() {
  const sel = document.getElementById('attendanceMonthSelect');
  if (sel) loadAttendanceTab(sel.value);
}

function openCheckinModal(eventId) {
  const sel = document.getElementById('checkinEventSelect');
  if (sel && currentAttendanceData && currentAttendanceData.events) {
    sel.innerHTML = currentAttendanceData.events.map(ev => 
      `<option value="${ev.id}" ${ev.id === eventId ? 'selected' : ''}>${ev.title} (${ev.event_date.split(' ')[0]})</option>`
    ).join('');
  }
  const codeInput = document.getElementById('checkinCodeInput');
  if (codeInput) codeInput.value = 'F4F2026';
  openModal('checkinModal');
}

async function handleCheckinSubmit(event) {
  event.preventDefault();
  const eventId = document.getElementById('checkinEventSelect').value;
  const checkinCode = document.getElementById('checkinCodeInput').value.trim();

  try {
    const res = await fetch('/api/events/checkin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
      body: JSON.stringify({ event_id: eventId, checkin_code: checkinCode })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    alert(data.message || 'Presence confirmed successfully!');
    closeModal('checkinModal');
    loadAttendanceTab(document.getElementById('attendanceMonthSelect')?.value);
    loadDashboardTab();
  } catch (err) {
    alert("Network error confirming presence. Please try again.");
  }
}

// ==========================================================================
// 1-TO-1 FOUNDER MEETINGS TRACKER
// ==========================================================================
async function loadMeetingsTab() {
  try {
    const res = await fetch('/api/founder-meetings', { headers: { 'Authorization': `Bearer ${state.token}` } });
    const data = await res.json();
    if (data.error) return;

    if (data.stats) {
      if (document.getElementById('meetingsThisMonth')) document.getElementById('meetingsThisMonth').innerText = data.stats.this_month;
      if (document.getElementById('meetingsMonthName')) document.getElementById('meetingsMonthName').innerText = data.stats.current_month_name;
      if (document.getElementById('meetingsSynergies')) document.getElementById('meetingsSynergies').innerText = data.stats.synergies;
      if (document.getElementById('meetingsTotal')) document.getElementById('meetingsTotal').innerText = data.stats.total;
    }

    const container = document.getElementById('meetingsFeedContainer');
    if (!container) return;

    if (!data.meetings || data.meetings.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: var(--grey-500);">
          <div class="empty-state-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--emerald-700)" stroke-width="1.75"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m19 11 2 2 4-4"/></svg></div>
          <div style="font-weight: 700; color: var(--ink-primary); font-size: 1.1rem; margin-bottom: 4px;">No 1-to-1 Meetings Logged Yet</div>
          <p style="font-size: 0.9rem;">Record individual coffee chats, strategy sessions, and partnerships with fellow founders.</p>
          <button class="btn btn-emerald" style="margin-top: 1rem;" onclick="openLogMeetingModal()">+ Log First 1:1 Meeting</button>
        </div>
      `;
      return;
    }

    container.innerHTML = data.meetings.map(m => {
      let outcomeClass = 'outcome-synergy';
      if (m.collaboration_outcome === 'Referral Exchanged') outcomeClass = 'outcome-referral';
      else if (m.collaboration_outcome === 'Deal In Progress') outcomeClass = 'outcome-deal';
      else if (m.collaboration_outcome === 'Follow-up Scheduled') outcomeClass = 'outcome-followup';

      const starCount = Math.max(1, Math.min(5, parseInt(m.rating, 10) || 5));
    const stars = Array(starCount).fill('<svg class="star-svg" width="13" height="13" viewBox="0 0 24 24" fill="#F59E0B" stroke="#D97706" stroke-width="1"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>').join('');

      return `
        <div class="meeting-item-card">
          <div style="display: flex; gap: 14px; align-items: flex-start; flex: 2; min-width: 280px;">
            <img src="${m.partner_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'}" alt="${m.partner_name || 'Member'}" loading="lazy" decoding="async" width="52" height="52" style="width: 52px; height: 52px; border-radius: 50%; object-fit: cover; border: 2px solid var(--emerald-400); box-shadow: 0 4px 10px rgba(4,120,87,0.15);">
            <div>
              <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 4px;">
                <span style="font-size: 1.15rem; font-weight: 800; color: var(--ink-primary);">${m.partner_name}</span>
                <span style="font-size: 0.85rem; font-weight: 700; color: var(--emerald-700);">(${m.partner_company})</span>
                <span class="outcome-pill ${outcomeClass}">${m.collaboration_outcome || 'Synergy'}</span>
              </div>
              <div style="font-size: 0.88rem; font-weight: 700; color: var(--ink-primary); margin-bottom: 4px;"><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg></span> ${m.agenda_topic}</div>
              ${m.discussion_notes ? `<p style="font-size: 0.85rem; color: var(--grey-600); margin-bottom: 6px; line-height: 1.5;">${m.discussion_notes}</p>` : ''}
              <div style="font-size: 0.8rem; color: var(--grey-500); display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <span><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></span> ${m.meeting_date ? m.meeting_date.split(' ')[0] : 'Recent'}</span>
                <span><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg></span> ${m.meeting_type || 'In-Person'}</span>
                ${m.location_venue ? `<span><span class="meta-tag-icon"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span> ${m.location_venue}</span>` : ''}
              </div>
            </div>
          </div>
          <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--emerald-800);">${stars}</div>
            <span style="font-size: 0.78rem; font-weight: 800; background: var(--mint-100); color: var(--emerald-900); padding: 2px 8px; border-radius: 4px;">Verified Record</span>
          </div>
        </div>
      `;
    }).join('');

  } catch (err) {
    console.error("loadMeetingsTab error:", err);
  }
}

function openLogMeetingModal() {
  const dateInput = document.getElementById('meetDate');
  if (dateInput) dateInput.value = new Date().toISOString().split('T')[0];
  openModal('logMeetingModal');
}

async function handleLogMeetingSubmit(event) {
  event.preventDefault();
  const payload = {
    partner_name: document.getElementById('meetPartnerName').value.trim(),
    partner_company: document.getElementById('meetPartnerCompany').value.trim(),
    meeting_date: document.getElementById('meetDate').value,
    meeting_type: document.getElementById('meetType').value,
    location_venue: document.getElementById('meetVenue').value.trim(),
    agenda_topic: document.getElementById('meetAgenda').value.trim(),
    discussion_notes: document.getElementById('meetNotes').value.trim(),
    collaboration_outcome: document.getElementById('meetOutcome').value,
    rating: parseInt(document.getElementById('meetRating').value) || 5
  };

  try {
    const res = await fetch('/api/founder-meetings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${state.token}` },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    alert("1-to-1 Founder Meeting logged successfully!");
    closeModal('logMeetingModal');
    document.getElementById('logMeetingForm').reset();
    loadMeetingsTab();
    loadDashboardTab();
  } catch (err) {
    alert("Network error saving meeting record.");
  }
}

// ==========================================
// CURATED MEETING PHOTOS SLIDER (16:9 RATIO)
// ==========================================
function renderMeetingPhotosSlider(photos) {
  const track = document.getElementById('meetingPhotosTrack');
  if (!track || !photos || photos.length === 0) return;
  track.innerHTML = '';

  // Ensure enough items for a wide continuous slider track
  let displayList = [...photos];
  while (displayList.length < 8) {
    displayList = displayList.concat(photos);
  }

  // Duplicate for seamless 50% translation marquee loop
  const fullLoop = displayList.concat(displayList);

  fullLoop.forEach(p => {
    const card = document.createElement('div');
    card.className = 'meeting-photo-card';
    card.innerHTML = `
      <img src="${p.image_url}" alt="${p.title}" class="meeting-photo-img" loading="lazy" decoding="async" width="440" height="248">
      <div class="meeting-photo-overlay">
        <span class="meeting-photo-tag">${p.tag || 'Curated Gathering'}</span>
        <h4 class="meeting-photo-title">${p.title}</h4>
        ${p.caption ? `<p class="meeting-photo-caption">${p.caption}</p>` : ''}
      </div>
    `;
    track.appendChild(card);
  });
}

function openAddMeetingPhotoModal() {
  const form = document.getElementById('addMeetingPhotoForm');
  if (form) form.reset();
  const prev = document.getElementById('photoPreviewImg');
  if (prev) prev.src = 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1280&q=80';
  const dateInput = document.getElementById('photoEventDate');
  if (dateInput) dateInput.value = new Date().toISOString().split('T')[0];
  const statusSpan = document.getElementById('photoUploadStatus');
  if (statusSpan) statusSpan.textContent = '';
  openModal('addMeetingPhotoModal');
}

function previewMeetingPhoto(url) {
  const prev = document.getElementById('photoPreviewImg');
  if (prev && url) {
    prev.src = url;
  }
}

async function handleMeetingPhotoUpload(input) {
  const file = input.files[0];
  if (!file) return;
  const statusSpan = document.getElementById('photoUploadStatus');
  if (statusSpan) statusSpan.textContent = 'Uploading 16:9 photo...';

  const reader = new FileReader();
  reader.onload = async function(e) {
    try {
      const resp = await fetch('/api/admin/upload-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          data_base64: e.target.result.split(',')[1]
        })
      });
      const res = await resp.json();
      if (res.url) {
        document.getElementById('photoImageUrl').value = res.url;
        previewMeetingPhoto(res.url);
        if (statusSpan) statusSpan.textContent = 'Uploaded successfully (16:9 ready)!';
      } else {
        if (statusSpan) statusSpan.textContent = 'Upload failed, please check file.';
      }
    } catch (err) {
      if (statusSpan) statusSpan.textContent = 'Error uploading photo file.';
    }
  };
  reader.readAsDataURL(file);
}

async function handleAddMeetingPhotoSubmit(event) {
  event.preventDefault();
  const title = document.getElementById('photoTitle').value.trim();
  const tag = document.getElementById('photoTag').value;
  const event_date = document.getElementById('photoEventDate').value;
  const image_url = document.getElementById('photoImageUrl').value.trim();
  const caption = document.getElementById('photoCaption').value.trim();

  try {
    const resp = await fetch('/api/meeting-photos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, tag, event_date, image_url, caption })
    });
    const data = await resp.json();
    if (data.success) {
      closeModal('addMeetingPhotoModal');
      // Refresh homepage slider
      const fetchResp = await fetch('/api/meeting-photos');
      const photosData = await fetchResp.json();
      if (photosData.photos) {
        renderMeetingPhotosSlider(photosData.photos);
        renderAdminMeetingPhotosList(photosData.photos);
      }
      alert('Meeting photo successfully added to the 16:9 slider!');
    } else {
      alert(data.error || 'Failed to add meeting photo.');
    }
  } catch (err) {
    alert('Error adding photo: ' + err.message);
  }
}

async function loadAdminMeetingPhotos() {
  try {
    const resp = await fetch('/api/meeting-photos');
    const data = await resp.json();
    if (data.photos) {
      renderAdminMeetingPhotosList(data.photos);
    }
  } catch (err) {
    console.error("loadAdminMeetingPhotos error:", err);
  }
}

function renderAdminMeetingPhotosList(photos) {
  const container = document.getElementById('adminMeetingPhotosList');
  if (!container) return;
  if (!photos || photos.length === 0) {
    container.innerHTML = '<p style="color: var(--grey-500); font-size: 0.9rem;">No meeting photos added yet.</p>';
    return;
  }
  container.innerHTML = photos.map(p => `
    <div style="background: var(--mint-50); border: 1px solid var(--mint-200); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column;">
      <div style="aspect-ratio: 16 / 9; overflow: hidden; background: #042F2C;">
        <img src="${p.image_url}" alt="${p.title}" loading="lazy" decoding="async" style="width: 100%; height: 100%; object-fit: cover; aspect-ratio: 16 / 9;">
      </div>
      <div style="padding: 12px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <span style="font-size: 0.72rem; font-weight: 800; color: var(--emerald-800); text-transform: uppercase; background: #E4F7EE; padding: 2px 6px; border-radius: 4px;">${p.tag || 'Curated Gathering'}</span>
          <h5 style="margin: 6px 0 2px 0; font-size: 0.98rem; color: var(--ink-primary);">${p.title}</h5>
          <p style="margin: 0; font-size: 0.8rem; color: var(--grey-600);">${p.caption || ''}</p>
        </div>
        <div style="margin-top: 12px; display: flex; justify-content: flex-end;">
          <button type="button" class="btn btn-outline-emerald" style="padding: 4px 10px; font-size: 0.75rem; color: #DC2626; border-color: #FECACA;" onclick="handleDeleteMeetingPhoto('${p.id}')"><svg class="icon-inline" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg> Remove</button>
        </div>
      </div>
    </div>
  `).join('');
}

async function handleDeleteMeetingPhoto(id) {
  if (!confirm('Are you sure you want to remove this photo from the 16:9 slider?')) return;
  try {
    const resp = await fetch('/api/meeting-photos/delete/' + id, { method: 'POST' });
    const data = await resp.json();
    if (data.success) {
      const fetchResp = await fetch('/api/meeting-photos');
      const photosData = await fetchResp.json();
      if (photosData.photos) {
        renderMeetingPhotosSlider(photosData.photos);
        renderAdminMeetingPhotosList(photosData.photos);
      }
    }
  } catch (err) {
    alert('Error deleting photo: ' + err.message);
  }
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function previewQuickPhoto(url) {
  // Optional URL preview hook
}

async function handleQuickPhotoUpload(input) {
  const file = input.files[0];
  if (!file) return;
  const statusSpan = document.getElementById('quickPhotoStatus');
  if (statusSpan) statusSpan.textContent = 'Uploading 16:9 photo file...';

  const reader = new FileReader();
  reader.onload = async function(e) {
    try {
      const resp = await fetch('/api/admin/upload-image', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.token}`
        },
        body: JSON.stringify({
          filename: file.name,
          data: e.target.result
        })
      });
      const res = await resp.json();
      if (res.url) {
        document.getElementById('quickPhotoUrl').value = res.url;
        if (statusSpan) statusSpan.textContent = 'Image uploaded successfully (16:9 ready)!';
      } else {
        if (statusSpan) statusSpan.textContent = res.error || 'Upload failed.';
      }
    } catch (err) {
      if (statusSpan) statusSpan.textContent = 'Error uploading photo file.';
    }
  };
  reader.readAsDataURL(file);
}

async function handleAdminQuickAddPhoto(event) {
  event.preventDefault();
  const title = document.getElementById('quickPhotoTitle').value.trim();
  const tag = document.getElementById('quickPhotoTag').value;
  const image_url = document.getElementById('quickPhotoUrl').value.trim();
  const caption = document.getElementById('quickPhotoCaption').value.trim();
  const statusSpan = document.getElementById('quickPhotoStatus');

  if (!image_url) {
    alert('Please provide an image URL or upload an image file.');
    return;
  }

  try {
    const resp = await fetch('/api/meeting-photos', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.token}`
      },
      body: JSON.stringify({ title, tag, image_url, caption })
    });
    const data = await resp.json();
    if (data.success) {
      document.getElementById('adminQuickAddPhotoForm').reset();
      if (statusSpan) statusSpan.textContent = 'Meeting photo added directly to 16:9 slider!';
      const fetchResp = await fetch('/api/meeting-photos');
      const photosData = await fetchResp.json();
      if (photosData.photos) {
        renderMeetingPhotosSlider(photosData.photos);
        renderAdminMeetingPhotosList(photosData.photos);
      }
      setTimeout(() => { if (statusSpan) statusSpan.textContent = ''; }, 3500);
    } else {
      alert(data.error || 'Failed to add photo.');
    }
  } catch (err) {
    alert('Error adding photo: ' + err.message);
  }
}

// ==========================================
// FOUNDERS COLLECTIVE CHAT LOGIC (SINGLE ROOM)
// ==========================================
async function loadChatMessages() {
  const container = document.getElementById('chatMessagesArea');
  const activeContainer = document.getElementById('chatActiveContainer');
  const gateCard = document.getElementById('chatGateCard');
  if (!container) return;

  try {
    const resp = await fetch('/api/chat/messages?channel=collective', {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    const data = await resp.json();

    if (resp.status === 403 || !data.has_membership) {
      if (activeContainer) activeContainer.style.display = 'none';
      if (gateCard) gateCard.style.display = 'flex';
      return;
    }

    if (activeContainer) activeContainer.style.display = 'flex';
    if (gateCard) gateCard.style.display = 'none';

    const messages = data.messages || [];
    if (messages.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; color: var(--grey-500); padding: 3rem 1rem;">
          <div class="empty-state-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--emerald-700)" stroke-width="1.75"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></div>
          <h4 style="margin: 0; color: var(--forest-900);">Welcome to the Founders Collective Chat</h4>
          <p style="font-size: 0.88rem; margin-top: 4px;">No messages yet. Be the first founder to post a question, share deal flow, or ask for peer insights!</p>
        </div>
      `;
      return;
    }

    const currentUserId = state.user ? state.user.id : null;
    container.innerHTML = messages.map(m => {
      const isMine = currentUserId && (m.user_id === currentUserId);
      const avatar = m.profile_photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80';
      const senderName = m.full_name || m.email || 'Fellow Founder';
      const senderBiz = m.business_name ? ` • ${m.business_name}` : '';
      const timeStr = m.created_at ? new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';

      return `
        <div class="chat-msg-row ${isMine ? 'mine' : ''}">
          <img src="${avatar}" alt="${senderName}" class="chat-msg-avatar" loading="lazy" decoding="async" width="34" height="34">
          <div class="chat-msg-body">
            <div class="chat-msg-sender">
              <strong>${senderName}</strong>
              <span class="chat-msg-biz">${senderBiz}</span>
              <span class="chat-msg-time">${timeStr}</span>
            </div>
            <div class="chat-bubble">${escapeHtml(m.message)}</div>
          </div>
        </div>
      `;
    }).join('');

    // Auto scroll to latest message
    container.scrollTop = container.scrollHeight;
  } catch (err) {
    console.error("loadChatMessages error:", err);
  }
}

function handleChatKeyDown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    handleSendChatMessage();
  }
}

async function handleSendChatMessage() {
  const input = document.getElementById('chatInputText');
  if (!input) return;
  const msg = input.value.trim();
  if (!msg) return;

  const sendBtn = document.getElementById('chatSendBtn');
  if (sendBtn) sendBtn.disabled = true;

  try {
    const resp = await fetch('/api/chat/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.token}`
      },
      body: JSON.stringify({
        channel: 'collective',
        message: msg
      })
    });
    const data = await resp.json();
    if (data.success) {
      input.value = '';
      await loadChatMessages();
    } else {
      alert(data.error || 'Failed to send message.');
    }
  } catch (err) {
    alert('Error sending message: ' + err.message);
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    input.focus();
  }
}


