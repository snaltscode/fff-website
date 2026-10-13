import re

def integrate():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update body tag with Stitch class
    html = re.sub(r'<body[^>]*>', '<body class="bg-[#FAF8F5] text-text-main antialiased relative min-h-screen">', html, count=1)

    # 2. Update Tailwind config to ensure all Stitch Screen 13 tokens exist
    tailwind_script_pattern = r'<script id="tailwind-config">.*?</script>'
    new_tailwind_script = '''<script id="tailwind-config">
    tailwind.config = {
      corePlugins: { preflight: false },
      darkMode: "class",
      theme: {
        extend: {
          "colors": {
            "canvas-cream": "#FAF8F5",
            "canvas-ivory": "#FBF9F6",
            "surface-subtle": "#F5F2EC",
            "card-border": "#E8E4DC",
            "border-hairline": "#EDE9E1",
            "primary-dark": "#064E3B",
            "primary-emerald": "#043E2E",
            "primary-light": "#0B664C",
            "text-main": "#1A1A1A",
            "text-muted": "#5A6260",
            "text-subtle": "#7E8784",
            "gold-accent": "#B89047",
            "on-primary-container": "#80bea6",
            "background": "#fff8f5",
            "surface-container": "#f4ece8",
            "tertiary-fixed-dim": "#4edea3",
            "on-secondary": "#ffffff",
            "secondary-container": "#fed488",
            "error-container": "#ffdad6",
            "primary-fixed": "#b0f0d6",
            "on-error-container": "#93000a",
            "on-secondary-container": "#785a1a",
            "on-background": "#1e1b19",
            "on-primary-fixed": "#002117",
            "gold-light": "#F5EFEB",
            "surface-container-high": "#eee7e3",
            "inverse-on-surface": "#f7efeb",
            "surface-tint": "#2b6954",
            "inverse-surface": "#33302d",
            "secondary": "#775a19",
            "on-surface": "#1e1b19",
            "inverse-primary": "#95d3ba",
            "tertiary-container": "#004f34",
            "surface": "#fff8f5",
            "error": "#ba1a1a",
            "on-surface-variant": "#404944",
            "surface-bright": "#fff8f5",
            "outline-variant": "#bfc9c3",
            "primary-container": "#064e3b",
            "tertiary": "#003623",
            "surface-dim": "#e0d8d5",
            "text-tertiary": "#6B7280",
            "surface-variant": "#e9e1dd",
            "secondary-fixed": "#ffdea5",
            "primary": "#003527",
            "primary-fixed-dim": "#95d3ba",
            "on-primary": "#ffffff",
            "text-primary": "#111827",
            "surface-card": "#FFFFFF",
            "surface-container-low": "#faf2ee",
            "outline": "#707974",
            "border-strong": "#D5D2CB",
            "on-secondary-fixed-variant": "#5d4201",
            "surface-container-lowest": "#ffffff",
            "on-primary-fixed-variant": "#0b513d",
            "emerald-deep": "#043E2E",
            "surface-container-highest": "#e9e1dd",
            "on-error": "#ffffff",
            "on-tertiary": "#ffffff",
            "on-tertiary-fixed": "#002113",
            "text-secondary": "#4B5563",
            "on-tertiary-container": "#31c98f",
            "on-secondary-fixed": "#261900",
            "tertiary-fixed": "#6ffbbe",
            "on-tertiary-fixed-variant": "#005236",
            "secondary-fixed-dim": "#e9c176"
          },
          "borderRadius": {
            "DEFAULT": "0.125rem",
            "lg": "0.25rem",
            "xl": "0.5rem",
            "full": "0.75rem"
          },
          "fontFamily": {
            "serif": ['"Playfair Display"', 'Georgia', 'serif'],
            "sans": ['"Plus Jakarta Sans"', 'system-ui', '-apple-system', 'sans-serif'],
            "headline-lg-mobile": [ "Playfair Display", "serif" ],
            "body-lg": [ "Plus Jakarta Sans", "sans-serif" ],
            "label-caps": [ "Plus Jakarta Sans", "sans-serif" ],
            "numeric-stat": [ "Playfair Display", "serif" ],
            "headline-md": [ "Playfair Display", "serif" ],
            "body-md": [ "Plus Jakarta Sans", "sans-serif" ],
            "body-sm": [ "Plus Jakarta Sans", "sans-serif" ],
            "display-hero": [ "Playfair Display", "serif" ],
            "label-md": [ "Plus Jakarta Sans", "sans-serif" ],
            "subhead-lg": [ "Plus Jakarta Sans", "sans-serif" ],
            "headline-sm": [ "Playfair Display", "serif" ],
            "headline-lg": [ "Playfair Display", "serif" ],
            "display-hero-mobile": [ "Playfair Display", "serif" ]
          }
        }
      }
    };
  </script>'''
    html = re.sub(tailwind_script_pattern, new_tailwind_script, html, flags=re.DOTALL)

    # 3. Build new Header & Public Page markup from Stitch Screen 13
    stitch_public_surface = '''  <!-- 2px Emerald Scroll Progress Bar -->
  <div class="scroll-progress-bar" id="scrollProgressBar"></div>

  <!-- TOP HEADER (Stitch Screen 13) -->
  <header class="sticky top-0 z-40 bg-[#FAF8F5]/90 backdrop-blur-md border-b border-card-border/60 transition-all" id="mainNavbar">
    <div class="max-w-7xl mx-auto px-6 lg:px-12 h-20 flex items-center justify-between">
      <!-- Logo -->
      <a class="flex items-center gap-3 group" href="#">
        <div class="tracking-tighter font-serif font-bold text-2xl text-primary-dark flex items-center">
          <img src="/assets/logo.svg" alt="Founder for Founder Logo" class="w-8 h-8 rounded-full object-cover mr-1" id="navLogo" width="32" height="32" decoding="async">
          <span class="text-3xl font-bold tracking-tight">F4F</span>
        </div>
        <div class="h-7 w-[1px] bg-card-border hidden sm:block"></div>
        <div class="flex flex-col">
          <span class="font-serif text-[15px] font-semibold tracking-tight text-text-main leading-none">Founder</span>
          <span class="font-serif text-[15px] font-semibold tracking-tight text-text-main leading-tight" id="navSubtitle">for Founder</span>
        </div>
      </a>
      <!-- Desktop Nav -->
      <nav class="hidden md:flex items-center gap-7 text-[13.5px] font-medium text-text-muted" id="publicNav">
        <a class="text-primary-dark font-semibold transition-colors" href="#">Home</a>
        <a class="hover:text-text-main transition-colors" href="#about">About</a>
        <a class="hover:text-text-main transition-colors" href="#experiences">Experiences</a>
        <a class="hover:text-text-main transition-colors" href="#needs-wants">Needs &amp; Wants</a>
        <a class="hover:text-text-main transition-colors" href="#community">Community</a>
        <a class="hover:text-text-main transition-colors" href="#faq">FAQ</a>
      </nav>
      <!-- Right CTAs -->
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-3" id="publicNavBtns">
          <button class="inline-flex items-center gap-2 bg-primary-dark hover:bg-primary-emerald text-white text-[13px] font-medium tracking-wide px-5 py-2.5 rounded-full transition-all shadow-sm" onclick="openShowInterestModal()">
            <span>Show Interest</span>
            <span class="text-base leading-none">→</span>
          </button>
          <button class="inline-flex items-center gap-1.5 border border-card-border hover:bg-surface-subtle text-text-main text-[13px] font-medium px-4 py-2 rounded-full transition-colors" onclick="openLoginModal()" title="Member Login">
            <span>Login</span>
          </button>
        </div>

        <!-- Authenticated Portal Nav Controls -->
        <div id="authNavControls" style="display: none; align-items: center; gap: 0.85rem;">
          <span id="navUserName" class="text-[13px] font-semibold text-primary-dark hidden sm:inline-block">Welcome, Member</span>
          <button class="inline-flex items-center gap-1 text-[12.5px] font-medium border border-card-border px-3 py-1.5 rounded-full hover:bg-surface-subtle" id="navAdminBtn" style="display: none;" onclick="switchPortalTab('admin');">
            <span class="material-symbols-outlined text-[16px]">admin_panel_settings</span> Admin CMS
          </button>
          <button class="inline-flex items-center gap-1 text-[12.5px] font-medium bg-primary-dark text-white px-3.5 py-1.5 rounded-full hover:bg-primary-emerald" onclick="switchPortalTab('dashboard');">
            <span class="material-symbols-outlined text-[16px]">dashboard</span> Member Portal
          </button>
          <button class="inline-flex items-center text-[12.5px] font-medium text-text-muted hover:text-text-main px-2 py-1" onclick="handleLogout();">
            Logout
          </button>
        </div>

        <!-- Mobile Hamburger Button -->
        <button class="mobile-nav-toggle md:hidden p-2 rounded-full hover:bg-surface-subtle text-text-main transition-colors flex items-center justify-center" id="mobileNavToggle" aria-label="Toggle navigation menu" aria-expanded="false" onclick="toggleMobileNav()">
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
          <button class="w-full py-2.5 rounded-full bg-primary-dark text-white text-[13.5px] font-medium" onclick="openShowInterestModal(); closeMobileNav();">Show Interest →</button>
          <button class="w-full py-2.5 rounded-full border border-card-border text-text-main text-[13.5px] font-medium" onclick="openLoginModal(); closeMobileNav();">Member Login</button>
        </li>
      </ul>
    </div>
  </header>

  <!-- PUBLIC HOMEPAGE CONTENT -->
  <div id="publicPage">

    <!-- SECTION 1: HERO (Stitch Screen 13 Editorial Layout) -->
    <section class="relative w-full overflow-hidden pt-8 pb-16 lg:pt-14 lg:pb-24 border-b border-card-border/50 bg-[#FAF8F5]" id="home">
      <div class="max-w-7xl mx-auto px-6 lg:px-12">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          <!-- Left Column Content -->
          <div class="lg:col-span-6 flex flex-col justify-center">
            <div class="hero-pill-badge inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/80 border border-card-border/80 text-[12px] text-text-muted mb-4 shadow-sm w-fit">
              <span class="w-2 h-2 rounded-full bg-primary-dark"></span>
              <span class="pill-text" id="heroBadge">CURATED FOUNDER NETWORK • BY APPLICATION ONLY</span>
            </div>
            <h1 class="font-serif text-4xl sm:text-5xl lg:text-[62px] text-text-main leading-[1.08] tracking-[-0.02em] font-normal" id="heroTitle">
              Beyond Networking.<br/>
              Into Real Connections.
            </h1>
            <p class="font-sans text-[15px] sm:text-[16px] text-text-muted mt-5 max-w-lg leading-relaxed" id="heroSubtitle">
              Founder for Founder brings ambitious entrepreneurs, business owners, and professionals into one curated network across India. By application only.
            </p>
            <!-- Buttons -->
            <div class="flex flex-wrap items-center gap-4 mt-7">
              <button class="inline-flex items-center gap-2 bg-primary-dark hover:bg-primary-emerald text-white text-[13.5px] font-medium px-6 py-3 rounded-full transition-all shadow-sm" onclick="openShowInterestModal()">
                <span>Show Interest</span>
                <span class="text-base leading-none">→</span>
              </button>
              <a class="inline-flex items-center gap-2 text-[13.5px] font-medium text-text-main hover:text-primary-dark transition-colors" href="#experiences">
                <span>Explore Experiences</span>
                <span class="text-base leading-none">→</span>
              </a>
            </div>
            <!-- Metrics with vertical divider -->
            <div class="flex items-center gap-8 mt-12 pt-6 border-t border-card-border/70 max-w-sm">
              <div class="flex flex-col">
                <span class="font-serif text-3xl lg:text-4xl font-semibold text-text-main tracking-tight" id="counterMembers">1528+</span>
                <span class="text-[12px] text-text-subtle mt-0.5 tracking-wide">Members</span>
              </div>
              <div class="h-10 w-[1px] bg-card-border"></div>
              <div class="flex flex-col">
                <span class="font-serif text-3xl lg:text-4xl font-semibold text-text-main tracking-tight" id="counterEvents">27</span>
                <span class="text-[12px] text-text-subtle mt-0.5 tracking-wide">Curated Gatherings</span>
              </div>
            </div>
          </div>
          <!-- Right Column Visual (Warm founder coffee laptop setting) -->
          <div class="lg:col-span-6 relative">
            <div class="relative w-full aspect-[4/3] sm:aspect-[14/10] rounded-2xl overflow-hidden shadow-sm border border-card-border/60">
              <img alt="Founder workspace coffee terrace" class="w-full h-full object-cover" id="heroCapsule1" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBQOGkFg7WlUWSrH99zAr_NpVfxigqQdvK1JXSl3dRMsAah88IIJNAhSx8OtC4DKo9EJqPKrthaRiIpLyqt_xcOwaZP62w7cSPmLdKivLOoQd09W35SQpnkWSfEWVisoyktKg1Orkg8BptmZwIKPc3y1r-4ghvDAecJkMjxHFDzIQYE2O1zppL4xfqRP3baviEwS-40bNBYfBFV6PFSQ0z7D12zfeBHWQ_3r5oCcjVYX2-bGarNL6J7"/>
              <div class="absolute inset-0 bg-gradient-to-tr from-black/40 via-transparent to-transparent"></div>
              <!-- Subtle Green Mug Overlay Replica Graphic on Mug -->
              <div class="absolute bottom-6 right-6 bg-primary-emerald/90 backdrop-blur-md text-white p-3.5 rounded-xl border border-white/10 shadow-lg text-right max-w-[170px]">
                <div class="font-serif italic text-[11px] text-[#A7F3D0] leading-none mb-1">Founder for Founder</div>
                <p class="font-sans text-[11.5px] leading-tight text-white/90">Create. Connect. Collaborate.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 2: CONNECTED BUSINESSES (Continuous Marquee) -->
    <section class="w-full bg-[#FAF8F5] py-5 overflow-hidden border-b border-card-border/60">
      <div class="animate-marquee items-center gap-10 whitespace-nowrap text-[12px] uppercase tracking-widest text-text-subtle font-medium">
        <span class="inline-flex items-center gap-8">
          <span>Apex Global Tech</span><span class="text-[9px] opacity-40">✦</span>
          <span>Precision Industries</span><span class="text-[9px] opacity-40">✦</span>
          <span>Elevate Digital</span><span class="text-[9px] opacity-40">✦</span>
          <span>Quantum Manufacturing</span><span class="text-[9px] opacity-40">✦</span>
          <span>Horizon Logistics</span><span class="text-[9px] opacity-40">✦</span>
          <span>Starlight Hospitality</span><span class="text-[9px] opacity-40">✦</span>
          <span>Venture Crest Advisors</span><span class="text-[9px] opacity-40">✦</span>
          <span>Omni Retail Ventures</span><span class="text-[9px] opacity-40">✦</span>
        </span>
        <span class="inline-flex items-center gap-8 ml-8">
          <span>Apex Global Tech</span><span class="text-[9px] opacity-40">✦</span>
          <span>Precision Industries</span><span class="text-[9px] opacity-40">✦</span>
          <span>Elevate Digital</span><span class="text-[9px] opacity-40">✦</span>
          <span>Quantum Manufacturing</span><span class="text-[9px] opacity-40">✦</span>
          <span>Horizon Logistics</span><span class="text-[9px] opacity-40">✦</span>
          <span>Starlight Hospitality</span><span class="text-[9px] opacity-40">✦</span>
          <span>Venture Crest Advisors</span><span class="text-[9px] opacity-40">✦</span>
          <span>Omni Retail Ventures</span><span class="text-[9px] opacity-40">✦</span>
        </span>
      </div>
    </section>

    <!-- SECTION 3: WHAT WE OFFER / ABOUT -->
    <section class="w-full py-16 lg:py-24 max-w-7xl mx-auto px-6 lg:px-12" id="about">
      <!-- Section Title with Editorial Line -->
      <div class="flex items-center gap-6 mb-12">
        <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight">What We Offer</h2>
        <div class="h-[1px] flex-1 bg-card-border"></div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Card 1 -->
        <div class="border-l border-card-border pl-5 flex flex-col justify-between py-1">
          <div>
            <h3 class="font-serif text-[19px] font-medium text-text-main leading-snug">
              Curated Founder<br/>Circle
            </h3>
            <p class="font-sans text-[13.5px] text-text-muted mt-3 leading-relaxed">
              Meaningful connections with like-minded builders.
            </p>
          </div>
        </div>
        <!-- Card 2 -->
        <div class="border-l border-card-border pl-5 flex flex-col justify-between py-1">
          <div>
            <h3 class="font-serif text-[19px] font-medium text-text-main leading-snug">
              Shared<br/>Experiences
            </h3>
            <p class="font-sans text-[13.5px] text-text-muted mt-3 leading-relaxed">
              From sports to dining, explore together.
            </p>
          </div>
        </div>
        <!-- Card 3 -->
        <div class="border-l border-card-border pl-5 flex flex-col justify-between py-1">
          <div>
            <h3 class="font-serif text-[19px] font-medium text-text-main leading-snug">
              Needs &amp; Wants<br/>Engine
            </h3>
            <p class="font-sans text-[13.5px] text-text-muted mt-3 leading-relaxed">
              Find what you need. Offer what you have.
            </p>
          </div>
        </div>
        <!-- Card 4 -->
        <div class="border-l border-card-border pl-5 flex flex-col justify-between py-1">
          <div>
            <h3 class="font-serif text-[19px] font-medium text-text-main leading-snug">
              Leads &amp;<br/>Introductions
            </h3>
            <p class="font-sans text-[13.5px] text-text-muted mt-3 leading-relaxed">
              Open doors to the right people and opportunities.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 4: PLATFORM FEATURES (Interactive Minimal Tabs) -->
    <section class="w-full py-12 bg-[#F6F3ED] border-y border-card-border/60">
      <div class="max-w-7xl mx-auto px-6 lg:px-12">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-8">
          <div>
            <span class="text-[11px] font-bold uppercase tracking-widest text-primary-dark">Platform Architecture</span>
            <h3 class="font-serif text-2xl sm:text-3xl text-text-main font-normal mt-1">Structured For Active Value</h3>
          </div>
          <!-- Tabs Navigation Pills -->
          <div class="flex flex-wrap gap-2 mt-4 md:mt-0" id="platform-tabs">
            <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-primary-dark text-white active" onclick="setStitchTab(0, this)">Curated Network</button>
            <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(1, this)">Needs &amp; Wants</button>
            <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(2, this)">Leads CRM</button>
            <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(3, this)">Experiences</button>
            <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(4, this)">Collaborations</button>
            <button class="tab-btn px-4 py-1.5 rounded-full text-[12.5px] font-medium transition-all bg-white text-text-muted border border-card-border hover:text-text-main" onclick="setStitchTab(5, this)">Challenges</button>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 lg:p-8 border border-card-border/80 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6" id="feature-box">
          <div class="max-w-2xl">
            <span class="text-[11px] uppercase tracking-widest text-gold-accent font-semibold block mb-1" id="feature-label">MODULE 01 • CURATION</span>
            <h4 class="font-serif text-2xl text-text-main font-medium mb-2" id="feature-title">Curated Founder Network</h4>
            <p class="font-sans text-[14px] text-text-muted leading-relaxed" id="feature-desc">Connect with verified founders and decision-makers in a high-trust, clutter-free environment designed for meaningful business growth.</p>
          </div>
          <div class="flex items-center gap-3">
            <button class="inline-flex items-center gap-1.5 bg-primary-dark hover:bg-primary-emerald text-white text-[12.5px] font-medium px-4 py-2 rounded-full transition-all" onclick="openShowInterestModal()">
              <span>Access Cohort</span>
              <span class="text-base leading-none">→</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: EXPERIENCES (Photo Carousel matching Reference) -->
    <section class="w-full py-16 lg:py-24 max-w-7xl mx-auto px-6 lg:px-12" id="experiences">
      <!-- Section Title with Editorial Line -->
      <div class="flex items-center justify-between gap-6 mb-10">
        <div class="flex items-center gap-6 flex-1">
          <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight">Experiences</h2>
          <div class="h-[1px] flex-1 bg-card-border hidden sm:block"></div>
        </div>
        <!-- Carousel Nav Buttons -->
        <div class="flex items-center gap-2">
          <button aria-label="Previous slide" class="w-9 h-9 rounded-full border border-card-border flex items-center justify-center text-text-main hover:bg-white transition-colors" onclick="scrollExperiences('left')">
            <span class="material-symbols-outlined text-[18px]">chevron_left</span>
          </button>
          <button aria-label="Next slide" class="w-9 h-9 rounded-full border border-card-border flex items-center justify-center text-text-main hover:bg-white transition-colors" onclick="scrollExperiences('right')">
            <span class="material-symbols-outlined text-[18px]">chevron_right</span>
          </button>
        </div>
      </div>
      <!-- Experience Cards Scroll Track -->
      <div class="flex gap-5 overflow-x-auto pb-4 scroll-smooth snap-x" id="experiences-track" style="scrollbar-width: none; -ms-overflow-style: none;">
        <!-- 1: Play Together -->
        <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-white rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
          <div class="h-44 w-full overflow-hidden bg-surface-subtle">
            <img alt="Play Together - Pickleball / Padel" id="formatImgPlay" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBVZvQ8mvPxjjMTjLrF6-VqxIN0JEH2LYfuTgdcdGk8PvQJyiu2u5oUtJijFilpwAZABufmCOZ06UT57PQqBGEKg1-9OMd-FRWPy29OF454SI1Ln-aaI9CEglLaVMReFz2gQ03uy4ow09oEq5zXUjdalnL-7FSNgARVaL5qOVsGy11qfvzW63V6icp4B0-nVZYF19XZFsC63s9ZAMvAZiIyVtOHp0EXxr4_1ZbrkQpBaEiN3iParP9H"/>
          </div>
          <div class="p-4 flex flex-col justify-between">
            <h3 class="font-serif text-[17px] font-medium text-text-main">Play Together</h3>
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
              <span class="text-[12px] text-text-subtle font-sans">Sports</span>
              <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </div>
        <!-- 2: Explore Together -->
        <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-white rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
          <div class="h-44 w-full overflow-hidden bg-surface-subtle">
            <img alt="Explore Together - Outdoor Trail & Hiking" id="formatImgExplore" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCw3xI8RlZpWZZ17uYgNPXasB04r1wJ0whnybywimVFdwREr2rr3DDSLYUulOUtaIVmEF80MqZbw10LmTsFrhl3rXyBNL72LAzwCDpNJJneZqJPTPRSkhlKzAiFKS0Tn1iRRN8nO65zy6XqDSx0PbtzudO-cEaeOigNSihGIOw_GdwmVBTeL7A0Cm4M1Z1dGv29lhLSDdtXG_2o5S3MccxG6bZxfslS2BnVSCHvd5UxkkZiTjyt0-6q"/>
          </div>
          <div class="p-4 flex flex-col justify-between">
            <h3 class="font-serif text-[17px] font-medium text-text-main">Explore Together</h3>
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
              <span class="text-[12px] text-text-subtle font-sans">Outdoors</span>
              <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </div>
        <!-- 3: Dine Together -->
        <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-white rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
          <div class="h-44 w-full overflow-hidden bg-surface-subtle">
            <img alt="Dine Together - Curated Founder Dinner" id="formatImgDine" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCBen8o-u4_a_KNZnmBPSlcSQkQnSlXVC-0qrB9AuScyPbRygpxb68mYWNoCy69eIlaNxi6FkrV7mJfwh3bUsuRLj84Od-p6BleYqSdJMRF79MsyY8pxbZwLS29Vp5e3DPlSRjeCYCtSUdxKbFOF4f26E9pgbmVgDz4jPROhIk2cqPzRgfkpEi-8iE7obRt1sv15_o7XqKE-PVrJM6xGmFN9_Tqsr5pAQOE7HF_VtMpZVUT8aD9EZn6"/>
          </div>
          <div class="p-4 flex flex-col justify-between">
            <h3 class="font-serif text-[17px] font-medium text-text-main">Dine Together</h3>
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
              <span class="text-[12px] text-text-subtle font-sans">Dining</span>
              <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </div>
        <!-- 4: Build Together -->
        <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-white rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
          <div class="h-44 w-full overflow-hidden bg-surface-subtle">
            <img alt="Build Together - Roundtable advisory" id="formatImgBuild" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDN0pvVm_B1pcvX3C1p41zAEVv0F7UOI4ZTEugE8UJNnDeu5eNbAPsWH_IRBeMTTrBdA1Zpcf2ZypCbINRgud_0WaGY9LhRanEqZLYWkrdklcms6PyKaBzR6EiAgA4rYlrNQ-aPnPLdocN7UEYfEq2eAVjX5vKcMzASL9PbNdFccHCH-3vD01dWm7WYDmctJQmiJRSbwgyZ7oPtz252aZQLyRXIxBYIhzTXyU4bbmWRw5KNEMp02I-u"/>
          </div>
          <div class="p-4 flex flex-col justify-between">
            <h3 class="font-serif text-[17px] font-medium text-text-main">Build Together</h3>
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
              <span class="text-[12px] text-text-subtle font-sans">Advisory</span>
              <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </div>
        <!-- 5: Celebrate Together -->
        <div class="snap-start flex-shrink-0 w-60 sm:w-64 bg-white rounded-xl border border-card-border/80 overflow-hidden group hover:shadow-md transition-shadow">
          <div class="h-44 w-full overflow-hidden bg-surface-subtle">
            <img alt="Celebrate Together - Social Gathering" id="formatImgCelebrate" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDMlhWLkz1P-mAPBK0gUIwbxPJcntsb_nuq1ISYkf94RDSh48oieYKwAMHeik8gD0Ev1u5UN-XgFp8CYopUvicZNBFwYnZ3sV9DL43PO02Ra8X0ENCaaSr2YHl121PlGI1_CAUaRP9E9uB33aoy9A-fhPPa1fn4ODQSR0o8gSOldIdnFRVHcVu-WJYsMtsdrx5u91M5OrNIuFwVbWfIO9F_ap7LdiFrLl6PmOLMCmy7I5ecoUoXXNBQ"/>
          </div>
          <div class="p-4 flex flex-col justify-between">
            <h3 class="font-serif text-[17px] font-medium text-text-main">Celebrate Together</h3>
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-card-border/40">
              <span class="text-[12px] text-text-subtle font-sans">Socials</span>
              <span class="text-[14px] text-text-main group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Upcoming Dynamic Events Grid if populated from Database -->
      <div id="upcomingEventsGrid" class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    </section>

    <!-- SECTION 7 & 11: HOW TO JOIN & FAQ SPLIT LAYOUT -->
    <section class="w-full py-16 lg:py-24 border-t border-card-border/60" id="how-it-works">
      <div class="max-w-7xl mx-auto px-6 lg:px-12">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
          <!-- LEFT COLUMN: How To Join Vertical Timeline -->
          <div class="lg:col-span-5 flex flex-col">
            <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight mb-8">
              How To Join
            </h2>
            <!-- Timeline sequence -->
            <div class="relative pl-6 space-y-7 before:absolute before:left-[7px] before:top-2 before:bottom-3 before:w-[1px] before:bg-card-border timeline-container">
              <!-- 01 -->
              <div class="relative flex items-start gap-4">
                <span class="absolute -left-[27px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary-dark ring-4 ring-[#FAF8F5]"></span>
                <span class="font-serif text-[15px] font-semibold text-text-main">01</span>
                <div>
                  <h4 class="font-sans font-semibold text-[14px] text-text-main">Show Interest</h4>
                  <p class="font-sans text-[13px] text-text-subtle mt-0.5">Fill in the application form.</p>
                </div>
              </div>
              <!-- 02 -->
              <div class="relative flex items-start gap-4">
                <span class="absolute -left-[27px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary-dark ring-4 ring-[#FAF8F5]"></span>
                <span class="font-serif text-[15px] font-semibold text-text-main">02</span>
                <div>
                  <h4 class="font-sans font-semibold text-[14px] text-text-main">Profile Screening</h4>
                  <p class="font-sans text-[13px] text-text-subtle mt-0.5">We review your background and intent.</p>
                </div>
              </div>
              <!-- 03 -->
              <div class="relative flex items-start gap-4">
                <span class="absolute -left-[27px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary-dark ring-4 ring-[#FAF8F5]"></span>
                <span class="font-serif text-[15px] font-semibold text-text-main">03</span>
                <div>
                  <h4 class="font-sans font-semibold text-[14px] text-text-main">Application Review</h4>
                  <p class="font-sans text-[13px] text-text-subtle mt-0.5">Our team evaluates your application.</p>
                </div>
              </div>
              <!-- 04 -->
              <div class="relative flex items-start gap-4">
                <span class="absolute -left-[27px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary-dark ring-4 ring-[#FAF8F5]"></span>
                <span class="font-serif text-[15px] font-semibold text-text-main">04</span>
                <div>
                  <h4 class="font-sans font-semibold text-[14px] text-text-main">Receive Invitation</h4>
                  <p class="font-sans text-[13px] text-text-subtle mt-0.5">Get notified about your selection.</p>
                </div>
              </div>
              <!-- 05 -->
              <div class="relative flex items-start gap-4">
                <span class="absolute -left-[27px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary-dark ring-4 ring-[#FAF8F5]"></span>
                <span class="font-serif text-[15px] font-semibold text-text-main">05</span>
                <div>
                  <h4 class="font-sans font-semibold text-[14px] text-text-main">Activate Membership</h4>
                  <p class="font-sans text-[13px] text-text-subtle mt-0.5">Complete the onboarding process.</p>
                </div>
              </div>
              <!-- 06 -->
              <div class="relative flex items-start gap-4">
                <span class="absolute -left-[27px] top-1.5 w-2.5 h-2.5 rounded-full bg-primary-dark ring-4 ring-[#FAF8F5]"></span>
                <span class="font-serif text-[15px] font-semibold text-text-main">06</span>
                <div>
                  <h4 class="font-sans font-semibold text-[14px] text-text-main">Connect &amp; Collaborate</h4>
                  <p class="font-sans text-[13px] text-text-subtle mt-0.5">Be part of meaningful conversations and opportunities.</p>
                </div>
              </div>
            </div>
          </div>
          <!-- RIGHT COLUMN: FAQ with View All and Accordion -->
          <div class="lg:col-span-7 flex flex-col" id="faq">
            <div class="flex items-center justify-between mb-8">
              <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight">
                FAQ
              </h2>
              <a class="inline-flex items-center gap-1 text-[13px] font-medium text-text-main hover:text-primary-dark transition-colors" href="#faq">
                <span>View all</span>
                <span>→</span>
              </a>
            </div>
            <!-- FAQ Accordion Container -->
            <div class="space-y-3" id="faqContainer">
              <!-- Item 1 -->
              <div class="faq-node bg-white rounded-xl border border-card-border/80 overflow-hidden">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-sans font-medium text-[14.5px] text-text-main">What is Founder for Founder?</span>
                  <span class="material-symbols-outlined text-[19px] text-text-subtle transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 text-[13.5px] text-text-muted leading-relaxed border-t border-card-border/40 pt-3">
                  Founder for Founder is a vetted pan-India business collective. Instead of superficial business card exchanges, we facilitate peer advisory roundtables, shared active experiences, and a structured Needs &amp; Wants marketplace.
                </div>
              </div>
              <!-- Item 2 -->
              <div class="faq-node bg-white rounded-xl border border-card-border/80 overflow-hidden">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-sans font-medium text-[14.5px] text-text-main">Who can apply?</span>
                  <span class="material-symbols-outlined text-[19px] text-text-subtle transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 text-[13.5px] text-text-muted leading-relaxed border-t border-card-border/40 pt-3">
                  Founders, Co-founders, Managing Directors, enterprise business owners, and active CXO leaders with operating businesses across India can apply.
                </div>
              </div>
              <!-- Item 3 -->
              <div class="faq-node bg-white rounded-xl border border-card-border/80 overflow-hidden">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-sans font-medium text-[14.5px] text-text-main">What kind of businesses are included?</span>
                  <span class="material-symbols-outlined text-[19px] text-text-subtle transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 text-[13.5px] text-text-muted leading-relaxed border-t border-card-border/40 pt-3">
                  Our community spans high-growth tech startups, industrial manufacturing, D2C brands, supply chain enterprises, real estate developers, and specialized professional firms.
                </div>
              </div>
              <!-- Item 4 -->
              <div class="faq-node bg-white rounded-xl border border-card-border/80 overflow-hidden">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-sans font-medium text-[14.5px] text-text-main">Is there a membership fee?</span>
                  <span class="material-symbols-outlined text-[19px] text-text-subtle transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 text-[13.5px] text-text-muted leading-relaxed border-t border-card-border/40 pt-3">
                  Yes, approved candidates receive an invitation link detailing our annual membership tiers, which cover curated gatherings, private retreats, and platform directory access.
                </div>
              </div>
              <!-- Item 5 -->
              <div class="faq-node bg-white rounded-xl border border-card-border/80 overflow-hidden">
                <button class="w-full px-5 py-4 text-left flex items-center justify-between gap-4" onclick="toggleFaqRef(this)">
                  <span class="font-sans font-medium text-[14.5px] text-text-main">How do I stay updated about events?</span>
                  <span class="material-symbols-outlined text-[19px] text-text-subtle transition-transform duration-200">add</span>
                </button>
                <div class="faq-content hidden px-5 pb-4 text-[13.5px] text-text-muted leading-relaxed border-t border-card-border/40 pt-3">
                  Members receive calendar invites, WhatsApp updates for chapter meetups, and can RSVP directly through the Member Portal.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 8: ACTIVE COMMUNITY NEEDS & WANTS (Opportunity Preview) -->
    <section class="w-full py-16 bg-[#FAF8F5] border-t border-card-border/60" id="needs-wants">
      <div class="max-w-7xl mx-auto px-6 lg:px-12">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
          <div>
            <span class="text-[11px] font-bold uppercase tracking-widest text-primary-dark">INTERNAL EXCHANGE</span>
            <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight mt-1">Active Community Needs &amp; Offers</h2>
          </div>
          <button class="inline-flex items-center gap-1.5 text-[13px] font-semibold text-primary-dark hover:underline" onclick="openShowInterestModal()">
            <span>+ Post a Need / Offer</span>
            <span>→</span>
          </button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="needsPreviewContainer">
          <!-- Requirements -->
          <div class="bg-white rounded-xl p-6 border border-card-border/80 shadow-sm">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-card-border/60">
              <span class="w-2 h-2 rounded-full bg-red-600"></span>
              <span class="text-[11px] font-bold tracking-widest uppercase text-text-main">I NEED (REQUIREMENTS)</span>
            </div>
            <div class="space-y-3">
              <div class="p-3.5 bg-[#FAF8F5] rounded-lg border border-card-border/40">
                <span class="text-[10px] text-text-subtle uppercase tracking-wider block mb-1">MANUFACTURING</span>
                <p class="text-[13.5px] font-medium text-text-main">High-volume manufacturing partner for precision components</p>
                <span class="text-[11.5px] text-text-subtle mt-1 block">Pan-India scale • Verified RFQ posted by MD Member</span>
              </div>
              <div class="p-3.5 bg-[#FAF8F5] rounded-lg border border-card-border/40">
                <span class="text-[10px] text-text-subtle uppercase tracking-wider block mb-1">TECHNOLOGY</span>
                <p class="text-[13.5px] font-medium text-text-main">Enterprise SaaS growth marketing advisor &amp; partner</p>
                <span class="text-[11.5px] text-text-subtle mt-1 block">Series A B2B firm • Direct peer recommendation sought</span>
              </div>
            </div>
          </div>
          <!-- Offers -->
          <div class="bg-white rounded-xl p-6 border border-card-border/80 shadow-sm">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-card-border/60">
              <span class="w-2 h-2 rounded-full bg-primary-dark"></span>
              <span class="text-[11px] font-bold tracking-widest uppercase text-text-main">I CAN HELP WITH (OFFERS)</span>
            </div>
            <div class="space-y-3">
              <div class="p-3.5 bg-[#FAF8F5] rounded-lg border border-card-border/40">
                <span class="text-[10px] text-text-subtle uppercase tracking-wider block mb-1">GLOBAL EXPANSION</span>
                <p class="text-[13.5px] font-medium text-text-main">Direct introductions to SEA retail distribution heads</p>
                <span class="text-[11.5px] text-text-subtle mt-1 block">Singapore &amp; Dubai • Offered by FMCG Founder</span>
              </div>
              <div class="p-3.5 bg-[#FAF8F5] rounded-lg border border-card-border/40">
                <span class="text-[10px] text-text-subtle uppercase tracking-wider block mb-1">CAPITAL ALLOCATION</span>
                <p class="text-[13.5px] font-medium text-text-main">Institutional debt structuring &amp; working capital credit lines</p>
                <span class="text-[11.5px] text-text-subtle mt-1 block">Fintech Leader • Direct advisory for verified members</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 9: COMMUNITY PERSPECTIVES / TESTIMONIALS -->
    <section class="w-full py-16 bg-[#F8F5EE] border-t border-card-border/60" id="community">
      <div class="max-w-7xl mx-auto px-6 lg:px-12">
        <div class="max-w-2xl mb-10">
          <span class="text-[11px] font-bold uppercase tracking-widest text-primary-dark">MEMBER STORIES</span>
          <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight mt-1">Founder Perspectives</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="testimonialsContainer">
          <div class="bg-white rounded-xl p-6 border border-card-border/80 shadow-sm flex flex-col justify-between">
            <p class="font-serif italic text-[15px] text-text-main leading-relaxed">
              "Traditional networking events yield business cards; shared experiences build lasting relationships. Founder for Founder creates spaces where ambitious minds connect with purpose."
            </p>
            <div class="mt-6 pt-4 border-t border-card-border/50">
              <h4 class="font-sans font-semibold text-[13.5px] text-text-main">Ananya Verma</h4>
              <span class="text-[11.5px] text-text-subtle">Founder &amp; CEO, Elevate Digital</span>
            </div>
          </div>
          <div class="bg-white rounded-xl p-6 border border-card-border/80 shadow-sm flex flex-col justify-between">
            <p class="font-serif italic text-[15px] text-text-main leading-relaxed">
              "The Needs &amp; Wants engine alone unlocked two credible manufacturing suppliers within our first month. The signal-to-noise ratio here is unmatched in India."
            </p>
            <div class="mt-6 pt-4 border-t border-card-border/50">
              <h4 class="font-sans font-semibold text-[13.5px] text-text-main">Rajesh Patel</h4>
              <span class="text-[11.5px] text-text-subtle">Managing Director, Quantum Manufacturing</span>
            </div>
          </div>
          <div class="bg-white rounded-xl p-6 border border-card-border/80 shadow-sm flex flex-col justify-between">
            <p class="font-serif italic text-[15px] text-text-main leading-relaxed">
              "Playing padel at 7 AM followed by frank conversations on enterprise sales barriers with founders who run 50+ crore businesses is priceless leverage."
            </p>
            <div class="mt-6 pt-4 border-t border-card-border/50">
              <h4 class="font-sans font-semibold text-[13.5px] text-text-main">Vikramaditya Rao</h4>
              <span class="text-[11.5px] text-text-subtle">Co-Founder, Horizon Logistics</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CURATED MEETING PHOTOS SLIDER (16:9 RATIO - CONTINUOUS RIGHT-TO-LEFT SLIDE) -->
    <section class="w-full py-16 bg-[#FAF8F5] border-t border-card-border/60" id="meetingPhotosSection" style="display: none;">
      <div class="max-w-7xl mx-auto px-6 lg:px-12 mb-8">
        <span class="text-[11px] font-bold uppercase tracking-widest text-primary-dark">FOUNDER INTERACTIONS • MOMENTS OF LEVERAGE</span>
        <h2 class="font-serif text-3xl sm:text-4xl text-text-main font-normal tracking-tight mt-1">Curated Gatherings &amp; Meeting Moments</h2>
        <p class="font-sans text-[14px] text-text-muted mt-2 max-w-2xl leading-relaxed">High-trust peer dialogues, confidential executive roundtables, private dinners, and strategic collaboration sessions captured across India.</p>
      </div>
      <div class="meeting-slider-wrapper overflow-hidden px-6 lg:px-12 max-w-7xl mx-auto">
        <div class="meeting-slider-track flex gap-4 overflow-x-auto" id="meetingPhotosTrack">
          <!-- Populated dynamically from CMS / Database -->
        </div>
      </div>
    </section>

    <!-- SECTION 10: CLOSING BANNER CTA -->
    <section class="w-full py-14 lg:py-20 px-6 lg:px-12 bg-[#FAF8F5] border-t border-card-border/60">
      <div class="max-w-7xl mx-auto">
        <div class="relative bg-[#EAE5DA]/70 border border-[#DDD6C8] rounded-2xl p-10 lg:p-16 text-center overflow-hidden">
          <div class="absolute left-6 top-6 bottom-6 w-[1px] bg-card-border hidden sm:block"></div>
          <div class="absolute left-9 top-8 bottom-8 w-[1px] bg-card-border hidden sm:block"></div>
          <div class="absolute right-6 top-6 bottom-6 w-[1px] bg-card-border hidden sm:block"></div>
          <div class="absolute right-9 top-8 bottom-8 w-[1px] bg-card-border hidden sm:block"></div>
          <div class="max-w-2xl mx-auto relative z-10 flex flex-col items-center">
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-text-main leading-tight tracking-tight">
              Your next meaningful business<br class="hidden sm:block"/> connection starts here.
            </h2>
            <div class="mt-8">
              <button class="inline-flex items-center gap-2 bg-primary-dark hover:bg-primary-emerald text-white text-[13.5px] font-medium px-7 py-3.5 rounded-full transition-all shadow-md" onclick="openShowInterestModal()">
                <span>Show Interest</span>
                <span class="text-base leading-none">→</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 12: FOOTER (Replicating Stitch Reference Exactly) -->
    <footer class="w-full bg-[#FAF8F5] border-t border-card-border/70 py-12" id="contact">
      <div class="max-w-7xl mx-auto px-6 lg:px-12">
        <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">
          <!-- Left: Logo & Motto -->
          <div class="flex flex-col">
            <div class="flex items-center gap-3">
              <img src="/assets/logo.svg" alt="Founder for Founder Logo" class="w-7 h-7 rounded-full object-cover" id="footerLogo" width="28" height="28" loading="lazy">
              <span class="font-serif font-bold text-2xl text-primary-dark tracking-tight">F4F</span>
              <div class="h-6 w-[1px] bg-card-border"></div>
              <div class="flex flex-col leading-none">
                <span class="font-serif text-[14px] font-medium text-text-main">Founder</span>
                <span class="font-serif text-[14px] font-medium text-text-main">for Founder</span>
              </div>
            </div>
            <p class="text-[12px] text-text-subtle mt-2 font-sans">Create. Connect. Collaborate. • Powered by <strong>snalts.co</strong></p>
          </div>
          <!-- Middle: Contact Email & Legal Links -->
          <div class="flex flex-col sm:flex-row sm:items-center gap-6 sm:gap-10 text-[13px] text-text-muted">
            <a class="inline-flex items-center gap-2 text-text-main hover:text-primary-dark transition-colors" href="mailto:connect.f4f@gmail.com">
              <svg class="w-4 h-4 text-text-subtle" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"></path>
              </svg>
              <span>connect.f4f@gmail.com</span>
            </a>
            <div class="flex flex-wrap items-center gap-4 text-text-subtle">
              <a class="hover:text-text-main transition-colors" href="/terms">Terms</a>
              <span>•</span>
              <a class="hover:text-text-main transition-colors" href="/privacy-policy">Privacy</a>
              <span>•</span>
              <a class="hover:text-text-main transition-colors" href="/refund-policy">Refund Policy</a>
              <span>•</span>
              <a class="hover:text-text-main transition-colors" href="/community-guidelines">Community Guidelines</a>
            </div>
          </div>
          <!-- Right: Socials & Powered by -->
          <div class="flex items-center gap-6 text-[13px] text-text-subtle">
            <div class="flex items-center gap-3 text-text-main">
              <!-- Instagram -->
              <a aria-label="Instagram" class="hover:text-primary-dark transition-colors p-1.5 rounded-full hover:bg-surface-subtle" href="https://www.instagram.com/founder_for_founder" target="_blank" rel="noopener noreferrer">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"></path></svg>
              </a>
              <!-- Facebook -->
              <a aria-label="Facebook" class="hover:text-primary-dark transition-colors p-1.5 rounded-full hover:bg-surface-subtle" href="https://www.facebook.com/share/19ZnPNuhPb/" target="_blank" rel="noopener noreferrer">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M9 8H6v4h3v12h5V12h3.642L18 8h-4V6.333C14 5.374 14.5 5 15.667 5H18V0h-3.808C10.595 0 9 1.583 9 4.615V8z"></path></svg>
              </a>
              <!-- LinkedIn -->
              <a aria-label="LinkedIn" class="hover:text-primary-dark transition-colors p-1.5 rounded-full hover:bg-surface-subtle" href="https://www.linkedin.com/company/founder-for-founder/" target="_blank" rel="noopener noreferrer">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"></path></svg>
              </a>
            </div>
          </div>
        </div>
        <div class="mt-8 pt-6 border-t border-card-border/60 text-center text-[12px] text-text-subtle">
          &copy; 2026 Founder for Founder. All rights reserved. Powered by snalts.co
        </div>
      </div>
    </footer>
  </div>'''

    # Pattern from scrollProgressBar / navbar up to portalPage
    # The original starts with <!-- 2px Emerald Scroll Progress Bar --> or <header class="navbar" id="mainNavbar">
    # and ends right before <!-- AUTHENTICATED MEMBER PORTAL & DASHBOARD -->
    pattern = r'<!-- 2px Emerald Scroll Progress Bar -->.*?(?=\s*<!-- AUTHENTICATED MEMBER PORTAL & DASHBOARD -->)'
    match = re.search(pattern, html, flags=re.DOTALL)
    if not match:
        print("Could not match the public surface pattern in public/index.html")
        return False

    html = html[:match.start()] + stitch_public_surface + '\n\n' + html[match.end():]

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("public/index.html successfully updated with Stitch Screen 13 public surface!")
    return True

if __name__ == '__main__':
    integrate()
