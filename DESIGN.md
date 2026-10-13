# DESIGN SYSTEM & STITCH INTEGRATION SPECIFICATION
## Founder for Founder — Modern Curated Network & Platform Experience

**Version:** 1.0.0  
**Status:** Stage 1 — Audit & Design System Architecture  
**Author:** Full-Stack Architecture & Performance Engineering Team  
**Last Updated:** October 2026  

---

## 1. System & Architecture Overview

Founder for Founder is a curated business network connecting founders, entrepreneurs, business owners, and professionals across India. The platform is designed around the core philosophy: *"Business brings us together. Experiences bring us closer."*

### 1.1 Technical Stack & Runtime Environment
- **Framework:** Next.js 14.2.15 (React 18.3.1, TypeScript 5.6.3, App Router).
- **Runtime:** Node.js (v20 / v22 with `--experimental-sqlite` native module support).
- **Core Architecture:** Dual-engine application:
  1. **Next.js App Router Server:** Manages SSR root layout (`src/app/layout.tsx`), 7 standalone legal routes, and 44 REST API endpoints (`src/app/api/`).
  2. **High-Performance Client Application Shell:** Hosted in `src/app/page.tsx` and hydrated via `public/js/app.js`, delivering instant tab switching, live filtering, and zero-latency client interactions.
- **Styling Architecture:**
  - **Base Design System:** `public/css/styles.css` / `src/app/globals.css` (2,807 lines of modular, zero-runtime CSS with custom property tokens).
  - **Google Stitch Utility Layer:** Tailwind CSS CDN loaded with `corePlugins: { preflight: false }` inside `src/app/layout.tsx` to enable Stitch design tokens without breaking existing landing page rules.
- **Database Engine:**
  - **Primary Local Database:** Embedded SQLite (`f4f_community.db` via `node:sqlite` DatabaseSync) tuned with high-performance PRAGMAs (`WAL`, `synchronous = NORMAL`, `cache_size = -64000`, `temp_store = MEMORY`, `busy_timeout = 30000`).
  - **Dual-Mode Cloud Database:** Supabase PostgreSQL integration (`@supabase/supabase-js`) active when credentials are provided in production.
- **Authentication System:**
  - Cryptographic token session management with PBKDF2 password hashing (100,000 iterations, SHA-256).
  - Passwordless 6-digit Email OTP with cryptographic hashing and 10-minute expiry window.
  - Google OAuth 2.0 / Google Identity Services integration with server-side token validation.
  - Role-Based Access Control: `admin`, `member`, `pending`, `suspended`.
- **Payment & Transaction Pipeline:**
  - Razorpay server-side order generation and signature verification (`/api/payments/activate`, `/api/events/pay`).
  - Supports tokenized membership onboarding and paid event ticket reservations.

---

## 2. Design Tokens & Visual Hierarchy

The Founder for Founder design system combines classic editorial elegance with contemporary executive technology aesthetics. The palette is grounded in deep emerald greens, warm gold accents, and warm ivory/cream surfaces.

### 2.1 Color Tokens

#### Primary Emerald Palette
| Token Name | Hex Code | Tailwind / CSS Variable | Usage |
| :--- | :--- | :--- | :--- |
| **Emerald Deep** | `#043E2E` | `colors.emerald-deep` / `--emerald-900` | High-contrast headers, brand anchors, primary CTA backgrounds |
| **Primary Emerald** | `#003527` | `colors.primary` / `--emerald-800` | Main brand identity, active navigation elements |
| **Primary Container** | `#064E3B` | `colors.primary-container` / `--emerald-700` | Sidebar backgrounds, dark card containers |
| **Primary Fixed** | `#B0F0D6` | `colors.primary-fixed` / `--mint-200` | Highlight badges, tag fills, selection indicators |
| **Mint Tint Light** | `#F3FBF7` | `--mint-50` / `--emerald-50` | Table row alternates, soft message bubbles |
| **Mint Accent** | `#10B981` | `--emerald-500` | Live activity indicators, online presence pulses |

