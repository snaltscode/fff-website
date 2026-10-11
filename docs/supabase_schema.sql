-- =========================================================
-- Founder for Founder - Supabase PostgreSQL Production Schema
-- Compatible with Supabase SQL Editor (PostgreSQL 15+)
-- =========================================================

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'MEMBER', -- 'SUPER_ADMIN', 'ADMIN', 'COMMUNITY_MANAGER', 'EVENT_HOST', 'MODERATOR', 'MEMBER', 'APPLICANT'
    status TEXT NOT NULL DEFAULT 'UNVERIFIED', -- 'UNVERIFIED', 'VERIFIED', 'SUSPENDED'
    email_verified INTEGER NOT NULL DEFAULT 0,
    email_verified_at TIMESTAMPTZ,
    google_id TEXT UNIQUE,
    auth_provider TEXT NOT NULL DEFAULT 'LOCAL', -- 'LOCAL', 'GOOGLE'
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. OTP RECORDS TABLE (Email Verification)
CREATE TABLE IF NOT EXISTS otp_records (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    otp_hash TEXT NOT NULL,
    purpose TEXT NOT NULL DEFAULT 'EMAIL_VERIFICATION',
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 5,
    expires_at TIMESTAMPTZ NOT NULL,
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 3. MEMBER PROFILES TABLE
CREATE TABLE IF NOT EXISTS member_profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    profile_photo TEXT,
    mobile TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    whatsapp_opt_in INTEGER NOT NULL DEFAULT 1,
    business_name TEXT NOT NULL,
    business_category TEXT NOT NULL,
    designation TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    business_stage TEXT DEFAULT 'Established',
    expertise TEXT,
    interests TEXT,
    website TEXT,
    instagram TEXT,
    linkedin TEXT,
    business_description TEXT NOT NULL,
    years_in_business INTEGER DEFAULT 1,
    what_i_need TEXT,
    what_i_can_offer TEXT,
    why_i_joined TEXT,
    team_size TEXT,
    annual_revenue_range TEXT,
    preferred_contact_method TEXT DEFAULT 'In-App',
    is_phone_visible INTEGER DEFAULT 1,
    is_email_visible INTEGER DEFAULT 1,
    verified_member INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 4. APPLICATIONS TABLE (Show Interest 12-Question Funnel)
CREATE TABLE IF NOT EXISTS applications (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    applicant_type TEXT NOT NULL DEFAULT 'Founder',
    business_name TEXT NOT NULL,
    business_category TEXT NOT NULL,
    designation TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    business_stage TEXT DEFAULT 'Established',
    business_model_category TEXT,
    firm_type TEXT,
    years_in_business TEXT,
    team_size TEXT,
    instagram TEXT,
    website TEXT,
    linkedin TEXT,
    business_description TEXT NOT NULL,
    what_need TEXT,
    what_offer TEXT,
    collaboration_preferences TEXT,
    why_join TEXT NOT NULL,
    consent_given INTEGER DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'SUBMITTED',
    admin_notes TEXT,
    invitation_token TEXT,
    invited_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 5. MEMBERSHIPS TABLE
CREATE TABLE IF NOT EXISTS memberships (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_name TEXT NOT NULL DEFAULT 'Founder Membership',
    amount NUMERIC(10,2) NOT NULL DEFAULT 1500.00,
    gst_rate NUMERIC(5,2) NOT NULL DEFAULT 18.00,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'PENDING',
    auto_renew INTEGER NOT NULL DEFAULT 1,
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    grace_period_ends_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 6. EVENTS & GATHERINGS TABLE
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'Founder / Business',
    signature_format TEXT DEFAULT 'The Founder Table',
    description TEXT NOT NULL,
    event_date TIMESTAMPTZ NOT NULL,
    time_str TEXT NOT NULL,
    venue TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    google_maps_url TEXT,
    host_name TEXT DEFAULT 'Founder for Founder Team',
    banner_url TEXT,
    capacity INTEGER DEFAULT 50,
    rsvp_deadline TIMESTAMPTZ,
    eligibility TEXT DEFAULT 'All Active Members',
    what_is_included TEXT DEFAULT 'Full session access, curated networking, refreshments',
    price_amount NUMERIC(10,2) DEFAULT 0.00,
    cancellation_terms TEXT DEFAULT 'Free cancellation up to 24 hours prior to event.',
    status TEXT NOT NULL DEFAULT 'UPCOMING',
    checkin_code TEXT DEFAULT 'F4F2026',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 7. EVENT RSVPS TABLE
CREATE TABLE IF NOT EXISTS event_rsvps (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'ATTENDING',
    payment_status TEXT NOT NULL DEFAULT 'FREE', -- 'FREE', 'PAID', 'PENDING'
    payment_id TEXT,
    amount_paid NUMERIC(10,2) DEFAULT 0.00,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (event_id, user_id)
);

-- 8. EVENT ATTENDANCE TRACKER
CREATE TABLE IF NOT EXISTS event_attendance (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    attended INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'PRESENT', -- 'PRESENT', 'ABSENT', 'EXCUSED'
    checkin_method TEXT DEFAULT 'HOST_PIN',
    marked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    verified_by TEXT,
    UNIQUE (event_id, user_id)
);

-- 9. PAYMENTS TABLE
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    membership_id TEXT REFERENCES memberships(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_id TEXT REFERENCES events(id) ON DELETE SET NULL,
    payment_type TEXT NOT NULL DEFAULT 'MEMBERSHIP',
    transaction_id TEXT UNIQUE NOT NULL,
    invoice_number TEXT,
    payment_gateway TEXT NOT NULL DEFAULT 'RAZORPAY',
    amount NUMERIC(10,2) NOT NULL,
    gst_amount NUMERIC(10,2) NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'PENDING',
    gateway_response TEXT,
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 10. CONNECTIONS & LEADS TABLE
CREATE TABLE IF NOT EXISTS connections (
    id TEXT PRIMARY KEY,
    requester_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipient_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'PENDING',
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 11. NEEDS & OFFERS TABLE
CREATE TABLE IF NOT EXISTS needs_offers (
    id TEXT PRIMARY KEY,
    creator_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    reach TEXT DEFAULT 'Pan India',
    target_date TIMESTAMPTZ,
    urgency TEXT DEFAULT 'Medium',
    help_type TEXT DEFAULT 'Direct Service',
    budget TEXT,
    location TEXT NOT NULL DEFAULT 'Pan India',
    expiry_date TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'OPEN',
    response_preference TEXT DEFAULT 'In-App',
    fulfilled_outcome TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 12. NEED RESPONSES TABLE
CREATE TABLE IF NOT EXISTS need_responses (
    id TEXT PRIMARY KEY,
    need_id TEXT NOT NULL REFERENCES needs_offers(id) ON DELETE CASCADE,
    responder_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'SENT',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 13. REFERRALS & DEALS CRM
CREATE TABLE IF NOT EXISTS referrals (
    id TEXT PRIMARY KEY,
    referrer_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referred_member_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_name TEXT NOT NULL,
    requirement TEXT NOT NULL,
    estimated_value NUMERIC(12,2) DEFAULT 0.00,
    status TEXT NOT NULL DEFAULT 'PENDING',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS business_deals (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    referral_id TEXT REFERENCES referrals(id) ON DELETE SET NULL,
    deal_title TEXT NOT NULL,
    client_name TEXT NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    source TEXT NOT NULL DEFAULT 'Founder for Founder',
    deal_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verified_by_admin INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 14. 1:1 MEETINGS TRACKER
CREATE TABLE IF NOT EXISTS founder_one_to_one_meetings (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    partner_founder_name TEXT NOT NULL,
    partner_company TEXT NOT NULL,
    meeting_date DATE NOT NULL,
    meeting_format TEXT DEFAULT 'In-Person Coffee',
    discussion_agenda TEXT NOT NULL,
    collaboration_outcome TEXT,
    synergy_rating INTEGER DEFAULT 5,
    confidential_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 15. FOUNDERS COLLECTIVE CHAT MESSAGES
CREATE TABLE IF NOT EXISTS community_chat_messages (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    channel TEXT NOT NULL DEFAULT 'lounge',
    message TEXT NOT NULL,
    reply_to_id TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 16. CMS & SITE SETTINGS
CREATE TABLE IF NOT EXISTS site_settings (
    key_name TEXT PRIMARY KEY,
    key_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hero_banners (
    id TEXT PRIMARY KEY,
    heading TEXT NOT NULL,
    subheading TEXT NOT NULL,
    cta_text TEXT NOT NULL,
    cta_url TEXT NOT NULL,
    banner_image_url TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_gallery (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    caption TEXT,
    image_url TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    tag TEXT DEFAULT 'Closed-Door Salon',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS faqs (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS testimonials (
    id TEXT PRIMARY KEY,
    author_name TEXT NOT NULL,
    author_title TEXT NOT NULL,
    business_name TEXT NOT NULL,
    quote TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Disable Row Level Security (RLS) initially so all tables are readable & writable
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE member_profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE events DISABLE ROW LEVEL SECURITY;
ALTER TABLE event_rsvps DISABLE ROW LEVEL SECURITY;
ALTER TABLE event_attendance DISABLE ROW LEVEL SECURITY;
ALTER TABLE applications DISABLE ROW LEVEL SECURITY;
ALTER TABLE memberships DISABLE ROW LEVEL SECURITY;
ALTER TABLE payments DISABLE ROW LEVEL SECURITY;
ALTER TABLE community_chat_messages DISABLE ROW LEVEL SECURITY;
ALTER TABLE founder_one_to_one_meetings DISABLE ROW LEVEL SECURITY;
ALTER TABLE needs_offers DISABLE ROW LEVEL SECURITY;
ALTER TABLE referrals DISABLE ROW LEVEL SECURITY;
ALTER TABLE business_deals DISABLE ROW LEVEL SECURITY;
ALTER TABLE site_settings DISABLE ROW LEVEL SECURITY;
ALTER TABLE hero_banners DISABLE ROW LEVEL SECURITY;
ALTER TABLE event_gallery DISABLE ROW LEVEL SECURITY;
ALTER TABLE faqs DISABLE ROW LEVEL SECURITY;
ALTER TABLE testimonials DISABLE ROW LEVEL SECURITY;

-- SEED DEFAULT EVENTS WITH GOOGLE MAPS
INSERT INTO events (id, title, category, signature_format, description, event_date, time_str, venue, city, google_maps_url, host_name, capacity, price_amount, what_is_included, status)
VALUES 
('evt-seed-1', 'Monthly Founder Meeting — October Edition', 'Founder / Business', 'The Founder Table', 'Curated dinner gathering with scale-up founders across India.', '2026-10-29 18:30:00+00', '06:30 PM - 09:30 PM', 'Grand Ballroom, Express Inn, Nashik', 'Pan India', 'https://www.google.com/maps/search/?api=1&query=Grand+Ballroom%2C+Express+Inn%2C+Nashik+Pan+India', 'F4F Leadership Council', 60, 0.00, 'Full session access, curated networking, dinner', 'UPCOMING'),
('evt-seed-2', 'First Light Club — Sunrise Founder Walk & Coffee', 'Outdoor & Adventure', 'First Light Club', 'Invigorating morning trail walk, mindful conversation, and coffee.', '2026-11-05 06:30:00+00', '06:30 AM - 09:00 AM', 'Cubbon Park, MG Road', 'Bengaluru', 'https://www.google.com/maps/search/?api=1&query=Cubbon+Park%2C+MG+Road+Bengaluru', 'Community Host', 25, 0.00, 'Morning coffee, trail guide', 'UPCOMING'),
('evt-seed-3', 'The Inner Circle Roundtable — Scaling B2B Sales', 'Founder / Business', 'The Inner Circle Roundtable', 'Interactive peer advisory roundtable focused on enterprise sales.', '2026-11-12 17:00:00+00', '05:00 PM - 07:30 PM', 'The Quorum Club, Two Horizon Center', 'Gurugram', 'https://www.google.com/maps/search/?api=1&query=The+Quorum+Club%2C+Two+Horizon+Center+Gurugram', 'Senior Advisory Committee', 20, 1499.00, 'Private salon access, keynote deck, fine refreshments', 'UPCOMING'),
('evt-seed-4', 'Pickleball & Founder Networking Challenge', 'Sports & Movement', 'The Founder Challenge', 'Friendly tournament and high-energy social for founders.', '2026-11-18 08:00:00+00', '08:00 AM - 11:00 AM', 'Padel & Sports Arena, Bandra West', 'Mumbai', 'https://www.google.com/maps/search/?api=1&query=Padel+%26+Sports+Arena%2C+Bandra+West+Mumbai', 'F4F Sports Committee', 30, 799.00, 'Court booking, equipment, breakfast refreshments', 'UPCOMING')
ON CONFLICT (id) DO NOTHING;
