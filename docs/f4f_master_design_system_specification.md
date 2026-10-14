# FOUNDER FOR FOUNDER (f4f)
## Master Design System & Developer Handoff Specification (v4.0)
*Target Stack: Tailwind CSS + Next.js / React / TypeScript / Vite | Ready for Google Antigravity & Production Engineers*

---

### 1. Brand Identity & Design Principles
- **Brand Name**: Founder for Founder (f4f)
- **Tagline**: *Create. Connect. Collaborate.*
- **Powered By**: `snalts.co`
- **Positioning**: A curated, application-based community connecting verified founders, business owners, and operators across India through shared experiences, peer dialogues, and credible collaboration.
- **Copy Guidelines**:
  - **Forbidden terms in public copy**: Do NOT use *"1%"*, *"exclusive"*, or *"premium"*. Replace with *"curated"*, *"vetted"*, *"high-signal"*, *"peer-to-peer"*.
  - **Public Pricing Rule**: Membership fees (₹1,500 + GST / mo) are strictly withheld from the public homepage and displayed ONLY within the authenticated Admissions/Onboarding and Account/Billing flows.
  - **Tone**: Sophisticated, restrained, human, and editorial — never corporate boilerplate or generic SaaS hype.

---

### 2. Design Tokens & Core Theme
```css
:root {
  /* Surfaces */
  --bg-primary: #ffffff;
  --bg-secondary: #fbfbf9;
  --bg-subtle: #f4f3f0;
  --border-subtle: #e5e4de;
  --border-focus: #064e3b;

  /* Typography Colors */
  --text-primary: #111827;     /* Slate-900 */
  --text-secondary: #4b5563;   /* Gray-600 */
  --text-tertiary: #9ca3af;    /* Gray-400 */
  --text-inverse: #ffffff;

  /* Brand Accents */
  --brand-emerald-900: #043e2e;
  --brand-emerald-800: #064e3b;
  --brand-emerald-700: #0d6e53;
  --brand-emerald-50:  #ecfdf5;
  --brand-gold-accent: #c59b27;
  --brand-gold-subtle: #fef9c3;

  /* Metrics / Semantic Status */
  --status-success-bg: #ecfdf5;
  --status-success-text: #065f46;
  --status-warning-bg: #fffbeb;
  --status-warning-text: #92400e;
  --status-review-bg: #eff6ff;
  --status-review-text: #1e40af;

  /* Radius System (Strict 6px Standard) */
  --radius-sm: 4px;
  --radius-md: 6px;   /* Standard default for cards, inputs, pills, buttons */
  --radius-lg: 8px;
  --radius-full: 9999px;
}
```

---

### 3. Typography Architecture
- **Headings (Display/Editorial)**: Serif (`Domine`, `Playfair Display`, or `Newsreader`). Font weights: 500 to 700. Letter-spacing: `-0.02em`.
- **Interface & Body**: Sans-serif (`Plus Jakarta Sans`, `Inter`, or `system-ui`). Font weights: 400 (Regular), 500 (Medium), 600 (Semibold). Letter-spacing: `normal` or `-0.01em` for subheads.
- **Microcopy / Badges / Monospace**: Monospace / Uppercase Sans tracking `+0.05em` to `+0.08em` for status tags (`CURATED FOUNDER NETWORK`, `BY APPLICATION ONLY`).

---

### 4. Cross-Page Component Standards

#### A. Global Navigation (Desktop & Mobile)
- **Desktop Header**:
  - Left: Official Knot Insignia (`{{DATA:IMAGE:IMAGE_31}}`) + "Founder for Founder | by snalts.co" lockup.
  - Center: Clean menu items: `About`, `Experiences`.
  - Right: `Login` (text link) + `Show Interest →` (Primary Emerald Button with 6px border radius).
- **Mobile Header & Navigation**:
  - Sticky clean top-app bar with crest lockup.
  - Dedicated bottom tab navigation for authenticated members (`Home`, `Needs & Wants`, `Experiences`, `Portal`, `Profile`).

#### B. Button Hierarchy
- **Primary**: Solid Deep Emerald (`#064e3b`), text `#ffffff`, border-radius `6px`, hover `bg-[#043e2e]`, active scale `0.99`.
- **Secondary**: Crisp white/light surface, border `1px solid #e5e4de`, text `#111827`, hover `bg-[#f4f3f0]`.
- **Tertiary / Subtle**: Transparent background, text `#064e3b`, arrow hover transition.

#### C. Forms & Admissions Flow
- Distraction-free multi-step progress bar (6 distinct stages: `Identity & Role`, `Business Scale`, `Web Footprint`, `Network Fit`, `Collaboration`, `Affirmation`).
- Inputs with floating subtle labels, 1px border `#e5e4de`, focused ring `#064e3b`.
- Transparent terms, non-disclosure affirmations, and 72-hour review SLA notification.

#### D. Member Portal & Dashboards
- **Presence & Accountability**: Real-time attendance rate (`100% Streak`), 1:1 conversation ledger, and peer synergy logging.
- **Opportunity Exchange**: "Needs & Wants Engine" tagged cleanly by `I NEED` and `I OFFER` with status badges.
- **Experiences Hub**: 5 Core Pillars: *Play Together* (Sports), *Explore Together* (Outdoors), *Dine Together* (Culinary), *Build Together* (Peer Advisory), *Celebrate Together* (Socials).

#### E. Admin Operations Console
- High-density vetting table with candidate dossiers, verification statuses (`Screening`, `Committee Review`, `Approved for Invite`), and direct token generation.
- Real-time gatekeeper for gatherings with capacity management and access PINs (`F4F2026`).
- Cryptographic zero-leak audit stream ensuring governance integrity under snalts.co covenant.

#### F. Legal & Utility Framework
- Standardized layout for `Terms & Conditions`, `Privacy Policy`, `Refund Policy`, `Community Guidelines`, and `404 Not Found`.
- Single column reading width (max-w-3xl), structured numbering, and breadcrumb navigation back to home.