#### Secondary Warm Gold & Accent Palette
| Token Name | Hex Code | Tailwind / CSS Variable | Usage |
| :--- | :--- | :--- | :--- |
| **Gold Primary** | `#775A19` | `colors.secondary` / `--gold-600` | Executive accents, founder badges, section sub-eyebrows |
| **Gold Container** | `#FED488` | `colors.secondary-container` | Warning banners, featured badges |
| **Gold Light** | `#F5EFEB` | `colors.gold-light` / `--gold-100` | VIP card backgrounds, testimonial quote cards |
| **Secondary Fixed Dim** | `#E9C176` | `colors.secondary-fixed-dim` | Inactive gold borders, secondary button outlines |

#### Neutral & Surface Canvas
| Token Name | Hex Code | Tailwind / CSS Variable | Usage |
| :--- | :--- | :--- | :--- |
| **Canvas Ivory** | `#FBFBFA` | `colors.canvas-ivory` / `--ivory-bg` | Main website background, light page canvas |
| **Surface Default** | `#FFF8F5` | `colors.surface` | Content panels, modal bodies |
| **Surface Card** | `#FFFFFF` | `colors.surface-card` / `--white` | Elevated interaction cards, white cards |
| **Surface Subtle** | `#F4F3F0` | `colors.surface-subtle` / `--grey-100` | Metric card backgrounds, muted containers |
| **Surface Container High**| `#EEE7E3` | `colors.surface-container-high` | Top announcement ribbon, secondary navigation rails |
| **Hairline Border** | `#EAE8E4` | `colors.border-hairline` / `--border-hairline` | Ultra-clean card dividers, table borders |
| **Strong Border** | `#D5D2CB` | `colors.border-strong` | Active input outlines, focused states |

#### Text & Typography Colors
| Token Name | Hex Code | Usage |
| :--- | :--- | :--- |
| **Text Primary** | `#111827` / `#1E1B19` | High-contrast headlines, card titles, table text |
| **Text Secondary** | `#4B5563` / `#404944` | Descriptive paragraphs, subtitles, meta text |
| **Text Tertiary** | `#6B7280` / `#707974` | Timestamps, placeholder labels, disabled states |
| **Text Inverted** | `#FFFFFF` | Text on emerald and dark surfaces |

---

### 2.2 Typography Specification

The typography pairing reflects an executive, intellectual editorial brand identity:

```
Headings & Display  : 'Playfair Display', serif (Weights: 500, 600, 700)
UI, Navigation & Body : 'Plus Jakarta Sans', sans-serif (Weights: 400, 500, 600, 700, 800)
Numbers & Big Stats  : 'Playfair Display', serif (Weight: 700)
Code & Monospace Tokens: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace
```

#### Typography Scale
| Style Role | Font Family | Size | Line Height | Letter Spacing | Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display Hero (Desktop)** | Playfair Display | 64px | 72px | -0.02em | 600 |
| **Display Hero (Mobile)** | Playfair Display | 40px | 48px | -0.015em | 600 |
| **Headline Large** | Playfair Display | 44px | 52px | -0.02em | 600 |
| **Headline Large (Mobile)**| Playfair Display | 32px | 40px | -0.01em | 600 |
| **Headline Medium** | Playfair Display | 28px | 36px | -0.01em | 600 |
| **Headline Small** | Playfair Display | 22px | 30px | 0em | 500 |
| **Subhead Large** | Plus Jakarta Sans | 20px | 30px | -0.01em | 400 / 500 |
| **Body Large** | Plus Jakarta Sans | 17px | 28px | 0em | 400 |
| **Body Medium** | Plus Jakarta Sans | 15px | 24px | 0em | 400 / 500 |
| **Body Small** | Plus Jakarta Sans | 13px | 20px | +0.005em | 400 / 500 |
| **Label Caps** | Plus Jakarta Sans | 11px | 16px | +0.12em | 700 (Uppercase) |
| **Numeric KPI Stat** | Playfair Display | 48px | 52px | -0.02em | 700 |

