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
    image: '/assets/hero_banner.jpg'
  },
  needs: {
    title: 'Needs & Wants Engine',
    text: 'A structured post engine allowing members to list explicit commercial requirements or high-value business offerings.',
    image: '/assets/hero_banner.jpg'
  },
  crm: {
    title: 'Leads & Referrals CRM',
    text: 'Record peer introductions, manage client deal pipelines, and track administrator-verified business generated.',
    image: '/assets/hero_banner.jpg'
  },
  meetings: {
    title: 'Founder Experiences',
    text: 'Activities spanning Play, Explore, Dine, Build, and Celebrate—from closed-door roundtables to sunrise trails and dinners.',
    image: '/assets/hero_banner.jpg'
  },
  collaborations: {
    title: 'Business Collaborations',
    text: 'Work alongside peers on strategic joint ventures, supplier partnerships, co-marketing, and co-founder alliances.',
    image: '/assets/hero_banner.jpg'
  },
  challenges: {
    title: 'Monthly Challenges',
    text: 'Participate in community milestone challenges focused on business growth, peer referrals, and introductions.',
    image: '/assets/hero_banner.jpg'
  }
};

// Clean branded initials avatar helper (memoized cache to eliminate allocations and CPU usage)
const _avatarCache = new Map();
function getInitialsAvatar(name) {
  const n = (name || 'Member').trim();
  const initials = n.split(' ').map(p => p[0]).filter(Boolean).slice(0, 2).join('').toUpperCase() || 'FF';
  if (_avatarCache.has(initials)) {
    return _avatarCache.get(initials);
  }
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
    <rect width="100" height="100" rx="20" fill="#064E3B"/>
    <text x="50" y="58" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="36" font-weight="700" fill="#F3FBF7" text-anchor="middle" dominant-baseline="middle">${initials}</text>
  </svg>`;
  const uri = `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
  _avatarCache.set(initials, uri);
  return uri;
}

