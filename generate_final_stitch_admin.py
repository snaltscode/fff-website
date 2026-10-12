# Script to generate the comprehensive, production-ready Stitch Admin Console HTML
import os

def generate_stitch_admin_markup():
    # 1. Top Ribbon & Utilities
    top_ribbon = '''<!-- Top Context Ribbon & Master Utilities -->
<div class="w-full bg-surface-container-low py-space-sm px-gutter">
  <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-space-sm">
    <div class="flex items-center gap-space-xs text-on-surface-variant font-label-md text-label-md">
      <span class="text-text-tertiary">Portal</span>
      <span class="material-symbols-outlined text-[16px] text-text-tertiary">chevron_right</span>
      <span class="text-primary font-semibold">Admin Console &amp; CMS</span>
      <span class="ml-space-sm inline-flex items-center gap-1 bg-surface-container-high px-2 py-0.5 rounded text-[11px] font-mono text-secondary">
        <span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>PROD-v2.6.4
      </span>
    </div>
    <div class="flex items-center gap-space-sm flex-wrap">
      <div class="relative flex-1 sm:w-72">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary text-[18px]">search</span>
        <input id="adminMasterSearch" class="w-full h-10 pl-9 pr-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm placeholder:text-text-tertiary focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="Search founders, applications, logs..." type="text" oninput="handleMasterAdminSearch(this.value)" />
      </div>
      <div class="relative" id="exportDropdownWrapper">
        <button class="h-10 px-space-md bg-surface-card text-on-surface font-label-md text-label-md rounded flex items-center gap-space-xs hover:bg-surface-container shadow-sm transition-colors cursor-pointer" id="exportBtn" type="button">
          <span class="material-symbols-outlined text-[18px]">file_download</span>
          <span>Export Data</span>
          <span class="material-symbols-outlined text-[16px]">expand_more</span>
        </button>
        <div class="hidden absolute right-0 mt-1 w-56 bg-surface-card rounded shadow-xl py-1 z-30 font-body-sm text-body-sm border border-hairline" id="exportMenu">
          <a class="px-4 py-2 hover:bg-surface-subtle flex items-center gap-2 text-on-surface" href="/api/admin/export/csv?type=members" target="_blank">
            <span class="material-symbols-outlined text-[16px] text-secondary">badge</span> Export Members (CSV)
          </a>
          <a class="px-4 py-2 hover:bg-surface-subtle flex items-center gap-2 text-on-surface" href="/api/admin/export/csv?type=applications" target="_blank">
            <span class="material-symbols-outlined text-[16px] text-secondary">how_to_reg</span> Export Applications (CSV)
          </a>
          <a class="px-4 py-2 hover:bg-surface-subtle flex items-center gap-2 text-on-surface" href="/api/admin/export/csv?type=audit" target="_blank">
            <span class="material-symbols-outlined text-[16px] text-secondary">security</span> Export Audit Trails (JSON)
          </a>
        </div>
      </div>
      <div class="h-10 pl-3 pr-3 bg-surface-card rounded flex items-center gap-space-sm shadow-sm">
        <div class="w-6 h-6 rounded-full bg-primary-container text-on-primary flex items-center justify-center font-label-caps text-label-caps">MA</div>
        <div class="hidden sm:flex flex-col text-left leading-tight">
          <span class="font-label-md text-label-md text-text-primary text-[12px]">Master Admin</span>
          <span class="font-body-sm text-body-sm text-text-tertiary text-[11px]" id="adminBadgeEmail">admin@founderforfounder.biz</span>
        </div>
        <span class="bg-secondary-container text-on-secondary-container px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase">ROOT</span>
      </div>
    </div>
  </div>
</div>'''

    # 2. Header Banner
    header_banner = '''<!-- Header Banner -->
<div class="bg-surface-card rounded-xl p-space-lg shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-md relative overflow-hidden border border-hairline">
  <div class="flex flex-col gap-space-xs max-w-2xl relative z-10">
    <div class="flex items-center gap-space-xs text-secondary">
      <span class="material-symbols-outlined text-[18px]">verified_user</span>
      <span class="font-label-caps text-label-caps uppercase tracking-wider">FOUNDER FOR FOUNDER • EXECUTIVE OPERATING SYSTEM</span>
    </div>
    <h1 class="font-headline-lg text-headline-lg text-text-primary leading-tight font-serif">Admin Console &amp; CMS Panel</h1>
    <p class="font-body-md text-body-md text-text-secondary leading-relaxed">
      Review membership applications, generate cryptographic invitations, manage dynamic hero/card media, and publish curated events across chapters.
    </p>
  </div>
  <div class="flex items-center gap-space-sm relative z-10 flex-wrap">
    <a class="h-11 px-space-md bg-surface-subtle text-on-surface font-label-md text-label-md rounded flex items-center gap-2 hover:bg-surface-container transition-colors" href="#applications-section">
      <span class="material-symbols-outlined text-[18px]">inbox</span> Review Applications
    </a>
    <a class="h-11 px-space-md bg-primary-container text-on-primary font-label-md text-label-md rounded flex items-center gap-2 hover:bg-emerald-deep shadow-sm transition-all" href="#event-publisher-section">
      <span class="material-symbols-outlined text-[18px]">add_circle</span> Publish Event
    </a>
  </div>
</div>'''

    # 3. Section 1: Executive KPI Strip
    sec1_kpi = '''<!-- Section 1: Executive KPI Summary Strip (3-Card Grid) -->
<section class="grid grid-cols-1 md:grid-cols-3 gap-gutter" id="adminMetricsGrid">
  <!-- Card 1: Membership Seats -->
  <div class="bg-surface-card rounded-xl p-space-lg shadow-sm flex flex-col justify-between relative border border-hairline">
    <div class="flex items-start justify-between">
      <div class="flex flex-col gap-1">
        <span class="font-label-caps text-label-caps uppercase tracking-wider text-text-tertiary">MEMBERSHIP SEATS</span>
        <span class="font-headline-md text-headline-md text-text-primary font-bold">Total Admitted Members</span>
      </div>
      <div class="w-10 h-10 rounded-lg bg-surface-subtle text-primary flex items-center justify-center">
        <span class="material-symbols-outlined text-[22px]">group</span>
      </div>
    </div>
    <div class="mt-space-md flex items-baseline gap-space-sm">
      <span class="font-numeric-stat text-numeric-stat text-primary font-bold" id="statTotalMembers">142</span>
      <span class="inline-flex items-center gap-1 bg-primary-fixed text-on-primary-fixed px-2 py-0.5 rounded text-[12px] font-bold">
        <span class="material-symbols-outlined text-[14px]">trending_up</span> Verified Active
      </span>
    </div>
    <p class="font-body-sm text-body-sm text-text-secondary mt-1">Active verified founders across Bengaluru, Mumbai, and Delhi NCR chapters</p>
  </div>

  <!-- Card 2: Treasury Run-Rate -->
  <div class="bg-surface-card rounded-xl p-space-lg shadow-sm flex flex-col justify-between relative border border-hairline">
    <div class="flex items-start justify-between">
      <div class="flex flex-col gap-1">
        <span class="font-label-caps text-label-caps uppercase tracking-wider text-text-tertiary">TREASURY RUN-RATE</span>
        <span class="font-headline-md text-headline-md text-text-primary font-bold">Active Membership MRR</span>
      </div>
      <div class="w-10 h-10 rounded-lg bg-gold-light text-secondary flex items-center justify-center">
        <span class="material-symbols-outlined text-[22px]">payments</span>
      </div>
    </div>
    <div class="mt-space-md flex items-baseline gap-space-sm">
      <span class="font-numeric-stat text-numeric-stat text-text-primary font-bold" id="statActiveMrr">₹7,10,000</span>
      <span class="inline-flex items-center gap-1 bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded text-[12px] font-bold">
        <span class="material-symbols-outlined text-[14px]">verified</span> 100% On-Track
      </span>
    </div>
    <p class="font-body-sm text-body-sm text-text-secondary mt-1">Quarterly &amp; annual guild subscription run-rate</p>
  </div>

  <!-- Card 3: Admissions Pipeline -->
  <div class="bg-surface-card rounded-xl p-space-lg shadow-sm flex flex-col justify-between relative border border-hairline">
    <div class="flex items-start justify-between">
      <div class="flex flex-col gap-1">
        <span class="font-label-caps text-label-caps uppercase tracking-wider text-text-tertiary">ADMISSIONS PIPELINE</span>
        <span class="font-headline-md text-headline-md text-text-primary font-bold">Pending Admissions Queue</span>
      </div>
      <div class="w-10 h-10 rounded-lg bg-surface-subtle text-primary flex items-center justify-center">
        <span class="material-symbols-outlined text-[22px]">hourglass_top</span>
      </div>
    </div>
    <div class="mt-space-md flex items-baseline gap-space-sm">
      <span class="font-numeric-stat text-numeric-stat text-primary font-bold" id="statPendingApps">18</span>
      <span class="inline-flex items-center gap-1 bg-primary-fixed text-on-primary-fixed px-2 py-0.5 rounded text-[12px] font-bold">
        <span class="material-symbols-outlined text-[14px]">inbox</span> Review Required
      </span>
    </div>
    <p class="font-body-sm text-body-sm text-text-secondary mt-1">Direct applicant intake queue awaiting background review</p>
  </div>
</section>'''

    # 4. Section 2: Membership Application Queue
    sec2_apps = '''<!-- Section 2: Membership Application Management Table -->
<section class="bg-surface-card rounded-xl shadow-sm overflow-hidden flex flex-col border border-hairline" id="applications-section">
  <div class="p-space-lg flex flex-col lg:flex-row lg:items-center justify-between gap-space-md bg-surface-card">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <span class="font-headline-md text-headline-md text-text-primary font-semibold">Membership Application Queue</span>
        <span class="bg-primary-fixed text-on-primary-fixed font-label-caps text-label-caps px-2 py-0.5 rounded-full" id="appQueueCountBadge">Active Queue</span>
      </div>
      <p class="font-body-sm text-body-sm text-text-secondary">Direct vetting panel for high-conviction founders and verified business leaders.</p>
    </div>

    <!-- Filter Controls -->
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-space-sm">
      <div class="relative w-full sm:w-64">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary text-[18px]">search</span>
        <input class="w-full h-10 pl-9 pr-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary" id="appSearch" placeholder="Filter name, company, city..." type="text" oninput="handleAppSearch(this.value)" />
      </div>
      <div class="flex items-center gap-1 bg-surface-subtle p-1 rounded overflow-x-auto">
        <button class="filter-tab px-3 py-1.5 rounded font-label-md text-label-md bg-surface-card text-primary shadow-sm cursor-pointer whitespace-nowrap" data-filter="all" onclick="filterApplications('all', this)">All</button>
        <button class="filter-tab px-3 py-1.5 rounded font-label-md text-label-md text-text-secondary hover:text-on-surface cursor-pointer whitespace-nowrap" data-filter="SUBMITTED" onclick="filterApplications('SUBMITTED', this)">Pending</button>
        <button class="filter-tab px-3 py-1.5 rounded font-label-md text-label-md text-text-secondary hover:text-on-surface cursor-pointer whitespace-nowrap" data-filter="UNDER_REVIEW" onclick="filterApplications('UNDER_REVIEW', this)">Under Review</button>
        <button class="filter-tab px-3 py-1.5 rounded font-label-md text-label-md text-text-secondary hover:text-on-surface cursor-pointer whitespace-nowrap" data-filter="APPROVED" onclick="filterApplications('APPROVED', this)">Approved</button>
        <button class="filter-tab px-3 py-1.5 rounded font-label-md text-label-md text-text-secondary hover:text-on-surface cursor-pointer whitespace-nowrap" data-filter="WAITLISTED" onclick="filterApplications('WAITLISTED', this)">Waitlisted</button>
      </div>
    </div>
  </div>

  <!-- Table Wrapper with Momentum Scroll -->
  <div class="w-full overflow-x-auto" id="applicationsTable">
    <table class="w-full text-left min-w-[1080px]">
      <thead>
        <tr class="bg-surface-subtle text-text-tertiary font-label-caps text-label-caps uppercase tracking-wider">
          <th class="py-3 px-space-md">Applicant</th>
          <th class="py-3 px-space-md">Role &amp; Track</th>
          <th class="py-3 px-space-md">Company &amp; Model</th>
          <th class="py-3 px-space-md">Direct Contact</th>
          <th class="py-3 px-space-md">Status</th>
          <th class="py-3 px-space-md">Update Status</th>
          <th class="py-3 px-space-md text-right">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-surface-subtle font-body-sm text-body-sm text-on-surface" id="applicationsTableBody">
        <tr>
          <td colspan="7" class="py-8 text-center text-text-tertiary">Loading applications data...</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Table Footer -->
  <div class="p-space-md border-t border-surface-subtle flex items-center justify-between text-text-tertiary font-body-sm text-body-sm bg-surface-card">
    <span id="appTableFooterCount">Showing applications</span>
    <span class="font-mono text-[12px] flex items-center gap-1">
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-deep"></span> Vetting Protocol Synchronized
    </span>
  </div>
</section>'''

    # 5. Section 3: Audit Logs Table
    sec3_audit = '''<!-- Section 3: System Audit & Security Logs Table -->
<section class="bg-surface-card rounded-xl shadow-sm overflow-hidden flex flex-col border border-hairline">
  <div class="p-space-lg flex items-center justify-between">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <span class="font-headline-md text-headline-md text-text-primary font-semibold">System Audit &amp; Security Logs</span>
        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-surface-subtle text-[11px] font-mono text-secondary">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-deep"></span> LIVE IMMUTABLE LEDGER
        </span>
      </div>
      <p class="font-body-sm text-body-sm text-text-secondary">Cryptographic event logging and administrative change tracking.</p>
    </div>
    <button class="h-9 px-3 rounded bg-surface-subtle hover:bg-surface-container text-on-surface font-label-md text-label-md flex items-center gap-1 transition-colors cursor-pointer" onclick="loadAdminTab()" type="button">
      <span class="material-symbols-outlined text-[16px]">refresh</span> Refresh Logs
    </button>
  </div>

  <div class="w-full overflow-x-auto" id="auditLogsTable">
    <table class="w-full text-left min-w-[960px]">
      <thead>
        <tr class="bg-surface-subtle text-text-tertiary font-label-caps text-label-caps uppercase tracking-wider">
          <th class="py-3 px-space-md">Timestamp (IST)</th>
          <th class="py-3 px-space-md">Action Type</th>
          <th class="py-3 px-space-md">Actor</th>
          <th class="py-3 px-space-md">Target Entity</th>
          <th class="py-3 px-space-md text-right">Client IP &amp; Origin</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-surface-subtle font-body-sm text-body-sm font-mono text-[13px]" id="auditLogsTableBody">
        <tr>
          <td colspan="5" class="py-8 text-center text-text-tertiary">Loading audit logs...</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>'''

    # 6. Section 4: 16:9 Meeting Photos Manager
    sec4_photos = '''<!-- Section 4: 16:9 Meeting Photos Gallery Manager -->
<section class="bg-surface-card rounded-xl shadow-sm p-space-lg flex flex-col gap-space-lg border border-hairline">
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-space-sm">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <span class="font-headline-md text-headline-md text-text-primary font-semibold">16:9 Meeting Photos Gallery Manager</span>
        <span class="bg-surface-subtle text-primary font-label-caps text-label-caps px-2 py-0.5 rounded">Continuous Homepage Reel</span>
      </div>
      <p class="font-body-sm text-body-sm text-text-secondary">
        Manage high-fidelity photography featured in the continuous right-to-left marquee slider for verified private salons and gatherings.
      </p>
    </div>
    <div class="flex items-center gap-2 text-text-tertiary font-body-sm text-body-sm">
      <span class="material-symbols-outlined text-[18px]">photo_library</span> Active Live Rotation
    </div>
  </div>

  <!-- Quick Add In-Card Form -->
  <form id="adminQuickAddPhotoForm" onsubmit="handleAdminQuickAddPhoto(event)" class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-md">
    <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
      <span class="material-symbols-outlined text-[18px]">add_photo_alternate</span>
      <span>Add New Meeting Photo to Live Slider</span>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-space-md">
      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Meeting Title *</label>
        <input id="quickPhotoTitle" class="h-10 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="e.g. Founders Executive Dinner — Indiranagar" type="text" required />
      </div>
      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Category Tag *</label>
        <select id="quickPhotoTag" class="h-10 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm cursor-pointer">
          <option value="Founder Dinner">Founder Dinner</option>
          <option value="Closed-Door Salon">Closed-Door Salon</option>
          <option value="1:1 Founder Meeting">1:1 Founder Meeting</option>
          <option value="Mastermind Roundtable">Mastermind Roundtable</option>
          <option value="Experiential &amp; Walks">Experiential &amp; Walks</option>
          <option value="Founder Retreat">Founder Retreat</option>
          <option value="Curated Gathering">Curated Gathering</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Photo Source URL (16:9) *</label>
        <div class="flex items-center gap-2">
          <input id="quickPhotoUrl" class="h-10 flex-1 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="https://images.unsplash.com/..." type="text" required />
          <label class="h-10 px-3 bg-surface-card hover:bg-surface-container rounded text-on-surface font-label-md text-label-md shadow-sm transition-colors flex items-center justify-center cursor-pointer">
            Browse
            <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'quickPhotoUrl', 'prev_quickPhotoUrl', 'upload_status_quickPhotoUrl')">
          </label>
          <span id="upload_status_quickPhotoUrl" style="display:none;"></span>
        </div>
      </div>
    </div>
    <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-space-md pt-1">
      <div class="flex-1">
        <input id="quickPhotoCaption" class="w-full h-10 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="Short caption / highlights (e.g. 14 founders discussing cross-border liquidity over omakase)" type="text" />
      </div>
      <button class="h-10 px-space-md bg-primary-container hover:bg-emerald-deep text-on-primary font-label-md text-label-md rounded flex items-center justify-center gap-2 shadow-sm transition-all whitespace-nowrap cursor-pointer" type="submit">
        <span class="material-symbols-outlined text-[18px]">add</span>
        <span>Add to 16:9 Slider</span>
      </button>
    </div>
  </form>

  <!-- Existing Photo Cards Grid -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter" id="adminMeetingPhotosList">
    <!-- Populated dynamically by renderAdminMeetingPhotosList -->
  </div>
</section>'''

    # 7. Section 5: Dynamic Media & Website Images CMS
    sec5_cms = '''<!-- Section 5: Dynamic Media & Website Images CMS -->
<section class="bg-surface-card rounded-xl shadow-sm p-space-lg flex flex-col gap-space-lg border border-hairline">
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-space-sm">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <span class="font-headline-md text-headline-md text-text-primary font-semibold">Dynamic Media &amp; Website Images CMS</span>
        <span class="bg-secondary-container text-on-secondary-container font-label-caps text-label-caps px-2 py-0.5 rounded">LIVE SYNCHRONIZER</span>
      </div>
      <p class="font-body-sm text-body-sm text-text-secondary">
        Configure visual assets, hero capsule compositions, value pillar illustrations, and OAuth identity credentials.
      </p>
    </div>
  </div>

  <form id="adminSettingsForm" onsubmit="handleSaveSettings(event)" class="flex flex-col gap-space-md">
    <!-- Sub-panel 1: Brand Identity & Hero Banner -->
    <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-md">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
          <span class="material-symbols-outlined text-[20px]">palette</span>
          <span>1. Brand Identity &amp; Hero Banner Assets</span>
        </div>
        <span class="text-text-tertiary text-[12px] font-mono">HERO_ROOT_SECTION</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">
        <div class="bg-surface-card p-space-md rounded flex flex-col gap-space-sm shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase">Navbar &amp; Footer Guild Emblem</span>
          <div class="flex items-center gap-space-md">
            <img id="prev_logo_url" src="/assets/logo.svg" alt="Guild Emblem Preview" class="w-14 h-14 rounded-full bg-primary object-contain p-2 flex-shrink-0" />
            <div class="flex-1 flex flex-col gap-1">
              <input id="set_logo_url" class="h-9 px-3 rounded bg-surface-subtle text-on-surface font-mono text-[12px] focus:outline-none focus:ring-1 focus:ring-primary truncate" type="text" placeholder="https://... or /assets/logo.svg" oninput="previewImageInput(this.value, 'prev_logo_url')" />
              <div class="flex items-center gap-2">
                <label class="h-7 px-2.5 bg-surface-subtle hover:bg-surface-container rounded text-primary text-[12px] font-medium transition-colors cursor-pointer">
                  Replace
                  <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_logo_url', 'prev_logo_url', 'upload_status_logo_url')">
                </label>
                <span id="upload_status_logo_url" class="text-text-tertiary text-[11px]">PNG/SVG 512x512 transparent</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-surface-card p-space-md rounded flex flex-col gap-space-sm shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase">Hero Scrim Background Canvas</span>
          <div class="flex items-center gap-space-md">
            <img id="prev_hero_banner_url" src="/assets/hero_banner.jpg" alt="Hero Canvas Preview" class="w-14 h-14 rounded bg-surface-container object-cover flex-shrink-0" />
            <div class="flex-1 flex flex-col gap-1">
              <input id="set_hero_banner_url" class="h-9 px-3 rounded bg-surface-subtle text-on-surface font-mono text-[12px] focus:outline-none focus:ring-1 focus:ring-primary truncate" type="text" placeholder="https://... or /assets/hero_banner.jpg" oninput="previewImageInput(this.value, 'prev_hero_banner_url')" />
              <div class="flex items-center gap-2">
                <label class="h-7 px-2.5 bg-surface-subtle hover:bg-surface-container rounded text-primary text-[12px] font-medium transition-colors cursor-pointer">
                  Replace
                  <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_hero_banner_url', 'prev_hero_banner_url', 'upload_status_hero_banner_url')">
                </label>
                <span id="upload_status_hero_banner_url" class="text-text-tertiary text-[11px]">Recommended 2560x1440 WebP</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">
        <div class="flex flex-col gap-1">
          <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Hero Main Headline</label>
          <input id="set_hero_heading" class="h-10 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" type="text" placeholder="A Curated Sovereign Guild for Visionary Indian Founders" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Hero Subheading</label>
          <input id="set_hero_subheading" class="h-10 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" type="text" placeholder="High-trust circles, vetted capital access, closed-door masterminds, and genuine peer camaraderie." />
        </div>
      </div>
    </div>

    <!-- Sub-panel 2: Hero Capsule Collage (3 Angled Images) -->
    <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-md">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
          <span class="material-symbols-outlined text-[20px]">view_carousel</span>
          <span>2. Hero Capsule Collage (3 Angled Featured Images)</span>
        </div>
        <span class="text-text-tertiary text-[12px] font-mono">HERO_TRIPTYCH_SLOT</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-space-md">
        <!-- Capsule 1 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <div class="flex items-center justify-between">
            <span class="font-label-caps text-label-caps text-text-tertiary uppercase">Capsule 1 (Left)</span>
            <span id="upload_status_hero_capsule_1_url" class="text-[11px] text-primary"></span>
          </div>
          <div class="aspect-[4/3] rounded overflow-hidden bg-surface-container">
            <img id="prev_hero_capsule_1_url" src="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80" alt="Capsule 1" class="w-full h-full object-cover" />
          </div>
          <div class="flex items-center gap-1">
            <input id="set_hero_capsule_1_url" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_hero_capsule_1_url')" />
            <label class="h-8 px-2 bg-surface-subtle hover:bg-surface-container rounded font-label-md text-label-md text-primary text-[11px] cursor-pointer flex items-center justify-center">
              Upload
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_hero_capsule_1_url', 'prev_hero_capsule_1_url', 'upload_status_hero_capsule_1_url')">
            </label>
          </div>
        </div>

        <!-- Capsule 2 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <div class="flex items-center justify-between">
            <span class="font-label-caps text-label-caps text-text-tertiary uppercase">Capsule 2 (Center)</span>
            <span id="upload_status_hero_capsule_2_url" class="text-[11px] text-primary"></span>
          </div>
          <div class="aspect-[4/3] rounded overflow-hidden bg-surface-container">
            <img id="prev_hero_capsule_2_url" src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80" alt="Capsule 2" class="w-full h-full object-cover" />
          </div>
          <div class="flex items-center gap-1">
            <input id="set_hero_capsule_2_url" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_hero_capsule_2_url')" />
            <label class="h-8 px-2 bg-surface-subtle hover:bg-surface-container rounded font-label-md text-label-md text-primary text-[11px] cursor-pointer flex items-center justify-center">
              Upload
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_hero_capsule_2_url', 'prev_hero_capsule_2_url', 'upload_status_hero_capsule_2_url')">
            </label>
          </div>
        </div>

        <!-- Capsule 3 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <div class="flex items-center justify-between">
            <span class="font-label-caps text-label-caps text-text-tertiary uppercase">Capsule 3 (Right)</span>
            <span id="upload_status_hero_capsule_3_url" class="text-[11px] text-primary"></span>
          </div>
          <div class="aspect-[4/3] rounded overflow-hidden bg-surface-container">
            <img id="prev_hero_capsule_3_url" src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80" alt="Capsule 3" class="w-full h-full object-cover" />
          </div>
          <div class="flex items-center gap-1">
            <input id="set_hero_capsule_3_url" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_hero_capsule_3_url')" />
            <label class="h-8 px-2 bg-surface-subtle hover:bg-surface-container rounded font-label-md text-label-md text-primary text-[11px] cursor-pointer flex items-center justify-center">
              Upload
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_hero_capsule_3_url', 'prev_hero_capsule_3_url', 'upload_status_hero_capsule_3_url')">
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Sub-panel 3: Core Philosophy Cards (4 Images) -->
    <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-md">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
          <span class="material-symbols-outlined text-[20px]">auto_stories</span>
          <span>3. Core Philosophy &amp; Methodology Cards (4 Cards)</span>
        </div>
        <span class="text-text-tertiary text-[12px] font-mono">PHILOSOPHY_GRID_SLOTS</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md">
        <!-- Philosophy 1 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">1. The Guild Circle</span>
          <img id="prev_philosophy_img_1" src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80" alt="Philosophy 1" class="h-24 w-full object-cover rounded" />
          <div class="flex items-center gap-1">
            <input id="set_philosophy_img_1" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_philosophy_img_1')" />
            <label class="h-7 px-2 bg-surface-subtle hover:bg-surface-container rounded text-primary text-[11px] font-medium cursor-pointer flex items-center justify-center">
              Up
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_philosophy_img_1', 'prev_philosophy_img_1', 'upload_status_philosophy_img_1')">
            </label>
          </div>
        </div>

        <!-- Philosophy 2 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">2. Real Experiences</span>
          <img id="prev_philosophy_img_2" src="https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=800&q=80" alt="Philosophy 2" class="h-24 w-full object-cover rounded" />
          <div class="flex items-center gap-1">
            <input id="set_philosophy_img_2" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_philosophy_img_2')" />
            <label class="h-7 px-2 bg-surface-subtle hover:bg-surface-container rounded text-primary text-[11px] font-medium cursor-pointer flex items-center justify-center">
              Up
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_philosophy_img_2', 'prev_philosophy_img_2', 'upload_status_philosophy_img_2')">
            </label>
          </div>
        </div>

        <!-- Philosophy 3 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">3. Needs &amp; Wants</span>
          <img id="prev_philosophy_img_3" src="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80" alt="Philosophy 3" class="h-24 w-full object-cover rounded" />
          <div class="flex items-center gap-1">
            <input id="set_philosophy_img_3" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_philosophy_img_3')" />
            <label class="h-7 px-2 bg-surface-subtle hover:bg-surface-container rounded text-primary text-[11px] font-medium cursor-pointer flex items-center justify-center">
              Up
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_philosophy_img_3', 'prev_philosophy_img_3', 'upload_status_philosophy_img_3')">
            </label>
          </div>
        </div>

        <!-- Philosophy 4 -->
        <div class="bg-surface-card p-3 rounded flex flex-col gap-2 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">4. Warm Referrals</span>
          <img id="prev_philosophy_img_4" src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80" alt="Philosophy 4" class="h-24 w-full object-cover rounded" />
          <div class="flex items-center gap-1">
            <input id="set_philosophy_img_4" class="h-8 px-2 flex-1 rounded bg-surface-subtle text-on-surface font-mono text-[11px] truncate" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_philosophy_img_4')" />
            <label class="h-7 px-2 bg-surface-subtle hover:bg-surface-container rounded text-primary text-[11px] font-medium cursor-pointer flex items-center justify-center">
              Up
              <input type="file" accept="image/*" style="display:none;" onchange="handleAdminFileUpload(this, 'set_philosophy_img_4', 'prev_philosophy_img_4', 'upload_status_philosophy_img_4')">
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Sub-panel 4: Ways We Connect & Collaborate (5 Pillars) -->
    <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-md">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
          <span class="material-symbols-outlined text-[20px]">hub</span>
          <span>4. Ways We Connect &amp; Collaborate (5 Pillars)</span>
        </div>
        <span class="text-text-tertiary text-[12px] font-mono">CONNECT_FORMATS</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-space-sm">
        <!-- Play -->
        <div class="bg-surface-card p-2.5 rounded flex flex-col gap-1.5 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">1. Play Together</span>
          <img id="prev_format_img_play" src="https://images.unsplash.com/photo-1554068865-24cecd4e34b8?auto=format&fit=crop&w=800&q=80" alt="Play" class="h-16 w-full object-cover rounded" />
          <input id="set_format_img_play" class="h-7 px-2 rounded bg-surface-subtle text-on-surface font-mono text-[10px]" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_format_img_play')" />
        </div>
        <!-- Explore -->
        <div class="bg-surface-card p-2.5 rounded flex flex-col gap-1.5 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">2. Explore &amp; Travel</span>
          <img id="prev_format_img_explore" src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80" alt="Explore" class="h-16 w-full object-cover rounded" />
          <input id="set_format_img_explore" class="h-7 px-2 rounded bg-surface-subtle text-on-surface font-mono text-[10px]" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_format_img_explore')" />
        </div>
        <!-- Dine -->
        <div class="bg-surface-card p-2.5 rounded flex flex-col gap-1.5 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">3. Dine &amp; Unwind</span>
          <img id="prev_format_img_dine" src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80" alt="Dine" class="h-16 w-full object-cover rounded" />
          <input id="set_format_img_dine" class="h-7 px-2 rounded bg-surface-subtle text-on-surface font-mono text-[10px]" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_format_img_dine')" />
        </div>
        <!-- Build -->
        <div class="bg-surface-card p-2.5 rounded flex flex-col gap-1.5 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">4. Build &amp; Scale</span>
          <img id="prev_format_img_build" src="https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80" alt="Build" class="h-16 w-full object-cover rounded" />
          <input id="set_format_img_build" class="h-7 px-2 rounded bg-surface-subtle text-on-surface font-mono text-[10px]" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_format_img_build')" />
        </div>
        <!-- Celebrate -->
        <div class="bg-surface-card p-2.5 rounded flex flex-col gap-1.5 shadow-sm border border-hairline">
          <span class="font-label-caps text-label-caps text-text-tertiary uppercase truncate">5. Celebrate Wins</span>
          <img id="prev_format_img_celebrate" src="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=800&q=80" alt="Celebrate" class="h-16 w-full object-cover rounded" />
          <input id="set_format_img_celebrate" class="h-7 px-2 rounded bg-surface-subtle text-on-surface font-mono text-[10px]" type="text" placeholder="Image URL..." oninput="previewImageInput(this.value, 'prev_format_img_celebrate')" />
        </div>
      </div>
    </div>

    <!-- Sub-panel 5: Platform Feature Tab Showcase & Google OAuth -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-space-md">
      <div class="lg:col-span-2 bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-sm">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
            <span class="material-symbols-outlined text-[20px]">tab</span>
            <span>5. Platform Feature Tab Images (6 Tabs)</span>
          </div>
          <span class="text-text-tertiary text-[12px] font-mono">PORTAL_SHOWCASE</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-space-sm pt-1">
          <div class="bg-surface-card p-2 rounded flex flex-col gap-1 shadow-sm border border-hairline">
            <span class="font-label-caps text-[10px] text-text-tertiary truncate">1. Network</span>
            <img id="prev_feature_img_network" src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80" alt="Network" class="h-14 w-full object-cover rounded" />
            <input id="set_feature_img_network" class="h-6 px-1.5 rounded bg-surface-subtle font-mono text-[9px]" type="text" placeholder="URL..." oninput="previewImageInput(this.value, 'prev_feature_img_network')" />
          </div>
          <div class="bg-surface-card p-2 rounded flex flex-col gap-1 shadow-sm border border-hairline">
            <span class="font-label-caps text-[10px] text-text-tertiary truncate">2. Needs/Wants</span>
            <img id="prev_feature_img_needs" src="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80" alt="Needs" class="h-14 w-full object-cover rounded" />
            <input id="set_feature_img_needs" class="h-6 px-1.5 rounded bg-surface-subtle font-mono text-[9px]" type="text" placeholder="URL..." oninput="previewImageInput(this.value, 'prev_feature_img_needs')" />
          </div>
          <div class="bg-surface-card p-2 rounded flex flex-col gap-1 shadow-sm border border-hairline">
            <span class="font-label-caps text-[10px] text-text-tertiary truncate">3. CRM</span>
            <img id="prev_feature_img_crm" src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80" alt="CRM" class="h-14 w-full object-cover rounded" />
            <input id="set_feature_img_crm" class="h-6 px-1.5 rounded bg-surface-subtle font-mono text-[9px]" type="text" placeholder="URL..." oninput="previewImageInput(this.value, 'prev_feature_img_crm')" />
          </div>
          <div class="bg-surface-card p-2 rounded flex flex-col gap-1 shadow-sm border border-hairline">
            <span class="font-label-caps text-[10px] text-text-tertiary truncate">4. Experiences</span>
            <img id="prev_feature_img_meetings" src="https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=800&q=80" alt="Experiences" class="h-14 w-full object-cover rounded" />
            <input id="set_feature_img_meetings" class="h-6 px-1.5 rounded bg-surface-subtle font-mono text-[9px]" type="text" placeholder="URL..." oninput="previewImageInput(this.value, 'prev_feature_img_meetings')" />
          </div>
          <div class="bg-surface-card p-2 rounded flex flex-col gap-1 shadow-sm border border-hairline">
            <span class="font-label-caps text-[10px] text-text-tertiary truncate">5. Masterminds</span>
            <img id="prev_feature_img_collaborations" src="https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&q=80" alt="Masterminds" class="h-14 w-full object-cover rounded" />
            <input id="set_feature_img_collaborations" class="h-6 px-1.5 rounded bg-surface-subtle font-mono text-[9px]" type="text" placeholder="URL..." oninput="previewImageInput(this.value, 'prev_feature_img_collaborations')" />
          </div>
          <div class="bg-surface-card p-2 rounded flex flex-col gap-1 shadow-sm border border-hairline">
            <span class="font-label-caps text-[10px] text-text-tertiary truncate">6. Challenges</span>
            <img id="prev_feature_img_challenges" src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80" alt="Challenges" class="h-14 w-full object-cover rounded" />
            <input id="set_feature_img_challenges" class="h-6 px-1.5 rounded bg-surface-subtle font-mono text-[9px]" type="text" placeholder="URL..." oninput="previewImageInput(this.value, 'prev_feature_img_challenges')" />
          </div>
        </div>
      </div>

      <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col justify-between gap-space-sm border border-hairline">
        <div class="flex flex-col gap-space-xs">
          <div class="flex items-center gap-2 text-primary font-label-md text-label-md">
            <span class="material-symbols-outlined text-[20px]">badge</span>
            <span>Google OAuth 2.0 Credentials</span>
          </div>
          <p class="font-body-sm text-[12px] text-text-secondary leading-relaxed">
            Provision the authorized client ID from Google Cloud Console for 1-click verified founder sign-in.
          </p>
          <div class="mt-2 flex flex-col gap-1">
            <label class="font-label-caps text-label-caps text-text-tertiary uppercase">OAuth Client ID</label>
            <input id="set_google_client_id" class="h-9 px-3 rounded bg-surface-card text-on-surface font-mono text-[11px] focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="e.g. 123456789-xyz.apps.googleusercontent.com" type="text" />
          </div>
        </div>
        <span class="text-[11px] text-text-tertiary">Authorized origins: http://localhost:3000 &amp; production domain.</span>
      </div>
    </div>

    <!-- Floating / Sticky Save Toolbar -->
    <div class="pt-space-md flex items-center justify-between bg-surface-card">
      <span class="text-text-tertiary font-body-sm text-body-sm flex items-center gap-1">
        <span class="material-symbols-outlined text-[16px]">info</span> Media synchronizer updates the public landing page instantly
      </span>
      <button class="h-11 px-space-xl bg-primary-container hover:bg-emerald-deep text-on-primary font-label-md text-label-md rounded flex items-center gap-2 shadow-sm transition-all cursor-pointer" id="saveCmsBtn" type="submit">
        <span class="material-symbols-outlined text-[18px]">sync</span>
        <span>Synchronize Media &amp; Brand Settings</span>
      </button>
    </div>
  </form>
</section>'''

    # 8. Section 6: Event Publisher
    sec6_events = '''<!-- Section 6: Event Creation & Ticketing Publisher -->
<section class="bg-surface-card rounded-xl shadow-sm p-space-lg flex flex-col gap-space-lg border border-hairline" id="event-publisher-section">
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-space-sm">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <span class="font-headline-md text-headline-md text-text-primary font-semibold">Event Creation &amp; Ticketing Publisher</span>
        <span class="bg-primary-fixed text-on-primary-fixed font-label-caps text-label-caps px-2 py-0.5 rounded">NEW GATHERING</span>
      </div>
      <p class="font-body-sm text-body-sm text-text-secondary">
        Publish exclusive roundtables, signature founder dinners, and private salon experiences directly to active members.
      </p>
    </div>
    <span class="font-label-caps text-label-caps text-secondary uppercase tracking-widest font-bold">DISPATCH ENGINE • INDIA</span>
  </div>

  <form class="flex flex-col gap-space-lg" id="adminCreateEventForm" onsubmit="handleAdminCreateEvent(event)">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">
      <div class="flex flex-col gap-1 md:col-span-2">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Event Title *</label>
        <input id="evt_title" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary" placeholder="e.g. Founders Executive Roundtable — Q4 Scaling &amp; Cross-Border Capital" required type="text" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Event Category *</label>
        <select id="evt_category" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer">
          <option value="Founder / Business">Founder / Business</option>
          <option value="Closed-Door Mastermind" selected>Closed-Door Mastermind</option>
          <option value="Sports & Movement">Sports &amp; Movement</option>
          <option value="Outdoor & Adventure">Outdoor &amp; Adventure</option>
          <option value="Food & Dining">Food &amp; Dining</option>
          <option value="Games & Socials">Games &amp; Socials</option>
          <option value="Creative Learning">Creative Learning</option>
        </select>
      </div>

      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Signature Format Program *</label>
        <select id="evt_signature_format" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer">
          <option value="The Founder Table">The Founder Table</option>
          <option value="Founder Playbook">Founder Playbook</option>
          <option value="First Light Club">First Light Club</option>
          <option value="The Inner Circle Roundtable" selected>The Inner Circle Roundtable</option>
          <option value="After Hours">After Hours</option>
          <option value="Founder Field Trip">Founder Field Trip</option>
          <option value="Members Host">Members Host</option>
        </select>
      </div>

      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Event Date *</label>
        <input id="evt_date" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary" required type="date" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Display Time Window *</label>
        <input id="evt_time_str" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary" required type="text" placeholder="e.g. 07:00 PM - 10:00 PM IST" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Venue Name / Address *</label>
        <input id="evt_venue" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary" required type="text" placeholder="e.g. Executive Lounge, 12th Main, Indiranagar" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Host City Chapter *</label>
        <select id="evt_city" class="h-11 px-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary cursor-pointer">
          <option value="Bengaluru" selected>Bengaluru</option>
          <option value="Mumbai">Mumbai</option>
          <option value="Delhi NCR">Delhi NCR</option>
          <option value="Hyderabad">Hyderabad</option>
          <option value="Pune">Pune</option>
          <option value="Chennai">Chennai</option>
          <option value="Goa (Retreat Only)">Goa (Retreat Only)</option>
        </select>
      </div>
    </div>

    <!-- Google Maps Integration Row -->
    <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-sm border border-hairline">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Google Maps Navigation URL</label>
        <div class="flex items-center gap-2">
          <button class="text-primary hover:underline text-[12px] font-medium flex items-center gap-1 cursor-pointer" type="button" onclick="generateMapLinkFromVenue()">
            <span class="material-symbols-outlined text-[14px]">auto_fix_high</span> Generate Link from Venue
          </button>
          <span class="text-text-tertiary">•</span>
          <a id="evt_map_preview_btn" class="text-secondary hover:underline text-[12px] font-medium flex items-center gap-1 cursor-pointer" href="#" target="_blank" rel="noopener noreferrer" style="display:none;">
            <span class="material-symbols-outlined text-[14px]">open_in_new</span> Test Link
          </a>
        </div>
      </div>
      <input id="evt_google_maps_url" class="h-10 px-3 rounded bg-surface-card text-on-surface font-mono text-[12px] focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" type="url" placeholder="https://maps.google.com/?q=..." oninput="updateMapPreview(this.value)" />
    </div>

    <!-- Event Description & Agenda -->
    <div class="flex flex-col gap-1">
      <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Event Agenda, Focus Topics &amp; Speaker Notes *</label>
      <textarea id="evt_description" class="p-3 rounded bg-surface-subtle text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary resize-none leading-relaxed" rows="4" required placeholder="Exclusive 12-founder dinner and mastermind diving into post-Series A org architecture, managing secondary liquidity for early angels..."></textarea>
    </div>

    <!-- Registration Pricing Options -->
    <div class="bg-surface-subtle rounded-lg p-space-md flex flex-col gap-space-md border border-hairline">
      <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Registration &amp; Ticketing Access</label>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">
        <label class="flex items-start gap-3 p-3 rounded bg-surface-card cursor-pointer shadow-sm border border-hairline">
          <input checked class="mt-1 text-primary focus:ring-primary" name="pricingType" type="radio" value="free" onchange="toggleEventPricingFields(false)" />
          <div class="flex flex-col">
            <span class="font-label-md text-label-md font-semibold text-text-primary">Complimentary Guild Gathering (₹0)</span>
            <span class="text-text-secondary text-[12px]">Included with sovereign annual membership pass. Strict RSVP cap enforced.</span>
          </div>
        </label>
        <label class="flex items-start gap-3 p-3 rounded bg-surface-card cursor-pointer shadow-sm border border-hairline">
          <input class="mt-1 text-primary focus:ring-primary" name="pricingType" type="radio" value="paid" onchange="toggleEventPricingFields(true)" />
          <div class="flex flex-col">
            <span class="font-label-md text-label-md font-semibold text-text-primary">Paid Curated Experience</span>
            <span class="text-text-secondary text-[12px]">Requires entry fee to cover fine dining or multi-day retreat hospitality.</span>
          </div>
        </label>
      </div>
      <div id="evt_paid_fields_container" style="display:none;" class="grid grid-cols-1 sm:grid-cols-2 gap-space-md pt-1">
        <div class="flex flex-col gap-1">
          <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Entry Fee (INR ₹)</label>
          <input id="evt_price_amount" class="h-10 px-3 rounded bg-surface-card text-on-surface font-mono text-[13px] focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="0" type="number" min="0" value="0" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="font-label-caps text-label-caps text-text-tertiary uppercase">Ticket Inclusions Note</label>
          <input id="evt_what_is_included" class="h-10 px-3 rounded bg-surface-card text-on-surface font-body-sm text-body-sm focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" type="text" placeholder="e.g. 3-Course Dinner, Sommelier Curations" value="Full session access, curated networking, refreshments" />
        </div>
      </div>
    </div>

    <!-- Action CTA -->
    <div class="flex flex-col sm:flex-row items-center justify-between gap-space-md pt-space-xs">
      <div class="flex items-center gap-2 text-text-tertiary text-[12px]">
        <span class="material-symbols-outlined text-[16px] text-secondary">mark_email_read</span>
        <span>Will trigger instant push alerts &amp; calendar ICS invites to verified chapter members</span>
      </div>
      <button class="w-full sm:w-auto h-12 px-space-xl bg-primary-container hover:bg-emerald-deep text-on-primary font-label-md text-label-md rounded flex items-center justify-center gap-2 shadow-md transition-all cursor-pointer" type="submit">
        <span class="material-symbols-outlined text-[20px]">send_and_archive</span>
        <span>Publish Event to Member Network</span>
      </button>
    </div>
  </form>
</section>'''

    # Complete assembled markup
    tab_admin_full = f'''      <!-- TAB 9: ADMIN DASHBOARD & CMS (STITCH INTEGRATED UI) -->
      <div id="tab-admin" class="portal-tab" style="display: none;">
        <div class="flex flex-col w-full font-body-md text-on-surface">
{top_ribbon}
          <div class="max-w-7xl mx-auto w-full px-gutter py-space-lg flex flex-col gap-space-xl">
{header_banner}
{sec1_kpi}
{sec2_apps}
{sec3_audit}
{sec4_photos}
{sec5_cms}
{sec6_events}
          </div>
        </div>
      </div>'''

    return tab_admin_full

if __name__ == '__main__':
    content = generate_stitch_admin_markup()
    with open('stitch_admin_full.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated stitch_admin_full.html ({len(content)} bytes)")