---

### 2.3 Spacing, Radii & Elevation Tokens

- **Border Radius:**
  - `DEFAULT`: `0.125rem` (2px)
  - `sm`: `0.25rem` (4px)
  - `md`: `0.375rem` (6px)
  - `lg`: `0.5rem` (8px)
  - `xl`: `0.75rem` (12px)
  - `full`: `9999px` (Pill badges, round buttons)
- **Spacing Units:**
  - `space-xs`: `0.25rem` (4px)
  - `space-sm`: `0.5rem` (8px)
  - `space-md`: `1.0rem` (16px)
  - `space-lg`: `1.75rem` (28px)
  - `space-xl`: `3.0rem` (48px)
  - `gutter`: `1.5rem` (24px)
  - `gutter-lg`: `2.5rem` (40px)
  - `margin-md`: `3.0rem` (48px)
  - `margin-lg`: `6.0rem` (96px)
- **Elevation / Shadows:**
  - `shadow-sm`: `0 1px 2px rgba(0, 0, 0, 0.05)`
  - `shadow-md`: `0 4px 12px rgba(6, 78, 59, 0.06)`
  - `shadow-lg`: `0 10px 25px rgba(6, 78, 59, 0.10)`
  - `shadow-modal`: `0 20px 45px rgba(0, 0, 0, 0.18)`

---

## 3. Component Design Rules

### 3.1 Buttons & Interactive Controls
1. **Primary Button (`.btn-emerald` / `.btn-primary`):**
   - Background: `#043E2E` (or `#003527`), text: `#FFFFFF`.
   - Hover: Brightens to `#064E3B`, subtle elevation increase (`0 4px 12px rgba(4,62,46,0.2)`).
   - Padding: `0.75rem 1.75rem`, font-weight `700`, uppercase letter-spacing `0.05em`.
   - Circular Icon Accent: Optional trailing circle icon `→` (`.btn-circle-icon`).
2. **Outline Button (`.btn-outline-emerald`):**
   - Background: Transparent, border: `1.5px solid #043E2E`, text: `#043E2E`.
   - Hover: Fills with `rgba(4,62,46,0.06)`.
3. **Gold Accent Button (`.btn-gold`):**
   - Background: `#775A19`, text: `#FFFFFF`, hover: `#5D4201`.
4. **Touch Target Rule:**
   - Every interactive button and input MUST meet a minimum height of `44px` on mobile viewports (<768px).

### 3.2 Badges & Eyebrows
- **Eyebrow Headers:** Font size 11px, weight 700, uppercase, letter-spacing `0.12em`. Contains a 6px circular green accent dot (`background: #10B981; box-shadow: 0 0 8px #10B981`).
- **Status Badges:**
  - Active / Approved: Background `rgba(16, 185, 129, 0.12)`, text `#064E3B`, border `1px solid rgba(16, 185, 129, 0.25)`.
  - Pending: Background `rgba(245, 158, 11, 0.12)`, text `#785A1A`, border `1px solid rgba(245, 158, 11, 0.25)`.
  - Rejected / Suspended: Background `rgba(239, 68, 68, 0.12)`, text `#991B1B`, border `1px solid rgba(239, 68, 68, 0.25)`.

### 3.3 Cards & Data Containers
- White background (`#FFFFFF`) with subtle 1px border (`#EAE8E4`) and `8px` corner radius.
- Hover transition: `transform: translateY(-2px); box-shadow: 0 8px 24px rgba(6,78,59,0.08);`.
- Header: Clear separation with optional label caps category badge.