// Initialize App on DOM Loaded (Instant Hydration + SWR Background Revalidation)
document.addEventListener('DOMContentLoaded', () => {
  // 1. Immediately hydrate DOM from local SWR cache (0ms instant paint)
  const initialCached = getStoredPublicContent();
  if (initialCached) {
    renderPublicContent(initialCached);
    if (initialCached.settings && initialCached.settings.google_client_id) {
      state.googleClientId = initialCached.settings.google_client_id;
      setupGoogleAuth(initialCached.settings.google_client_id);
    }
  }

  // 2. Fetch fresh public content in background
  fetchPublicContent();
  fetchAuthConfig();
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

// Persistent Stale-While-Revalidate (SWR) LocalStorage Cache
const PUBLIC_CACHE_STORAGE_KEY = 'f4f_public_content_cache_v2';
let cachedPublicData = null;

function getStoredPublicContent() {
  try {
    const raw = localStorage.getItem(PUBLIC_CACHE_STORAGE_KEY);
    if (!raw) return null;
    const obj = JSON.parse(raw);
    return obj && obj.data ? obj.data : null;
  } catch (e) {
    return null;
  }
}

function setStoredPublicContent(data) {
  try {
    localStorage.setItem(PUBLIC_CACHE_STORAGE_KEY, JSON.stringify({
      data: data,
      saved_at: Date.now()
    }));
  } catch (e) {}
}

async function fetchPublicContent(force = false) {
  try {
    // 1. Immediately hydrate from memory or localStorage if available
    if (!force && !cachedPublicData) {
      const stored = getStoredPublicContent();
      if (stored) {
        cachedPublicData = stored;
        renderPublicContent(stored);
      }
    }

    // 2. Fetch fresh updates from API in the background
    const res = await fetch('/api/public/content');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    cachedPublicData = data;
    setStoredPublicContent(data);
    renderPublicContent(data);

    // Auto-setup Google OAuth if client ID is provided in public settings
    if (data.settings && data.settings.google_client_id && !state.googleClientId) {
      state.googleClientId = data.settings.google_client_id;
      setupGoogleAuth(data.settings.google_client_id);
    }
  } catch (err) {
    console.warn("Public content background revalidation notice:", err);
  }
}

function renderPublicContent(data) {
  if (!data) return;

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
      const isMobile = typeof window !== 'undefined' && window.innerWidth <= 991;
      const gradient = isMobile
        ? 'linear-gradient(180deg, rgba(243, 251, 247, 0.96) 0%, rgba(243, 251, 247, 0.85) 55%, rgba(243, 251, 247, 0.35) 100%)'
        : 'linear-gradient(to right, rgba(243, 251, 247, 0.94) 0%, rgba(243, 251, 247, 0.78) 42%, rgba(243, 251, 247, 0.35) 75%, rgba(243, 251, 247, 0.08) 100%)';
      heroEl.style.backgroundImage = `${gradient}, url('${heroUrl}')`;
      heroEl.style.backgroundSize = 'cover';
      heroEl.style.backgroundPosition = isMobile ? 'center' : 'center right';
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

  // Live Database Counters (Authentic figures from verified database records)
  if (data.counters) {
    const activeMembersTotal = data.counters.active_members || 0;
    if (document.getElementById('counterMembers')) {
      document.getElementById('counterMembers').innerText = activeMembersTotal > 0 ? `${activeMembersTotal}+` : 'Curated';
    }
    const eventsTotal = data.counters.published_events || 0;
    if (document.getElementById('counterEvents')) {
      document.getElementById('counterEvents').innerText = eventsTotal > 0 ? `${eventsTotal}+` : 'Pan-India';
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

  // Testimonials (Display only genuine, verified endorsements; hide section if none exist)
  const storiesSection = document.getElementById('stories');
  const testimonialsContainer = document.getElementById('testimonialsContainer');
  if (storiesSection) {
    if (!data.testimonials || data.testimonials.length === 0) {
      storiesSection.style.display = 'none';
    } else if (testimonialsContainer) {
      storiesSection.style.display = 'block';
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
  alert("Google Sign-In is being configured. Please sign in using your registered email and password or request an email OTP.");
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
    renderAuthenticatedUI(data);
  } catch (err) {
    alert("Google authentication request failed. Please check your network connection.");
  }
}

// Passwordless Login / Verification via Email OTP
async function handleSendLoginOtp() {
  const emailInput = document.getElementById('login_email');
  const email = (emailInput ? emailInput.value : '').trim().toLowerCase();
  if (!email || !email.includes('@')) {
    alert("Please enter your registered email address first.");
    if (emailInput) emailInput.focus();
    return;
  }
  try {
    const res = await fetch('/api/auth/send-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    const otpSection = document.getElementById('loginOtpSection');
    if (otpSection) {
      otpSection.style.display = 'block';
      const otpInput = document.getElementById('login_otp');
      if (otpInput) otpInput.focus();
    }
    alert(`Verification OTP sent to ${email}. Please check your inbox.`);
  } catch (e) {
    alert("Failed to send OTP. Please check your network connection.");
  }
}

async function handleVerifyLoginOtp() {
  const email = (document.getElementById('login_email') ? document.getElementById('login_email').value : '').trim().toLowerCase();
  const otpInput = document.getElementById('login_otp');
  const otp = (otpInput ? otpInput.value : '').trim();
  if (!otp || otp.length < 4) {
    alert("Please enter the verification code sent to your email.");
    if (otpInput) otpInput.focus();
    return;
  }
  try {
    const res = await fetch('/api/auth/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp })
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
      return;
    }
    if (data.token) {
      state.token = data.token;
      state.user = data.user;
      localStorage.setItem('f4f_token', data.token);
      closeModal('loginModal');
      renderAuthenticatedUI(data);
    } else {
      alert("Email verified successfully! You can now log in.");
    }
  } catch (e) {
    alert("Verification failed. Please check your network connection.");
  }
}


// Login
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
  if (document.getElementById('dashboardWelcome')) document.getElementById('dashboardWelcome').innerText = `Welcome back, ${name}`;
  if (document.getElementById('portalUserName')) document.getElementById('portalUserName').innerText = name;
  if (document.getElementById('accName')) document.getElementById('accName').innerText = name;
  if (data.profile && data.profile.business_name) {
    const roleText = `${data.profile.designation || 'Founder'} • ${data.profile.business_name}`;
    if (document.getElementById('portalUserRole')) document.getElementById('portalUserRole').innerText = roleText;
    if (document.getElementById('accRole')) document.getElementById('accRole').innerText = roleText;
  }
  const initials = (name || 'Member').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() || 'ME';
  if (document.getElementById('portalUserAvatar')) document.getElementById('portalUserAvatar').innerText = initials;
  if (document.getElementById('accAvatar')) document.getElementById('accAvatar').innerText = initials;

  const isAdmin = data.user && (data.user.role === 'ADMIN' || data.user.role === 'SUPER_ADMIN');
  if (document.getElementById('adminTabLink')) document.getElementById('adminTabLink').style.display = isAdmin ? 'flex' : 'none';
  if (document.getElementById('navAdminBtn')) document.getElementById('navAdminBtn').style.display = isAdmin ? 'inline-flex' : 'none';

  loadDashboardTab();

  // Pre-fetch secondary tabs during browser idle to make subsequent clicks instant
  if (typeof requestIdleCallback === 'function') {
    requestIdleCallback(() => {
      loadDirectoryTab();
      loadEventsTab();
    }, { timeout: 2500 });
  } else {
    setTimeout(() => {
      loadDirectoryTab();
      loadEventsTab();
    }, 800);
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

  // Support both canonical tab names and Stitch slug aliases
  const aliasMap = {
    'discover-founders': 'directory',
    'needs-and-wants': 'needs',
    'leads-and-crm': 'crm',
    'one-on-one-meetings': 'meetings',
    'founders-chat': 'chat',
    'events-and-experiences': 'events',
    'account-and-billing': 'account'
  };
  const canonicalTab = aliasMap[tabName] || tabName;

  document.querySelectorAll('.portal-tab').forEach(t => t.style.display = 'none');
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));

  // Update top interactive view switcher tab buttons if present
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('bg-primary-container', 'text-on-primary', 'shadow-sm', 'font-semibold');
    btn.classList.add('text-on-surface-variant');
  });
  const ribbonBtn = document.querySelector(`.tab-btn[data-tab-target="${canonicalTab}"]`) ||
                    document.querySelector(`.tab-btn[data-tab-target="${tabName}"]`);
  if (ribbonBtn) {
    ribbonBtn.classList.remove('text-on-surface-variant');
    ribbonBtn.classList.add('bg-primary-container', 'text-on-primary', 'shadow-sm', 'font-semibold');
  }

  const tab = document.getElementById(`tab-${canonicalTab}`);
  if (tab) {
    tab.style.display = 'block';
  } else {
    console.error("Portal tab not found:", canonicalTab);
  }

  let activeEl = el;
  if (!activeEl) {
    activeEl = Array.from(document.querySelectorAll('.sidebar-item')).find(item => 
      item.getAttribute('onclick')?.includes(`'${canonicalTab}'`) ||
      item.getAttribute('onclick')?.includes(`'${tabName}'`)
    );
  }
  if (activeEl) {
    activeEl.classList.add('active');
    if (window.innerWidth < 992) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (canonicalTab === 'admin') loadAdminTab();
  else if (canonicalTab === 'dashboard') loadDashboardTab();
  else if (canonicalTab === 'directory') loadDirectoryTab();
  else if (canonicalTab === 'needs') loadNeedsTab();
  else if (canonicalTab === 'crm') loadCRMTab();
  else if (canonicalTab === 'attendance') loadAttendanceTab();
  else if (canonicalTab === 'meetings') loadMeetingsTab();
  else if (canonicalTab === 'chat') loadChatMessages();
  else if (canonicalTab === 'events') loadEventsTab();
  else if (canonicalTab === 'challenge') loadChallengeTab();
}

// Dashboard Tab Loader with SWR Instant Rendering & Consolidated Single-Roundtrip API
function renderDashboardMetrics(data) {
  if (!data) return;
  if (data.crm) {
    if (document.getElementById('dashBizGenerated')) {
      document.getElementById('dashBizGenerated').innerText = `${data.crm.referrals_received || 0} Deals`;
    }
    if (document.getElementById('dashLeadsWon')) {
      document.getElementById('dashLeadsWon').innerText = data.crm.leads_won || 0;
    }
  }
  if (data.attendance && document.getElementById('dashAttendanceRate')) {
    document.getElementById('dashAttendanceRate').innerHTML = `${data.attendance.attendance_rate}% Event Presence <span class="badge-pulse-green" style="font-size: 0.78rem; background: #A7F3D0; color: #064E3B; padding: 2px 8px; border-radius: 12px; font-weight: 800;">Streak: ${data.attendance.attendance_streak} Gatherings</span>`;
  }
  if (data.meetings && document.getElementById('dashMeetingsStat')) {
    document.getElementById('dashMeetingsStat').innerText = `${data.meetings.this_month} 1-to-1 Founder Meetings logged in ${data.meetings.current_month_name}`;
  }
}

async function loadDashboardTab() {
  if (!state.token) return;

  // 1. Instant SWR render from sessionStorage (0ms latency!)
  try {
    const cached = sessionStorage.getItem('f4f_dash_cache');
    if (cached) {
      renderDashboardMetrics(JSON.parse(cached));
    }
  } catch (e) {}

  // 2. High-speed single consolidated endpoint with parallel fallback
  try {
    const res = await fetch('/api/portal/dashboard-summary', { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (res.ok) {
      const data = await res.json();
      renderDashboardMetrics(data);
      try { sessionStorage.setItem('f4f_dash_cache', JSON.stringify(data)); } catch (e) {}
      return;
    }
  } catch (e) {}

  // Fallback: Parallel Promise.allSettled across individual endpoints
  try {
    const [crmRes, attRes, meetRes] = await Promise.allSettled([
      fetch('/api/crm/metrics', { headers: { 'Authorization': `Bearer ${state.token}` } }).then(r => r.json()),
      fetch('/api/attendance/summary', { headers: { 'Authorization': `Bearer ${state.token}` } }).then(r => r.json()),
      fetch('/api/founder-meetings', { headers: { 'Authorization': `Bearer ${state.token}` } }).then(r => r.json())
    ]);

    const combined = {
      crm: crmRes.status === 'fulfilled' && !crmRes.value.error ? crmRes.value : {},
      attendance: attRes.status === 'fulfilled' && !attRes.value.error ? attRes.value : {},
      meetings: meetRes.status === 'fulfilled' && meetRes.value.stats ? meetRes.value.stats : {}
    };
    renderDashboardMetrics(combined);
    try { sessionStorage.setItem('f4f_dash_cache', JSON.stringify(combined)); } catch (e) {}
  } catch (err) {
    console.error("Dashboard metrics error:", err);
  }
}

// Directory Loader with SWR Cache
let _cachedDirectoryMembers = null;
async function loadDirectoryTab() {
  if (_cachedDirectoryMembers) {
    renderMembers(_cachedDirectoryMembers);
  }
  try {
    const res = await fetch('/api/members', { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (res.ok) {
      const data = await res.json();
      _cachedDirectoryMembers = data.members || [];
      renderMembers(_cachedDirectoryMembers);
    }
  } catch (err) {
    console.error("Directory fetch error:", err);
  }
}

function filterDirectory() {
  const query = document.getElementById('dirSearchInput').value.toLowerCase();
  const stage = document.getElementById('dirStageFilter').value;
  fetch(`/api/members?q=${encodeURIComponent(query)}&stage=${encodeURIComponent(stage)}`, { headers: { 'Authorization': `Bearer ${state.token}` } })
    .then(r => r.json())
    .then(d => {
      _cachedDirectoryMembers = d.members || [];
      renderMembers(_cachedDirectoryMembers);
    })
    .catch(() => {});
}

function renderMembers(members) {
  const container = document.getElementById('directoryContainer');
  if (!container) return;
  container.innerHTML = '';
  members.forEach(m => {
    const card = document.createElement('div');
    card.className = 'card';
    const avatarSrc = (m.profile_photo && !m.profile_photo.includes('unsplash.com')) ? m.profile_photo : getInitialsAvatar(m.full_name);
    card.innerHTML = `
      <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
        <img src="${avatarSrc}" alt="${m.full_name || 'Member'}" loading="lazy" decoding="async" width="52" height="52" style="width: 52px; height: 52px; border-radius: 12px; border: 1px solid var(--mint-200); object-fit: cover;">
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

// Needs Loader with SWR Cache
let _cachedNeedsList = null;
function renderNeedsCards(needs) {
  const container = document.getElementById('needsContainer');
  if (!container) return;
  container.innerHTML = '';
  (needs || []).forEach(n => {
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

async function loadNeedsTab() {
  if (_cachedNeedsList) {
    renderNeedsCards(_cachedNeedsList);
  }
  try {
    const res = await fetch('/api/needs', { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (res.ok) {
      const data = await res.json();
      _cachedNeedsList = data.needs || [];
      renderNeedsCards(_cachedNeedsList);
    }
  } catch (err) {
    console.error("Needs fetch error:", err);
  }
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
let _cachedCRMData = null;

function renderCRMLeads(leads) {
  const list = document.getElementById('leadsList');
  if (!list) return;
  list.innerHTML = '';

  (leads || []).forEach(l => {
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

async function loadCRMTab() {
  if (_cachedCRMData) {
    renderCRMLeads(_cachedCRMData.leads || []);
  }
  try {
    const res = await fetch('/api/crm/metrics', { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (res.ok) {
      const data = await res.json();
      _cachedCRMData = data;
      renderCRMLeads(data.leads || []);
    }
  } catch (err) {
    console.error("CRM fetch error:", err);
  }
}

// Events Loader
let _cachedEventsList = null;

function renderEventsTabList(events) {
  const container = document.getElementById('eventsContainer');
  if (!container) return;
  container.innerHTML = '';

  (events || []).forEach(evt => {
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

async function loadEventsTab() {
  if (_cachedEventsList) {
    renderEventsTabList(_cachedEventsList);
  }
  try {
    const res = await fetch('/api/events', { headers: { 'Authorization': `Bearer ${state.token}` } });
    if (res.ok) {
      const data = await res.json();
      state.eventsList = data.events || [];
      _cachedEventsList = state.eventsList;
      renderEventsTabList(_cachedEventsList);
    }
  } catch (err) {
    console.error("Events fetch error:", err);
  }
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

// Admin CMS Loader (Parallel Execution of Overview, Logs, Settings, and Photos)
async function loadAdminTab() {
  try {
    const authHeaders = { 'Authorization': `Bearer ${state.token}` };
    const [overviewRes, auditRes, setRes, photosRes] = await Promise.allSettled([
      fetch('/api/admin/overview', { headers: authHeaders }),
      fetch('/api/admin/audit-logs', { headers: authHeaders }),
      fetch('/api/admin/settings', { headers: authHeaders }),
      fetch('/api/meeting-photos')
    ]);

    // 1. Process Overview & Recent Applications (Stitch Integrated)
    if (overviewRes.status === 'fulfilled' && overviewRes.value.ok) {
      const data = await overviewRes.value.json();
      if (data.metrics) {
        const totalEl = document.getElementById('statTotalMembers');
        const mrrEl = document.getElementById('statActiveMrr');
        const appsEl = document.getElementById('statPendingApps');
        if (totalEl) totalEl.textContent = data.metrics.total_members ?? 0;
        if (mrrEl) mrrEl.textContent = `₹${(data.metrics.mrr || 0).toLocaleString('en-IN')}`;
        if (appsEl) appsEl.textContent = data.metrics.new_applications ?? 0;
      }

      state.adminApplications = data.recent_applications || [];
      renderAdminApplications(state.adminApplications);
    }

    // 2. Process Audit Logs (Stitch Integrated)
    if (auditRes.status === 'fulfilled' && auditRes.value.ok) {
      const auditData = await auditRes.value.json();
      renderAdminAuditLogs(auditData.audit_logs || []);
    }

    // 3. Process Site Settings Customizer
    if (setRes.status === 'fulfilled' && setRes.value.ok) {
      const setData = await setRes.value.json();
      if (setData.settings) {
        setData.settings.forEach(s => {
          const input = document.getElementById(`set_${s.key_name}`);
          if (input) input.value = s.key_value || '';
          const prev = document.getElementById(`prev_${s.key_name}`);
          if (prev && s.key_value) prev.src = s.key_value;
        });
      }
    }

    // 4. Process Admin Meeting Photos Gallery (16:9)
    if (photosRes.status === 'fulfilled' && photosRes.value.ok) {
      const photosData = await photosRes.value.json();
      if (photosData.photos) {
        renderAdminMeetingPhotosList(photosData.photos);
      }
    }
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

function renderAttendanceData(data) {
  if (!data) return;

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
  if (document.getElementById('attStandingTier')) document.getElementById('attStandingTier').innerHTML = `<svg class="icon-inline" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> ${data.accountability_tier}`;
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
}

async function loadAttendanceTab(selectedMonth) {
  if (currentAttendanceData && (!selectedMonth || selectedMonth === currentAttendanceData.selected_month)) {
    renderAttendanceData(currentAttendanceData);
  }
  try {
    const url = selectedMonth ? `/api/attendance/summary?month=${encodeURIComponent(selectedMonth)}` : '/api/attendance/summary';
    const res = await fetch(url, { headers: { 'Authorization': `Bearer ${state.token}` } });
    const data = await res.json();
    if (data.error) {
      console.error("Attendance fetch error:", data.error);
      return;
    }
    currentAttendanceData = data;
    renderAttendanceData(data);
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
    currentAttendanceData = null;
    loadAttendanceTab(document.getElementById('attendanceMonthSelect')?.value);
    loadDashboardTab();
  } catch (err) {
    alert("Network error confirming presence. Please try again.");
  }
}

// ==========================================================================
// 1-TO-1 FOUNDER MEETINGS TRACKER
// ==========================================================================
let _cachedMeetingsData = null;

function renderMeetingsData(data) {
  if (!data) return;

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

    const partnerAvatarSrc = (m.partner_avatar && !m.partner_avatar.includes('unsplash.com')) ? m.partner_avatar : getInitialsAvatar(m.partner_name);
    return `
      <div class="meeting-item-card">
        <div style="display: flex; gap: 14px; align-items: flex-start; flex: 2; min-width: 280px;">
          <img src="${partnerAvatarSrc}" alt="${m.partner_name || 'Member'}" loading="lazy" decoding="async" width="52" height="52" style="width: 52px; height: 52px; border-radius: 50%; object-fit: cover; border: 2px solid var(--emerald-400); box-shadow: 0 4px 10px rgba(4,120,87,0.15);">
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
}

async function loadMeetingsTab() {
  if (_cachedMeetingsData) {
    renderMeetingsData(_cachedMeetingsData);
  }
  try {
    const res = await fetch('/api/founder-meetings', { headers: { 'Authorization': `Bearer ${state.token}` } });
    const data = await res.json();
    if (data.error) return;
    _cachedMeetingsData = data;
    renderMeetingsData(data);
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
    _cachedMeetingsData = null;
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
  const section = document.getElementById('meetingPhotosSection');
  if (!photos || photos.length === 0) {
    if (section) section.style.display = 'none';
    return;
  }
  if (section) section.style.display = 'block';
  if (!track) return;
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
  if (prev) prev.src = '/assets/hero_banner.jpg';
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
    container.innerHTML = '<p class="col-span-1 sm:col-span-2 md:col-span-3 text-text-tertiary text-center py-8">No meeting photos added yet. Use the quick add form above to publish photography to the continuous 16:9 marquee slider.</p>';
    return;
  }
  container.innerHTML = photos.map(p => `
    <div class="bg-surface-card rounded-lg overflow-hidden shadow-sm flex flex-col group border border-hairline">
      <div class="aspect-video w-full relative overflow-hidden bg-surface-container">
        <img class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" src="${escapeHtml(p.image_url)}" alt="${escapeHtml(p.title)}" loading="lazy" decoding="async">
        <div class="absolute inset-0 bg-gradient-to-t from-primary/80 via-transparent to-transparent"></div>
        <span class="absolute top-3 left-3 bg-primary-container/90 backdrop-blur-sm text-on-primary font-label-caps text-label-caps px-2 py-0.5 rounded">
          ${escapeHtml(p.tag || 'Curated Gathering')}
        </span>
        <div class="absolute bottom-3 left-3 right-3 text-on-primary">
          <span class="font-label-md text-label-md font-semibold block truncate">${escapeHtml(p.title)}</span>
          <span class="font-body-sm text-[12px] opacity-80 block truncate">${escapeHtml(p.caption || '16:9 Slider Active')}</span>
        </div>
      </div>
      <div class="p-3 flex items-center justify-between bg-surface-card">
        <span class="text-text-tertiary text-[12px]">Continuous Slider Active</span>
        <button type="button" class="w-8 h-8 rounded flex items-center justify-center text-error hover:bg-error-container hover:text-on-error-container transition-colors cursor-pointer" title="Delete from slider" onclick="handleDeleteMeetingPhoto('${p.id}')">
          <span class="material-symbols-outlined text-[18px]">delete</span>
        </button>
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
      const senderName = m.full_name || m.email || 'Fellow Founder';
      const avatar = (m.profile_photo && !m.profile_photo.includes('unsplash.com')) ? m.profile_photo : getInitialsAvatar(senderName);
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



// ==========================================
// STITCH ADMIN CONSOLE DYNAMIC RENDER & FILTERS
// ==========================================
let currentAppFilter = 'all';
let currentAppSearch = '';

function renderAdminApplications(apps) {
  const tbody = document.getElementById('applicationsTableBody');
  const countBadge = document.getElementById('appQueueCountBadge');
  const footerCount = document.getElementById('appTableFooterCount');
  if (countBadge) {
    countBadge.textContent = `${apps.length} in Queue`;
  }
  if (footerCount) {
    footerCount.textContent = `Showing ${apps.length} application${apps.length === 1 ? '' : 's'}`;
  }
  if (!tbody) return;

  if (!apps || apps.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="py-12 text-center text-text-tertiary">No applications match the current filter.</td></tr>`;
    return;
  }

  tbody.innerHTML = apps.map(app => {
    const inviteLink = app.invitation_token ? `${window.location.origin}/#activate?token=${app.invitation_token}` : '';
    const initials = (app.full_name || 'Founder').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();

    // Status pill styles matching Stitch theme
    let statusPill = '';
    if (app.status === 'APPROVED' || app.status === 'INVITED' || app.status === 'CONVERTED') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary-fixed text-on-primary-fixed font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-emerald-deep"></span> ${app.status}</span>`;
    } else if (app.status === 'UNDER_REVIEW') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-secondary"></span> REVIEW</span>`;
    } else if (app.status === 'WAITLISTED') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container-high text-text-secondary font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-outline"></span> WAITLIST</span>`;
    } else if (app.status === 'DECLINED') {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-error-container text-on-error-container font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-error"></span> DECLINED</span>`;
    } else {
      statusPill = `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-subtle text-on-surface-variant font-label-caps text-label-caps"><span class="w-1.5 h-1.5 rounded-full bg-secondary"></span> PENDING</span>`;
    }

    return `
      <tr class="hover:bg-surface-subtle/50 transition-colors">
        <td class="py-4 px-space-md">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-primary text-on-primary font-semibold flex items-center justify-center font-label-md text-label-md flex-shrink-0">
              ${initials}
            </div>
            <div class="flex flex-col">
              <span class="font-label-md text-label-md text-text-primary font-semibold">${escapeHtml(app.full_name)}</span>
              <span class="text-text-tertiary text-[12px] flex items-center gap-1">
                <span class="material-symbols-outlined text-[13px]">location_on</span> ${escapeHtml(app.city || 'Pan India')}
              </span>
            </div>
          </div>
        </td>
        <td class="py-4 px-space-md">
          <div class="flex flex-col gap-1 items-start">
            <span class="inline-flex items-center px-2 py-0.5 rounded bg-surface-subtle text-primary font-label-caps text-label-caps">${escapeHtml(app.applicant_type || 'Founder')}</span>
            <span class="text-text-tertiary text-[11px]">${escapeHtml(app.designation || 'Founding Team')}</span>
          </div>
        </td>
        <td class="py-4 px-space-md">
          <div class="flex flex-col">
            <span class="font-medium text-text-primary">${escapeHtml(app.business_name || 'Private Venture')}</span>
            <span class="text-text-secondary text-[12px]">${escapeHtml(app.business_model_category || 'Product Based')}</span>
          </div>
        </td>
        <td class="py-4 px-space-md">
          <div class="flex flex-col text-[12px]">
            <span class="text-primary font-mono select-all">${escapeHtml(app.email)}</span>
            <div class="flex items-center gap-1 text-text-secondary mt-0.5">
              <span class="font-mono">${escapeHtml(app.phone)}</span>
              <span class="material-symbols-outlined text-[13px] text-secondary" title="Verified phone">verified</span>
            </div>
          </div>
        </td>
        <td class="py-4 px-space-md">
          ${statusPill}
        </td>
        <td class="py-4 px-space-md">
          <select class="h-9 px-2 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer border border-hairline" onchange="updateAppStatus('${app.id}', this.value)">
            <option value="SUBMITTED" ${app.status === 'SUBMITTED' ? 'selected' : ''}>SUBMITTED</option>
            <option value="UNDER_REVIEW" ${app.status === 'UNDER_REVIEW' ? 'selected' : ''}>UNDER_REVIEW</option>
            <option value="APPROVED" ${app.status === 'APPROVED' ? 'selected' : ''}>APPROVED</option>
            <option value="INVITED" ${app.status === 'INVITED' ? 'selected' : ''}>INVITED</option>
            <option value="WAITLISTED" ${app.status === 'WAITLISTED' ? 'selected' : ''}>WAITLISTED</option>
            <option value="DECLINED" ${app.status === 'DECLINED' ? 'selected' : ''}>DECLINED</option>
          </select>
        </td>
        <td class="py-4 px-space-md text-right">
          <div class="flex items-center justify-end gap-2">
            <button class="h-9 px-3 rounded bg-surface-subtle hover:bg-surface-container font-label-md text-label-md text-on-surface flex items-center gap-1.5 transition-colors cursor-pointer" onclick="openViewApplicationModal('${app.id}')">
              <span class="material-symbols-outlined text-[16px]">visibility</span>
              <span>Inspect</span>
            </button>
            ${inviteLink ? `
              <button class="h-9 px-3 rounded bg-surface-subtle hover:bg-surface-container font-label-md text-label-md text-primary flex items-center gap-1.5 transition-colors cursor-pointer" onclick="navigator.clipboard.writeText('${inviteLink}'); alert('Invitation Token Link Copied:\n${inviteLink}');">
                <span class="material-symbols-outlined text-[16px]">content_copy</span>
                <span>Copy Token</span>
              </button>
            ` : `
              <button class="h-9 px-3 rounded bg-primary-container hover:bg-emerald-deep font-label-md text-label-md text-on-primary flex items-center gap-1.5 shadow-sm transition-all cursor-pointer" onclick="updateAppStatus('${app.id}', 'APPROVED')">
                <span class="material-symbols-outlined text-[16px]">send</span>
                <span>Approve</span>
              </button>
            `}
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function renderAdminAuditLogs(logs) {
  const tbody = document.getElementById('auditLogsTableBody');
  if (!tbody) return;
  if (!logs || logs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="py-8 text-center text-text-tertiary">No audit logs recorded yet.</td></tr>`;
    return;
  }
  tbody.innerHTML = logs.map(log => {
    let actionBadge = `<span class="bg-surface-subtle text-primary px-2 py-0.5 rounded text-[11px] font-bold">${escapeHtml(log.action_type || 'AUDIT_LOG')}</span>`;
    if ((log.action_type || '').includes('APPROV') || (log.action_type || '').includes('CREATE')) {
      actionBadge = `<span class="bg-primary-fixed text-on-primary-fixed px-2 py-0.5 rounded text-[11px] font-bold">${escapeHtml(log.action_type)}</span>`;
    } else if ((log.action_type || '').includes('TOKEN') || (log.action_type || '').includes('INVIT')) {
      actionBadge = `<span class="bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded text-[11px] font-bold">${escapeHtml(log.action_type)}</span>`;
    }

    return `
      <tr class="hover:bg-surface-subtle/50 transition-colors">
        <td class="py-3.5 px-space-md text-text-tertiary">${escapeHtml(log.created_at || '')}</td>
        <td class="py-3.5 px-space-md">${actionBadge}</td>
        <td class="py-3.5 px-space-md text-text-primary font-mono text-[12px]">${escapeHtml(log.user_id || 'Master Admin')}</td>
        <td class="py-3.5 px-space-md text-text-secondary">${escapeHtml(log.entity_type || 'SYSTEM')} ${log.entity_id ? `(#${escapeHtml(String(log.entity_id).slice(0,8))})` : ''}</td>
        <td class="py-3.5 px-space-md text-right text-text-tertiary font-mono">${escapeHtml(log.ip_address || '127.0.0.1')}</td>
      </tr>
    `;
  }).join('');
}

function filterApplications(filterStatus, clickedTab) {
  currentAppFilter = filterStatus;
  const filterTabs = document.querySelectorAll('.filter-tab');
  filterTabs.forEach(t => {
    t.classList.remove('bg-surface-card', 'text-primary', 'shadow-sm');
    t.classList.add('text-text-secondary');
  });
  if (clickedTab) {
    clickedTab.classList.add('bg-surface-card', 'text-primary', 'shadow-sm');
    clickedTab.classList.remove('text-text-secondary');
  }
  applyAdminAppFilters();
}

function handleAppSearch(query) {
  currentAppSearch = (query || '').toLowerCase().trim();
  applyAdminAppFilters();
}

function handleMasterAdminSearch(query) {
  handleAppSearch(query);
  const searchInput = document.getElementById('appSearch');
  if (searchInput) searchInput.value = query;
}

function applyAdminAppFilters() {
  const allApps = state.adminApplications || [];
  const filtered = allApps.filter(app => {
    // Status Filter
    if (currentAppFilter !== 'all') {
      if (currentAppFilter === 'SUBMITTED' && app.status !== 'SUBMITTED') return false;
      if (currentAppFilter === 'UNDER_REVIEW' && app.status !== 'UNDER_REVIEW') return false;
      if (currentAppFilter === 'APPROVED' && (app.status !== 'APPROVED' && app.status !== 'INVITED' && app.status !== 'CONVERTED')) return false;
      if (currentAppFilter === 'WAITLISTED' && app.status !== 'WAITLISTED') return false;
    }
    // Search Text
    if (currentAppSearch) {
      const q = currentAppSearch;
      const match = (app.full_name || '').toLowerCase().includes(q) ||
                    (app.business_name || '').toLowerCase().includes(q) ||
                    (app.email || '').toLowerCase().includes(q) ||
                    (app.city || '').toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });
  renderAdminApplications(filtered);
}

// Global Export Dropdown Toggle Listener
document.addEventListener('click', (e) => {
  const exportBtn = document.getElementById('exportBtn');
  const exportMenu = document.getElementById('exportMenu');
  if (!exportBtn || !exportMenu) return;
  if (exportBtn.contains(e.target)) {
    e.stopPropagation();
    exportMenu.classList.toggle('hidden');
  } else if (!exportMenu.contains(e.target)) {
    exportMenu.classList.add('hidden');
  }
});
