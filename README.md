# Founder for Founder

> **Production-Ready Curated Business Community Platform**  
> A connected ecosystem connecting founders, entrepreneurs, business owners, and professionals across India.  
> Powered by `snalts.co`.

---

## Brand Identity & Core Philosophy

- **Tagline**: *Create. Connect. Collaborate.*
- **Homepage Headline**: *Your next big opportunity could start with a conversation.*
- **Positioning**: *A curated business network for founders.*
- **Vision**: *To build a connected ecosystem of founders across India where ideas turn into action, relationships open doors, and collaboration drives business forward.*
- **Design Palette**: Light Mint (`#F3FBF7`), Soft Mint (`#E4F7EE`), Vibrant Emerald (`#10B981`, `#047857`), Deep Emerald (`#064E3B`), Refined Gold (`#C9A227`), Pure Ink (`#0B0F0D`), and Crisp White (`#FFFFFF`).

---

## Mandatory Brand Rules

- Never use the term "1% Club".
- Never describe the community or membership as "exclusive" or "premium". Use "curated".
- Membership pricing is **NEVER** displayed on the public homepage.
- The platform represents a **Pan-India Network** across cities.
- All statistics, testimonials, and member counts are backed by authentic database entries. Empty sections are gracefully hidden.

---

## Architecture & Tech Stack

- **Backend REST API**: Python native HTTP server with SQLite database engine (`database.py`, `server.py`).
- **Database**: SQLite (`f4f_community.db`), structured with 26 production tables (`schema.sql`).
- **Frontend SPA**: Responsive HTML5, Editorial CSS3 Design System (`public/css/styles.css`), and ES6 JavaScript (`public/js/app.js`).
- **Authentication**: JWT Bearer token sessions + **Cryptographically Secure 6-Digit Email OTP Verification**.
- **Membership Engine**: ₹1,500/month + 18% GST auto-renewable model with payment confirmation verification.
- **WhatsApp Policy**: WhatsApp is strictly a 1-way notification channel; the web application is the core community hub.

---

## Environment Configuration (`.env.example`)

Copy `.env.example` to `.env` for custom local configuration:

```env
PORT=8000
DATABASE_URL=f4f_community.db
AUTH_SECRET=founder_for_founder_secret_key_2026
APP_URL=http://localhost:8000
PAYMENT_PROVIDER_KEY=
PAYMENT_WEBHOOK_SECRET=
EMAIL_PROVIDER_KEY=
EMAIL_FROM=noreply@founderforfounder.in
WHATSAPP_API_KEY=
WHATSAPP_PHONE_NUMBER_ID=
```

---

## Local Development & Server Launch

1. **Initialize Database & Seed Data**:
   ```bash
   python database.py
   ```

2. **Launch Production REST API & Web Server**:
   ```bash
   python server.py
   ```

3. **Open Application**:
   Navigate to `http://localhost:8000` in your web browser.

---

## Default Accounts

- **Admin Account**:
  - Email: `admin@founderforfounder.in`
  - Password: `Admin@123`

---

## Key Features Built

1. **Public Landing Page**: Hero banner with slanted capsule collage & floating dots, About section, Circular image cluster, 6-step How It Works journey with scrubbed progress, Community Features tabs, Instagram Reels & YouTube video block, Testimonials, Upcoming Events, Needs Preview, and Deep Emerald Footer CTA.
2. **Show Interest Funnel & Mandatory Email OTP Verification**: Cryptographically secure 6-digit OTP generation, hashing, rate limiting, and 30-second resend cooldown timer.
3. **Membership Activation**: Server-side confirmed payment flow for ₹1,500/mo + GST with status lifecycle tracking.
4. **Member Portal & Directory**: Searchable founder directory, Needs & Wants opportunity engine ("I NEED", "I CAN OFFER"), Leads & Referrals CRM tracker, Business Deals verification.
5. **Monthly Founder Meetings**: Scheduled event management (held 28th–31st of every month), RSVP tracking, and Meeting Reports.
6. **Monthly Founder Challenge**: Active monthly target tracking and live community leaderboard.
7. **Admin Dashboard & CMS**: Full control over applications, members, Hero banner copy, Brand Logo URL, Instagram Reels & YouTube embeds, Past Event Gallery photos, and CSV data export.