### 3.4 Form Inputs & Dialogs
- Inputs: Height 44px, background `#FFFFFF`, border `1px solid #D5D2CB`, radius `6px`, padding `0.5rem 0.85rem`.
- Focus state: Border color `#064E3B`, box-shadow `0 0 0 3px rgba(6,78,59,0.12)`.
- Modals: Dark blur overlay (`rgba(0,0,0,0.5)`, `backdrop-filter: blur(4px)`). Centered dialog with max-width `440px` (small), `560px` (medium), or `840px` (large).

---

## 4. Responsive Viewport Specifications

| Viewport Width | Device Class | Layout Adaptation Rules |
| :--- | :--- | :--- |
| **320px – 375px** | Small Mobile | Single column, padding 1rem (16px), stacked CTA buttons, drawer menu, zero horizontal overflow |
| **390px – 430px** | Modern & Large Mobile | Single column with fluid typography (`clamp()`), sticky bottom actions, 44px touch targets |
| **768px – 992px** | Tablet | 2-column card grids, compact vertical portal sidebar, adjusted hero capsule collage |
| **1024px – 1366px**| Laptop & Desktop | Full sidebar portal navigation, 3-column feature grids, 16:9 infinite horizontal photo slider |
| **1920px+** | Large Desktop | Centered content container with `max-w-7xl` (1280px) or `1440px` boundary |

---

## 5. Screen-to-Route and Module Mapping

```
                                  Platform Navigation Tree
                                              │
         ┌────────────────────────────────────┴─────────────────────────────────────┐
         ▼                                                                          ▼
  Public Surface                                                            Authenticated Core
  ├── / (Landing Page)                                                      ├── Member Portal (#portalPage)
  ├── /terms & /terms-and-conditions                                        │   ├── Dashboard (#tab-dashboard)
  ├── /privacy-policy                                                       │   ├── Directory (#tab-directory)
  ├── /refund-policy & /refund-and-cancellation-policy                      │   ├── Needs & Wants (#tab-needs)
  ├── /community-guidelines & /guidelines                                   │   ├── CRM Pipeline (#tab-crm)
  └── Token Invitation Activation Flow                                      │   ├── Attendance Tracker (#tab-attendance)
                                                                            │   ├── 1:1 Meetings (#tab-meetings)
                                                                            │   ├── Founders Chat (#tab-chat)
                                                                            │   ├── Events & Experiences (#tab-events)
                                                                            │   ├── Monthly Challenge (#tab-challenge)
                                                                            │   └── Account & Billing (#tab-account)
                                                                            └── Admin Console & CMS Panel (#tab-admin)
                                                                                (Imported from Google Stitch: 9952682829066972868)
```

### Detailed Route Inventory

| Route / Screen ID | View Context | Corresponding Stitch Design Screen | Implementation Status |
| :--- | :--- | :--- | :--- |
| `/` (`#publicPage`) | Public Homepage & Landing | **Screen: Public Homepage & Brand Showcase** | Pending Stitch Screen Import |
| `#showInterestModal` | Application Modal | **Screen: Membership Application Form** | Active in Codebase |
| `#loginModal` | Auth Modal | **Screen: Login & OTP Sheet** | Active in Codebase |
| `/terms` & `/terms-and-conditions` | Legal Page | **Screen: Legal & Terms Agreement** | Active in Next.js App Router |
| `/privacy-policy` | Legal Page | **Screen: Privacy Policy** | Active in Next.js App Router |
| `/refund-policy` | Legal Page | **Screen: Refund & Cancellation Policy**| Active in Next.js App Router |
| `/community-guidelines` | Legal Page | **Screen: Community Charter & Guidelines** | Active in Next.js App Router |
| `/api/public/invitation/[token]` | Activation Flow | **Screen: Member Invitation & Razorpay Checkout** | Active in Codebase |
| `#tab-dashboard` | Member Portal | **Screen: Member Executive Dashboard** | Pending Stitch Screen Import |
| `#tab-directory` | Member Portal | **Screen: Discover Founders Directory** | Pending Stitch Screen Import |
| `#tab-needs` | Member Portal | **Screen: Needs & Wants Opportunity Engine** | Pending Stitch Screen Import |
| `#tab-crm` | Member Portal | **Screen: Leads & Deals CRM** | Pending Stitch Screen Import |
| `#tab-attendance` | Member Portal | **Screen: Attendance & Accountability Tracker** | Pending Stitch Screen Import |
| `#tab-meetings` | Member Portal | **Screen: 1-to-1 Founder Meetings Logger** | Pending Stitch Screen Import |
| `#tab-chat` | Member Portal | **Screen: Founders Community Chat Room** | Pending Stitch Screen Import |
| `#tab-events` | Member Portal | **Screen: Curated Experiences & Ticket RSVP** | Pending Stitch Screen Import |
| `#tab-challenge` | Member Portal | **Screen: Monthly Founder Challenges** | Pending Stitch Screen Import |
| `#tab-account` | Member Portal | **Screen: Account, Profile & Billing** | Pending Stitch Screen Import |
| `#tab-admin` | Admin Portal | **Screen: Admin Console & Executive CMS Panel** | **Successfully Imported from Google Stitch** (`9952682829066972868`) |

