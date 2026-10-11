# FOUNDER FOR FOUNDER (f4f) — MASTER RECONSTRUCTION PROMPT & SYSTEM SPECIFICATION
> **Version 3.4 • Powered by snalts.co • Production Blueprint**  
> *Consolidated master prompt and end-to-end engineering specification to regenerate the entire Founder for Founder web platform from scratch.*

---

## TABLE OF CONTENTS
1. [How to Use This Master Prompt](#1-how-to-use-this-master-prompt)
2. [The Verbatim Master AI Prompt](#2-the-verbatim-master-ai-prompt)
3. [Brand Identity, Copy Deck & Positioning](#3-brand-identity-copy-deck--positioning)
4. [Strict Design System, CSS & Animation Tokens](#4-strict-design-system-css--animation-tokens)
5. [Curated 16:9 Meeting Photos Slower Steady Slider](#5-curated-169-meeting-photos-slower-steady-slider)
6. [12-Question Comprehensive Admissions Questionnaire](#6-12-question-comprehensive-admissions-questionnaire)
7. [Monthly Attendance Accountability Tracker](#7-monthly-attendance-accountability-tracker)
8. [Founder 1-to-1 Meetings Tracker](#8-founder-1-to-1-meetings-tracker)
9. [Founders Collective Chat Lounge](#9-founders-collective-chat-lounge)
10. [Dynamic Content Management System (CMS) & Media Engine](#10-dynamic-content-management-system-cms--media-engine)
11. [Complete SQLite Database Schema (All 13 Tables DDL)](#11-complete-sqlite-database-schema-all-13-tables-ddl)
12. [Complete REST API Endpoints Specification](#12-complete-rest-api-endpoints-specification)
13. [Frontend Page & Component Architecture](#13-frontend-page--component-architecture)
14. [Official Social Media Profiles Architecture (Footer Only)](#14-official-social-media-profiles-architecture-footer-only)
15. [Verification & Quality Assurance Checklist](#15-verification--quality-assurance-checklist)

---

## 1. HOW TO USE THIS MASTER PROMPT

This document serves as the **single source of truth** for the Founder for Founder ecosystem. It can be fed in its entirety (or section-by-section) into any advanced AI coding assistant (Antigravity, Claude, ChatGPT, Cursor, Gemini) or handed to a senior full-stack engineering team.

### Primary Directives:
* **Zero External Heavy Dependencies**: No node_modules, webpack, vite, react, or external backend frameworks. The backend is 100% self-contained Python 3 standard library (`http.server`, `urllib`, `sqlite3`, `hashlib`, `json`). The frontend is high-performance Vanilla HTML5, modern CSS3 with custom properties, and modular Vanilla JavaScript.
* **Single Directory Architecture**: Runs effortlessly locally or deployed on any Linux/Windows server with `python server.py`.
* **Zero Missing Features**: Contains the complete Admissions Funnel, Attendance Tracker, 1:1 Meetings Logger, Curated 16:9 Meeting Photos Slider, Official Social Links, Collective Chat Lounge, Media CMS, and Member Portal.

---

## 2. THE VERBATIM MASTER AI PROMPT

Copy and paste the following prompt block directly to command an AI assistant to build the entire platform:

```markdown
Act as a Principal Full-Stack Engineer, Product Architect, and UI/UX Designer.
Build a complete, standalone, production-ready community and collaboration platform for "Founder for Founder" (powered by snalts.co) — a vetted, high-trust network of ambitious startup founders and scale-up leaders across India.

The entire solution must be contained in a single project directory with zero heavy build tools or framework overhead. Use a clean, robust Python 3 standard library HTTP backend with SQLite database persistence, paired with a modern Vanilla HTML5, CSS3, and JavaScript Single Page Application (SPA).

KEY SYSTEM MANDATES & ARCHITECTURE:

1. STRICT BRAND IDENTITY & DESIGN SYSTEM:
   - Platform: "Founder for Founder", powered by snalts.co.
   - Palette: Deep Forest Emerald (#064E3B, #047857), Mint Accents (#10B981, #34D399, #A7F3D0), Warm Mint Tint (#F3FBF7, #E4F7EE), Deep Ink (#0B0F0D).
   - Rich Gradients: Use linear-gradient(135deg, #064E3B 0%, #047857 50%, #059669 100%) on banner highlights, counter strips, and key CTA accents.
   - Typography: 'DM Serif Display' for headings, 'Plus Jakarta Sans' for body and interface elements.
   - MANDATORY PROHIBITION OF ITALIC/SLANTED TEXT: All text must be strictly upright ('font-style: normal !important;'). Never use slanted or italic styling anywhere across the application.
   - Button Corners: Strict 6px corner radius ('border-radius: 6px !important;'). Never use pill-shaped rounded-full buttons.
   - Card Images: No opaque, frosted, or tinted rectangular boxes over card photography in 'Ways We Collaborate', 'Core Philosophy', 'Curated Experiences', or 'Meeting Photos'. Content must sit directly over the imagery with a subtle bottom gradient scrim (linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(6,78,59,0.3) 40%, rgba(0,0,0,0.92) 100%)) and dual text shadows (0 2px 4px rgba(0,0,0,0.85), 0 4px 12px rgba(0,0,0,0.6)).
   - Card Badges: Crisp Mint Emerald (#A7F3D0) text on translucent dark emerald backgrounds (rgba(6,78,59,0.75)) with glowing 1px border (#10B981).

2. COMMUNITY METRICS & BRAND STRIP:
   - Live verified counters: '1,528+ Verified Founders & Operators', '27 Curated Gatherings & Private Experiences', '4.9/5 Peer Trust Rating'.
   - DO NOT display 'verified business generated' metric on the public landing strip.
   - Display a dedicated heading: 'Businesses Connected With Us' positioned immediately above the continuously scrolling horizontal brand marquee strip.

3. DYNAMIC MEDIA & CONTENT MANAGEMENT SYSTEM (CMS):
   - Every single image and banner must be editable dynamically through an Admin CMS:
     * Hero background image
     * Brand logo
     * 3 Capsule collage photos
     * 4 Core Philosophy card photos
     * 5 Ways We Collaborate card photos
     * 6 Platform Feature showcase tab photos
     * Gathering posters & event images
     * Meeting Photos Gallery (16:9 aspect ratio slider)
   - Provide an Admin Media Manager supporting both drag-and-drop file upload (stored in '/assets/uploads/') and direct image URL input with real-time thumbnail previews.
   - Persist all CMS settings in the SQLite 'system_settings' and 'event_gallery' tables so custom changes survive server restarts.
   - Frontend must hydrate all images and text dynamically from 'GET /api/public/content' on load.

4. 12-POINT COMPREHENSIVE ADMISSIONS QUESTIONNAIRE ("SHOW INTEREST"):
   - When a person shows interest in joining the community, capture their complete founder and business intelligence through a structured multi-step modal with all 12 questions:
     1. Name of Business (`business_name`)
     2. Brief about Business (`business_description` - products, target clients, scale)
     3. Business being carried out from how many years (`years_in_business`: Less than 1 Year, 1-2 Years, 3-5 Years, 5-10 Years, 10+ Years)
     4. Team Size (`team_size`: Solo Founder [1], 2-10 Members, 11-50 Members, 51-200 Members, 200+ Members)
     5. Type of Firm (`firm_type`: Private Limited [Pvt Ltd], LLP, Partnership Firm, Sole Proprietorship, Public Limited, OPC, Other)
     6. Business Instagram Link if any (`instagram`, optional URL)
     7. LinkedIn of Founder if any (`linkedin`, optional URL)
     8. Website of Business if any (`website`, optional URL)
     9. Category of Business (`business_model_category`: Product Based, Service Based, Manufacturing, Hybrid, Other)
     10. What they can contribute (`what_offer`: superpower, mentoring, vendor introductions, strategic resources)
     11. What they are looking for (`what_need`: critical bottlenecks, talent, advisory, introductions)
     12. Collaboration & Connection Preferences (`collaboration_preferences` multi-select choice cards):
         * [Dining & Talks] Curated Founders Dinners (Private dining & off-the-record growth talks)
         * [Executive Roundtable] Executive Roundtables & Salons (Problem-solving masterminds & playbooks)
         * [Sports & Movement] Sports & Movement (Badminton, Pickleball, Golf, Morning Walks & Fitness)
         * [1-to-1 Coffee] 1-to-1 Founder Coffee Meetings (Strategic deep-dive peer dialogues & mutual intros)
         * [Annual Retreat] Annual Weekend Retreats (3-day immersive offsites, wellness & strategy)
         * [Advisory Pod] Peer Advisory & Accountability Pods (Closed-pod monthly sprints & OKR reviews)
         * [Virtual Strategy] Virtual Strategy Syncs (Focused online roundtables & lightning AMAs)
     Plus core applicant identity: Full Name, Role/Designation, Work Email, City, Phone Number, WhatsApp Number, Growth Stage, Why Join, and Verification Consent.
   - Admin Application Inspector: Interactive modal in Admin Console rendering all 12 answers, clickable social/web links, category badges, and one-click 'Approve & Generate Invite' action.

5. CURATED MEETING PHOTOS SLIDER (16:9 ASPECT RATIO & SLOWER STEADY MOTION):
   - Replace former "As Seen on Instagram and Media" section with a dedicated Curated Meeting Photos Showcase:
     * Strict 16:9 Aspect Ratio: Cards and images strictly enforce `aspect-ratio: 16 / 9;` (`object-fit: cover;`) for a uniform, cinematic, distortion-free presentation.
     * Slower Steady Right-to-Left Slide: Moves continuously from right to left using `@keyframes slideRightToLeft { from { transform: translateX(0); } to { transform: translateX(-50%); } }` with a relaxed 85s linear infinite duration. Hover smoothly pauses animation.
     * Direct Photography & Contrast: Format pill tags ('Closed-Door Salon', 'Founder Dinner', '1:1 Meeting', 'Mastermind', 'Experiential', 'Founder Retreat'), titles, captions, and dates sit over subtle bottom gradient shadow scrims with dual text shadows. No obscuring frosted boxes.
     * Clean Public Presentation: NO "Add Meeting Photo" button on the public homepage. The section header is centered and executive.
     * Admin Dashboard Management: Meeting photos are added and managed strictly from the Admin Dashboard via a quick in-card upload form and admin modal, plus thumbnail deletion list.
     * SQLite Persistence: Managed in `event_gallery` table (`id`, `title`, `caption`, `image_url`, `event_date`, `tag`, `display_order`, `is_active`).

6. MONTHLY ATTENDANCE ACCOUNTABILITY TRACKER:
   - Built-in monthly attendance tracker to monitor members' presence across all curated gatherings and private sessions hosted in any month.
   - Monthly selector dropdown (e.g., October 2026, September 2026, August 2026) with automatic KPI calculations:
     * Monthly Attendance Rate %: calculated accurately against *completed* events in that calendar month.
     * Events Attended vs Hosted count.
     * Consecutive Gathering Streak tracker.
     * Dynamic Progress Bar: visual color-coded progress indicator (Emerald for >=80%, Amber for 50-79%, Coral for <50%).
   - Event Presence Table: Complete list of monthly events with date, city, venue format, status badge (PRESENT, UPCOMING, MISSED), and verified check-in timestamp.
   - Host PIN Check-In System: Modal allowing attendees to enter the 6-digit Host Event Code (e.g., 'F4F2026') upon arrival at the venue to instantly record presence and mark status as PRESENT.
   - Admin Manual Override: Admin endpoint ('POST /api/admin/events/attendance') to manually verify or update member attendance.

7. FOUNDER 1-TO-1 MEETINGS TRACKER:
   - Dedicated private tracker for founders to log, track, and measure 1-to-1 peer meetings with other community members.
   - Summary Metrics Bar: Total 1:1 Meetings Logged, This Month's Meetings, and Synergies / Deals Unlocked.
   - Interactive Meeting Logger Modal:
     * Partner Founder Name & Partner Company
     * Meeting Date & Format (In-Person Coffee, Executive Dinner, Strategy Salon, Virtual)
     * Discussion Agenda & Key Strategic Topics
     * Collaboration Outcome tag (e.g. 'Warm Client Intro Made', 'Co-Founder / Advisor Match', 'Cross-Selling Partnership', 'Vendor Due Diligence', 'Investment Lead')
     * Synergy Rating: 1 to 5 Stars
     * Confidential Notes & Takeaways
   - Dynamic 1:1 Meetings Card Feed: Clean cards displaying meeting partner, format badge, date, star rating, outcome pills, and expandable meeting notes.

8. FOUNDERS COLLECTIVE CHAT LOUNGE (ACTIVE MEMBERSHIP GATED — SINGLE UNIFIED ROOM):
   - A real-time, confidential discussion space exclusively reserved for verified active members and administrators to interact collectively in a single, unified founder lounge.
   - Strict Gating: Access is strictly gated by active membership status (`memberships.status == 'ACTIVE'`). Non-members or expired profiles receive a 403 Forbidden response and see an elegant lock gatecard ('Founders Collective Chat Requires an Active Membership') with a CTA to activate membership.
   - Single Unified Lounge: Streamlined single collective room for all members — eliminating fragmented channels to concentrate founder presence, deal flow, and peer collaborations in one high-signal stream.
   - High-Contrast Typography & Sent Message Styling:
     * User's Own Sent Messages: Rendered on the right in a luminous fresh mint bubble (`background: #A7F3D0; border: 1px solid #34D399;`) with pure black font color (`color: #000000 !important; font-weight: 500;`) for razor-sharp readability.
     * Peer Messages: Rendered on the left in soft neutral cards (`background: #F1F7F4; border: 1px solid var(--mint-200); color: #1A3026;`).
   - Clean Member Portal: Founder Video Spotlight is removed from the member portal to maintain maximum focus on high-signal peer networking.

9. OFFICIAL SOCIAL PROFILES FOOTER INTEGRATION:
   - Clean shortcut buttons for official profiles placed strictly in the website footer (removed from header and hero banner to preserve a focused, executive hero aesthetic).
   - Official Profiles:
     * Instagram: https://www.instagram.com/founder_for_founder
     * Facebook: https://www.facebook.com/share/19ZnPNuhPb/
     * LinkedIn: https://www.linkedin.com/company/founder-for-founder/
   - Visual Styling:
     * Format: Square buttons with slight curves (44x44px, border-radius: 8px).
     * Color Theme Harmony: Styled to seamlessly match the website's dark emerald & mint palette — deep emerald background (rgba(6, 78, 59, 0.75)), 1px emerald border outline (var(--emerald-600)), and luminous mint SVG icons (var(--mint-200)).
     * Hover States: Lifts smoothly (translateY(-3px)), shifts into radiant interactive emerald gradient (linear-gradient(135deg, #047857 0%, #059669 100%)), border glows luminous mint (#34D399), and icon illuminates in crisp white.
     * Minimalist Logo-Only Architecture: Features strictly the official SVG logos of the respective platforms without text strings or clutter.

10. ULTRA-DYNAMIC & ANIMATED FRONTEND UI:
    - Fluid micro-interactions and smooth hardware-accelerated animations across the entire application:
      * CSS Keyframes: '@keyframes slideRightToLeft' for continuous steady meeting photo sliding; '@keyframes emeraldPulse' for live indicators; '@keyframes tabSlideIn' for seamless tab switching; '@keyframes floatSmooth' for hero floating cards.
      * Micro-Elevations: Cards and interactive modules elevate smoothly on hover ('transform: translateY(-4px); box-shadow: 0 12px 28px rgba(6,78,59,0.15)').
      * Button State Feedback: Subtle press bounce ('active: scale(0.98)'), smooth gradient transition, and luminous borders.
      * Dynamic Progress Visuals: Animated fill-up bars for attendance metrics and meeting synergy scores.
      * Zero page reload delays: Instant DOM updates and seamless modal dialogs with backdrop blur.

11. BACKEND & PERSISTENCE:
    - Pure Python 3 `http.server` implementation serving static assets and dynamic REST JSON endpoints (`/api/...`).
    - SQLite database (`f4f_community.db`) with 13 relational tables and automated default schema migration.
    - Default Seed Accounts: Admin (`admin@founderforfounder.com` / `FounderAdmin2026!`) and Sample Member (`arjun@zenithfintech.com` / `FounderPass2026!`).
```

---

## 3. BRAND IDENTITY, COPY DECK & POSITIONING

### Core Brand Principles
* **Entity**: Founder for Founder (f4f)
* **Parentage**: Powered by **snalts.co** — an ecosystem builder driving peer-to-peer founder leverage.
* **Core Philosophy**: Not an open networking forum, generic coworking directory, or noisy WhatsApp group. It operates on mutual peer accountability, zero sales pitch tolerance, radical transparency, and tangible deal flow.
* **Verified Public Proof Metrics**:
  * `1,528+ Verified Founders & Operators`
  * `27 Curated Gatherings & Private Experiences`
  * `4.9/5 Peer Trust Rating`
  * *(MANDATE: Never show "verified business generated" on the public landing strip).*

### Exact Headings & Eyebrows
| Section | Eyebrow | Section Heading |
|---|---|---|
| **Marquee** | *None* | `Businesses Connected With Us` |
| **Core Philosophy** | `FOUNDATION • UNCOMPROMISING PRINCIPLES` | `Built on Real Founder Empathy, Not Vanity Networking` |
| **Ways We Collaborate** | `CURATED ENGAGEMENT • HIGH SIGNAL` | `Five High-Impact Formats for Mutual Founder Leverage` |
| **How It Works** | `VETTED ADMISSION • SELECTIVE ONBOARDING` | `How to Join the Founder for Founder Ecosystem` |
| **Platform Features** | `MEMBER PORTAL • PRIVATE ARCHITECTURE` | `The Private Infrastructure Powering Founder Collaboration` |
| **Curated Meeting Photos** | `FOUNDER INTERACTIONS • MOMENTS OF LEVERAGE` | `Curated Founder Gatherings & Meeting Moments` |
| **Attendance Tracker** | `MEMBER ACCOUNTABILITY • MONTHLY PRESENCE` | `Monthly Gathering Attendance & Consistency Tracker` |
| **1:1 Meetings Tracker** | `PEER CONNECTIONS • SYNERGY ACCELERATOR` | `Private Founder 1-to-1 Meetings & Synergy Tracker` |
| **Founders Chat Lounge** | `COMMUNITY STREAM • HIGH SIGNAL` | `Founders Collective Lounge` |

---

## 4. STRICT DESIGN SYSTEM, CSS & ANIMATION TOKENS

### Color Tokens
```css
:root {
  --emerald-950: #042F2C; /* Foundation dark */
  --emerald-900: #064E3B; /* Deep brand emerald */
  --emerald-800: #065F46; /* Container headers */
  --emerald-700: #047857; /* Primary buttons & active accents */
  --emerald-600: #059669; /* Interactive hover */
  --emerald-500: #10B981; /* Luminous green indicators */
  --emerald-400: #34D399; /* Card hover borders & active glows */
  --emerald-200: #A7F3D0; /* Card pill headers & sent chat bubble */
  --emerald-100: #C9EFDD; /* Hairline borders */
  --emerald-50:  #E4F7EE; /* Warm mint backgrounds */
  
  --mint-500: #10B981;
  --mint-400: #34D399;
  --mint-300: #6EE7B7;
  --mint-200: #A7F3D0;
  --mint-100: #D1FAE5;
  --mint-50:  #F0FDF4;

  --ink-primary:   #0B0F0D;
  --ink-secondary: #2C3531;
  --ink-muted:     #556960;
  --white:         #FFFFFF;
  --border-hairline: #E1ECE6;
}
```

### Critical CSS Mandates
1. **NO ITALIC / SLANTED TEXT**:
   ```css
   * {
     font-style: normal !important;
   }
   ```
2. **6px BUTTON CORNERS**:
   ```css
   .btn, button, input[type="submit"] {
     border-radius: 6px !important;
     font-weight: 600;
   }
   ```
3. **NO BOXES OVER CARD PHOTOS**:
   In `Ways We Collaborate`, `Core Philosophy`, `Curated Experiences`, and `Meeting Photos`, image cards must display content directly over photography:
   ```css
   .collab-card-overlay, .photo-overlay {
     position: absolute;
     inset: 0;
     background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(6,78,59,0.3) 40%, rgba(0,0,0,0.92) 100%);
     display: flex;
     flex-direction: column;
     justify-content: flex-end;
     padding: 1.75rem;
   }
   .collab-card-title, .photo-card-title {
     color: #FFFFFF;
     text-shadow: 0 2px 4px rgba(0,0,0,0.85), 0 4px 12px rgba(0,0,0,0.6);
   }
   .format-badge, .collab-badge {
     display: inline-block;
     background: rgba(6, 78, 59, 0.85);
     color: #A7F3D0 !important;
     border: 1px solid #10B981;
     box-shadow: 0 0 10px rgba(16, 185, 129, 0.35);
     font-size: 0.75rem;
     font-weight: 700;
     padding: 0.3rem 0.75rem;
     border-radius: 4px;
     letter-spacing: 0.05em;
   }
   ```
4. **SMOOTH KEYFRAME ANIMATIONS**:
   ```css
   @keyframes slideRightToLeft {
     from { transform: translateX(0); }
     to { transform: translateX(-50%); }
   }
   @keyframes emeraldPulse {
     0%, 100% { opacity: 1; transform: scale(1); }
     50% { opacity: 0.4; transform: scale(0.92); }
   }
   @keyframes floatSmooth {
     0%, 100% { transform: translateY(0); }
     50% { transform: translateY(-8px); }
   }
   @keyframes tabSlideIn {
     from { opacity: 0; transform: translateY(12px); }
     to { opacity: 1; transform: translateY(0); }
   }
   ```

---

## 5. CURATED 16:9 MEETING PHOTOS SLOWER STEADY SLIDER

### Specifications
* **Section ID**: `#meetingPhotosSection`
* **Aspect Ratio**: Strictly enforced 16:9 (`aspect-ratio: 16 / 9;`, `object-fit: cover;`). Width is 440px on desktop, 320px on mobile.
* **Continuous Motion**: Powered by `@keyframes slideRightToLeft` with a relaxed **85s linear infinite** duration (`animation: slideRightToLeft 85s linear infinite;`).
* **Hover Interaction**: Pauses smoothly on mouse hover (`:hover { animation-play-state: paused; }`).
* **Edge Masking**: The slider wrapper features aesthetic edge gradient masks (`mask-image: linear-gradient(to right, transparent, black 4%, black 96%, transparent)`).
* **Public Page Cleanliness**: The public landing page header is centered with **zero action buttons** (`Add Meeting Photo` button removed).
* **Admin Dashboard Management**: Photos are uploaded and managed via:
  1. Quick In-Card Direct Form in `#tab-admin`.
  2. "+ Add New Meeting Photo (Modal)" in Admin Dashboard.
  3. Interactive photo deletion list with instant removal.

---

## 6. 12-QUESTION COMPREHENSIVE ADMISSIONS QUESTIONNAIRE

When a founder clicks **"Apply for Membership"** or **"Show Interest"**, launch a multi-step modal capturing all 12 key founder and enterprise data points:

1. **Name of Business**: `business_name` (Text input, required)
2. **Brief about Business**: `business_description` (Textarea: products, target clients, scale, required)
3. **Business being carried out from how many years**: `years_in_business` (Select: `Less than 1 Year`, `1-2 Years`, `3-5 Years`, `5-10 Years`, `10+ Years`)
4. **Team Size**: `team_size` (Select: `Solo Founder [1]`, `2-10 Members`, `11-50 Members`, `51-200 Members`, `200+ Members`)
5. **Type of Firm**: `firm_type` (Select: `Private Limited [Pvt Ltd]`, `LLP`, `Partnership Firm`, `Sole Proprietorship`, `Public Limited`, `OPC`, `Other`)
6. **Business Instagram Link**: `instagram` (URL, optional)
7. **LinkedIn of Founder**: `linkedin` (URL, optional)
8. **Website of Business**: `website` (URL, optional)
9. **Category of Business**: `business_model_category` (Select: `Product Based`, `Service Based`, `Manufacturing`, `Hybrid`, `Other`)
10. **What they can contribute**: `what_offer` (Textarea: superpower, mentoring, vendor introductions, strategic resources)
11. **What they are looking for**: `what_need` (Textarea: bottlenecks, talent, advisory, intros)
12. **How would they like to collaborate / connect**: `collaboration_preferences` (Multi-Select Checkbox Choice Cards):
    * `[Dining & Talks] Curated Founders Dinners` (Private dining & off-the-record growth talks)
    * `[Executive Roundtable] Executive Roundtables & Salons` (Problem-solving masterminds & playbooks)
    * `[Sports & Movement] Sports & Movement` (Badminton, Pickleball, Golf, Morning Walks & Fitness)
    * `[1-to-1 Coffee] 1-to-1 Founder Coffee Meetings` (Strategic deep-dive peer dialogues & mutual intros)
    * `[Annual Retreat] Annual Weekend Retreats` (3-day immersive offsites, wellness & strategy)
    * `[Advisory Pod] Peer Advisory & Accountability Pods` (Closed-pod monthly sprints & OKR reviews)
    * `[Virtual Strategy] Virtual Strategy Syncs` (Focused online roundtables & lightning AMAs)

### Plus Core Applicant Identity:
* `full_name` (Full Name)
* `role` (Designation / Title)
* `email` (Work Email)
* `phone` (Mobile Number)
* `whatsapp` (WhatsApp Number)
* `city` (City of Operations)
* `stage` (Bootstrap / Seed / Series A / Profitable)
* `reason_to_join` (Why Founder for Founder?)

---

## 7. MONTHLY ATTENDANCE ACCOUNTABILITY TRACKER

### Core Engine & Formulas
* **Monthly Selector Dropdown**: Filters all gatherings by chosen month (e.g. October 2026, September 2026).
* **Attendance % Formula**:
  $$\text{Attendance Rate \%} = \frac{\text{Events Attended by Member in Month}}{\text{Completed Events in Calendar Month}} \times 100$$
  *(Note: Upcoming events in the current month do not penalize the founder's score).*
* **Streak Tracker**: Calculates consecutive gatherings attended without missing.
* **Progress Bar**: Color-coded dynamically:
  * `>= 80%`: Radiant Emerald (`#10B981`)
  * `50% - 79%`: Warm Amber (`#F59E0B`)
  * `< 50%`: Soft Coral (`#EF4444`)
* **Event Presence Table**: Columns: Date, Event Name, Format Tag, City, Status Pill (`PRESENT`, `UPCOMING`, `MISSED`), and Verified Timestamp.
* **Host PIN Check-In System**: Modal prompt allowing attendees to enter the 6-digit Host Event Code (`F4F2026`) upon arrival at the venue to instantly record presence and mark status as `PRESENT`.

---

## 8. FOUNDER 1-TO-1 MEETINGS TRACKER

### Feature Architecture
* **Summary Metrics Strip**:
  * Total 1:1 Meetings Logged
  * This Month's Meetings Count
  * Synergies & Deals Unlocked
* **Interactive Meeting Logger Modal**:
  * Partner Founder Name & Partner Startup Name
  * Meeting Date & Format (`In-Person Coffee`, `Executive Dinner`, `Strategy Salon`, `Virtual Sync`)
  * Strategic Discussion Agenda
  * Collaboration Outcome Tag (`Warm Client Intro Made`, `Co-Founder / Advisor Match`, `Cross-Selling Partnership`, `Vendor Due Diligence`, `Investment Lead`, `Brainstorming & Empathy`)
  * Synergy Rating: 1 to 5 Stars (1-5 Gold SVG Stars)
  * Confidential Notes & Action Items
* **Dynamic Feed**: Rendered as crisp interactive cards with star rating displays, outcome badges, and expandable notes.

---

## 9. FOUNDERS COLLECTIVE CHAT LOUNGE

### Access Control & Gating
* **Strict Active Membership Gating**:
  * Backend checks `memberships.status == 'ACTIVE'` or `users.role == 'ADMIN'`.
  * If unauthenticated or expired, backend returns `403 Forbidden` with `{ has_membership: false }`.
  * Frontend renders a frosted lock gatecard: **"Founders Collective Chat Requires an Active Membership"** with an immediate button to activate membership.
* **Single Unified Collective Room**:
  * Zero side-channel distractions. All verified founders communicate in one collective lounge stream to concentrate high-value interactions.
* **High-Contrast Message Typography**:
  * **User's Sent Messages (`.chat-msg-row.mine .chat-bubble`)**:
    * Background: `#A7F3D0` (Luminous fresh mint).
    * Border: `1px solid #34D399`.
    * Font Color: `#000000 !important;` (Pure black text, 500 font-weight).
    * Guaranteed WCAG AAA contrast ratio.
  * **Peer Messages (`.chat-msg-row:not(.mine) .chat-bubble`)**:
    * Background: `#F1F7F4` (Clean neutral).
    * Border: `1px solid var(--mint-200)`.
    * Font Color: `#1A3026`.
* **Portal Cleanliness**: Founder Video Spotlight has been permanently removed from the member portal.

---

## 10. DYNAMIC CONTENT MANAGEMENT SYSTEM (CMS) & MEDIA ENGINE

### CMS Architecture
* **`system_settings` Table**: Stores key-value pairs for all public imagery and text copy:
  * `brand_logo_url`: Official brand logo SVG/PNG.
  * `hero_banner_url`: Hero background photography.
  * `img_capsule_1`, `img_capsule_2`, `img_capsule_3`: Hero capsule collage photos.
  * `img_phil_1`, `img_phil_2`, `img_phil_3`, `img_phil_4`: 4 Philosophy cards.
  * `img_collab_1`, `img_collab_2`, `img_collab_3`, `img_collab_4`, `img_collab_5`: 5 Collaboration cards.
  * `img_feat_1` to `img_feat_6`: 6 Platform Feature Showcase tab images.
* **`event_gallery` Table**: Stores dynamic 16:9 meeting photos slider items with `title`, `caption`, `image_url`, `event_date`, `tag`, and `display_order`.
* **Media Uploader**: Supports drag-and-drop or file selector, storing files safely into `/assets/uploads/` with unique hex hashes, alongside direct external URL input.
* **Hydration**: When the client loads `index.html`, `loadPublicContent()` fetches `GET /api/public/content` and injects saved assets dynamically into the DOM.

---

## 11. COMPLETE SQLITE DATABASE SCHEMA (ALL 13 TABLES DDL)

Execute the following SQLite DDL to create the complete data layer:

```sql
-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT DEFAULT 'MEMBER' CHECK(role IN ('MEMBER', 'ADMIN', 'APPLICANT')),
  is_verified INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. FOUNDER PROFILES
CREATE TABLE IF NOT EXISTS founder_profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  phone TEXT,
  whatsapp TEXT,
  city TEXT,
  company_name TEXT,
  company_stage TEXT,
  industry TEXT,
  founder_role TEXT,
  bio TEXT,
  profile_photo TEXT,
  linkedin_url TEXT,
  twitter_url TEXT,
  website_url TEXT,
  superpower TEXT,
  critical_ask TEXT,
  is_spotlight INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. MEMBERSHIPS
CREATE TABLE IF NOT EXISTS memberships (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER UNIQUE NOT NULL,
  tier TEXT DEFAULT 'FOUNDER_CORE' CHECK(tier IN ('FOUNDER_CORE', 'FOUNDER_ELITE', 'LIFETIME')),
  status TEXT DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'PAUSED', 'EXPIRED', 'PENDING')),
  valid_from DATE NOT NULL,
  valid_until DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. EVENTS & GATHERINGS
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  event_type TEXT CHECK(event_type IN ('DINNER', 'ROUNDTABLE', 'RETREAT', 'SALON', 'WORKSHOP', 'SPORTS')),
  description TEXT,
  city TEXT NOT NULL,
  venue_name TEXT,
  venue_address TEXT,
  google_maps_url TEXT,
  event_date DATE NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  total_seats INTEGER NOT NULL,
  available_seats INTEGER NOT NULL,
  price_amount REAL DEFAULT 0.0,
  what_is_included TEXT,
  host_code TEXT DEFAULT 'F4F2026',
  poster_url TEXT,
  is_private INTEGER DEFAULT 1,
  status TEXT DEFAULT 'UPCOMING' CHECK(status IN ('UPCOMING', 'COMPLETED', 'CANCELLED')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. EVENT REGISTRATIONS
CREATE TABLE IF NOT EXISTS event_registrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  status TEXT DEFAULT 'CONFIRMED' CHECK(status IN ('CONFIRMED', 'WAITLISTED', 'CANCELLED')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(event_id, user_id),
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. EVENT ATTENDANCE
CREATE TABLE IF NOT EXISTS event_attendance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  verified_by TEXT DEFAULT 'HOST_PIN',
  attendance_status TEXT DEFAULT 'PRESENT' CHECK(attendance_status IN ('PRESENT', 'ABSENT', 'EXCUSED')),
  UNIQUE(event_id, user_id),
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 7. FOUNDER 1-TO-1 MEETINGS
CREATE TABLE IF NOT EXISTS founder_one_to_one_meetings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  partner_founder_name TEXT NOT NULL,
  partner_company TEXT NOT NULL,
  meeting_date DATE NOT NULL,
  meeting_format TEXT DEFAULT 'IN_PERSON_COFFEE',
  discussion_agenda TEXT NOT NULL,
  collaboration_outcome TEXT,
  synergy_rating INTEGER DEFAULT 5,
  confidential_notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 8. NEEDS & WANTS MATCHING ENGINE
CREATE TABLE IF NOT EXISTS needs_wants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  entry_type TEXT CHECK(entry_type IN ('NEED', 'WANT')),
  category TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT DEFAULT 'OPEN' CHECK(status IN ('OPEN', 'MATCHED', 'CLOSED')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 9. REFERRALS
CREATE TABLE IF NOT EXISTS referrals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  referrer_user_id INTEGER NOT NULL,
  nominee_name TEXT NOT NULL,
  nominee_email TEXT NOT NULL,
  nominee_company TEXT NOT NULL,
  nominee_linkedin TEXT,
  nominee_phone TEXT,
  notes TEXT,
  status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'APPROVED', 'INVITED', 'REJECTED')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (referrer_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 10. SYSTEM SETTINGS (DYNAMIC CMS)
CREATE TABLE IF NOT EXISTS system_settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. FOUNDER APPLICATIONS (12-POINT QUESTIONNAIRE)
CREATE TABLE IF NOT EXISTS founder_applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  business_name TEXT NOT NULL,
  role TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  whatsapp TEXT,
  city TEXT,
  stage TEXT,
  business_description TEXT,
  years_in_business TEXT,
  team_size TEXT,
  firm_type TEXT,
  instagram TEXT,
  linkedin TEXT,
  website TEXT,
  business_model_category TEXT,
  what_offer TEXT,
  what_need TEXT,
  collaboration_preferences TEXT,
  reason_to_join TEXT,
  status TEXT DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'APPROVED', 'REJECTED', 'INVITED')),
  reviewed_by TEXT,
  reviewed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. CURATED MEETING PHOTOS GALLERY (16:9 SLIDER)
CREATE TABLE IF NOT EXISTS event_gallery (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  caption TEXT,
  image_url TEXT NOT NULL,
  event_date DATE,
  tag TEXT DEFAULT 'Closed-Door Salon',
  display_order INTEGER DEFAULT 0,
  is_active INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. FOUNDERS COLLECTIVE CHAT MESSAGES
CREATE TABLE IF NOT EXISTS community_chat_messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel TEXT NOT NULL DEFAULT 'lounge',
  user_id INTEGER NOT NULL,
  message TEXT NOT NULL,
  reply_to_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (reply_to_id) REFERENCES community_chat_messages(id) ON DELETE SET NULL
);

-- PERFORMANCE INDEXES
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date);
CREATE INDEX IF NOT EXISTS idx_attendance_user_event ON event_attendance(user_id, event_id);
CREATE INDEX IF NOT EXISTS idx_meetings_user ON founder_one_to_one_meetings(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_channel_created ON community_chat_messages(channel, created_at);
CREATE INDEX IF NOT EXISTS idx_gallery_order ON event_gallery(display_order);
```

---

## 12. COMPLETE REST API ENDPOINTS SPECIFICATION

All dynamic interactions occur over clean JSON endpoints:

### Public & Authentication Endpoints
* `GET /api/public/content` — Returns all dynamic CMS keys (`system_settings`), upcoming events, verified counters, and brand configurations.
* `POST /api/public/show-interest` — Ingests the 12-question admissions form into `founder_applications`.
* `GET /api/auth/config` — Returns Google OAuth configuration (`google_client_id`, `google_auth_enabled`).
* `POST /api/auth/google` — Authenticates user via Google OAuth 2.0 credential (JWT ID Token) verified against Google's tokeninfo API. Automatically provisions member account, verified profile, active 1-year membership, and returns active session token. Also supports developer/demo testing mode.
* `POST /api/auth/login` — Authenticates user via email + password, issues session cookie or token.
* `GET /api/auth/me` — Validates session token, returns current user details, profile, and membership status.
* `POST /api/public/auth/register` — Self-registration endpoint.
* `GET /api/meeting-photos` — Returns active 16:9 meeting photos from `event_gallery` sorted by `display_order ASC`.

### Curated Meeting Photos Endpoints
* `POST /api/meeting-photos/add` — Adds a new 16:9 meeting photo with title, caption, date, tag, and image URL.
* `POST /api/meeting-photos/delete` — Accepts `{ id }` to delete a meeting photo from the gallery.

### Founders Collective Chat Endpoints (Active Membership Gated)
* `GET /api/chat/messages?channel=lounge` — Returns last 100 messages joined with user avatar, name, and business badge. Returns `403 Forbidden` if user is not an active member or admin.
* `POST /api/chat/messages` — Stores sent message. Validates active membership.

### Monthly Attendance Tracker Endpoints
* `GET /api/attendance/summary?month=YYYY-MM` — Returns attendance percentage, attended count, completed events count, consecutive streak, and list of monthly gatherings with status (`PRESENT`, `UPCOMING`, `MISSED`).
* `POST /api/events/checkin` — Accepts `{ event_id, pin }`. Verifies Host PIN (`F4F2026`) and marks attendee as `PRESENT`.

### Founder 1:1 Meetings Endpoints
* `GET /api/founder-meetings` — Returns list of logged 1:1 meetings for current founder along with summary KPIs (total, monthly, synergies unlocked).
* `POST /api/founder-meetings` — Logs a new 1:1 meeting with partner name, company, date, format, agenda, outcome, star rating, and notes.

### Admin Endpoints
* `GET /api/admin/applications` — Returns list of all admissions applications.
* `POST /api/admin/applications/review` — Approves/rejects application, optionally generates user invite.
* `POST /api/admin/content/update` — Updates CMS keys in `system_settings`.
* `POST /api/admin/media/upload` — Handles multipart file upload to `/assets/uploads/`.
* `POST /api/admin/events/attendance` — Admin manual override for attendance.

---

## 13. FRONTEND PAGE & COMPONENT ARCHITECTURE

### File Structure
```
├── vercel.json                      # Vercel serverless routing, installCommand & buildCommand overrides
├── pyproject.toml                   # uv & Vercel Python zero-dependency manifest
├── server.py                        # Python 3 standard library backend HTTP server
├── database.py                      # SQLite database layer with /tmp serverless support
├── schema.sql                       # Complete SQL schema & DDL
├── f4f_community.db                 # SQLite database file
├── api/
│   └── index.py                     # Vercel serverless function entrypoint (handler class)
├── docs/
│   ├── generate_master_docx.py      # Script to generate Word doc master prompt
│   ├── Founder_for_Founder_Master_Prompt.docx # Formatted Word specification document
│   ├── MASTER_PROMPT.md             # Comprehensive master prompt file
│   └── MASTER_PROMPT.txt            # Raw text version of master prompt
├── public/
│   ├── index.html                   # Complete SPA HTML markup with Google Auth
│   ├── css/
│   │   └── styles.css               # Design system, animations, high-contrast typography
│   ├── js/
│   │   └── app.js                   # Application state, API clients, Google GSI auth
│   └── assets/
│       ├── logo.svg                 # Founder for Founder vector logo
│       ├── hero_banner.jpg          # High-contrast hero photo
│       └── uploads/                 # Local directory for user & admin uploaded media
```

### SPA Tab Views
* `#tab-home` — Public landing page (Hero, Capsule Collage, Counters Strip, Marquee, Philosophy, Collaboration Pillars, How It Works, Features, Upcoming Events, 16:9 Photos Slider, FAQ, Social Footer).
* `#tab-portal` — Member Portal (Member Directory, Needs & Wants Engine, Referral Hub, Gatherings RSVP, Attendance Tracker, 1:1 Meetings Tracker, Collective Chat Lounge).
* `#tab-admin` — Admin Console (Applications Review, CMS Content Editor, Media Manager, Meeting Photos Gallery Manager).

---

## 14. OFFICIAL SOCIAL MEDIA PROFILES ARCHITECTURE (FOOTER ONLY)

### URLs & Direct Links
* **LinkedIn**: `https://www.linkedin.com/company/founder-for-founder/`
* **Instagram**: `https://www.instagram.com/founder_for_founder`
* **Facebook**: `https://www.facebook.com/share/19ZnPNuhPb/`

### Visual Guidelines
* **Placement**: Strictly in the website footer (`.footer-social-links`). Removed from header and hero banner.
* **Dimensions**: Square 44x44px buttons with slight curves (`border-radius: 8px !important;`).
* **Theme Styling**: Deep emerald glass background (`rgba(6, 78, 59, 0.75)`), 1px emerald border (`#059669`), and luminous mint icons (`#A7F3D0`).
* **Hover Interaction**: Lifts by -3px, transitions to interactive gradient (`linear-gradient(135deg, #047857, #059669)`), with `#34D399` border glow and white SVG icons.
* **Minimalist Architecture**: Displays strictly the official platform SVG logos with zero accompanying text labels.

---

## 15. VERIFICATION & QUALITY ASSURANCE CHECKLIST

When the build is complete, verify each of the following points:

- [x] **No Italic/Slanted Fonts**: Entire CSS enforces `font-style: normal !important;`.
- [x] **Button Geometry**: All buttons enforce `border-radius: 6px !important;`.
- [x] **No Obscuring Boxes**: Collaboration, Philosophy, and Meeting Photo cards render text directly over photography with gradient scrims and dual text shadows.
- [x] **Marquee Heading**: "Businesses Connected With Us" appears directly above the brand marquee.
- [x] **Counters**: "1,528+ Verified Founders", "27 Curated Gatherings", "4.9/5 Peer Trust". No "verified business generated" metric.
- [x] **Social Icons**: Placed exclusively in the footer as 44x44px curved square buttons in emerald theme.
- [x] **Curated Meeting Photos**: Strictly 16:9 ratio, steady right-to-left slide at 85s duration, pause on hover. No "Add Meeting Photo" button on the home page. Added and managed from Admin Dashboard.
- [x] **Admissions Funnel**: Captures all 12 questions with multi-select collaboration options.
- [x] **Attendance Tracker**: Accurately computes attendance % against completed events, logs consecutive streaks, and enables Host PIN check-in (`F4F2026`).
- [x] **1:1 Meetings Tracker**: Allows logging partner founder, company, format, agenda, outcome, star rating, and confidential notes.
- [x] **Founders Collective Chat Lounge**: Single unified room with active membership gating (403 gatecard for non-members). Sent messages render in luminous mint bubble with pure black text (`#000000 !important`). Founder Video Spotlight removed.
- [x] **Dynamic Media CMS**: All imagery and text persist in SQLite `system_settings` and `event_gallery`.
- [x] **Backend & API**: Python server handles all routes with 200 OK and valid JSON.
- [x] **Google Authentication**: Native Google Identity Services client button on login modal, backend token verification via Google tokeninfo, auto-provisioning of member accounts, active memberships, and developer test mode.
- [x] **Vercel Serverless Ready**: Configured `vercel.json` rewrites, `requirements.txt`, `api/index.py` serverless function, and `/tmp` auto-seeding SQLite path handler.
- [x] **Optional Event Registration Fees & Payment Gateway**: Admins can optionally add entry fees (₹) and ticket inclusions. Free events confirm directly; paid events launch `#eventPaymentModal` with 18% GST calculation, UPI/Cards/NetBanking/1-Click pay, generating transaction IDs (`PAY_EVT_...`) and verified invoice receipts (`INV-EVT-...`).
- [x] **Google Maps Venue Location Provision**: Admin event creation includes dedicated Google Maps Location URL field with "Auto-Generate Link" helper and live test preview. Public event showcase, member portal gathering cards, and payment gateway modal render clickable Google Maps links opening directly in navigation apps.

---

## 16. VERCEL SERVERLESS DEPLOYMENT SPECIFICATION

The platform is engineered to deploy directly to Vercel with zero external build frameworks:

### Architecture
1. **Static Frontend Routing**: Vercel serves all static assets directly from `public/` at the root path (`/`, `/css/*`, `/js/*`, `/assets/*`).
2. **Serverless Python API**: Vercel routes `/api/(.*)` to `api/index.py`, executing the serverless `handler` class inheriting from `server.F4FHTTPRequestHandler`.
3. **Dynamic Proxy Path Resolution**: The backend inspects `x-forwarded-uri` and `x-matched-path` headers to accurately map rewritten serverless paths.
4. **Serverless SQLite `/tmp` Auto-Seed Engine**:
   - Because Vercel serverless execution environments enforce a read-only filesystem on `/var/task`, the database manager (`database.py`) automatically copies the initial seed database to `/tmp/f4f_community.db` on first boot.
   - All subsequent transactions (logins, submissions, chat messages, attendance logs) execute with full read-write privileges without read-only filesystem exceptions.

### Deployment Steps
1. Push this repository to a GitHub account.
2. Log in to [Vercel](https://vercel.com/) and click **New Project**.
3. Import the GitHub repository.
4. Leave all build settings at default (`vercel.json` handles all routing automatically).
5. (Optional) Add `GOOGLE_CLIENT_ID` in the Vercel Project Environment Variables.
6. Click **Deploy**. The platform goes live with an instant global SSL URL (e.g., `https://founder-for-founder.vercel.app`).

---

## 17. OPTIONAL EVENT REGISTRATION FEES & PAYMENT GATEWAY ARCHITECTURE

To support exclusive, premium, or venue-intensive gatherings (e.g., private dining salons, annual retreats, factory offsites), gatherings can optionally require an entry registration fee while keeping community gatherings free by default.

### Admin Provision & Experience Controls
* **Optional Toggle**: In Admin CMS Event Creation form (`#adminCreateEventForm`), admins select between:
  * **Free for Members (₹0)**: Standard community gathering included in monthly membership.
  * **Paid Gathering**: Reveals the Entry Fee (`evt_price_amount`, in ₹ INR) and Ticket Inclusions input (`evt_what_is_included`).
* **Database Representation**:
  * `events.price_amount` (REAL, default 0.0): Numeric entry ticket price.
  * `events.what_is_included` (TEXT): Breakdown of what the member receives (e.g., *4-course dinner, private salon access, keynote deck*).

### Public & Member Portal Event Badging
* **Public Showcase (`#upcomingEventsGrid`)**:
  * Paid Gathering: Displays gold pill badge: `₹1,499 ENTRY FEE`.
  * Free Gathering: Displays emerald pill badge: `FREE FOR MEMBERS`.
* **Member Portal Gatherings Tab (`#eventsContainer`)**:
  * Unregistered Paid Event: Renders `PAY & REGISTER (₹X)` action button.
  * Unregistered Free Event: Renders `RSVP FOR EVENT (FREE)` action button.
  * Registered & Paid Event: Renders `SEAT CONFIRMED (PAID)` checkmark button.
  * Registered Free Event: Renders `RSVP CONFIRMED` checkmark button.

### Event Payment Gateway Modal (`#eventPaymentModal`)
* **Itemized Order Summary**:
  * Base Registration Fee (₹ Subtotal)
  * GST Calculation (18% Statutory Rate)
  * Total Payable (₹ Total)
* **What is Included Banner**: Highlighted card reinforcing exact ticket inclusions and venue privileges.
* **Payment Gateway Options**:
  1. **UPI / QR Code**: Instant payments via Google Pay, PhonePe, Paytm, BHIM.
  2. **Credit & Debit Cards**: Major cards supported (Visa, Mastercard, RuPay).
  3. **NetBanking**: Direct bank debits across all major Indian scheduled banks.
  4. **1-Click Pay**: Instant Razorpay Sandbox simulator for instant demo confirmations.
* **Post-Payment Confirmation Card**:
  * Automatically transitions to confirmed seat state.
  * Displays unique Tax Invoice Number (`INV-EVT-2026-XXXX`).
  * Displays Gateway Transaction Reference (`PAY_EVT_XXXX`).
  * Instant status update in `event_rsvps` (`payment_status='PAID'`, `status='ATTENDING'`).

---

## 18. GOOGLE MAPS VENUE LOCATION ARCHITECTURE & PROVISION

To ensure frictionless attendance and precise navigation to curated founder gatherings across cities, each event includes comprehensive Google Maps location integration:

### Admin Event Creation Provision
* **Dedicated Input**: In the Admin CMS Event Creation form (`#adminCreateEventForm`), the venue row features:
  * **Venue / Address** (`#evt_venue`): Specific physical place or address (e.g. *The Quorum Club, Two Horizon Center, Golf Course Road*).
  * **City** (`#evt_city`): City location (e.g. *Gurugram*, *Bengaluru*, *Mumbai*, *Delhi NCR*).
  * **Google Maps Location URL** (`#evt_google_maps_url`): Optional link input accepting any Google Maps share link (`maps.app.goo.gl`), pin coordinate link, or place URL.
  * **Auto-Generate Map Link Helper**: A dedicated helper button (`#evt_btn_auto_map`) that automatically constructs an accurate Google Maps search URL from the entered venue and city:
    `https://www.google.com/maps/search/?api=1&query={venue}+{city}`
  * **Live "Test Map" Preview**: A dynamic test button (`#evt_map_preview_btn`) enabling admins to immediately preview and verify the pin in a new tab before publishing.
* **Backend Automatic Fallback Generator**:
  * If an admin enters a venue name and city but leaves `google_maps_url` blank, `server.py` automatically generates and stores the query-based Google Maps search link.

### Visual Display & Member Navigation
* **Public Landing Page Showcase (`#upcomingEventsGrid`)**:
  * Directly adjacent to the venue name, renders a styled "Google Maps" external link button with an SVG location pin and external link icon, opening the exact map coordinates in a new tab (`target="_blank" rel="noopener noreferrer"`).
* **Member Portal Gatherings Tab (`#eventsContainer`)**:
  * Each gathering card prominently features an interactive Google Maps location button next to the venue line, allowing members to navigate directly using Google Maps on desktop or mobile.
* **Event Payment Gateway Modal (`#eventPaymentModal`)**:
  * The order summary and venue details line includes an inline "View Map &rarr;" link so members can double-check the gathering venue before completing paid or free registrations.

