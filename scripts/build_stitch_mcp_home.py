import os
import re
import subprocess
from prepare_questionnaire import get_prepared_questionnaire

def build_home():
    # 1. Read Stitch MCP Home Desktop screen
    with open('stitch_mcp_export/html/b12ad31e7d8b4172af2f869e9eed8c5c_Founder for Founder _ Home _Desktop_.html', 'r', encoding='utf-8') as f:
        mcp_home = f.read()

    # 2. Remove any restrictive scroll styles from raw Stitch export & clean up characters
    mcp_home = mcp_home.replace('body{overscroll-behavior:none;}', '')
    mcp_home = mcp_home.replace('::-webkit-scrollbar{display:none;}', '')
    mcp_home = mcp_home.replace('\ufffd', '•')
    mcp_home = mcp_home.replace('01  Sports', '01 • Sports')
    mcp_home = mcp_home.replace('02  Outdoor', '02 • Outdoor')
    mcp_home = mcp_home.replace('03  Food', '03 • Food')
    mcp_home = mcp_home.replace('04  High-Trust', '04 • High-Trust')
    mcp_home = mcp_home.replace('05  Continuous', '05 • Continuous')
    mcp_home = mcp_home.replace('FOUNDER INTERACTIONS  MOMENTS', 'FOUNDER INTERACTIONS • MOMENTS')

    # 3. Get prepared Admissions Questionnaire HTML
    q_content = get_prepared_questionnaire()

    # 4. Read Authenticated Member Portal and other Modals from backup-stitch-redesign
    backup_index = subprocess.check_output(['git', 'show', 'backup-stitch-redesign:public/index.html']).decode('utf-8')

    portal_start = backup_index.find('<!-- AUTHENTICATED MEMBER PORTAL & DASHBOARD -->')
    if portal_start == -1:
        portal_start = backup_index.find('<div id="portalPage"')

    portal_end = backup_index.find('<!-- MODAL 1: SHOW INTEREST APPLICATION')
    if portal_end == -1:
        portal_end = backup_index.find('<div class="modal-overlay" id="showInterestModal"')

    # Remaining modals starting with appDetailModal
    modal2_start = backup_index.find('id="appDetailModal"')
    p_modal2 = backup_index.rfind('<!--', 0, modal2_start) if modal2_start != -1 else modal2_start

    modals_end = backup_index.find('<script src="/js/app.js')
    if modals_end == -1:
        modals_end = backup_index.find('<!-- SCRIPTS -->')

    portal_html = backup_index[portal_start:portal_end]
    other_modals = backup_index[p_modal2:modals_end]

    # 5. Enhance <head> with styles.css link, responsive meta, Material Symbols & robust animations
    head_insertion = '''
  <link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/css/styles.css">
  <style id="f4f-core-styles">
    /* Google Material Symbols Font Protection */
    .material-symbols-outlined,
    .material-symbols {
      font-family: 'Material Symbols Outlined' !important;
      font-weight: normal !important;
      font-style: normal !important;
      font-size: 24px;
      line-height: 1;
      letter-spacing: normal;
      text-transform: none;
      display: inline-block;
      white-space: nowrap;
      word-wrap: normal;
      direction: ltr;
      -webkit-font-feature-settings: 'liga' !important;
      font-feature-settings: 'liga' !important;
      -webkit-font-smoothing: antialiased !important;
      -moz-osx-font-smoothing: grayscale !important;
      font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
      vertical-align: middle;
      user-select: none;
    }

    /* Unblocked, Natural Window Scrolling */
    html {
      scroll-behavior: smooth !important;
      overflow-x: hidden !important;
      overflow-y: auto !important;
      -webkit-overflow-scrolling: touch !important;
      height: auto !important;
    }
    body {
      margin: 0 !important;
      padding: 0 !important;
      overflow-x: hidden !important;
      overflow-y: visible !important;
      position: relative !important;
      min-height: 100vh !important;
      overscroll-behavior-y: auto !important;
      background-color: transparent !important;
    }

    /* Fixed Static Textured Background Layer (Stationary while text and tabs scroll) */
    #static-textured-bg {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      width: 100vw !important;
      height: 100vh !important;
      z-index: -10 !important;
      pointer-events: none !important;
      overflow: hidden !important;
      background-color: #faf8ff;
      will-change: transform;
    }

    /* Foreground content, text, cards, and tabs scroll smoothly over the static background */
    main, section, #portalPage, #publicPage {
      position: relative;
      z-index: 1;
    }

    /* Executive Section Transparency for Visible Static Texture */
    #publicPage section.bg-surface-container-lowest,
    body > section.bg-surface-container-lowest {
      background-color: rgba(255, 255, 255, 0.82) !important;
      backdrop-filter: blur(2px);
      -webkit-backdrop-filter: blur(2px);
    }
    #publicPage section.bg-surface-container-low,
    body > section.bg-surface-container-low {
      background-color: rgba(242, 243, 255, 0.85) !important;
      backdrop-filter: blur(2px);
      -webkit-backdrop-filter: blur(2px);
    }
    /* Executive Guild Styled Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #f2f3ff;
    }
    ::-webkit-scrollbar-thumb {
      background: #064e3b;
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #003527;
    }

    /* Executive Guild Overrides & Modal Safety Guard */
    .portal-container { display: none !important; }
    .portal-container.active { display: flex !important; }
    
    .modal-overlay:not(.active) {
      display: none !important;
      pointer-events: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      z-index: -100 !important;
    }
    .modal-overlay.active {
      display: flex !important;
      pointer-events: auto !important;
      visibility: visible !important;
      opacity: 1 !important;
      z-index: 2000 !important;
    }
    .modal-overlay {
      transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), backdrop-filter 0.25s ease;
    }
    @keyframes modalScaleUp {
      0% {
        opacity: 0;
        transform: scale(0.96) translateY(12px);
      }
      100% {
        opacity: 1;
        transform: scale(1) translateY(0);
      }
    }
    .modal-overlay.active > div {
      animation: modalScaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Infinite Marquee Stream Animation */
    @keyframes continuousMarquee {
      0% {
        transform: translate3d(0, 0, 0);
      }
      100% {
        transform: translate3d(-50%, 0, 0);
      }
    }
    .animate-marquee-infinite {
      display: flex !important;
      width: max-content !important;
      animation: continuousMarquee 32s linear infinite !important;
      will-change: transform;
    }
    .animate-marquee-infinite:hover {
      animation-play-state: paused !important;
    }

    /* Interactive FAQ Accordion Animation */
    details summary {
      cursor: pointer;
      user-select: none;
    }
    details summary::-webkit-details-marker {
      display: none;
    }
    details summary .material-symbols-outlined {
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    details[open] summary .material-symbols-outlined {
      transform: rotate(180deg) !important;
    }
    details[open] p {
      animation: accordionFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes accordionFadeIn {
      from {
        opacity: 0;
        transform: translateY(-6px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    details[open] {
      border-color: rgba(6, 78, 59, 0.25) !important;
      box-shadow: 0 4px 16px -2px rgba(6, 78, 59, 0.08) !important;
    }

    /* Executive Guild Card Hover Lift */
    .hover-lift {
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease !important;
    }
    .hover-lift:hover {
      transform: translateY(-4px) !important;
      box-shadow: 0 12px 28px -6px rgba(6, 78, 59, 0.12), 0 4px 12px rgba(0, 0, 0, 0.04) !important;
    }

    /* Subtle Pulsing & Smooth Rotation */
    @keyframes subtlePulse {
      0%, 100% {
        transform: scale(1);
        opacity: 1;
      }
      50% {
        transform: scale(1.15);
        opacity: 0.85;
      }
    }
    .animate-pulse {
      animation: subtlePulse 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite !important;
    }
    @keyframes spinSmooth {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    .animate-spin {
      animation: spinSmooth 1s linear infinite !important;
    }

    /* Fade-in for form step transitions */
    @keyframes fadeInSlide {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in {
      animation: fadeInSlide 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Ensure Stitch typography */
    h1, h2, h3, .font-headline-hero, .font-headline-lg, .font-headline-md, .font-headline-sm {
      font-family: 'Domine', serif !important;
    }
    body, p, button, input, select, textarea, label, td, th,
    span:not(.material-symbols-outlined):not(.material-symbols) {
      font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    /* Executive Dark Footer with Pure White Text */
    footer {
      background: #002117 !important;
      color: #ffffff !important;
    }
    footer h1, footer h2, footer h3, footer h4,
    footer p, footer a, footer span, footer div, footer li {
      color: #ffffff !important;
    }
    footer a {
      color: rgba(255, 255, 255, 0.8) !important;
      transition: color 0.2s ease;
    }
    footer a:hover {
      color: #ffffff !important;
    }
    footer .text-secondary-fixed,
    footer .font-label-status {
      color: #6ffbbe !important;
    }
    footer .text-white\\/60 {
      color: rgba(255, 255, 255, 0.6) !important;
    }
    footer .text-white\\/70 {
      color: rgba(255, 255, 255, 0.7) !important;
    }
    footer .text-white\\/75 {
      color: rgba(255, 255, 255, 0.75) !important;
    }
    footer .text-white\\/80 {
      color: rgba(255, 255, 255, 0.8) !important;
    }
    footer .text-white\\/85 {
      color: rgba(255, 255, 255, 0.85) !important;
    }

    /* Mobile font scale for inputs (prevents iOS auto-zoom) */
    input, select, textarea {
      font-size: 16px !important;
    }
  </style>
'''
    mcp_home = mcp_home.replace('</head>', head_insertion + '\n</head>')

    # 5b. Insert Fixed Static Textured Background immediately after <body ...>
    static_bg_html = '''
<!-- Fixed Static Textured Background (Executive Alliance Theme) -->
<div id="static-textured-bg" class="fixed inset-0 pointer-events-none z-[-10] overflow-hidden" aria-hidden="true">
  <!-- Layer 1: Ambient Executive Mesh Gradients (Emerald, Mint blooms) -->
  <div class="absolute -top-[12%] -left-[10%] w-[50vw] h-[50vw] max-w-[700px] max-h-[700px] rounded-full bg-gradient-to-br from-emerald-500/12 via-[#006c49]/10 to-transparent blur-[110px] transform-gpu"></div>
  <div class="absolute top-[28%] -right-[12%] w-[55vw] h-[55vw] max-w-[750px] max-h-[750px] rounded-full bg-gradient-to-bl from-[#6ffbbe]/15 via-emerald-700/8 to-transparent blur-[130px] transform-gpu"></div>
  <div class="absolute top-[65%] -left-[10%] w-[45vw] h-[45vw] max-w-[650px] max-h-[650px] rounded-full bg-gradient-to-tr from-[#003527]/10 via-[#064e3b]/8 to-transparent blur-[120px] transform-gpu"></div>
  <div class="absolute -bottom-[15%] right-[10%] w-[60vw] h-[60vw] max-w-[800px] max-h-[800px] rounded-full bg-gradient-to-tl from-emerald-600/10 via-[#6ffbbe]/8 to-transparent blur-[140px] transform-gpu"></div>

  <!-- Layer 2: Theme-Relevant Geometric Network Matrix & Architectural Lattice (SVG) -->
  <div class="absolute inset-0 bg-repeat opacity-[0.035] mix-blend-multiply" style="background-image: url('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%2248%22%20height%3D%2248%22%20viewBox%3D%220%200%2048%2048%22%3E%0A%20%20%3Cpath%20d%3D%22M48%200L0%200%200%2048%22%20fill%3D%22none%22%20stroke%3D%22%23003527%22%20stroke-width%3D%220.6%22%20stroke-dasharray%3D%222%202%22%20stroke-opacity%3D%220.8%22/%3E%0A%20%20%3Cpath%20d%3D%22M24%2017L31%2024L24%2031L17%2024Z%22%20fill%3D%22none%22%20stroke%3D%22%23064e3b%22%20stroke-width%3D%220.75%22/%3E%0A%20%20%3Ccircle%20cx%3D%2224%22%20cy%3D%2224%22%20r%3D%221.75%22%20fill%3D%22%23006c49%22/%3E%0A%20%20%3Ccircle%20cx%3D%220%22%20cy%3D%220%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%20%20%3Ccircle%20cx%3D%2248%22%20cy%3D%220%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%20%20%3Ccircle%20cx%3D%220%22%20cy%3D%2248%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%20%20%3Ccircle%20cx%3D%2248%22%20cy%3D%2248%22%20r%3D%221.5%22%20fill%3D%22%23064e3b%22/%3E%0A%3C/svg%3E'); background-size: 48px 48px;"></div>
  
  <!-- Layer 3: Tactile Micro-Dot Mesh Texture -->
  <div class="absolute inset-0 opacity-[0.025] mix-blend-overlay" style="background-image: radial-gradient(#003527 0.75px, transparent 0.75px); background-size: 24px 24px;"></div>
</div>
'''
    body_tag_match = re.search(r'<body[^>]*>', mcp_home)
    if body_tag_match:
        mcp_home = mcp_home[:body_tag_match.end()] + '\n' + static_bg_html + mcp_home[body_tag_match.end():]

    # 6. Responsive Header Replacement
    old_header_match = re.search(r'<header[^>]*>.*?</header>', mcp_home, re.DOTALL)
    if old_header_match:
        responsive_header = '''
  <header class="fixed top-0 left-0 w-full z-50 bg-surface-container-lowest/90 backdrop-blur-xl border-b border-surface-container/60 shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
    <div class="h-16 sm:h-20 max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-12 flex items-center justify-between gap-4">
      
      <!-- Brand Logo & Identity -->
      <a href="/" class="flex items-center gap-2.5 sm:gap-3 group shrink-0">
        <img alt="Founder for Founder Logo" class="w-8 h-8 sm:w-9 sm:h-9 rounded-full object-cover shadow-[0_2px_8px_rgba(6,78,59,0.14)]" src="/assets/logo.svg">
        <div class="flex flex-col">
          <span class="font-title-md text-sm sm:text-base text-primary font-bold tracking-tight">Founder for Founder</span>
          <span class="font-label-status text-[9px] sm:text-[10px] uppercase text-on-surface-variant tracking-wider">by snalts.co</span>
        </div>
      </a>

      <!-- Desktop Navigation Links -->
      <nav class="hidden md:flex items-center gap-6 lg:gap-8">
        <a class="font-body-md text-sm text-on-surface-variant hover:text-primary transition-colors font-medium" href="#philosophy">The Alliance</a>
        <a class="font-body-md text-sm text-on-surface-variant hover:text-primary transition-colors font-medium" href="#pillars">5 Pillars</a>
        <a class="font-body-md text-sm text-on-surface-variant hover:text-primary transition-colors font-medium" href="#gatherings">Gatherings</a>
        <a class="font-body-md text-sm text-on-surface-variant hover:text-primary transition-colors font-medium" href="#testimonials-faqs">Clarity &amp; FAQ</a>
      </nav>

      <!-- Desktop & Mobile Action Area -->
      <div class="flex items-center gap-2 sm:gap-4">
        <!-- Auth Controls (Hidden when logged out) -->
        <div id="authNavControls" class="hidden items-center gap-2 sm:gap-3">
          <span class="font-label-md text-xs sm:text-sm text-primary font-semibold hidden lg:inline" id="navUserName">Welcome</span>
          <button class="px-3 sm:px-4 py-1.5 sm:py-2 rounded-[6px] bg-secondary-container text-on-secondary-container font-label-md text-xs sm:text-sm font-semibold hover:opacity-90 transition-all cursor-pointer" onclick="switchPortalTab('dashboard', this)">Portal</button>
          <button class="px-3 sm:px-4 py-1.5 sm:py-2 rounded-[6px] bg-surface-container-highest text-primary font-label-md text-xs sm:text-sm font-semibold hover:bg-surface-container transition-all cursor-pointer hidden" id="navAdminBtn" onclick="switchPortalTab('admin', this)">Admin</button>
          <button class="px-2.5 sm:px-3 py-1.5 rounded-[6px] text-error font-label-md text-xs sm:text-sm font-medium hover:bg-error-container/30 transition-all cursor-pointer" onclick="logout()">Logout</button>
        </div>

        <!-- Public Actions -->
        <div id="publicNav" class="flex items-center gap-2 sm:gap-4">
          <a class="font-title-md text-xs sm:text-sm text-on-surface-variant hover:text-primary transition-colors font-semibold px-2 py-1.5" href="javascript:void(0)" onclick="openLoginModal()">Login</a>
          <a class="inline-flex items-center gap-1 sm:gap-1.5 px-3.5 sm:px-5 py-2 sm:py-2.5 bg-primary-container text-on-primary font-title-md text-xs sm:text-sm rounded-[6px] shadow-[0_4px_16px_rgba(6,78,59,0.18)] hover:bg-primary transition-all font-semibold" href="javascript:void(0)" onclick="openShowInterestModal()">
            <span>Show Interest</span>
            <span class="material-symbols-outlined text-base leading-none">arrow_forward</span>
          </a>
        </div>

        <!-- Mobile Hamburger Menu Button -->
        <button id="mobileNavToggle" onclick="toggleMobileMenu()" class="md:hidden p-2 text-primary rounded-[6px] hover:bg-surface-container transition-colors cursor-pointer" aria-label="Toggle navigation menu" type="button">
          <span class="material-symbols-outlined text-2xl" id="mobileNavIcon">menu</span>
        </button>
      </div>
    </div>

    <!-- Responsive Slide-Down Mobile Drawer -->
    <div id="mobileNavDrawer" class="hidden md:hidden bg-surface-container-lowest border-b border-surface-container px-4 py-6 shadow-xl flex-col gap-4">
      <a href="#philosophy" onclick="toggleMobileMenu()" class="font-title-md text-base text-on-surface hover:text-primary py-2 border-b border-surface-container/50">The Alliance</a>
      <a href="#pillars" onclick="toggleMobileMenu()" class="font-title-md text-base text-on-surface hover:text-primary py-2 border-b border-surface-container/50">5 Pillars of Peer Engagement</a>
      <a href="#gatherings" onclick="toggleMobileMenu()" class="font-title-md text-base text-on-surface hover:text-primary py-2 border-b border-surface-container/50">Curated Gatherings</a>
      <a href="#testimonials-faqs" onclick="toggleMobileMenu()" class="font-title-md text-base text-on-surface hover:text-primary py-2 border-b border-surface-container/50">Clarity &amp; FAQ</a>
      <div class="flex items-center gap-4 py-2 text-xs text-on-surface-variant border-b border-surface-container/50">
        <a href="/terms" class="hover:text-primary">Terms</a>
        <span>•</span>
        <a href="/privacy-policy" class="hover:text-primary">Privacy</a>
        <span>•</span>
        <a href="/community-guidelines" class="hover:text-primary">Guidelines</a>
      </div>
      <div class="pt-2 flex flex-col gap-2">
        <button onclick="toggleMobileMenu(); openShowInterestModal();" class="w-full py-3 rounded-[6px] bg-primary-container text-on-primary font-bold text-center text-sm shadow">
          Request Admissions &rarr;
        </button>
        <button onclick="toggleMobileMenu(); openLoginModal();" class="w-full py-2.5 rounded-[6px] bg-surface-container text-primary font-semibold text-center text-sm">
          Member Login
        </button>
      </div>
    </div>
  </header>
'''
        mcp_home = mcp_home[:old_header_match.start()] + responsive_header + mcp_home[old_header_match.end():]

    # 7. Responsive Hero Section Enhancement
    mcp_home = re.sub(
        r'<h1\s+class="[^"]*font-headline-hero[^"]*"',
        '<h1 class="font-headline-hero text-3xl sm:text-4xl md:text-5xl lg:text-[56px] text-primary tracking-tight font-bold leading-[1.15] sm:leading-tight text-center"',
        mcp_home
    )
    mcp_home = re.sub(
        r'<p\s+class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto leading-relaxed text-center">',
        '<p class="font-body-lg text-sm sm:text-base md:text-lg text-on-surface-variant max-w-2xl mx-auto leading-relaxed text-center px-4">',
        mcp_home
    )
    mcp_home = re.sub(
        r'<div class="flex flex-wrap items-center justify-center gap-space-md pt-space-sm">',
        '<div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-3 pt-space-sm w-full max-w-sm sm:max-w-none mx-auto px-4">',
        mcp_home
    )

    # 8. Infinite Continuous Marquee Ticker Stream
    infinite_marquee_html = '''<!-- Ticker Stream -->
<div class="relative w-full overflow-hidden py-3">
  <!-- Gradient Edge Masking for Smooth Infinite Blend -->
  <div class="pointer-events-none absolute left-0 top-0 bottom-0 w-16 sm:w-28 z-10 bg-gradient-to-r from-surface-container-lowest to-transparent"></div>
  <div class="pointer-events-none absolute right-0 top-0 bottom-0 w-16 sm:w-28 z-10 bg-gradient-to-l from-surface-container-lowest to-transparent"></div>

  <!-- Smooth Infinite Scrolling Ticker -->
  <div class="flex gap-10 sm:gap-12 whitespace-nowrap animate-marquee-infinite shrink-0 items-center px-4">
    <!-- Brand Group 1 -->
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Apex Global Tech
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Precision Industries
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Elevate Digital
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Quantum Manufacturing
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Horizon Logistics
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Pinnacle Real Estate
    </span>
    <span class="font-title-md text-sm sm:text-base text-primary font-bold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-tertiary-container">stars</span> snalts.co
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Nexus Dynamics
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> CloudScale Solutions
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Vertex Media
    </span>

    <!-- Brand Group 2 (Exact Duplicate for Seamless Continuous Loop) -->
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Apex Global Tech
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Precision Industries
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Elevate Digital
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Quantum Manufacturing
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Horizon Logistics
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Pinnacle Real Estate
    </span>
    <span class="font-title-md text-sm sm:text-base text-primary font-bold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-tertiary-container">stars</span> snalts.co
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Nexus Dynamics
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> CloudScale Solutions
    </span>
    <span class="font-title-md text-sm sm:text-base text-on-surface-variant font-semibold hover:text-primary transition-colors flex items-center gap-2 cursor-default">
      <span class="material-symbols-outlined text-sm text-secondary">diamond</span> Vertex Media
    </span>
  </div>
</div>
</section>
<!-- CORE PHILOSOPHY -->'''

    mcp_home = re.sub(
        r'<!-- Ticker Stream -->.*?<!-- CORE PHILOSOPHY -->',
        infinite_marquee_html,
        mcp_home,
        flags=re.DOTALL
    )

    # 9. Anchor IDs
    mcp_home = mcp_home.replace('<!-- CORE PHILOSOPHY -->\n<section', '<!-- CORE PHILOSOPHY -->\n<section id="philosophy"')
    mcp_home = mcp_home.replace('<!-- THE 5 PILLARS OF PEER ENGAGEMENT -->\n<section', '<!-- THE 5 PILLARS OF PEER ENGAGEMENT -->\n<section id="pillars"')
    mcp_home = mcp_home.replace('<!-- MOMENTS OF LEVERAGE / CURATED GATHERINGS -->\n<section', '<!-- MOMENTS OF LEVERAGE / CURATED GATHERINGS -->\n<section id="gatherings"')

    # Wire up CTA buttons in sections
    mcp_home = re.sub(r'data-path="show-interest"\s+href="#"', 'href="javascript:void(0)" onclick="openShowInterestModal()"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="show-interest"', 'href="javascript:void(0)" onclick="openShowInterestModal()"', mcp_home)
    mcp_home = re.sub(r'data-path="login"\s+href="#"', 'href="javascript:void(0)" onclick="openLoginModal()"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="login"', 'href="javascript:void(0)" onclick="openLoginModal()"', mcp_home)
    mcp_home = re.sub(r'data-path="experiences"\s+href="#"', 'href="#pillars"', mcp_home)
    mcp_home = re.sub(r'href="#"\s+data-path="experiences"', 'href="#pillars"', mcp_home)

    # Add hover-lift to cards
    mcp_home = mcp_home.replace('class="flex flex-col p-space-lg rounded-xl bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 shadow-sm hover:shadow-md group"',
                                'class="flex flex-col p-space-lg rounded-xl bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 shadow-sm hover:shadow-md hover-lift group"')
    mcp_home = mcp_home.replace('class="flex flex-col bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg transition-all duration-300"',
                                'class="flex flex-col bg-surface-container-lowest rounded-2xl p-space-lg shadow-sm hover:shadow-lg hover-lift transition-all duration-300"')
    mcp_home = mcp_home.replace('class="flex flex-col bg-surface-container-low rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group"',
                                'class="flex flex-col bg-surface-container-low rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover-lift transition-shadow group"')

    # 10. Dynamic CMS Section (Testimonials, FAQs, Event Gallery, Counters)
    dynamic_cms_section = '''
<!-- DYNAMIC CMS SECTION: TESTIMONIALS & FAQS -->
<section class="w-full bg-surface-container-low py-16 sm:py-20 lg:py-28" id="testimonials-faqs">
  <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-12 flex flex-col gap-12 sm:gap-16">
    
    <!-- Dynamic Counters -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 w-full" id="countersGrid">
      <div class="flex flex-col items-center p-4 sm:p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift text-center">
        <span class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold" id="statMembers">120+</span>
        <span class="font-label-md text-[10px] sm:text-xs text-on-surface-variant uppercase tracking-wider mt-1">Vetted Founders</span>
      </div>
      <div class="flex flex-col items-center p-4 sm:p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift text-center">
        <span class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold" id="statCities">14</span>
        <span class="font-label-md text-[10px] sm:text-xs text-on-surface-variant uppercase tracking-wider mt-1">Metros & Hubs</span>
      </div>
      <div class="flex flex-col items-center p-4 sm:p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift text-center">
        <span class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold" id="statGMV">₹450Cr+</span>
        <span class="font-label-md text-[10px] sm:text-xs text-on-surface-variant uppercase tracking-wider mt-1">Cumulative GMV</span>
      </div>
      <div class="flex flex-col items-center p-4 sm:p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift text-center">
        <span class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold" id="statAttendance">94%</span>
        <span class="font-label-md text-[10px] sm:text-xs text-on-surface-variant uppercase tracking-wider mt-1">Gathering Presence</span>
      </div>
    </div>

    <!-- Testimonials Header -->
    <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-2 px-4">
      <span class="font-label-status text-xs uppercase text-secondary font-bold tracking-widest">
        PEER PERSPECTIVES
      </span>
      <h2 class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold">
        What Founders Say
      </h2>
      <p class="font-body-lg text-sm sm:text-base text-on-surface-variant">
        Authentic reflections from leaders scaling ventures inside the Founder for Founder network.
      </p>
    </div>

    <!-- Testimonials Container -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6" id="testimonialsContainer">
      <div class="flex flex-col p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift border border-surface-container/60">
        <p class="font-body-md text-sm text-on-surface leading-relaxed flex-1 italic mb-4">
          “Founder for Founder is completely different from noisy networking clubs. The intimate dinners and closed-door salons gave us direct access to high-integrity enterprise partners.”
        </p>
        <div class="flex items-center gap-3 pt-3 border-t border-surface-container">
          <div class="w-10 h-10 rounded-full bg-primary-fixed flex items-center justify-center font-bold text-on-primary-fixed shrink-0">AK</div>
          <div class="flex flex-col">
            <span class="font-title-md text-sm text-primary font-bold">Anand Krishnamurthy</span>
            <span class="font-label-md text-xs text-on-surface-variant">Founder, QuantLogix</span>
          </div>
        </div>
      </div>
      <div class="flex flex-col p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift border border-surface-container/60">
        <p class="font-body-md text-sm text-on-surface leading-relaxed flex-1 italic mb-4">
          “The sports meetups and weekend retreats create a level of camaraderie you just can't manufacture in conference ballrooms. Unmatched peer trust.”
        </p>
        <div class="flex items-center gap-3 pt-3 border-t border-surface-container">
          <div class="w-10 h-10 rounded-full bg-secondary-fixed flex items-center justify-center font-bold text-on-secondary-fixed shrink-0">PS</div>
          <div class="flex flex-col">
            <span class="font-title-md text-sm text-primary font-bold">Pooja Sharma</span>
            <span class="font-label-md text-xs text-on-surface-variant">Co-Founder, BioVeda Labs</span>
          </div>
        </div>
      </div>
      <div class="flex flex-col p-6 rounded-2xl bg-surface-container-lowest shadow-sm hover-lift border border-surface-container/60">
        <p class="font-body-md text-sm text-on-surface leading-relaxed flex-1 italic mb-4">
          “Through the Needs & Wants engine, we closed two key vendor partnerships within our first three weeks. High signal, zero spam.”
        </p>
        <div class="flex items-center gap-3 pt-3 border-t border-surface-container">
          <div class="w-10 h-10 rounded-full bg-primary-fixed-dim flex items-center justify-center font-bold text-on-primary-fixed shrink-0">RV</div>
          <div class="flex flex-col">
            <span class="font-title-md text-sm text-primary font-bold">Rohan Verma</span>
            <span class="font-label-md text-xs text-on-surface-variant">CEO, UrbanScale Logistics</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Gallery Container -->
    <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-2 px-4 mt-6 sm:mt-10">
      <span class="font-label-status text-xs uppercase text-secondary font-bold tracking-widest">
        COMMUNITY ARCHIVE
      </span>
      <h2 class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold">
        Glimpses from Recent Gatherings
      </h2>
      <p class="font-body-lg text-sm sm:text-base text-on-surface-variant">
        Moments of candid exchange, executive roundtables, and sports sessions.
      </p>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2 sm:gap-4" id="photoGalleryContainer">
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm hover-lift">
        <img src="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=600&q=80" alt="Executive Dinner" class="w-full h-full object-cover">
      </div>
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm hover-lift">
        <img src="https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=600&q=80" alt="Founder Roundtable" class="w-full h-full object-cover">
      </div>
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm hover-lift">
        <img src="https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=600&q=80" alt="Sports Meetup" class="w-full h-full object-cover">
      </div>
      <div class="aspect-video rounded-xl bg-surface-container overflow-hidden shadow-sm hover-lift">
        <img src="https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=600&q=80" alt="Annual Retreat" class="w-full h-full object-cover">
      </div>
    </div>

    <!-- FAQs Section -->
    <div class="flex flex-col items-center text-center max-w-3xl mx-auto gap-2 px-4 mt-6 sm:mt-10">
      <span class="font-label-status text-xs uppercase text-secondary font-bold tracking-widest">
        CLARITY &amp; TRANSPARENCY
      </span>
      <h2 class="font-headline-lg text-2xl sm:text-3xl md:text-4xl text-primary font-bold">
        Frequently Asked Questions
      </h2>
      <p class="font-body-lg text-sm sm:text-base text-on-surface-variant">
        Everything you need to know about our community structure, admissions, and participation.
      </p>
    </div>

    <div class="max-w-3xl mx-auto w-full flex flex-col gap-3 px-2 sm:px-0" id="faqsContainer">
      <details class="group bg-surface-container-lowest p-4 sm:p-5 rounded-xl shadow-sm border border-surface-container cursor-pointer transition-all">
        <summary class="font-title-md text-sm sm:text-base text-primary font-bold list-none flex justify-between items-center">
          <span>Who is eligible to join Founder for Founder?</span>
          <span class="material-symbols-outlined text-secondary transition-transform">expand_more</span>
        </summary>
        <p class="font-body-md text-sm text-on-surface-variant mt-3 leading-relaxed">
          Membership is strictly curated for active equity founders, co-founders, managing directors, and executive operators running registered businesses across India.
        </p>
      </details>
      <details class="group bg-surface-container-lowest p-4 sm:p-5 rounded-xl shadow-sm border border-surface-container cursor-pointer transition-all">
        <summary class="font-title-md text-sm sm:text-base text-primary font-bold list-none flex justify-between items-center">
          <span>How does the admissions review work?</span>
          <span class="material-symbols-outlined text-secondary transition-transform">expand_more</span>
        </summary>
        <p class="font-body-md text-sm text-on-surface-variant mt-3 leading-relaxed">
          Every application is reviewed on a rolling 72-hour window by our peer review committee to verify leadership track records, operational scale, and community alignment.
        </p>
      </details>
      <details class="group bg-surface-container-lowest p-4 sm:p-5 rounded-xl shadow-sm border border-surface-container cursor-pointer transition-all">
        <summary class="font-title-md text-sm sm:text-base text-primary font-bold list-none flex justify-between items-center">
          <span>What formats are included in membership?</span>
          <span class="material-symbols-outlined text-secondary transition-transform">expand_more</span>
        </summary>
        <p class="font-body-md text-sm text-on-surface-variant mt-3 leading-relaxed">
          Members gain access to sports &amp; movement gatherings (pickleball, golf, badminton), intimate founder dinners, confidential advisory roundtables, retreats, and the digital portal.
        </p>
      </details>
      <details class="group bg-surface-container-lowest p-4 sm:p-5 rounded-xl shadow-sm border border-surface-container cursor-pointer transition-all">
        <summary class="font-title-md text-sm sm:text-base text-primary font-bold list-none flex justify-between items-center">
          <span>Is member information kept confidential?</span>
          <span class="material-symbols-outlined text-secondary transition-transform">expand_more</span>
        </summary>
        <p class="font-body-md text-sm text-on-surface-variant mt-3 leading-relaxed">
          Yes. All gatherings operate under strict Chatham House Rule and community non-solicitation guidelines. Private phone numbers and personal emails are never published publicly.
        </p>
      </details>
    </div>

  </div>
</section>
'''
    mcp_home = mcp_home.replace('<!-- FINAL CALL TO ACTION BANNER -->', dynamic_cms_section + '\n<!-- FINAL CALL TO ACTION BANNER -->')

    # 10.5 Replace Footer with Executive Dark Theme & Pure White Text
    old_footer_match = re.search(r'<footer[^>]*>.*?</footer>', mcp_home, re.DOTALL)
    if old_footer_match:
        executive_white_footer = '''
<footer class="w-full bg-[#002117] text-white mt-space-xl shadow-[0_-4px_24px_rgba(0,33,23,0.18)] border-t border-[#064e3b]/60">
  <div class="max-w-[1440px] mx-auto px-margin-mobile md:px-margin lg:px-margin-desktop py-space-xl">
    <div class="flex flex-col lg:flex-row justify-between items-start gap-gutter-lg pb-space-xl border-b border-[#064e3b]/50">
      
      <!-- Brand & Mission Column -->
      <div class="flex flex-col gap-space-md max-w-sm">
        <div class="flex items-center gap-space-sm">
          <div class="w-8 h-8 rounded-full bg-secondary-fixed flex items-center justify-center text-on-secondary-fixed shadow-sm">
            <span class="material-symbols-outlined text-sm leading-none">handshake</span>
          </div>
          <span class="font-headline-sm text-headline-sm text-white font-bold tracking-tight">Founder for Founder</span>
        </div>
        <p class="font-body-md text-body-md text-white/80 leading-relaxed">
          The curated private alliance for high-growth founders, institutional operators, and venture builders across India.
        </p>
        <div class="flex items-center gap-2 font-label-md text-label-md text-white/85">
          <span class="material-symbols-outlined text-base text-secondary-fixed">mail</span>
          <a class="hover:text-white transition-colors underline decoration-white/30 underline-offset-4" href="mailto:connect.f4f@gmail.com">connect.f4f@gmail.com</a>
        </div>
        <div class="font-label-md text-label-md text-white/70">
          Powered by <a class="font-title-md text-white font-semibold hover:underline" href="https://snalts.co" target="_blank" rel="noopener">snalts.co</a>
        </div>
      </div>

      <!-- Footer Navigation Columns -->
      <div class="flex flex-col sm:flex-row gap-gutter-lg">
        <!-- Platform Links -->
        <div class="flex flex-col gap-space-sm">
          <span class="font-label-status text-label-status uppercase text-secondary-fixed font-bold tracking-wider">Platform</span>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/#philosophy">The Alliance</a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/#pillars">5 Pillars of Engagement</a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/#gatherings">Curated Gatherings</a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/#testimonials-faqs">Clarity &amp; FAQ</a>
          <a class="font-body-md text-body-md text-secondary-fixed font-semibold hover:text-white transition-colors" href="javascript:void(0)" onclick="openShowInterestModal()">Apply for Membership &rarr;</a>
        </div>

        <!-- Governance & Legal Links -->
        <div class="flex flex-col gap-space-sm">
          <span class="font-label-status text-label-status uppercase text-secondary-fixed font-bold tracking-wider">Governance &amp; Legal</span>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/terms">Terms &amp; Conditions</a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/privacy-policy">Privacy Policy</a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/refund-policy">Refund &amp; Cancellation</a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors" href="/community-guidelines">Community Guidelines</a>
        </div>

        <!-- Connect Links -->
        <div class="flex flex-col gap-space-sm">
          <span class="font-label-status text-label-status uppercase text-secondary-fixed font-bold tracking-wider">Connect</span>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors flex items-center gap-space-xs" href="https://linkedin.com" target="_blank" rel="noopener">
            <span class="material-symbols-outlined text-base text-secondary-fixed">public</span>LinkedIn
          </a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors flex items-center gap-space-xs" href="https://instagram.com" target="_blank" rel="noopener">
            <span class="material-symbols-outlined text-base text-secondary-fixed">photo_camera</span>Instagram
          </a>
          <a class="font-body-md text-body-md text-white/75 hover:text-white transition-colors flex items-center gap-space-xs" href="https://facebook.com" target="_blank" rel="noopener">
            <span class="material-symbols-outlined text-base text-secondary-fixed">share</span>Facebook
          </a>
        </div>
      </div>

    </div>

    <!-- Bottom Copyright & Privacy Notice -->
    <div class="pt-space-lg flex flex-col sm:flex-row justify-between items-center gap-space-md text-center sm:text-left">
      <p class="font-label-md text-label-md text-white/60">© 2026 Founder for Founder (f4f). All rights reserved.</p>
      <p class="font-label-md text-label-md text-white/60">Private Membership Alliance • Chatham House Rule • Verified Founders Only</p>
    </div>
  </div>
</footer>
'''
        mcp_home = mcp_home[:old_footer_match.start()] + executive_white_footer + mcp_home[old_footer_match.end():]

    # 10b. Section background transparency with backdrop blur to let static texture show through
    mcp_home = mcp_home.replace(
        'class="relative w-full overflow-hidden bg-surface-container-lowest"',
        'class="relative w-full overflow-hidden bg-surface-container-lowest/80 backdrop-blur-[2px]"'
    )
    mcp_home = mcp_home.replace(
        'class="w-full bg-surface-container-low py-8 overflow-hidden shadow-inner"',
        'class="w-full bg-surface-container-low/80 py-8 overflow-hidden shadow-inner backdrop-blur-[2px]"'
    )
    mcp_home = mcp_home.replace(
        'class="w-full bg-surface-container-lowest py-20 lg:py-28"',
        'class="w-full bg-surface-container-lowest/80 py-20 lg:py-28 backdrop-blur-[2px]"'
    )
    mcp_home = mcp_home.replace(
        'class="w-full bg-surface-container-low py-20 lg:py-28"',
        'class="w-full bg-surface-container-low/80 py-20 lg:py-28 backdrop-blur-[2px]"'
    )
    mcp_home = mcp_home.replace(
        'class="w-full bg-surface-container-low py-16 sm:py-20 lg:py-28"',
        'class="w-full bg-surface-container-low/80 py-16 sm:py-20 lg:py-28 backdrop-blur-[2px]"'
    )

    # 11. Wrap public content in <div id="publicPage"> with pb-20 for mobile bottom bar
    main_pos = mcp_home.find('<main')
    footer_end_pos = mcp_home.find('</footer>') + len('</footer>')

    public_content = mcp_home[main_pos:footer_end_pos]
    wrapped_public = f'''
<div id="publicPage" class="w-full pb-20 md:pb-0">
{public_content}
</div>

<!-- Mobile Bottom Navigation Bar (Stitch Mobile Screen 21aec84f) -->
<nav class="md:hidden fixed bottom-0 left-0 w-full z-40 bg-surface-container-lowest/95 backdrop-blur-xl border-t border-surface-container shadow-[0_-2px_12px_rgba(0,53,39,0.06)]" id="mobileBottomNav">
  <div class="h-16 px-4 grid grid-cols-4 items-center text-center">
    <a href="#" class="flex flex-col items-center justify-center py-1 text-primary">
      <span class="material-symbols-outlined text-xl">cottage</span>
      <span class="text-[10px] font-bold mt-0.5">Home</span>
    </a>
    <a href="#pillars" class="flex flex-col items-center justify-center py-1 text-on-surface-variant hover:text-primary">
      <span class="material-symbols-outlined text-xl">auto_awesome</span>
      <span class="text-[10px] font-medium mt-0.5">Pillars</span>
    </a>
    <a href="#gatherings" class="flex flex-col items-center justify-center py-1 text-on-surface-variant hover:text-primary">
      <span class="material-symbols-outlined text-xl">event</span>
      <span class="text-[10px] font-medium mt-0.5">Gatherings</span>
    </a>
    <a href="javascript:void(0)" onclick="openShowInterestModal()" class="flex flex-col items-center justify-center py-1 text-secondary font-bold">
      <span class="material-symbols-outlined text-xl">handshake</span>
      <span class="text-[10px] font-bold mt-0.5">Apply</span>
    </a>
  </div>
</nav>
'''

    # 12. Build Admissions Questionnaire Modal (Screen 975ae924) with responsive layout
    admissions_modal_html = f'''
<!-- STITCH ADMISSIONS QUESTIONNAIRE MODAL (Screen 975ae924) -->
<div class="modal-overlay" id="showInterestModal" style="display:none;">
  <div class="relative w-full max-w-4xl mx-2 sm:mx-auto my-auto bg-surface rounded-2xl shadow-2xl overflow-hidden border border-surface-container flex flex-col max-h-[92vh]">
    
    <!-- Top Sticky Modal Header with Close Button -->
    <div class="sticky top-0 z-50 bg-surface-container-lowest/95 backdrop-blur-md px-4 sm:px-6 py-3 border-b border-surface-container flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse"></span>
        <span class="font-label-status text-xs uppercase font-bold text-primary tracking-wider" id="modalTrackerText">ADMISSIONS DOSSIER</span>
      </div>
      <button class="w-8 h-8 rounded-full bg-surface-container hover:bg-surface-container-high flex items-center justify-center text-on-surface transition-colors cursor-pointer" onclick="closeModal('showInterestModal')" type="button" aria-label="Close modal">
        <span class="material-symbols-outlined text-xl">close</span>
      </button>
    </div>

    <!-- Modal Scrollable Content -->
    <div class="flex-1 overflow-y-auto p-4 sm:p-8 overscroll-contain">
      {q_content}
    </div>
  </div>
</div>
'''

    # 13. Dynamic Modal Control & Admissions Navigation Scripts
    scripts_html = '''
<!-- Dynamic Modal Control & Responsive Mobile Scripts -->
<script>
function toggleMobileMenu() {
  const drawer = document.getElementById('mobileNavDrawer');
  const icon = document.getElementById('mobileNavIcon');
  if (!drawer) return;
  const isHidden = drawer.classList.contains('hidden');
  if (isHidden) {
    drawer.classList.remove('hidden');
    drawer.classList.add('flex');
    if (icon) icon.textContent = 'close';
  } else {
    drawer.classList.add('hidden');
    drawer.classList.remove('flex');
    if (icon) icon.textContent = 'menu';
  }
}

function closeMobileMenu() {
  const drawer = document.getElementById('mobileNavDrawer');
  const icon = document.getElementById('mobileNavIcon');
  if (drawer) {
    drawer.classList.add('hidden');
    drawer.classList.remove('flex');
  }
  if (icon) icon.textContent = 'menu';
}

function openShowInterestModal() {
  closeMobileMenu();
  const m = document.getElementById('showInterestModal');
  if (m) {
    m.classList.add('active');
    m.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    navigateToStep(1);
  }
}

function openLoginModal() {
  closeMobileMenu();
  const m = document.getElementById('loginModal');
  if (m) {
    m.classList.add('active');
    m.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.remove('active');
    m.style.display = 'none';
  }
  // Restore body scrolling if no modals are open
  const anyOpen = document.querySelector('.modal-overlay.active, .modal-overlay[style*="display: flex"]');
  if (!anyOpen) {
    document.body.style.overflow = '';
  }
}

// ESC key to close modal
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active, #showInterestModal').forEach(m => {
      if (m.id) closeModal(m.id);
    });
  }
});

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
        stepElem.classList.add('animate-fade-in');
      } else {
        stepElem.classList.remove('flex');
        stepElem.classList.remove('animate-fade-in');
        stepElem.classList.add('hidden');
      }
    }

    const bubble = document.getElementById('step-bubble-' + i);
    if (bubble) {
      if (i < currentStep) {
        bubble.className = "w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-primary text-on-primary font-label-md text-xs sm:text-sm flex items-center justify-center transition-all shrink-0";
        bubble.innerHTML = '<span class="material-symbols-outlined text-sm leading-none">check</span>';
      } else if (i === currentStep) {
        bubble.className = "w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-primary-container text-on-primary font-label-md text-xs sm:text-sm flex items-center justify-center transition-all ring-2 ring-primary/20 shrink-0";
        bubble.innerText = i;
      } else {
        bubble.className = "w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-surface-container text-on-surface font-label-md text-xs sm:text-sm flex items-center justify-center transition-all shrink-0";
        bubble.innerText = i;
      }
    }

    if (i < totalSteps) {
      const line = document.getElementById('line-' + i);
      if (line) {
        line.className = (i < currentStep) ? "h-0.5 flex-1 min-w-3 sm:min-w-4 bg-primary transition-colors" : "h-0.5 flex-1 min-w-3 sm:min-w-4 bg-surface-container-high transition-colors";
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
      nextBtn.innerText = "CONTINUE TO SECTION " + (currentStep + 1) + " &rarr;";
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

document.addEventListener('DOMContentLoaded', () => {
  navigateToStep(1);
});
</script>

<script src="/js/app.js?v=8.2" defer></script>
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

    print(f'Successfully built responsive public/index.html ({len(final_html)} bytes)')

if __name__ == '__main__':
    build_home()
