# scripts/update_stitch_home.py
import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate boundaries
nav_start = content.find('<!-- TOP HEADER')
portal_start = content.find('<!-- AUTHENTICATED MEMBER PORTAL & DASHBOARD -->')

if nav_start == -1 or portal_start == -1:
    raise ValueError("Could not find section boundaries in public/index.html")

new_header_and_public_page = '''<!-- TOP HEADER (Executive Guild Stitch Design) -->
  <header class="fixed top-0 left-0 w-full z-50 bg-surface-container-lowest/80 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] border-b border-card-border/60 transition-all" id="mainNavbar">
    <div class="h-20 max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop flex items-center justify-between gap-gutter">
      <!-- Logo -->
      <div class="flex items-center gap-space-md">
        <a class="flex items-center gap-space-sm group flex-shrink-0" data-path="home" href="#">
          <img alt="Founder for Founder Logo" class="w-8 h-8 rounded-full object-cover shadow-[0_2px_8px_rgba(6,78,59,0.12)]" id="navLogo" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAvBj1Udgkn75M25pSizwn82V3qhdlhpbv6BPHdZYyuByLQ_H6OGYrCOEUJgYKFsgD-F3Hz1TkcZruQOp-kdPe-E49aisCSJ7G3KTpdThqsRuelQzWsQ-cPFfBgr5VU4cll2CBeLS-VzdlXWyJ0_8fRpznsQIQesKlKIr-W3MXvvJdM185dtVVUJEtdM4k_Mmk3djDiC5iWiC1AaZHjd5R3DrePYjfcJXPwBpFUNysbL-m5xNuV4Koaav-HuPVZKx44uRQ" width="32" height="32" decoding="async">
          <div class="flex flex-col">
            <div class="flex items-center gap-1.5">
              <span class="font-title-md text-title-md text-primary tracking-tight font-bold whitespace-nowrap">Founder for Founder</span>
              <span class="text-xs font-serif font-bold text-secondary">F4F</span>
            </div>
            <span class="font-label-status text-label-status uppercase text-on-surface-variant tracking-wider whitespace-nowrap" id="navSubtitle">by snalts.co</span>
          </div>
        </a>
      </div>

      <!-- Desktop Nav -->
      <nav class="hidden md:flex items-center gap-gutter" data-active-classes="text-primary font-title-md" id="publicNav">
        <a class="font-body-md text-body-md text-primary font-semibold hover:text-primary transition-colors" data-path="home" href="#">Home</a>
        <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" data-path="about" href="#about">About</a>
        <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" data-path="experiences" href="#experiences">Experiences</a>
        <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="#needs-wants">Needs &amp; Wants</a>
        <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="#community">Community</a>
        <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="#faq">FAQ</a>
      </nav>

      <!-- Right CTAs -->
      <div class="flex items-center gap-space-md flex-shrink-0">
        <div class="hidden sm:flex items-center gap-3" id="publicNavBtns">
          <button class="font-title-md text-title-md text-on-surface-variant hover:text-primary transition-colors px-3 py-1.5" onclick="openLoginModal()" title="Member Login">Login</button>
          <button class="inline-flex items-center gap-space-xs px-space-lg py-space-sm bg-primary-container text-on-primary font-title-md text-title-md rounded-[6px] shadow-[0_4px_16px_rgba(6,78,59,0.18)] hover:bg-primary hover:text-on-primary transition-all whitespace-nowrap" onclick="openShowInterestModal()">
            <span>Show Interest</span>
            <span class="material-symbols-outlined text-lg leading-none">arrow_forward</span>
          </button>
        </div>

        <!-- Mobile Quick CTA -->
        <button class="sm:hidden inline-flex items-center gap-1 bg-primary-container hover:bg-primary text-white text-[12px] font-medium px-3 py-1.5 rounded-[6px] whitespace-nowrap" onclick="openShowInterestModal()">
          <span>Show Interest</span>
          <span class="material-symbols-outlined text-sm leading-none">arrow_forward</span>
        </button>

        <!-- Authenticated Portal Nav Controls -->
        <div id="authNavControls" style="display: none; align-items: center; gap: 0.85rem;">
          <span id="navUserName" class="text-[13px] font-semibold text-primary hidden sm:inline-block">Welcome, Member</span>
          <button class="inline-flex items-center gap-1 text-[12.5px] font-medium border border-card-border px-3 py-1.5 rounded-[6px] hover:bg-surface-subtle" id="navAdminBtn" style="display: none;" onclick="switchPortalTab('admin');">
            <span class="material-symbols-outlined text-[16px]">admin_panel_settings</span> Admin CMS
          </button>
          <button class="inline-flex items-center gap-1 text-[12.5px] font-medium bg-primary-container text-white px-3.5 py-1.5 rounded-[6px] hover:bg-primary" onclick="switchPortalTab('dashboard');">
            <span class="material-symbols-outlined text-[16px]">dashboard</span> Member Portal
          </button>
          <button class="inline-flex items-center text-[12.5px] font-medium text-text-muted hover:text-text-main px-2 py-1" onclick="handleLogout();">
            Logout
          </button>
        </div>

        <!-- Mobile Hamburger Button -->
        <button class="mobile-nav-toggle md:hidden p-2 rounded-[6px] hover:bg-surface-subtle text-text-main transition-colors flex items-center justify-center" id="mobileNavToggle" aria-label="Toggle navigation menu" aria-expanded="false" onclick="toggleMobileNav()">
          <span class="hamburger-bar"></span>
          <span class="hamburger-bar"></span>
          <span class="hamburger-bar"></span>
        </button>
      </div>
    </div>

    <!-- Mobile Drawer Backdrop Overlay -->
    <div class="nav-drawer-backdrop" id="navDrawerBackdrop" onclick="closeMobileNav()"></div>

    <!-- Navigation Drawer Wrapper (Mobile Slide Drawer) -->
    <div class="nav-drawer md:hidden" id="navDrawer">
      <ul class="flex flex-col gap-4 p-6 bg-white border-b border-card-border">
        <li><a href="#" class="block text-[15px] font-medium text-text-main" onclick="closeMobileNav()">Home</a></li>
        <li><a href="#about" class="block text-[15px] font-medium text-text-muted hover:text-text-main" onclick="closeMobileNav()">About</a></li>
        <li><a href="#experiences" class="block text-[15px] font-medium text-text-muted hover:text-text-main" onclick="closeMobileNav()">Experiences</a></li>
        <li><a href="#needs-wants" class="block text-[15px] font-medium text-text-muted hover:text-text-main" onclick="closeMobileNav()">Needs &amp; Wants</a></li>
        <li><a href="#community" class="block text-[15px] font-medium text-text-muted hover:text-text-main" onclick="closeMobileNav()">Community</a></li>
        <li><a href="#faq" class="block text-[15px] font-medium text-text-muted hover:text-text-main" onclick="closeMobileNav()">FAQ</a></li>
        <li class="pt-4 border-t border-card-border flex flex-col gap-2">
          <button class="w-full py-2.5 rounded-[6px] bg-primary-container text-white text-[13.5px] font-medium" onclick="openShowInterestModal(); closeMobileNav();">Show Interest →</button>
          <button class="w-full py-2.5 rounded-[6px] border border-card-border text-text-main text-[13.5px] font-medium" onclick="openLoginModal(); closeMobileNav();">Member Login</button>
        </li>
      </ul>
    </div>
  </header>

  <!-- PUBLIC HOMEPAGE CONTENT -->
  <div id="publicPage">
    <main class="w-full pt-20 bg-surface-container-lowest min-h-screen">
      <div class="flex flex-col w-full">

        <!-- HERO SECTION (Stitch Screen b12ad31e) -->
        <section class="relative w-full overflow-hidden bg-surface-container-lowest border-b border-card-border/40" id="home">
          <!-- Subtle architectural glow effects -->
          <div class="absolute -top-32 right-1/4 w-[500px] h-[500px] bg-secondary-fixed/20 rounded-full blur-3xl pointer-events-none -z-10"></div>
          <div class="absolute top-1/2 left-0 w-96 h-96 bg-primary-fixed/30 rounded-full blur-3xl pointer-events-none -z-10"></div>

          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop pt-10 pb-16 lg:pt-16 lg:pb-24">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
              
              <!-- Left Column Content -->
              <div class="lg:col-span-6 flex flex-col items-center lg:items-start text-center lg:text-left gap-space-md">
                <div class="hero-pill-badge inline-flex items-center gap-space-xs px-3 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-status text-label-status tracking-widest uppercase w-fit shadow-sm">
                  <span class="w-2 h-2 rounded-full bg-secondary inline-block animate-pulse"></span>
                  <span id="heroBadge">CURATED FOUNDER NETWORK • BY APPLICATION ONLY</span>
                </div>

                <h1 class="font-headline-hero text-headline-hero text-primary tracking-tight font-bold leading-tight" id="heroTitle">
                  Beyond Networking.<br class="hidden sm:inline">
                  <span class="text-secondary">Into Real Connections.</span>
                </h1>

                <p class="font-body-lg text-body-lg text-on-surface-variant max-w-xl leading-relaxed" id="heroSubtitle">
                  Founder for Founder brings ambitious entrepreneurs, business owners, and professionals into one curated network. Share experiences, explore opportunities, exchange trusted referrals, and build lasting business relationships across India.
                </p>

                <div class="flex items-center justify-center lg:justify-start gap-space-sm p-space-sm px-space-md bg-surface-container-low rounded-xl w-fit shadow-sm my-1">
                  <span class="material-symbols-outlined text-secondary text-lg">spa</span>
                  <p class="font-title-md text-title-md text-primary font-semibold">“Business brings us together. Experiences bring us closer.”</p>
                </div>

                <div class="flex flex-wrap items-center justify-center lg:justify-start gap-space-md pt-space-xs">
                  <button class="inline-flex items-center justify-center gap-space-xs px-7 py-3 bg-primary-container text-on-primary font-title-md text-title-md rounded-[6px] shadow-[0_6px_20px_rgba(6,78,59,0.24)] hover:bg-secondary hover:text-on-primary transition-all duration-200" onclick="openShowInterestModal()">
                    <span>Show Interest</span>
                    <span class="material-symbols-outlined text-lg">arrow_forward</span>
                  </button>
                  <a class="inline-flex items-center justify-center gap-space-xs px-7 py-3 bg-surface-container-lowest text-primary font-title-md text-title-md rounded-[6px] border border-card-border shadow-sm hover:bg-surface-container transition-all duration-200" href="#experiences">
                    <span>Explore Experiences</span>
                  </a>
                </div>

                <!-- Metrics Strip with vertical divider -->
                <div class="flex items-center gap-8 mt-6 pt-6 border-t border-card-border/70 max-w-sm w-full justify-center lg:justify-start">
                  <div class="flex flex-col text-left">
                    <span class="font-headline-md text-2xl lg:text-3xl font-bold text-primary tracking-tight" id="counterMembers">1,528+</span>
                    <span class="font-label-md text-label-md text-on-surface-variant mt-0.5 tracking-wide">Verified Founders</span>
                  </div>
                  <div class="h-10 w-[1px] bg-card-border"></div>
                  <div class="flex flex-col text-left">
                    <span class="font-headline-md text-2xl lg:text-3xl font-bold text-primary tracking-tight" id="counterEvents">27</span>
                    <span class="font-label-md text-label-md text-on-surface-variant mt-0.5 tracking-wide">Curated Gatherings</span>
                  </div>
                  <div class="h-10 w-[1px] bg-card-border"></div>
                  <div class="flex flex-col text-left">
                    <span class="font-headline-md text-2xl lg:text-3xl font-bold text-secondary tracking-tight">4.9/5</span>
                    <span class="font-label-md text-label-md text-on-surface-variant mt-0.5 tracking-wide">Peer Trust</span>
                  </div>
                </div>
              </div>

              <!-- Right Column Visual (Warm founder coffee laptop setting) -->
              <div class="lg:col-span-6 relative">
                <div class="relative w-full aspect-[4/3] sm:aspect-[14/10] rounded-2xl overflow-hidden shadow-lg border border-card-border/60">
                  <img alt="Founder workspace coffee terrace" class="w-full h-full object-cover" id="heroCapsule1" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBQOGkFg7WlUWSrH99zAr_NpVfxigqQdvK1JXSl3dRMsAah88IIJNAhSx8OtC4DKo9EJqPKrthaRiIpLyqt_xcOwaZP62w7cSPmLdKivLOoQd09W35SQpnkWSfEWVisoyktKg1Orkg8BptmZwIKPc3y1r-4ghvDAecJkMjxHFDzIQYE2O1zppL4xfqRP3baviEwS-40bNBYfBFV6PFSQ0z7D12zfeBHWQ_3r5oCcjVYX2-bGarNL6J7"/>
                  <div class="absolute inset-0 bg-gradient-to-tr from-black/40 via-transparent to-transparent"></div>
                  <!-- Green Mug / Card Badge Overlay -->
                  <div class="absolute bottom-6 right-6 bg-primary-container/90 backdrop-blur-md text-white p-3.5 rounded-xl border border-white/10 shadow-lg text-right max-w-[180px]">
                    <div class="font-headline-sm text-[12px] text-primary-fixed leading-none mb-1 font-bold">Founder for Founder</div>
                    <p class="font-body-sm text-[11px] leading-tight text-white/90">Create. Connect. Collaborate.</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </section>

        <!-- BUSINESSES CONNECTED MARQUEE TICKER (Stitch Reference) -->
        <section class="w-full bg-surface-container-low py-8 overflow-hidden shadow-inner border-b border-card-border/60">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop mb-4">
            <div class="flex items-center justify-between">
              <span class="font-label-status text-label-status uppercase text-on-surface-variant font-bold tracking-widest">
                Businesses Connected With Us
              </span>
              <span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">
                Ambitious enterprises, scaling ventures &amp; industry leaders across India
              </span>
            </div>
          </div>
          <!-- Continuous Marquee Stream -->
          <div class="relative w-full flex overflow-x-hidden">
            <div class="animate-marquee flex gap-12 whitespace-nowrap shrink-0 items-center px-4">
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Apex Global Tech
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Precision Industries
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Elevate Digital
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Quantum Manufacturing
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Horizon Logistics
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Pinnacle Real Estate
              </span>
              <span class="font-title-md text-title-md text-primary font-bold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">stars</span> snalts.co
              </span>
              <!-- Repeat for seamless loop -->
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Apex Global Tech
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Precision Industries
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Elevate Digital
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Quantum Manufacturing
              </span>
            </div>
          </div>
        </section>

        <!-- CORE PHILOSOPHY (Stitch Screen b12ad31e) -->
        <section class="w-full bg-surface-container-lowest py-20 lg:py-28" id="about">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop flex flex-col gap-space-xl">
            <!-- Section Header -->
            <div class="flex flex-col md:flex-row md:items-end justify-between gap-space-md">
              <div class="flex flex-col gap-space-xs max-w-2xl">
                <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
                  WHAT WE OFFER • CORE PHILOSOPHY
                </span>
                <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
                  What We Offer: Beyond conventional networking into practical collaboration.
                </h2>
              </div>
              <p class="font-body-md text-body-md text-on-surface-variant max-w-md">
                Traditional networking events yield business cards; shared experiences build lasting relationships. Founder for Founder creates spaces where ambitious minds connect with purpose.
              </p>
            </div>

            <!-- 4 Pillars Grid Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter">
              <!-- Card 1 -->
              <div class="flex flex-col p-space-lg rounded-xl bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 shadow-sm hover:shadow-md group">
                <div class="w-12 h-12 rounded-lg bg-primary-fixed flex items-center justify-center text-on-primary-fixed mb-space-md group-hover:bg-primary-container group-hover:text-on-primary transition-colors">
                  <span class="material-symbols-outlined text-2xl">groups_3</span>
                </div>
                <span class="font-label-status text-label-status uppercase text-secondary font-bold mb-1">Curated Network</span>
                <h3 class="font-title-lg text-title-lg text-primary font-bold mb-2">Curated Founder Circle</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Connect directly with vetted decision-makers, entrepreneurs, and business owners in high-trust peer circles.
                </p>
              </div>

              <!-- Card 2 -->
              <div class="flex flex-col p-space-lg rounded-xl bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 shadow-sm hover:shadow-md group">
                <div class="w-12 h-12 rounded-lg bg-primary-fixed flex items-center justify-center text-on-primary-fixed mb-space-md group-hover:bg-primary-container group-hover:text-on-primary transition-colors">
                  <span class="material-symbols-outlined text-2xl">interests</span>
                </div>
                <span class="font-label-status text-label-status uppercase text-secondary font-bold mb-1">Real Connections</span>
                <h3 class="font-title-lg text-title-lg text-primary font-bold mb-2">Shared Experiences</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Connect over sports, dining, adventure, roundtables, and creative learning rather than dull elevator pitches.
                </p>
              </div>

              <!-- Card 3 -->
              <div class="flex flex-col p-space-lg rounded-xl bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 shadow-sm hover:shadow-md group">
                <div class="w-12 h-12 rounded-lg bg-primary-fixed flex items-center justify-center text-on-primary-fixed mb-space-md group-hover:bg-primary-container group-hover:text-on-primary transition-colors">
                  <span class="material-symbols-outlined text-2xl">sync_alt</span>
                </div>
                <span class="font-label-status text-label-status uppercase text-secondary font-bold mb-1">Opportunity Exchange</span>
                <h3 class="font-title-lg text-title-lg text-primary font-bold mb-2">Needs &amp; Wants Engine</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Post specific commercial requirements or offer high-value solutions directly to trusted peers.
                </p>
              </div>

              <!-- Card 4 -->
              <div class="flex flex-col p-space-lg rounded-xl bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 shadow-sm hover:shadow-md group">
                <div class="w-12 h-12 rounded-lg bg-primary-fixed flex items-center justify-center text-on-primary-fixed mb-space-md group-hover:bg-primary-container group-hover:text-on-primary transition-colors">
                  <span class="material-symbols-outlined text-2xl">handshake</span>
                </div>
                <span class="font-label-status text-label-status uppercase text-secondary font-bold mb-1">Trusted Referrals</span>
                <h3 class="font-title-lg text-title-lg text-primary font-bold mb-2">Leads &amp; Introductions</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Generate credible client referrals and track business outcomes with authentic relationship tools.
                </p>
              </div>
            </div>

            <!-- Architectural Vision Statement Banner -->
            <div class="w-full bg-primary rounded-2xl p-space-lg md:p-space-xl flex flex-col md:flex-row items-center justify-between gap-space-lg text-on-primary shadow-xl">
              <div class="flex items-center gap-space-md max-w-2xl">
                <div class="w-12 h-12 rounded-full bg-secondary flex items-center justify-center shrink-0">
                  <span class="material-symbols-outlined text-on-secondary text-2xl">lightbulb</span>
                </div>
                <div class="flex flex-col">
                  <span class="font-label-status text-label-status uppercase text-primary-fixed tracking-widest font-bold">Our Vision</span>
                  <p class="font-title-lg text-title-lg font-medium text-surface-bright mt-1">
                    “To build a connected ecosystem of founders across India where ideas turn into action, relationships open doors, and collaboration drives business forward.”
                  </p>
                </div>
              </div>
              <button class="shrink-0 px-6 py-3 bg-primary-fixed text-on-primary-fixed font-title-md text-title-md rounded-[6px] hover:bg-surface-container-lowest transition-all duration-200" onclick="openShowInterestModal()">
                Join the Ecosystem
              </button>
            </div>
          </div>
        </section>

        <!-- THE 5 PILLARS OF PEER ENGAGEMENT (WAYS WE COLLABORATE) -->
        <section class="w-full bg-surface-container-low py-20 lg:py-28" id="experiences">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop flex flex-col gap-space-xl">
            <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-space-xs">
              <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
                WAYS WE COLLABORATE
              </span>
              <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
                The 5 Pillars of Peer Engagement
              </h2>
              <p class="font-body-lg text-body-lg text-on-surface-variant">
                Our experience formats are designed to foster trust, camaraderie, and strategic business growth.
              </p>
            </div>

            <!-- 5 Pillar Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
              <!-- Pillar 1 -->
              <div class="flex flex-col bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg transition-all duration-300">
                <div class="flex items-center justify-between pb-space-md">
                  <span class="px-2.5 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-status text-label-status uppercase font-bold">
                    01 • Sports &amp; Movement
                  </span>
                  <span class="material-symbols-outlined text-secondary text-2xl">sports_tennis</span>
                </div>
                <h3 class="font-headline-sm text-headline-sm text-primary font-bold mb-2">Play Together</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Sports, movement, and friendly competition: pickleball, padel, tennis, golf, badminton, cycling, morning runs, chess, and yoga sessions.
                </p>
                <div class="mt-space-md pt-space-sm flex flex-wrap gap-1.5">
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Pickleball</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Golf</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Tennis</span>
                </div>
              </div>

              <!-- Pillar 2 -->
              <div class="flex flex-col bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg transition-all duration-300">
                <div class="flex items-center justify-between pb-space-md">
                  <span class="px-2.5 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-status text-label-status uppercase font-bold">
                    02 • Outdoor &amp; Adventure
                  </span>
                  <span class="material-symbols-outlined text-secondary text-2xl">hiking</span>
                </div>
                <h3 class="font-headline-sm text-headline-sm text-primary font-bold mb-2">Explore Together</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Outdoor and adventure activities: mountain treks, nature trails, weekend road trips, founder retreats, and city field trips.
                </p>
                <div class="mt-space-md pt-space-sm flex flex-wrap gap-1.5">
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Treks</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Weekend Offsites</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Field Trips</span>
                </div>
              </div>

              <!-- Pillar 3 -->
              <div class="flex flex-col bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg transition-all duration-300">
                <div class="flex items-center justify-between pb-space-md">
                  <span class="px-2.5 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-status text-label-status uppercase font-bold">
                    03 • Food &amp; Culinary
                  </span>
                  <span class="material-symbols-outlined text-secondary text-2xl">restaurant</span>
                </div>
                <h3 class="font-headline-sm text-headline-sm text-primary font-bold mb-2">Dine Together</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Food and dining gatherings: curated founder dinners, Sunday brunches, chef's tables, coffee cupping, and culinary workshops.
                </p>
                <div class="mt-space-md pt-space-sm flex flex-wrap gap-1.5">
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Chef's Table</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Brunches</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Coffee Cupping</span>
                </div>
              </div>

              <!-- Pillar 4 -->
              <div class="flex flex-col bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg transition-all duration-300">
                <div class="flex items-center justify-between pb-space-md">
                  <span class="px-2.5 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-status text-label-status uppercase font-bold">
                    04 • Business &amp; Advisory
                  </span>
                  <span class="material-symbols-outlined text-secondary text-2xl">pie_chart</span>
                </div>
                <h3 class="font-headline-sm text-headline-sm text-primary font-bold mb-2">Build Together</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                  Founder and business experiences: peer advisory roundtables, reverse pitching, business problem-solving, founder office hours, and execution sprints.
                </p>
                <div class="mt-space-md pt-space-sm flex flex-wrap gap-1.5">
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Roundtables</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Office Hours</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Sprints</span>
                </div>
              </div>

              <!-- Pillar 5 -->
              <div class="flex flex-col md:col-span-2 lg:col-span-2 bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg transition-all duration-300">
                <div class="flex items-center justify-between pb-space-md">
                  <span class="px-2.5 py-1 rounded bg-secondary-fixed text-on-secondary-fixed font-label-status text-label-status uppercase font-bold">
                    05 • Socials &amp; Reflection
                  </span>
                  <span class="material-symbols-outlined text-secondary text-2xl">celebration</span>
                </div>
                <h3 class="font-headline-sm text-headline-sm text-primary font-bold mb-2">Celebrate Together</h3>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed max-w-xl">
                  Games, socials, and reflection: after-hours socials, trivia, live music, creative learning, storytelling, and milestone celebrations where leaders unwind and reflect together.
                </p>
                <div class="mt-space-md pt-space-sm flex flex-wrap gap-1.5">
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">After-Hours</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Live Music</span>
                  <span class="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-label-md text-label-md">Storytelling</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- MOMENTS OF LEVERAGE / CURATED GATHERINGS -->
        <section class="w-full bg-surface-container-lowest py-20 lg:py-28">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop flex flex-col gap-space-xl">
            <div class="flex flex-col gap-space-xs max-w-3xl">
              <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
                FOUNDER INTERACTIONS • MOMENTS OF LEVERAGE
              </span>
              <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
                Curated Founder Gatherings
              </h2>
              <p class="font-body-lg text-body-lg text-on-surface-variant">
                High-trust peer dialogues, confidential executive roundtables, private dinners, and strategic collaboration sessions captured across India.
              </p>
            </div>

            <!-- 3 Curated Gatherings Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter">
              <!-- Gathering 1 -->
              <div class="flex flex-col bg-surface-container-low rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group">
                <div class="relative h-56 w-full overflow-hidden bg-surface-container-highest">
                  <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" data-alt="Intimate evening private dinner for ten startup founders in Bengaluru." src="https://lh3.googleusercontent.com/aida-public/AB6AXuDPzpz1OPO0RR5Lf25ca0bsyRcYP9rppLOq4KQ-D-eMnFnLEM7gCeeZaG-Im-fxnRYlBlnGaIPeGyhQl-kRl3-sN4702goHnlZ7bBlrgHzLjGKh3ad56gpGiQbUhAdHa53_fkZ2qiYGl8tNoEmjCd8KkUGgTIBHHCRidRSSTtsx-XkLvhE0W22rulkFSydMPfGak5gr5r_Ms5RYBQ0ecTCtc2Ei6yZKis_o8D0Vb00MpCKJ7qGp5LU63w">
                  <div class="absolute top-3 right-3 px-3 py-1 rounded bg-surface-container-lowest/90 backdrop-blur-md text-primary font-label-status text-label-status font-bold uppercase shadow-sm">
                    Closed-Door
                  </div>
                </div>
                <div class="p-space-lg flex flex-col gap-space-sm flex-1">
                  <span class="font-label-status text-label-status uppercase text-secondary font-bold">Bengaluru • Private Dining</span>
                  <h3 class="font-title-lg text-title-lg text-primary font-bold">The Founder's Table</h3>
                  <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed flex-1">
                    Intimate 10-founder dinner focusing on revenue retention models, unit economics, and capital allocation strategies without the noise of mass networking.
                  </p>
                  <div class="pt-space-sm flex items-center justify-between text-on-surface-variant font-label-md text-label-md">
                    <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">schedule</span> 3.5 Hours</span>
                    <span class="font-semibold text-primary">Invitation Only</span>
                  </div>
                </div>
              </div>

              <!-- Gathering 2 -->
              <div class="flex flex-col bg-surface-container-low rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group">
                <div class="relative h-56 w-full overflow-hidden bg-surface-container-highest">
                  <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" data-alt="Confidential executive salon in Mumbai." src="https://lh3.googleusercontent.com/aida-public/AB6AXuBMnalFfKizQsNAnqJL98AepkpFJbg5KTJIo-GbrSok6lU2dpDtIgi70N7hiI0lgxLerwowFCsW6bVKEoDQUZPcvZIE5k4Kljgh74Ftpy9TWdNcHQXZKoNJPNnT565mdpn3kEizde52hIa2t2SX1mW0eFDB8hspjZeFsI7xs2GyCjSkOhQPg3boX6JSL6jiU7g0WWC7OQyqnj6VTwqdqGoxvBDDWkMu6UXkP-Ayg9jCuG1PbPscQWDYSA">
                  <div class="absolute top-3 right-3 px-3 py-1 rounded bg-surface-container-lowest/90 backdrop-blur-md text-primary font-label-status text-label-status font-bold uppercase shadow-sm">
                    Advisory Salon
                  </div>
                </div>
                <div class="p-space-lg flex flex-col gap-space-sm flex-1">
                  <span class="font-label-status text-label-status uppercase text-secondary font-bold">Mumbai • Executive Suite</span>
                  <h3 class="font-title-lg text-title-lg text-primary font-bold">Strategic Salons</h3>
                  <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed flex-1">
                    Confidential problem-solving sprints tackling enterprise deal closures, key leadership hiring, and expansion roadblocks with vetted cross-domain advisors.
                  </p>
                  <div class="pt-space-sm flex items-center justify-between text-on-surface-variant font-label-md text-label-md">
                    <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">groups</span> 12 Founders</span>
                    <span class="font-semibold text-primary">Peer Vetted</span>
                  </div>
                </div>
              </div>

              <!-- Gathering 3 -->
              <div class="flex flex-col bg-surface-container-low rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group">
                <div class="relative h-56 w-full overflow-hidden bg-surface-container-highest">
                  <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" data-alt="Two founders in intensive 1-on-1 strategic dialogue in Gurugram." src="https://lh3.googleusercontent.com/aida-public/AB6AXuCLAgRhW4rr6KD7pzxyFvd_kaCn545uuUbmCo-hUiuJqnUt7cp9aJK5GFjB6jBlY1wsMoU6RsDnTTcracCSmhW164qii5z_gV_prJPLRXqHK4dTm2j6MfhDW3hHCbwR_Pf2ScMgC0ylOckGNxyL8ZGN3KGSx3GAjJD8uXZakvDlpi7PvhZAft8P01FskcvfKgRoNOxdbdkMC6Iwd8xDHIsVeOjaLIeIveM38HVVhzJgC8JL8iJ571JxWg">
                  <div class="absolute top-3 right-3 px-3 py-1 rounded bg-surface-container-lowest/90 backdrop-blur-md text-primary font-label-status text-label-status font-bold uppercase shadow-sm">
                    1-on-1 Dialogue
                  </div>
                </div>
                <div class="p-space-lg flex flex-col gap-space-sm flex-1">
                  <span class="font-label-status text-label-status uppercase text-secondary font-bold">Gurugram • Matched Meet</span>
                  <h3 class="font-title-lg text-title-lg text-primary font-bold">Bilateral Advisory</h3>
                  <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed flex-1">
                    Curated 1:1 introductions matched specifically by complementary commercial capabilities, mutual business needs, and sector-aligned supply chains.
                  </p>
                  <div class="pt-space-sm flex items-center justify-between text-on-surface-variant font-label-md text-label-md">
                    <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">handshake</span> Algorithmic Match</span>
                    <span class="font-semibold text-primary">High-Signal</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- PLATFORM FEATURES (Interactive Minimal Tabs) -->
        <section class="w-full py-16 bg-surface-container-low border-y border-card-border/60">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop">
            <div class="flex flex-col md:flex-row md:items-end justify-between mb-8">
              <div>
                <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">Platform Architecture</span>
                <h3 class="font-headline-lg text-headline-lg text-primary font-bold mt-1">Structured For Active Value</h3>
              </div>
              <!-- Tabs Navigation Pills -->
              <div class="flex flex-wrap gap-2 mt-4 md:mt-0" id="platform-tabs">
                <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-primary-container text-white active" onclick="setStitchTab(0, this)">Curated Network</button>
                <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(1, this)">Needs &amp; Wants</button>
                <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(2, this)">Leads CRM</button>
                <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(3, this)">Experiences</button>
                <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(4, this)">Collaborations</button>
                <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(5, this)">Challenges</button>
              </div>
            </div>
            <div class="bg-surface-container-lowest rounded-2xl p-6 lg:p-8 border border-card-border/80 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6" id="feature-box">
              <div class="max-w-2xl">
                <span class="font-label-status text-label-status uppercase text-secondary font-bold block mb-1" id="feature-label">MODULE 01 • CURATION</span>
                <h4 class="font-headline-md text-2xl text-primary font-bold mb-2" id="feature-title">Curated Founder Network</h4>
                <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed" id="feature-desc">Connect with verified founders and decision-makers in a high-trust, clutter-free environment designed for meaningful business growth.</p>
              </div>
              <div class="flex items-center gap-3">
                <button class="inline-flex items-center gap-1.5 bg-primary-container hover:bg-primary text-white text-[12.5px] font-medium px-4 py-2 rounded-[6px] transition-all" onclick="openShowInterestModal()">
                  <span>Access Cohort</span>
                  <span class="material-symbols-outlined text-sm">arrow_forward</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- EXPERIENCES PHOTO CAROUSEL -->
        <section class="w-full py-16 lg:py-24 max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop">
          <!-- Section Title with Editorial Line -->
          <div class="flex items-center justify-between gap-6 mb-10">
            <div class="flex items-center gap-6 flex-1">
              <h2 class="font-headline-lg text-headline-lg text-primary font-bold tracking-tight">Experiences</h2>
              <div class="h-[1px] flex-1 bg-card-border hidden sm:block"></div>
            </div>
            <!-- Carousel Nav Buttons -->
            <div class="flex items-center gap-2">
              <button aria-label="Previous slide" class="w-9 h-9 rounded-[6px] border border-card-border flex items-center justify-center text-text-main hover:bg-surface-container-low transition-colors" onclick="scrollExperiences('left')">
                <span class="material-symbols-outlined text-[18px]">chevron_left</span>
              </button>
              <button aria-label="Next slide" class="w-9 h-9 rounded-[6px] border border-card-border flex items-center justify-center text-text-main hover:bg-surface-container-low transition-colors" onclick="scrollExperiences('right')">
                <span class="material-symbols-outlined text-[18px]">chevron_right</span>
              </button>
            </div>
          </div>
          <!-- Experience Cards Scroll Track -->
          <div class="flex gap-5 overflow-x-auto pb-4 scroll-smooth snap-x" id="experiences-track" style="scrollbar-width: none; -ms-overflow-style: none;">
            <!-- 1: Play Together -->
            <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
              <div class="h-44 w-full overflow-hidden bg-surface-subtle">
                <img alt="Play Together - Pickleball / Padel" id="formatImgPlay" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBVZvQ8mvPxjjMTjLrF6-VqxIN0JEH2LYfuTgdcdGk8PvQJyiu2u5oUtJijFilpwAZABufmCOZ06UT57PQqBGEKg1-9OMd-FRWPy29OF454SI1Ln-aaI9CEglLaVMReFz2gQ03uy4ow09oEq5zXUjdalnL-7FSNgARVaL5qOVsGy11qfvzW63V6icp4B0-nVZYF19XZFsC63s9ZAMvAZiIyVtOHp0EXxr4_1ZbrkQpBaEiN3iParP9H"/>
              </div>
              <div class="p-4 flex flex-col justify-between">
                <h3 class="font-title-lg text-title-lg text-primary font-bold">Play Together</h3>
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
                  <span class="font-label-md text-label-md text-on-surface-variant font-sans">Sports</span>
                  <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </div>
            </div>
            <!-- 2: Explore Together -->
            <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
              <div class="h-44 w-full overflow-hidden bg-surface-subtle">
                <img alt="Explore Together - Outdoor Trail & Hiking" id="formatImgExplore" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCw3xI8RlZpWZZ17uYgNPXasB04r1wJ0whnybywimVFdwREr2rr3DDSLYUulOUtaIVmEF80MqZbw10LmTsFrhl3rXyBNL72LAzwCDpNJJneZqJPTPRSkhlKzAiFKS0Tn1iRRN8nO65zy6XqDSx0PbtzudO-cEaeOigNSihGIOw_GdwmVBTeL7A0Cm4M1Z1dGv29lhLSDdtXG_2o5S3MccxG6bZxfslS2BnVSCHvd5UxkkZiTjyt0-6q"/>
              </div>
              <div class="p-4 flex flex-col justify-between">
                <h3 class="font-title-lg text-title-lg text-primary font-bold">Explore Together</h3>
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
                  <span class="font-label-md text-label-md text-on-surface-variant font-sans">Outdoors</span>
                  <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </div>
            </div>
            <!-- 3: Dine Together -->
            <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
              <div class="h-44 w-full overflow-hidden bg-surface-subtle">
                <img alt="Dine Together - Curated Founder Dinner" id="formatImgDine" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCBen8o-u4_a_KNZnmBPSlcSQkQnSlXVC-0qrB9AuScyPbRygpxb68mYWNoCy69eIlaNxi6FkrV7mJfwh3bUsuRLj84Od-p6BleYqSdJMRF79MsyY8pxbZwLS29Vp5e3DPlSRjeCYCtSUdxKbFOF4f26E9pgbmVgDz4jPROhIk2cqPzRgfkpEi-8iE7obRt1sv15_o7XqKE-PVrJM6xGmFN9_Tqsr5pAQOE7HF_VtMpZVUT8aD9EZn6"/>
              </div>
              <div class="p-4 flex flex-col justify-between">
                <h3 class="font-title-lg text-title-lg text-primary font-bold">Dine Together</h3>
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
                  <span class="font-label-md text-label-md text-on-surface-variant font-sans">Dining</span>
                  <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </div>
            </div>
            <!-- 4: Build Together -->
            <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
              <div class="h-44 w-full overflow-hidden bg-surface-subtle">
                <img alt="Build Together - Roundtable advisory" id="formatImgBuild" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDN0pvVm_B1pcvX3C1p41zAEVv0F7UOI4ZTEugE8UJNnDeu5eNbAPsWH_IRBeMTTrBdA1Zpcf2ZypCbINRgud_0WaGY9LhRanEqZLYWkrdklcms6PyKaBzR6EiAgA4rYlrNQ-aPnPLdocN7UEYfEq2eAVjX5vKcMzASL9PbNdFccHCH-3vD01dWm7WYDmctJQmiJRSbwgyZ7oPtz252aZQLyRXIxBYIhzTXyU4bbmWRw5KNEMp02I-u"/>
              </div>
              <div class="p-4 flex flex-col justify-between">
                <h3 class="font-title-lg text-title-lg text-primary font-bold">Build Together</h3>
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
                  <span class="font-label-md text-label-md text-on-surface-variant font-sans">Advisory</span>
                  <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </div>
            </div>
            <!-- 5: Celebrate Together -->
            <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
              <div class="h-44 w-full overflow-hidden bg-surface-subtle">
                <img alt="Celebrate Together - Social Gathering" id="formatImgCelebrate" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDMlhWLkz1P-mAPBK0gUIwbxPJcntsb_nuq1ISYkf94RDSh48oieYKwAMHeik8gD0Ev1u5UN-XgFp8CYopUvicZNBFwYnZ3sV9DL43PO02Ra8X0ENCaaSr2YHl121PlGI1_CAUaRP9E9uB33aoy9A-fhPPa1fn4ODQSR0o8gSOldIdnFRVHcVu-WJYsMtsdrx5u91M5OrNIuFwVbWfIO9F_ap7LdiFrLl6PmOLMCmy7I5ecoUoXXNBQ"/>
              </div>
              <div class="p-4 flex flex-col justify-between">
                <h3 class="font-title-lg text-title-lg text-primary font-bold">Celebrate Together</h3>
                <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
                  <span class="font-label-md text-label-md text-on-surface-variant font-sans">Socials</span>
                  <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </div>
            </div>
          </div>
          <div id="upcomingEventsGrid" class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
        </section>

        <!-- APPLICATION JOURNEY (HOW TO JOIN - 6 STEPS) -->
        <section class="w-full bg-surface-container-low py-20 lg:py-28" id="how-it-works">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop flex flex-col gap-space-xl">
            <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-space-xs">
              <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">
                APPLICATION JOURNEY
              </span>
              <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
                How To Join Founder for Founder
              </h2>
              <p class="font-body-lg text-body-lg text-on-surface-variant">
                A structured, application-based onboarding process to ensure high-signal community alignment.
              </p>
            </div>

            <!-- 6 Horizontal Timeline Steps -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-gutter-sm">
              <!-- Step 1 -->
              <div class="flex flex-col p-space-md rounded-xl bg-surface-container-lowest shadow-sm hover:shadow-md transition-shadow">
                <div class="w-9 h-9 rounded-[6px] bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center font-bold mb-space-sm">
                  1
                </div>
                <h4 class="font-title-md text-title-md text-primary font-bold mb-1">Show Interest</h4>
                <p class="font-body-sm text-body-sm text-on-surface-variant leading-normal">
                  Submit application details &amp; select your executive leadership role.
                </p>
              </div>

              <!-- Step 2 -->
              <div class="flex flex-col p-space-md rounded-xl bg-surface-container-lowest shadow-sm hover:shadow-md transition-shadow">
                <div class="w-9 h-9 rounded-[6px] bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center font-bold mb-space-sm">
                  2
                </div>
                <h4 class="font-title-md text-title-md text-primary font-bold mb-1">Profile Screening</h4>
                <p class="font-body-sm text-body-sm text-on-surface-variant leading-normal">
                  Review of business background, operating track record &amp; scale goals.
                </p>
              </div>

              <!-- Step 3 -->
              <div class="flex flex-col p-space-md rounded-xl bg-surface-container-lowest shadow-sm hover:shadow-md transition-shadow">
                <div class="w-9 h-9 rounded-[6px] bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center font-bold mb-space-sm">
                  3
                </div>
                <h4 class="font-title-md text-title-md text-primary font-bold mb-1">Application Review</h4>
                <p class="font-body-sm text-body-sm text-on-surface-variant leading-normal">
                  Evaluated by the admissions review committee within 72 hours.
                </p>
              </div>

              <!-- Step 4 -->
              <div class="flex flex-col p-space-md rounded-xl bg-surface-container-lowest shadow-sm hover:shadow-md transition-shadow">
                <div class="w-9 h-9 rounded-[6px] bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center font-bold mb-space-sm">
                  4
                </div>
                <h4 class="font-title-md text-title-md text-primary font-bold mb-1">Receive Invite</h4>
                <p class="font-body-sm text-body-sm text-on-surface-variant leading-normal">
                  Approved applicants receive private verification tokens and onboarding details.
                </p>
              </div>

              <!-- Step 5 -->
              <div class="flex flex-col p-space-md rounded-xl bg-surface-container-lowest shadow-sm hover:shadow-md transition-shadow">
                <div class="w-9 h-9 rounded-[6px] bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center font-bold mb-space-sm">
                  5
                </div>
                <h4 class="font-title-md text-title-md text-primary font-bold mb-1">Activate Access</h4>
                <p class="font-body-sm text-body-sm text-on-surface-variant leading-normal">
                  Complete membership setup &amp; unlock verified founder credentials.
                </p>
              </div>

              <!-- Step 6 -->
              <div class="flex flex-col p-space-md rounded-xl bg-surface-container-lowest shadow-sm hover:shadow-md transition-shadow">
                <div class="w-9 h-9 rounded-[6px] bg-secondary text-on-secondary font-headline-sm text-headline-sm flex items-center justify-center font-bold mb-space-sm">
                  6
                </div>
                <h4 class="font-title-md text-title-md text-primary font-bold mb-1">Engage &amp; Grow</h4>
                <p class="font-body-sm text-body-sm text-on-surface-variant leading-normal">
                  Access private portal, RSVP for curated experiences &amp; collaborate.
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- ACTIVE COMMUNITY NEEDS & WANTS (Opportunity Preview) -->
        <section class="w-full py-20 bg-surface-container-lowest border-t border-card-border/60" id="needs-wants">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
              <div>
                <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">INTERNAL EXCHANGE</span>
                <h2 class="font-headline-lg text-headline-lg text-primary font-bold tracking-tight mt-1">Active Community Needs &amp; Offers</h2>
              </div>
              <button class="inline-flex items-center gap-1.5 text-sm font-semibold text-secondary hover:text-primary transition-colors" onclick="openShowInterestModal()">
                <span>+ Post a Need / Offer</span>
                <span class="material-symbols-outlined text-sm">arrow_forward</span>
              </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="needsPreviewContainer">
              <!-- Requirements -->
              <div class="bg-surface-container-low rounded-xl p-6 border border-card-border/80 shadow-sm">
                <div class="flex items-center gap-2 mb-4 pb-3 border-b border-card-border/60">
                  <span class="w-2 h-2 rounded-full bg-error"></span>
                  <span class="font-label-status text-label-status font-bold tracking-widest uppercase text-on-surface">I NEED (REQUIREMENTS)</span>
                </div>
                <div class="space-y-3">
                  <div class="p-3.5 bg-surface-container-lowest rounded-lg border border-card-border/40">
                    <span class="font-label-status text-[10px] text-secondary uppercase tracking-wider block mb-1">MANUFACTURING</span>
                    <p class="font-title-md text-[14px] text-primary font-semibold">High-volume manufacturing partner for precision components</p>
                    <span class="font-body-sm text-[11.5px] text-on-surface-variant mt-1 block">Pan-India scale • Verified RFQ posted by MD Member</span>
                  </div>
                  <div class="p-3.5 bg-surface-container-lowest rounded-lg border border-card-border/40">
                    <span class="font-label-status text-[10px] text-secondary uppercase tracking-wider block mb-1">TECHNOLOGY</span>
                    <p class="font-title-md text-[14px] text-primary font-semibold">Enterprise SaaS growth marketing advisor &amp; partner</p>
                    <span class="font-body-sm text-[11.5px] text-on-surface-variant mt-1 block">Series A B2B firm • Direct peer recommendation sought</span>
                  </div>
                </div>
              </div>
              <!-- Offers -->
              <div class="bg-surface-container-low rounded-xl p-6 border border-card-border/80 shadow-sm">
                <div class="flex items-center gap-2 mb-4 pb-3 border-b border-card-border/60">
                  <span class="w-2 h-2 rounded-full bg-secondary"></span>
                  <span class="font-label-status text-label-status font-bold tracking-widest uppercase text-on-surface">I CAN HELP WITH (OFFERS)</span>
                </div>
                <div class="space-y-3">
                  <div class="p-3.5 bg-surface-container-lowest rounded-lg border border-card-border/40">
                    <span class="font-label-status text-[10px] text-secondary uppercase tracking-wider block mb-1">GLOBAL EXPANSION</span>
                    <p class="font-title-md text-[14px] text-primary font-semibold">Direct introductions to SEA retail distribution heads</p>
                    <span class="font-body-sm text-[11.5px] text-on-surface-variant mt-1 block">Singapore &amp; Dubai • Offered by FMCG Founder</span>
                  </div>
                  <div class="p-3.5 bg-surface-container-lowest rounded-lg border border-card-border/40">
                    <span class="font-label-status text-[10px] text-secondary uppercase tracking-wider block mb-1">CAPITAL ALLOCATION</span>
                    <p class="font-title-md text-[14px] text-primary font-semibold">Institutional debt structuring &amp; working capital credit lines</p>
                    <span class="font-body-sm text-[11.5px] text-on-surface-variant mt-1 block">Fintech Leader • Direct advisory for verified members</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- COMMUNITY PERSPECTIVES / TESTIMONIALS -->
        <section class="w-full py-20 bg-surface-container-low border-t border-card-border/60" id="community">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop">
            <div class="max-w-2xl mb-10">
              <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">MEMBER STORIES</span>
              <h2 class="font-headline-lg text-headline-lg text-primary font-bold tracking-tight mt-1">Founder Perspectives</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="testimonialsContainer">
              <div class="bg-surface-container-lowest rounded-xl p-6 border border-card-border/80 shadow-sm flex flex-col justify-between">
                <p class="font-body-md text-on-surface leading-relaxed">
                  "Traditional networking events yield business cards; shared experiences build lasting relationships. Founder for Founder creates spaces where ambitious minds connect with purpose."
                </p>
                <div class="mt-6 pt-4 border-t border-card-border/50">
                  <h4 class="font-title-md text-primary font-bold">Ananya Verma</h4>
                  <span class="font-label-md text-on-surface-variant">Founder &amp; CEO, Elevate Digital</span>
                </div>
              </div>
              <div class="bg-surface-container-lowest rounded-xl p-6 border border-card-border/80 shadow-sm flex flex-col justify-between">
                <p class="font-body-md text-on-surface leading-relaxed">
                  "The Needs &amp; Wants engine alone unlocked two credible manufacturing suppliers within our first month. The signal-to-noise ratio here is unmatched in India."
                </p>
                <div class="mt-6 pt-4 border-t border-card-border/50">
                  <h4 class="font-title-md text-primary font-bold">Rajesh Patel</h4>
                  <span class="font-label-md text-on-surface-variant">Managing Director, Quantum Manufacturing</span>
                </div>
              </div>
              <div class="bg-surface-container-lowest rounded-xl p-6 border border-card-border/80 shadow-sm flex flex-col justify-between">
                <p class="font-body-md text-on-surface leading-relaxed">
                  "Playing padel at 7 AM followed by frank conversations on enterprise sales barriers with founders who run 50+ crore businesses is priceless leverage."
                </p>
                <div class="mt-6 pt-4 border-t border-card-border/50">
                  <h4 class="font-title-md text-primary font-bold">Vikramaditya Rao</h4>
                  <span class="font-label-md text-on-surface-variant">Co-Founder, Horizon Logistics</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- CURATED MEETING PHOTOS SLIDER (16:9 RATIO) -->
        <section class="w-full py-16 bg-surface-container-lowest border-t border-card-border/60" id="meetingPhotosSection" style="display: none;">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop mb-8">
            <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">FOUNDER INTERACTIONS • MOMENTS OF LEVERAGE</span>
            <h2 class="font-headline-lg text-headline-lg text-primary font-bold tracking-tight mt-1">Curated Gatherings &amp; Meeting Moments</h2>
            <p class="font-body-md text-on-surface-variant mt-2 max-w-2xl leading-relaxed">High-trust peer dialogues, confidential executive roundtables, private dinners, and strategic collaboration sessions captured across India.</p>
          </div>
          <div class="meeting-slider-wrapper overflow-hidden px-margin-mobile md:px-margin lg:px-margin-desktop max-w-[1440px] mx-auto">
            <div class="meeting-slider-track flex gap-4 overflow-x-auto" id="meetingPhotosTrack"></div>
          </div>
        </section>

        <!-- FAQ SECTION -->
        <section class="w-full py-20 bg-surface-container-low border-t border-card-border/60" id="faq">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop">
            <div class="flex items-center justify-between mb-8">
              <div class="flex flex-col gap-1">
                <span class="font-label-status text-label-status uppercase text-secondary font-bold tracking-widest">COMMON QUESTIONS</span>
                <h2 class="font-headline-lg text-headline-lg text-primary font-bold tracking-tight">Frequently Asked Questions</h2>
              </div>
              <a class="inline-flex items-center gap-1 font-title-md text-title-md text-secondary hover:text-primary transition-colors" href="#faq">
                <span>View all</span>
                <span class="material-symbols-outlined text-sm">arrow_forward</span>
              </a>
            </div>
            <!-- FAQ Accordion Container -->
            <div class="space-y-3" id="faqContainer">
              <!-- Item 1 -->
              <div class="faq-node bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden shadow-sm">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-title-md text-title-md text-primary font-bold">What is Founder for Founder?</span>
                  <span class="material-symbols-outlined text-[19px] text-on-surface-variant transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 font-body-md text-body-md text-on-surface-variant leading-relaxed border-t border-card-border/40 pt-3">
                  Founder for Founder is a vetted pan-India business collective. Instead of superficial business card exchanges, we facilitate peer advisory roundtables, shared active experiences, and a structured Needs &amp; Wants marketplace.
                </div>
              </div>
              <!-- Item 2 -->
              <div class="faq-node bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden shadow-sm">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-title-md text-title-md text-primary font-bold">Who can apply?</span>
                  <span class="material-symbols-outlined text-[19px] text-on-surface-variant transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 font-body-md text-body-md text-on-surface-variant leading-relaxed border-t border-card-border/40 pt-3">
                  Founders, Co-founders, Managing Directors, enterprise business owners, and active CXO leaders with operating businesses across India can apply.
                </div>
              </div>
              <!-- Item 3 -->
              <div class="faq-node bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden shadow-sm">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-title-md text-title-md text-primary font-bold">What kind of businesses are included?</span>
                  <span class="material-symbols-outlined text-[19px] text-on-surface-variant transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 font-body-md text-body-md text-on-surface-variant leading-relaxed border-t border-card-border/40 pt-3">
                  Our community spans high-growth tech startups, industrial manufacturing, D2C brands, supply chain enterprises, real estate developers, and specialized professional firms.
                </div>
              </div>
              <!-- Item 4 -->
              <div class="faq-node bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden shadow-sm">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-title-md text-title-md text-primary font-bold">Is there a membership fee?</span>
                  <span class="material-symbols-outlined text-[19px] text-on-surface-variant transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 font-body-md text-body-md text-on-surface-variant leading-relaxed border-t border-card-border/40 pt-3">
                  Yes, approved candidates receive an invitation link detailing our annual membership tiers, which cover curated gatherings, private retreats, and platform directory access.
                </div>
              </div>
              <!-- Item 5 -->
              <div class="faq-node bg-surface-container-lowest rounded-xl border border-card-border/80 overflow-hidden shadow-sm">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-title-md text-title-md text-primary font-bold">How do I stay updated about events?</span>
                  <span class="material-symbols-outlined text-[19px] text-on-surface-variant transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 font-body-md text-body-md text-on-surface-variant leading-relaxed border-t border-card-border/40 pt-3">
                  Members receive calendar invites, WhatsApp updates for chapter meetups, and can RSVP directly through the Member Portal.
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- FINAL CALL TO ACTION BANNER (Stitch Screen b12ad31e) -->
        <section class="w-full bg-surface-container-lowest py-20 lg:py-28">
          <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop">
            <div class="relative overflow-hidden rounded-3xl bg-surface-container p-space-xl md:p-16 lg:p-20 shadow-xl flex flex-col md:flex-row items-center justify-between gap-space-xl">
              <!-- Ambient background decorative blur -->
              <div class="absolute -right-20 -bottom-20 w-80 h-80 bg-secondary-fixed/30 rounded-full blur-3xl pointer-events-none"></div>
              <div class="flex flex-col gap-space-sm max-w-2xl relative z-10 text-left">
                <div class="inline-flex items-center gap-space-xs px-3 py-1 rounded-full bg-surface-container-lowest text-secondary font-label-status text-label-status tracking-widest uppercase w-fit shadow-sm">
                  APPLICATION WINDOW OPEN
                </div>
                <h2 class="font-headline-lg text-headline-lg text-primary font-bold">
                  Your next meaningful business connection starts here.
                </h2>
                <p class="font-body-lg text-body-lg text-on-surface-variant leading-relaxed">
                  Discover a curated network built around founders, opportunities, and collaboration across India.
                </p>
                <span class="font-label-md text-label-md text-on-surface-variant pt-2">
                  By application only • Rolling 72-hour review committee
                </span>
              </div>
              <div class="relative z-10 shrink-0">
                <button class="inline-flex items-center justify-center gap-space-xs px-8 py-4 bg-primary text-on-primary font-title-lg text-title-lg rounded-[6px] shadow-[0_8px_24px_rgba(0,53,39,0.25)] hover:bg-secondary hover:text-on-primary transition-all duration-200" onclick="openShowInterestModal()">
                  <span>Show Interest</span>
                  <span class="material-symbols-outlined text-xl">arrow_forward</span>
                </button>
              </div>
            </div>
          </div>
        </section>

      </div>
    </main>

    <!-- FOOTER (Stitch Executive Guild) -->
    <footer class="w-full bg-surface-container-low mt-space-xl shadow-[0_-1px_12px_rgba(0,0,0,0.02)] border-t border-card-border/60" id="contact">
      <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop py-space-xl">
        <div class="flex flex-col lg:flex-row justify-between items-start gap-gutter-lg pb-space-xl">
          <div class="flex flex-col gap-space-md max-w-sm">
            <div class="flex items-center gap-space-sm">
              <img src="/assets/logo.svg" alt="Founder for Founder Logo" class="w-7 h-7 rounded-full object-cover" id="footerLogo" width="28" height="28" loading="lazy">
              <span class="font-headline-sm text-headline-sm text-primary font-bold">Founder for Founder</span>
              <span class="font-serif font-bold text-secondary text-sm">F4F</span>
            </div>
            <p class="font-body-md text-body-md text-on-surface-variant">
              The curated private network for elite founders, institutional operators, and business leaders across India.
            </p>
            <div class="flex items-center gap-space-xs font-label-md text-label-md text-on-surface-variant">
              <span class="material-symbols-outlined text-base">mail</span>
              <a class="hover:text-primary transition-colors" href="mailto:connect.f4f@gmail.com">connect.f4f@gmail.com</a>
            </div>
            <div class="font-label-md text-label-md text-on-surface-variant">
              Powered by <a class="font-title-md text-primary font-bold hover:underline" href="#">snalts.co</a>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-gutter-lg">
            <div class="flex flex-col gap-space-sm">
              <span class="font-label-status text-label-status uppercase text-primary font-bold tracking-wider">Platform</span>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" data-path="about" href="#about">About Network</a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" data-path="experiences" href="#experiences">Experiences &amp; Summits</a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" data-path="show-interest" href="#" onclick="openShowInterestModal()">Apply for Membership</a>
            </div>

            <div class="flex flex-col gap-space-sm">
              <span class="font-label-status text-label-status uppercase text-primary font-bold tracking-wider">Governance &amp; Legal</span>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="/terms">Terms &amp; Conditions</a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="/privacy-policy">Privacy Policy</a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="/refund-policy">Refund Policy</a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors" href="/community-guidelines">Community Guidelines</a>
            </div>

            <div class="flex flex-col gap-space-sm">
              <span class="font-label-status text-label-status uppercase text-primary font-bold tracking-wider">Connect</span>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors flex items-center gap-space-xs" href="https://www.linkedin.com/company/founder-for-founder/" target="_blank" rel="noopener noreferrer">
                <span class="material-symbols-outlined text-base">public</span>LinkedIn
              </a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors flex items-center gap-space-xs" href="https://www.instagram.com/founder_for_founder" target="_blank" rel="noopener noreferrer">
                <span class="material-symbols-outlined text-base">photo_camera</span>Instagram
              </a>
              <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors flex items-center gap-space-xs" href="https://www.facebook.com/share/19ZnPNuhPb/" target="_blank" rel="noopener noreferrer">
                <span class="material-symbols-outlined text-base">share</span>Facebook
              </a>
            </div>
          </div>
        </div>

        <div class="pt-space-lg flex flex-col sm:flex-row justify-between items-center gap-space-md text-center sm:text-left border-t border-card-border/60">
          <p class="font-label-md text-label-md text-on-surface-variant">&copy; 2026 Founder for Founder (f4f). All rights reserved.</p>
          <p class="font-label-md text-label-md text-on-surface-variant">Private Membership Network. Verified Founders Only. • Powered by snalts.co</p>
        </div>
      </div>
    </footer>
  </div>

  '''

updated_content = content[:nav_start] + new_header_and_public_page + content[portal_start:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated public/index.html with revised Stitch designs successfully!")
