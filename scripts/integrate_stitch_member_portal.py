#!/usr/bin/env python3
"""
Integrate the Google Stitch Member Portal design into public/index.html.
Preserves all dynamic element IDs, API bindings, and onclick event handlers.
"""

import sys

PORTAL_REPLACEMENT = '''    <div class="portal-sidebar bg-surface-container-lowest border-r border-border-hairline shadow-sm">
      <div class="portal-sidebar-brand px-space-sm mb-space-md text-left">
        <div class="flex items-center gap-space-sm">
          <img src="/assets/logo.svg" class="w-8 h-8 rounded-full object-cover" alt="Member Portal Logo" loading="lazy" decoding="async" width="32" height="32">
          <div>
            <div class="font-headline-sm text-[16px] text-primary font-bold tracking-tight leading-tight">FOUNDER FOR FOUNDER</div>
            <div class="text-[11px] font-semibold text-secondary uppercase tracking-wider">Curated Member Portal</div>
          </div>
        </div>
      </div>

      <div class="px-space-sm mb-space-xs hidden lg:block">
        <span class="font-label-caps text-label-caps text-text-tertiary uppercase tracking-wider">Executive Console</span>
      </div>

      <ul class="sidebar-menu">
        <li class="sidebar-item active" onclick="switchPortalTab('dashboard', this)">
          <span class="material-symbols-outlined text-[18px]">dashboard</span>
          <span>Dashboard</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('directory', this)">
          <span class="material-symbols-outlined text-[18px]">group</span>
          <span>Discover Founders</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('needs', this)">
          <span class="material-symbols-outlined text-[18px]">handshake</span>
          <span>Needs &amp; Wants</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('crm', this)">
          <span class="material-symbols-outlined text-[18px]">conversion_path</span>
          <span>Leads &amp; CRM</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('attendance', this)">
          <span class="material-symbols-outlined text-[18px]">verified</span>
          <span>Attendance</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('meetings', this)">
          <span class="material-symbols-outlined text-[18px]">event_available</span>
          <span>1:1 Meetings</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('chat', this)">
          <span class="material-symbols-outlined text-[18px]">forum</span>
          <span>Founders Chat</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('events', this)">
          <span class="material-symbols-outlined text-[18px]">local_activity</span>
          <span>Events &amp; Experiences</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('challenge', this)">
          <span class="material-symbols-outlined text-[18px]">trophy</span>
          <span>Monthly Challenge</span>
        </li>
        <li class="sidebar-item" onclick="switchPortalTab('account', this)">
          <span class="material-symbols-outlined text-[18px]">credit_card</span>
          <span>Account &amp; Billing</span>
        </li>
        <li class="sidebar-item" id="adminTabLink" style="display: none; color: var(--emerald-700);" onclick="switchPortalTab('admin', this)">
          <span class="material-symbols-outlined text-[18px]">shield_person</span>
          <span>Admin CMS Panel</span>
        </li>
      </ul>

      <div class="hidden lg:block mt-auto pt-space-md border-t border-border-hairline">
        <div class="p-space-sm rounded bg-surface-subtle text-text-secondary">
          <span class="font-label-caps text-label-caps text-secondary block mb-1 uppercase tracking-wider">Concierge Desk</span>
          <span class="font-body-sm text-body-sm text-on-surface-variant block leading-snug">Private inquiries &amp; introductions are live.</span>
        </div>
      </div>
    </div>

    <div class="portal-main">

      <!-- Interactive View Switcher Tabs Ribbon -->
      <div class="mb-space-lg bg-surface-container-lowest p-space-xs rounded shadow-sm overflow-x-auto no-scrollbar border border-border-hairline">
        <div class="flex items-center gap-1 min-w-max" id="portal-tab-bar">
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 bg-primary-container text-on-primary shadow-sm font-semibold cursor-pointer" data-tab-target="dashboard" onclick="switchPortalTab('dashboard')" type="button">
            <span class="material-symbols-outlined text-[18px]">dashboard</span>
            <span>Executive Overview</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="directory" onclick="switchPortalTab('directory')" type="button">
            <span class="material-symbols-outlined text-[18px]">group</span>
            <span>Directory</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="needs" onclick="switchPortalTab('needs')" type="button">
            <span class="material-symbols-outlined text-[18px]">handshake</span>
            <span>Needs &amp; Wants</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="crm" onclick="switchPortalTab('crm')" type="button">
            <span class="material-symbols-outlined text-[18px]">conversion_path</span>
            <span>Deals Pipeline</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="attendance" onclick="switchPortalTab('attendance')" type="button">
            <span class="material-symbols-outlined text-[18px]">verified</span>
            <span>Attendance</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="meetings" onclick="switchPortalTab('meetings')" type="button">
            <span class="material-symbols-outlined text-[18px]">event_available</span>
            <span>1:1 Meetings</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="chat" onclick="switchPortalTab('chat')" type="button">
            <span class="material-symbols-outlined text-[18px]">forum</span>
            <span>Collective Chat</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="events" onclick="switchPortalTab('events')" type="button">
            <span class="material-symbols-outlined text-[18px]">local_activity</span>
            <span>Experiences</span>
          </button>
          <button class="tab-btn px-4 py-2 rounded text-label-md font-label-md transition-all flex items-center gap-2 text-on-surface-variant hover:bg-surface-subtle hover:text-on-surface cursor-pointer" data-tab-target="account" onclick="switchPortalTab('account')" type="button">
            <span class="material-symbols-outlined text-[18px]">badge</span>
            <span>Dossier &amp; Pass</span>
          </button>
        </div>
      </div>

      <!-- PORTAL HEADER WITH WELCOME & QUICK ACTIONS -->
      <div class="mb-space-lg bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-space-md border border-border-hairline">
        <div class="flex flex-col gap-1 max-w-2xl">
          <div class="flex items-center gap-space-sm">
            <span class="px-2 py-0.5 rounded-full text-label-caps font-label-caps bg-primary-fixed/60 text-primary uppercase font-bold">Executive Portfolio</span>
            <span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <span class="font-body-sm text-body-sm text-text-tertiary">Syndicate ID #FFF-BLR-0284</span>
          </div>
          <h1 class="font-headline-md text-headline-md text-text-primary tracking-tight font-bold" id="dashboardWelcome">Welcome, Member</h1>
          <p class="font-body-md text-body-md text-text-secondary leading-relaxed">Your curated founder network overview, peer accountability metrics, and active strategic pipeline.</p>
        </div>
        <div class="flex flex-wrap items-center gap-space-sm">
          <button class="px-4 py-2.5 rounded bg-surface-subtle text-text-primary hover:bg-surface-container-high transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm border border-border-hairline cursor-pointer" onclick="openLogMeetingModal()" type="button">
            <span class="material-symbols-outlined text-[18px] text-primary">add_circle</span>
            <span>Log 1:1 Meeting</span>
          </button>
          <button class="px-4 py-2.5 rounded bg-surface-subtle text-text-primary hover:bg-surface-container-high transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm border border-border-hairline cursor-pointer" onclick="openPostNeedModal()" type="button">
            <span class="material-symbols-outlined text-[18px] text-secondary">campaign</span>
            <span>Post a Strategic Need</span>
          </button>
          <button class="px-4 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm cursor-pointer" onclick="switchPortalTab('events')" type="button">
            <span class="material-symbols-outlined text-[18px] text-primary-fixed">confirmation_number</span>
            <span>View Upcoming Pass</span>
          </button>
        </div>
      </div>

      <!-- TAB 1: DASHBOARD OVERVIEW -->
      <div id="tab-dashboard" class="portal-tab active">
        <!-- 3 High Value Metric Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-space-md mb-space-lg">
          <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col justify-between border border-border-hairline">
            <div class="flex items-center justify-between mb-space-sm">
              <span class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Syndicate Status</span>
              <span class="w-8 h-8 rounded bg-primary-fixed/40 text-primary flex items-center justify-center">
                <span class="material-symbols-outlined text-[20px]">workspace_premium</span>
              </span>
            </div>
            <div>
              <div class="flex items-baseline gap-2">
                <span class="font-numeric-stat text-numeric-stat text-primary-container font-bold" id="dashMembershipStatus">ACTIVE</span>
                <span class="font-label-caps text-label-caps text-secondary font-bold">MEMBER</span>
              </div>
              <p class="font-body-sm text-body-sm text-text-tertiary mt-1" id="dashRenewalText">Annual Founder Pass • Renews Monthly</p>
            </div>
          </div>

          <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col justify-between border border-border-hairline">
            <div class="flex items-center justify-between mb-space-sm">
              <span class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Community Collaborations</span>
              <span class="w-8 h-8 rounded bg-surface-subtle text-text-primary flex items-center justify-center">
                <span class="material-symbols-outlined text-[20px]">hub</span>
              </span>
            </div>
            <div>
              <div class="font-numeric-stat text-numeric-stat text-text-primary font-bold" id="dashBizGenerated">Active</div>
              <p class="font-body-sm text-body-sm text-text-tertiary mt-1">Connected via Curated Community</p>
            </div>
          </div>

          <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col justify-between border border-border-hairline">
            <div class="flex items-center justify-between mb-space-sm">
              <span class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Pipeline Generated</span>
              <span class="w-8 h-8 rounded bg-secondary-fixed/50 text-secondary flex items-center justify-center">
                <span class="material-symbols-outlined text-[20px]">payments</span>
              </span>
            </div>
            <div>
              <div class="font-numeric-stat text-numeric-stat text-secondary font-bold" id="dashLeadsWon">0</div>
              <p class="font-body-sm text-body-sm text-text-tertiary mt-1">Active Deals &amp; Referrals Pipeline</p>
            </div>
          </div>
        </div>

        <!-- Monthly Presence & 1-on-1 Peer Accountability Banner -->
        <div class="bg-surface-container-low p-space-md lg:p-space-lg rounded shadow-sm flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-space-md mb-space-lg border border-border-hairline">
          <div class="flex items-start gap-space-md">
            <div class="w-12 h-12 rounded bg-primary-container text-on-primary flex items-center justify-center shrink-0 shadow-sm">
              <span class="material-symbols-outlined text-[26px]">task_alt</span>
            </div>
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-space-sm flex-wrap">
                <span class="font-label-caps text-label-caps text-primary font-bold uppercase">Monthly Presence &amp; Accountability</span>
                <span class="px-2 py-0.5 rounded-full text-label-caps font-label-caps bg-primary-fixed text-primary-container uppercase font-bold">Verified Streak</span>
              </div>
              <h2 class="font-headline-sm text-headline-sm text-text-primary font-semibold" id="dashAttendanceRate">100% Gathering Attendance Logged</h2>
              <p class="font-body-md text-body-md text-text-secondary" id="dashMeetingsStat">Peer Masterminds completed this month • Verified gathering check-in.</p>
            </div>
          </div>
          <div class="flex items-center gap-space-sm shrink-0 flex-wrap">
            <button class="px-4 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary text-label-md font-label-md transition-colors flex items-center gap-2 shadow-sm cursor-pointer" onclick="openLogMeetingModal()" type="button">
              <span class="material-symbols-outlined text-[18px]">add</span>
              <span>Log 1:1 Meeting</span>
            </button>
            <button class="px-4 py-2.5 rounded bg-surface-container-lowest text-text-primary hover:bg-surface-subtle text-label-md font-label-md transition-colors flex items-center gap-2 shadow-sm border border-border-hairline cursor-pointer" onclick="switchPortalTab('attendance')" type="button">
              <span class="material-symbols-outlined text-[18px]">history</span>
              <span>View History</span>
            </button>
          </div>
        </div>

        <!-- Two-Column Grid: Next Curated Gathering Ticket & Executive Deal Highlights -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-space-md">
          <!-- Next Curated Gathering Pass -->
          <div class="lg:col-span-6 bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col justify-between border border-border-hairline">
            <div>
              <div class="flex items-center justify-between mb-space-md">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-secondary text-[20px]">stars</span>
                  <span class="font-label-caps text-label-caps text-secondary uppercase font-bold">Your Next Curated Experience</span>
                </div>
                <span class="px-2.5 py-0.5 rounded-full text-label-caps font-label-caps bg-secondary-fixed/50 text-secondary uppercase font-bold">Dine • Flagship</span>
              </div>
              <h3 class="font-headline-sm text-headline-sm text-text-primary mb-2">The Inner Circle Dinner: AI Founders &amp; Compute Strategies</h3>
              <p class="font-body-md text-body-md text-text-secondary mb-space-md leading-relaxed">
                Intimate closed-door dinner hosted at The Leela Palace, exploring local GPU cluster access, token optimization, and enterprise pricing models.
              </p>
              <div class="flex flex-col gap-2 font-body-sm text-body-sm text-text-tertiary mb-space-md">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-[18px] text-primary">calendar_today</span>
                  <span>Thu, 24 Oct 2026 • 07:00 PM IST</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-[18px] text-primary">location_on</span>
                  <span>The Leela Palace, Old Airport Road, Bengaluru</span>
                </div>
              </div>
            </div>
            <div class="flex items-center justify-between pt-space-sm border-t border-border-hairline">
              <span class="font-label-caps text-label-caps text-primary font-bold uppercase">RSVP Confirmed (#FF-892)</span>
              <button class="px-4 py-2 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md cursor-pointer" onclick="switchPortalTab('events')" type="button">
                View Digital Pass
              </button>
            </div>
          </div>

          <!-- Recent Community Opportunities -->
          <div class="lg:col-span-6 bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col justify-between border border-border-hairline">
            <div>
              <div class="flex items-center justify-between mb-space-md">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-primary text-[20px]">handshake</span>
                  <span class="font-label-caps text-label-caps text-primary uppercase font-bold">Live Opportunities</span>
                </div>
                <button class="text-label-caps font-label-caps text-secondary hover:underline uppercase cursor-pointer" onclick="switchPortalTab('needs')">View All →</button>
              </div>
              <h3 class="font-headline-sm text-headline-sm text-text-primary mb-2">Recent Community Opportunities</h3>
              <div id="recentOpportunitiesList" class="flex flex-col gap-3 mt-4"></div>
            </div>
            <div class="pt-space-sm border-t border-border-hairline flex items-center justify-between">
              <span class="font-body-sm text-body-sm text-text-tertiary">Verified peer-to-peer asks</span>
              <button class="px-4 py-2 rounded bg-surface-subtle text-text-primary hover:bg-surface-container-high transition-colors text-label-md font-label-md cursor-pointer" onclick="openPostNeedModal()" type="button">
                + Post a Need
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: MEMBER DIRECTORY -->
      <div id="tab-directory" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm mb-space-md border border-border-hairline">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-space-md mb-space-md">
            <div>
              <span class="font-label-caps text-label-caps text-primary uppercase font-bold">Curated Member Directory</span>
              <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Discover Fellow Founders</h2>
              <p class="font-body-md text-body-md text-text-secondary">Search verified venture operators, cross-disciplinary leaders, and capital allocators across India.</p>
            </div>
            <div class="flex items-center gap-space-sm text-label-caps text-label-caps text-text-tertiary uppercase">
              <span class="material-symbols-outlined text-[18px] text-secondary">verified</span>
              <span>Vetted Community Directory</span>
            </div>
          </div>

          <!-- Search & Filters -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-space-sm pt-space-xs">
            <div class="md:col-span-6 relative">
              <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary text-[20px]">search</span>
              <input type="text" id="dirSearchInput" class="w-full pl-10 pr-4 py-2.5 rounded bg-surface-subtle text-text-primary placeholder:text-text-tertiary text-body-md font-body-md focus:outline-none focus:bg-surface-container-lowest focus:ring-1 focus:ring-primary shadow-sm border border-border-hairline" placeholder="Search by name, company, expertise, category, or city..." onkeyup="filterDirectory()">
            </div>
            <div class="md:col-span-3">
              <select id="dirStageFilter" class="w-full px-3 py-2.5 rounded bg-surface-subtle text-text-primary text-body-md font-body-md focus:outline-none focus:ring-1 focus:ring-primary shadow-sm border border-border-hairline" onchange="filterDirectory()">
                <option value="">All Business Stages</option>
                <option value="Early">Early</option>
                <option value="Seed">Seed</option>
                <option value="Growth">Growth</option>
                <option value="Established">Established</option>
                <option value="Scaling">Scaling</option>
              </select>
            </div>
            <div class="md:col-span-3">
              <select id="dirCityFilter" class="w-full px-3 py-2.5 rounded bg-surface-subtle text-text-primary text-body-md font-body-md focus:outline-none focus:ring-1 focus:ring-primary shadow-sm border border-border-hairline" onchange="filterDirectory()">
                <option value="">All Cities</option>
                <option value="Bengaluru">Bengaluru</option>
                <option value="Mumbai">Mumbai</option>
                <option value="Delhi NCR">Delhi NCR</option>
                <option value="Hyderabad">Hyderabad</option>
                <option value="Pune">Pune</option>
                <option value="Chennai">Chennai</option>
              </select>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-space-md" id="directoryContainer"></div>
      </div>

      <!-- TAB 3: NEEDS & WANTS ENGINE -->
      <div id="tab-needs" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-space-md mb-space-md border border-border-hairline">
          <div>
            <span class="font-label-caps text-label-caps text-secondary uppercase font-bold">Collective Strategic Marketplace</span>
            <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Needs &amp; Wants Asks</h2>
            <p class="font-body-md text-body-md text-text-secondary">High-leverage asks posted by vetted founders. No noise, purely verified peer-to-peer introductions.</p>
          </div>
          <button class="px-4 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm shrink-0 cursor-pointer" onclick="openPostNeedModal()" type="button">
            <span class="material-symbols-outlined text-[18px]">add</span>
            <span>Post a Strategic Need</span>
          </button>
        </div>

        <!-- Category Filter Pills -->
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar mb-space-md">
          <button class="px-3.5 py-1.5 rounded-full text-label-caps font-label-caps bg-primary-container text-on-primary uppercase cursor-pointer" type="button">All Asks</button>
          <button class="px-3.5 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Customer Leads</button>
          <button class="px-3.5 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Fundraising</button>
          <button class="px-3.5 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Executive Hiring</button>
          <button class="px-3.5 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Tech &amp; Infra</button>
          <button class="px-3.5 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Legal &amp; Tax</button>
        </div>

        <div class="flex flex-col gap-space-md" id="needsContainer"></div>
      </div>

      <!-- TAB 4: LEADS & REFERRALS CRM -->
      <div id="tab-crm" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-md mb-space-md border border-border-hairline">
          <div>
            <span class="font-label-caps text-label-caps text-primary uppercase font-bold">Inter-Founders Deal Flow</span>
            <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Leads &amp; Referrals CRM Pipeline</h2>
            <p class="font-body-md text-body-md text-text-secondary">Record, introduce, and track your business deals and peer referrals with trusted partners.</p>
          </div>
          <div class="flex items-center gap-space-sm flex-wrap">
            <button class="px-4 py-2.5 rounded bg-surface-subtle text-text-primary hover:bg-surface-container-high transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm border border-border-hairline cursor-pointer" onclick="openRecordDealModal()" type="button">
              <span class="material-symbols-outlined text-[18px] text-secondary">handshake</span>
              <span>Record Business Deal</span>
            </button>
            <button class="px-4 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm cursor-pointer" onclick="openAddLeadModal()" type="button">
              <span class="material-symbols-outlined text-[18px]">add</span>
              <span>Add Lead</span>
            </button>
          </div>
        </div>

        <div class="bg-primary-fixed/20 border border-primary-fixed p-space-md rounded mb-space-md text-body-sm text-primary flex items-start gap-space-sm">
          <span class="material-symbols-outlined text-[20px] text-primary shrink-0">info</span>
          <div>
            <strong>Consent Disclaimer:</strong> Leads and referrals shared within Founder for Founder are business opportunities and trusted peer introductions, not guaranteed commercial outcomes. Always confirm consent before sharing external contact details.
          </div>
        </div>

        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm border border-border-hairline">
          <h3 class="font-headline-sm text-headline-sm text-text-primary mb-space-md">My Active Opportunities &amp; Leads</h3>
          <div id="leadsList" class="flex flex-col gap-3"></div>
        </div>
      </div>

      <!-- TAB 5: MONTHLY ATTENDANCE TRACKER -->
      <div id="tab-attendance" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-md mb-space-md border border-border-hairline">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-primary-fixed/50 text-primary-container rounded-full text-label-caps font-label-caps font-bold uppercase mb-2">
              <span class="material-symbols-outlined text-[16px]">verified</span>
              <span>MONTHLY PRESENCE &amp; ACCOUNTABILITY</span>
            </div>
            <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Monthly Event Attendance Tracker</h2>
            <p class="font-body-md text-body-md text-text-secondary">Verify your presence across all curated gatherings, private roundtables, and retreats hosted each month.</p>
          </div>
          <div class="flex items-center gap-space-sm flex-wrap">
            <select id="attendanceMonthSelect" class="px-3 py-2 rounded bg-surface-subtle font-label-md text-label-md text-text-primary border border-border-hairline shadow-sm cursor-pointer" onchange="filterAttendanceMonth()">
              <option value="2026-10">October 2026</option>
              <option value="2026-11">November 2026</option>
            </select>
            <button class="px-4 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm cursor-pointer" onclick="openCheckinModal()" type="button">
              <span class="material-symbols-outlined text-[18px]">pin</span>
              <span>PIN Check-In</span>
            </button>
          </div>
        </div>

        <!-- Attendance Stats KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md mb-space-lg">
          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Monthly Attendance Rate</div>
            <div class="flex items-baseline gap-2 my-2">
              <span class="font-numeric-stat text-3xl font-bold text-primary" id="attRateValue">100%</span>
              <span class="font-body-sm text-body-sm text-text-tertiary" id="attEventsAttendedRatio">(3/3 Completed)</span>
            </div>
            <div class="w-full h-2 bg-surface-subtle rounded-full overflow-hidden mt-1">
              <div id="attRateBar" class="h-full bg-primary-container rounded-full transition-all duration-500" style="width: 100%;"></div>
            </div>
          </div>

          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Events Hosted This Month</div>
            <div class="font-numeric-stat text-3xl font-bold text-text-primary my-2" id="attTotalEvents">4</div>
            <div class="font-body-sm text-xs text-primary">Across All Signature Formats</div>
          </div>

          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Active Presence Streak</div>
            <div class="font-numeric-stat text-3xl font-bold text-secondary my-2" id="attStreakValue">3</div>
            <div class="font-body-sm text-xs text-text-tertiary">Consecutive Gatherings Attended</div>
          </div>

          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Accountability Standing</div>
            <div class="font-headline-sm text-lg font-bold text-primary my-2 flex items-center gap-1" id="attStandingTier">
              <span class="material-symbols-outlined text-[20px] text-primary">verified</span>
              <span>High-Signal Founder</span>
            </div>
            <div class="font-body-sm text-xs text-text-secondary">High-Trust &amp; Full Peer Leverage</div>
          </div>
        </div>

        <!-- Monthly Event Presence Table / Feed -->
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm border border-border-hairline">
          <div class="flex items-center justify-between mb-space-md flex-wrap gap-2">
            <h3 class="font-headline-sm text-headline-sm text-text-primary" id="attendanceListTitle">Gatherings Hosted in October 2026</h3>
            <span class="font-body-sm text-body-sm text-text-tertiary">Real-time check-in and attendance verification log</span>
          </div>
          <div id="attendanceEventsList" class="flex flex-col gap-3"></div>
        </div>
      </div>

      <!-- TAB 6: 1-TO-1 FOUNDER MEETINGS TRACKER -->
      <div id="tab-meetings" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-md mb-space-md border border-border-hairline">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-primary-fixed/50 text-primary-container rounded-full text-label-caps font-label-caps font-bold uppercase mb-2">
              <span class="material-symbols-outlined text-[16px]">groups</span>
              <span>PEER-TO-PEER ENGAGEMENT</span>
            </div>
            <h2 class="font-headline-md text-headline-md text-text-primary font-bold">1-to-1 Founder Meetings Tracker</h2>
            <p class="font-body-md text-body-md text-text-secondary">Log, review, and track individual 1:1 conversations, strategic synergies, and relationship outcomes with fellow members.</p>
          </div>
          <button class="px-4 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm cursor-pointer" onclick="openLogMeetingModal()" type="button">
            <span class="material-symbols-outlined text-[18px]">add</span>
            <span>Log 1:1 Founder Meeting</span>
          </button>
        </div>

        <!-- 1:1 Meeting KPI Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-space-md mb-space-lg">
          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">1:1 Meetings This Month</div>
            <div class="font-numeric-stat text-3xl font-bold text-primary my-2" id="meetingsThisMonth">3</div>
            <div class="font-body-sm text-xs text-primary" id="meetingsMonthName">October 2026</div>
          </div>
          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Synergies &amp; Deals Spawned</div>
            <div class="font-numeric-stat text-3xl font-bold text-text-primary my-2" id="meetingsSynergies">2</div>
            <div class="font-body-sm text-xs text-text-tertiary">Referrals &amp; Partnerships in Progress</div>
          </div>
          <div class="bg-surface-container-lowest p-space-md rounded shadow-sm border border-border-hairline flex flex-col justify-between">
            <div class="font-label-caps text-label-caps text-text-tertiary uppercase font-bold">Lifetime 1:1 Conversations</div>
            <div class="font-numeric-stat text-3xl font-bold text-text-primary my-2" id="meetingsTotal">3</div>
            <div class="font-body-sm text-xs text-text-tertiary">High-Trust Peer Exchanges</div>
          </div>
        </div>

        <!-- 1:1 Meetings Feed -->
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm border border-border-hairline">
          <div class="flex items-center justify-between mb-space-md flex-wrap gap-2">
            <h3 class="font-headline-sm text-headline-sm text-text-primary">Recorded 1-to-1 Meetings</h3>
            <span class="font-body-sm text-body-sm text-text-tertiary">Confidential record for your personal CRM &amp; peer leverage</span>
          </div>
          <div id="meetingsFeedContainer" class="flex flex-col gap-3"></div>
        </div>
      </div>

      <!-- TAB 7: EVENTS & EXPERIENCES HUB -->
      <div id="tab-events" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-md mb-space-md border border-border-hairline">
          <div>
            <span class="font-label-caps text-label-caps text-primary uppercase font-bold">Curated Gatherings</span>
            <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Experiences &amp; Salons Hub</h2>
            <p class="font-body-md text-body-md text-text-secondary">Activities across our 5 Pillars: Play, Explore, Dine, Build, and Celebrate.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="px-3 py-1.5 rounded bg-secondary-fixed/40 text-secondary text-label-caps font-label-caps font-bold uppercase">12 Seats Strict Cap Per Table</span>
          </div>
        </div>

        <!-- 5 Pillars Filter Bar -->
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar mb-space-md">
          <button class="px-4 py-1.5 rounded-full text-label-caps font-label-caps bg-primary-container text-on-primary uppercase cursor-pointer" type="button">All Pillars</button>
          <button class="px-4 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Play</button>
          <button class="px-4 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Explore</button>
          <button class="px-4 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Dine (Salons)</button>
          <button class="px-4 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Build (Hackathons)</button>
          <button class="px-4 py-1.5 rounded-full text-label-caps font-label-caps bg-surface-container-lowest text-text-secondary hover:text-text-primary uppercase shadow-sm border border-border-hairline cursor-pointer" type="button">Celebrate</button>
        </div>

        <div id="eventsContainer" class="flex flex-col gap-space-lg"></div>
      </div>

      <!-- TAB 8: CHALLENGES -->
      <div id="tab-challenge" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm mb-space-md border border-border-hairline">
          <span class="font-label-caps text-label-caps text-primary uppercase font-bold">Syndicate Growth</span>
          <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Monthly Founder Challenge</h2>
          <p class="font-body-md text-body-md text-text-secondary">Community-wide accountability sprints to scale key operational benchmarks together.</p>
        </div>

        <div id="challengeDetailsCard" class="card mb-6"></div>

        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm border border-border-hairline">
          <h3 class="font-headline-sm text-headline-sm text-text-primary mb-space-md">Community Leaderboard</h3>
          <div id="leaderboardList" class="flex flex-col gap-2"></div>
        </div>
      </div>

      <!-- TAB 9: FOUNDERS COLLECTIVE CHAT -->
      <div id="tab-chat" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-md mb-space-md border border-border-hairline">
          <div>
            <div class="flex items-center gap-2 mb-1 flex-wrap">
              <span class="px-2.5 py-0.5 rounded-full text-label-caps font-label-caps bg-primary-fixed text-primary-container font-bold uppercase">ACTIVE MEMBERS ONLY</span>
              <span class="text-body-sm font-semibold text-primary flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">lock</span> Confidential &amp; Curated
              </span>
            </div>
            <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Founders Collective Lounge</h2>
            <p class="font-body-md text-body-md text-text-secondary">Unfiltered peer discussions, deal flow, strategic introductions, and collaboration with verified founders across India.</p>
          </div>
          <div class="flex items-center gap-3">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10B981]"></span>
            <span class="font-label-md text-label-md font-bold text-primary">Vetted Founders Room</span>
          </div>
        </div>

        <!-- Membership Active Room -->
        <div id="chatActiveContainer" class="chat-container">
          <div class="chat-layout single-room bg-surface-container-lowest rounded shadow-sm border border-border-hairline overflow-hidden">
            <!-- Messages Stream Area -->
            <div class="chat-main-pane">
              <div class="chat-main-header p-space-md border-b border-border-hairline flex items-center justify-between bg-surface-subtle">
                <div>
                  <h4 class="font-label-md text-label-md font-bold text-primary flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px]">forum</span>
                    <span>Founders Collective Lounge</span>
                  </h4>
                  <div class="font-body-sm text-xs text-text-tertiary">Unified founder room for all verified members — discuss challenges, exchange warm intros, and collaborate.</div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="font-label-caps text-xs text-primary bg-primary-fixed/40 px-2 py-1 rounded flex items-center gap-1 font-bold">
                    <span class="material-symbols-outlined text-[14px]">shield</span> Honor Code
                  </span>
                  <button type="button" class="px-3 py-1 rounded bg-surface-container-lowest text-text-primary hover:bg-surface-container-high transition-colors text-body-sm font-medium border border-border-hairline cursor-pointer flex items-center gap-1" onclick="loadChatMessages()">
                    <span class="material-symbols-outlined text-[16px]">refresh</span> Refresh
                  </button>
                </div>
              </div>

              <div class="chat-messages-area p-space-md min-h-[360px] max-h-[500px] overflow-y-auto flex flex-col gap-3" id="chatMessagesArea">
                <!-- Dynamically populated messages -->
              </div>

              <!-- Chat Composer Area -->
              <div class="chat-composer-area p-space-md border-t border-border-hairline bg-surface-subtle flex gap-space-sm items-center">
                <textarea id="chatInputText" class="w-full p-2.5 rounded bg-surface-container-lowest text-text-primary text-body-md border border-border-hairline focus:outline-none focus:ring-1 focus:ring-primary shadow-sm" placeholder="Type your message to the founder community... (Press Enter to send, Shift+Enter for new line)" rows="1" onkeydown="handleChatKeyDown(event)"></textarea>
                <button type="button" class="px-5 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md flex items-center gap-2 shadow-sm cursor-pointer shrink-0" id="chatSendBtn" onclick="handleSendChatMessage()">
                  <span>Send</span>
                  <span class="material-symbols-outlined text-[16px]">send</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Membership Gate Fallback for Non-Members -->
        <div id="chatGateCard" class="chat-gate-overlay bg-surface-container-lowest p-space-xl rounded shadow-sm border border-border-hairline text-center" style="display: none;">
          <div class="w-16 h-16 rounded-full bg-primary-fixed/40 text-primary flex items-center justify-center mx-auto mb-space-md">
            <span class="material-symbols-outlined text-[32px]">lock</span>
          </div>
          <h3 class="font-headline-sm text-headline-sm text-text-primary mb-2">Founders Collective Chat Requires an Active Membership</h3>
          <p class="font-body-md text-body-md text-text-secondary max-w-xl mx-auto mb-space-lg">
            To maintain a high-trust, confidential environment, access to the Founders Collective Chat is exclusively reserved for vetted, active community members. Activate your membership to join live conversations, explore deal flows, and connect directly with fellow founders across India.
          </p>
          <div class="flex gap-space-md flex-wrap justify-center">
            <button class="px-5 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md cursor-pointer" onclick="switchPortalTab('account')">
              Activate Membership Plan →
            </button>
            <button class="px-5 py-2.5 rounded bg-surface-subtle text-text-primary hover:bg-surface-container-high transition-colors text-label-md font-label-md border border-border-hairline cursor-pointer" onclick="switchPortalTab('dashboard')">
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      <!-- TAB 10: ACCOUNT & BILLING SETTINGS -->
      <div id="tab-account" class="portal-tab" style="display: none;">
        <div class="bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm mb-space-md border border-border-hairline">
          <span class="font-label-caps text-label-caps text-primary uppercase font-bold">Executive Credentials</span>
          <h2 class="font-headline-md text-headline-md text-text-primary font-bold">Dossier, Membership &amp; Privacy</h2>
          <p class="font-body-md text-body-md text-text-secondary">Manage your accredited founder identity, billing renewal terms, and contact discoverability settings.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
          <!-- Member Pass Details Card -->
          <div class="lg:col-span-5 bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm flex flex-col justify-between border border-border-hairline">
            <div>
              <div class="flex items-center justify-between mb-space-md">
                <span class="font-label-caps text-label-caps text-secondary uppercase font-bold">Curated Member Pass</span>
                <span class="px-2.5 py-0.5 rounded-full text-label-caps font-label-caps bg-primary-fixed/50 text-primary-container font-bold uppercase">Active Tier</span>
              </div>
              <div class="p-space-md rounded bg-surface-subtle mb-space-md">
                <div class="flex items-center gap-3 mb-space-sm">
                  <div class="w-12 h-12 rounded-full bg-primary-container text-on-primary flex items-center justify-center font-bold text-label-md" id="accAvatar">ME</div>
                  <div>
                    <h3 class="font-label-md text-label-md text-text-primary font-bold" id="accName">Member Name</h3>
                    <span class="font-body-sm text-body-sm text-text-tertiary" id="accRole">Executive Founder</span>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-2 pt-2 border-t border-border-hairline text-body-sm">
                  <div>
                    <span class="font-label-caps text-[10px] text-text-tertiary uppercase block">Member Pass ID</span>
                    <span class="font-mono text-xs font-semibold text-text-primary">#FFF-BLR-0284</span>
                  </div>
                  <div>
                    <span class="font-label-caps text-[10px] text-text-tertiary uppercase block">Valid Through</span>
                    <span class="font-body-sm text-xs font-semibold text-text-primary" id="accountRenewalDate">Auto-renews monthly</span>
                  </div>
                </div>
              </div>
              <div class="space-y-3 font-body-sm text-body-sm text-text-secondary">
                <div class="flex items-center justify-between py-1">
                  <span>Chapter Affiliation</span>
                  <span class="font-medium text-text-primary">Bengaluru Executive Core</span>
                </div>
                <div class="flex items-center justify-between py-1">
                  <span>Host Privileges</span>
                  <span class="font-medium text-primary">Accredited Member</span>
                </div>
              </div>
            </div>
            <div class="pt-space-md border-t border-border-hairline mt-space-md flex items-center justify-between">
              <span class="font-body-sm text-xs text-text-tertiary">Membership Plan</span>
              <button class="text-error hover:underline text-body-sm font-semibold cursor-pointer" onclick="handleCancelAutoRenew()" type="button">Cancel Auto-Renewal</button>
            </div>
          </div>

          <!-- Privacy & Visibility Preferences Form -->
          <div class="lg:col-span-7 bg-surface-container-lowest p-space-md lg:p-space-lg rounded shadow-sm border border-border-hairline">
            <h3 class="font-headline-sm text-headline-sm text-text-primary mb-2">Privacy &amp; Visibility Preferences</h3>
            <p class="font-body-sm text-body-sm text-text-secondary mb-space-md">Control how your contact details appear in the verified member directory.</p>
            <form id="privacyForm" onsubmit="handleSavePrivacy(event)" class="space-y-4">
              <div>
                <label class="block font-label-md text-label-md text-text-primary mb-1">Preferred Contact Method</label>
                <select id="acc_contact_method" class="w-full px-3 py-2.5 rounded bg-surface-subtle text-text-primary text-body-md border border-border-hairline focus:outline-none focus:ring-1 focus:ring-primary shadow-sm">
                  <option value="In-App">In-App Messaging</option>
                  <option value="Email">Email</option>
                  <option value="WhatsApp">WhatsApp</option>
                </select>
              </div>
              <div class="flex items-center gap-3 py-1">
                <input type="checkbox" id="acc_phone_visible" checked class="w-4 h-4 rounded text-primary focus:ring-primary border-border-hairline">
                <label for="acc_phone_visible" class="font-body-sm text-body-sm text-text-primary">Show my phone number to approved members</label>
              </div>
              <div class="flex items-center gap-3 py-1">
                <input type="checkbox" id="acc_email_visible" checked class="w-4 h-4 rounded text-primary focus:ring-primary border-border-hairline">
                <label for="acc_email_visible" class="font-body-sm text-body-sm text-text-primary">Show my email to approved members</label>
              </div>
              <button type="submit" class="px-5 py-2.5 rounded bg-primary-container text-on-primary hover:bg-tertiary transition-colors text-label-md font-label-md shadow-sm cursor-pointer">
                Save Preferences
              </button>
            </form>
          </div>
        </div>
      </div>
'''

def main():
    target_path = 'public/index.html'
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    start_anchor = '<div id="portalPage" class="portal-container">\n    <div class="portal-sidebar">'
    end_anchor = '      <!-- TAB 9: ADMIN DASHBOARD & CMS -->'
    
    start_pos = content.find(start_anchor)
    if start_pos == -1:
        print(f"Error: start anchor not found: {start_anchor}")
        sys.exit(1)
        
    start_cut = start_pos + len('<div id="portalPage" class="portal-container">\n')
    
    end_pos = content.find(end_anchor, start_cut)
    if end_pos == -1:
        print(f"Error: end anchor not found: {end_anchor}")
        sys.exit(1)

    new_content = content[:start_cut] + PORTAL_REPLACEMENT + '\n' + content[end_pos:]

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("Successfully integrated Stitch Member Portal into public/index.html!")

if __name__ == '__main__':
    main()