---

## 6. Google Stitch Integration Audit & Retrieval Report

### 6.1 Stitch MCP Status
- **MCP Connection Status:** No native `stitch` MCP tool or server is installed or registered in the Antigravity configuration.
- **Audited Tool Directory:** `C:\Users\HP\.gemini\antigravity\mcp` currently hosts `chrome_devtools`, `dak-notebook`, `dak-viz`, and `gemini-api-docs`.
- **Primary Stitch Project ID:** `9952682829066972868` (`https://stitch.withgoogle.com/projects/9952682829066972868`).

### 6.2 Retrieved & Verified Screens
- **Admin Console & CMS Panel (`#tab-admin`):**
  - Design specifications, component layouts, Tailwind tokens, and Google Material Symbols successfully imported from project `9952682829066972868`.
  - Fully integrated into `public/index.html` and `src/app/page.tsx` with live verification tests passing (`tests/verify_admin_ui_live.py`).
  - Key sections active:
    1. Top Context Ribbon (Live System Status, DB indicator, pending items chip).
    2. Executive KPI Metrics Strip (Total Inquiries, Active Members, Experience Registrations, Business Volume).
    3. Membership Applications Review Queue (Search, tab filters, modal detail reviews, Approve/Reject/Status actions).
    4. Audit Logs (Timestamped administrator activity logs).
    5. Curated Meeting Photos Manager (16:9 ratio moments CMS with preview and delete).
    6. Dynamic Media CMS (Hero banners, video links, philosophy cards, format images).
    7. Event Publisher (Live gathering creation with pricing and date pickers).

### 6.3 Pending Stitch Screens
The following screens have not yet been extracted from Stitch into the workspace:
1. **Public Landing Page Screen (`/`):** Hero section, 16:9 meeting moments slider, 5 experience format cards, 6-step application journey, community features tabbed showcase, live FAQ accordion, and footer.
2. **Authenticated Member Portal Screen (`#portalPage`):** Executive member dashboard, founder directory cards, needs & wants opportunity board, leads/deals CRM pipeline, accountability presence tracker, and chat interface.

### 6.4 Next Step to Import Pending Stitch Screens
Since the direct Stitch MCP server is not available, the remaining screens can be imported seamlessly via one of two reliable methods:
- **Method A (Recommended):** Export the HTML/CSS markup for the Public Landing Page and Member Portal directly from Google Stitch and provide the code snippets or files.
- **Method B:** If the user has a Chrome browser session running with remote debugging enabled (`--remote-debugging-port=9222`) logged into Stitch, the `chrome_devtools` MCP can inspect and extract the remaining screens automatically.

---

## 7. Comprehensive Implementation Checklist

### Phase 1: Audit, Tokens & Design Architecture (Current Stage)
- [x] Complete architectural audit of Next.js 14, SQLite/Supabase, Auth, and Razorpay flows.
- [x] Extract and document color palette, typography hierarchy, spacing, and component tokens.
- [x] Verify status of Google Stitch MCP connection and historical projects.
- [x] Author comprehensive `DESIGN.md` in repository root.
- [x] Map all 19 application screens and routes to Stitch design interfaces.

### Phase 2: Public Landing Page Redesign
- [ ] Align Hero Section with Stitch layout while preserving dynamic stats counters (`#counterMembers`, `#counterEvents`).
- [ ] Upgrade Capsule Collage graphics to fluid responsive containers.
- [ ] Apply Stitch typography (`Playfair Display` headlines, `Plus Jakarta Sans` body) across all sections.
- [ ] Refresh 4 Core Philosophy cards and 5 Experience Format cards with Stitch tokens.
- [ ] Implement responsive 6-Step Application Journey timeline for mobile (320px–430px).
- [ ] Optimize 16:9 Continuous Meeting Moments Slider (`#meetingPhotosTrack`) with lazy loading and hardware-accelerated CSS transforms.
- [ ] Modernize FAQ accordion and Final CTA band with Stitch emerald/gold accents.
- [ ] Verify zero horizontal overflow at 320px, 375px, 390px, 430px, 768px, 1024px, 1366px, and 1920px.

### Phase 3: Member Portal Redesign
- [ ] Refactor Portal Sidebar with Stitch active indicator pills and mobile bottom navigation sheet.
- [ ] Re-theme Executive Dashboard Overview (`#tab-dashboard`) with Stitch KPI cards and streak tracker.
- [ ] Upgrade Founder Directory (`#tab-directory`) cards with high-trust badge styling and fast client search.
- [ ] Harmonize Needs & Wants Board (`#tab-needs`) with Stitch badge hierarchy and quick-action response triggers.
- [ ] Enhance Leads & Referrals CRM (`#tab-crm`) deal pipeline visualization and consent disclaimer styling.
- [ ] Polish Attendance Tracker (`#tab-attendance`) and 1:1 Meeting Logger (`#tab-meetings`).
- [ ] Modernize Founders Chat (`#tab-chat`) message bubbles and timestamp typography.
- [ ] Re-style Events & Experiences Hub (`#tab-events`) with Razorpay checkout triggers.
- [ ] Re-skin Account & Billing tab (`#tab-account`) and auto-renewal management controls.

### Phase 4: Modals & Dialog System
- [ ] Apply Stitch card styling and backdrop blur to `#showInterestModal` (Membership Application Form).
- [ ] Harmonize `#loginModal` and `#otpModal` with unified input styling and Google One Tap button.
- [ ] Re-skin `#activationModal` for invited members completing Razorpay onboarding.
- [ ] Polish Event Payment (`#eventPaymentModal`), Check-in (`#checkinModal`), and Log Meeting (`#logMeetingModal`) sheets.

### Phase 5: Legal & Information Pages
- [ ] Apply unified Stitch typography and header/footer chrome to `/terms` and `/terms-and-conditions`.
- [ ] Apply unified Stitch typography to `/privacy-policy`.
- [ ] Apply unified Stitch typography to `/refund-policy` and `/refund-and-cancellation-policy`.
- [ ] Apply unified Stitch typography to `/community-guidelines` and `/guidelines`.

### Phase 6: Quality Assurance & Performance Testing
- [ ] Run responsive layout verification across all 8 target viewport widths (320px to 1920px).
- [ ] Audit touch target sizes (≥44px) across all interactive elements.
- [ ] Verify zero console errors, zero layout shifts (CLS < 0.1), and optimal LCP (< 2.5s).
- [ ] Validate complete end-to-end user flows (Application -> Approval -> Invitation -> Razorpay -> Portal -> Admin).
