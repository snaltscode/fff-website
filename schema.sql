-- SQL Schema for Founder for Founder
-- SQLite Compatible Schema

PRAGMA foreign_keys = ON;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'MEMBER', -- 'SUPER_ADMIN', 'ADMIN', 'COMMUNITY_MANAGER', 'EVENT_HOST', 'MODERATOR', 'MEMBER', 'APPLICANT'
    status TEXT NOT NULL DEFAULT 'UNVERIFIED', -- 'UNVERIFIED', 'VERIFIED', 'SUSPENDED'
    email_verified INTEGER NOT NULL DEFAULT 0,
    email_verified_at DATETIME,
    google_id TEXT UNIQUE,
    auth_provider TEXT NOT NULL DEFAULT 'LOCAL', -- 'LOCAL', 'GOOGLE'
    avatar_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- OTP Records Table (Email Verification)
CREATE TABLE IF NOT EXISTS otp_records (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    otp_hash TEXT NOT NULL,
    purpose TEXT NOT NULL DEFAULT 'EMAIL_VERIFICATION', -- 'EMAIL_VERIFICATION', 'LOGIN', 'PASSWORD_RESET'
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 5,
    expires_at DATETIME NOT NULL,
    verified_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Member Profiles Table
CREATE TABLE IF NOT EXISTS member_profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    profile_photo TEXT,
    mobile TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    whatsapp_opt_in INTEGER NOT NULL DEFAULT 1,
    business_name TEXT NOT NULL,
    business_category TEXT NOT NULL,
    designation TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    business_stage TEXT DEFAULT 'Established', -- 'Early', 'Seed', 'Growth', 'Established', 'Scaling'
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
    preferred_contact_method TEXT DEFAULT 'In-App', -- 'In-App', 'Email', 'WhatsApp', 'Phone'
    is_phone_visible INTEGER DEFAULT 1,
    is_email_visible INTEGER DEFAULT 1,
    verified_member INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Applications Table (Show Interest Funnel)
CREATE TABLE IF NOT EXISTS applications (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    applicant_type TEXT NOT NULL DEFAULT 'Founder', -- 'Founder', 'Business Owner', 'Professional'
    business_name TEXT NOT NULL,
    business_category TEXT NOT NULL,
    designation TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    business_stage TEXT DEFAULT 'Established',
    business_model_category TEXT, -- 'Product Based', 'Service Based', 'Manufacturing', 'Hybrid / Product & Service', 'Other'
    firm_type TEXT, -- 'Private Limited', 'LLP', 'Partnership', 'Sole Proprietorship', 'Public Limited', 'OPC', 'Other'
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
    status TEXT NOT NULL DEFAULT 'SUBMITTED', -- 'SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'INVITED', 'DECLINED', 'WAITLISTED', 'CONVERTED'
    admin_notes TEXT,
    invitation_token TEXT,
    invited_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Memberships Table
CREATE TABLE IF NOT EXISTS memberships (
    id TEXT PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    plan_name TEXT NOT NULL DEFAULT 'Founder Membership',
    amount REAL NOT NULL DEFAULT 1500.0,
    gst_rate REAL NOT NULL DEFAULT 18.0,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'PENDING', -- 'ACTIVE', 'PENDING', 'PAYMENT_FAILED', 'SUSPENDED', 'EXPIRED', 'CANCELLED'
    auto_renew INTEGER NOT NULL DEFAULT 1,
    current_period_start DATETIME,
    current_period_end DATETIME,
    grace_period_ends_at DATETIME,
    cancelled_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    membership_id TEXT, -- NULL for event registrations
    user_id TEXT NOT NULL,
    event_id TEXT, -- NULL for membership renewals
    payment_type TEXT NOT NULL DEFAULT 'MEMBERSHIP', -- 'MEMBERSHIP', 'EVENT_REGISTRATION'
    transaction_id TEXT UNIQUE NOT NULL,
    invoice_number TEXT,
    payment_gateway TEXT NOT NULL DEFAULT 'RAZORPAY',
    amount REAL NOT NULL,
    gst_amount REAL NOT NULL,
    total_amount REAL NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'SUCCESS', 'FAILED', 'REFUNDED'
    gateway_response TEXT,
    paid_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL
);

-- Connections Table
CREATE TABLE IF NOT EXISTS connections (
    id TEXT PRIMARY KEY,
    requester_id TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'ACCEPTED', 'DECLINED'
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Needs & Wants Table
CREATE TABLE IF NOT EXISTS needs_offers (
    id TEXT PRIMARY KEY,
    creator_id TEXT NOT NULL,
    type TEXT NOT NULL, -- 'NEED' or 'WANT' ('OFFER')
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    reach TEXT DEFAULT 'Pan India',
    target_date DATETIME,
    urgency TEXT DEFAULT 'Medium', -- 'Low', 'Medium', 'High', 'Immediate'
    help_type TEXT DEFAULT 'Direct Service', -- 'Direct Service', 'Warm Intro', 'Advice', 'Supplier', 'Co-investing'
    budget TEXT,
    location TEXT NOT NULL DEFAULT 'Pan India',
    expiry_date DATETIME,
    status TEXT NOT NULL DEFAULT 'OPEN', -- 'OPEN', 'IN_PROGRESS', 'FULFILLED', 'CLOSED'
    response_preference TEXT DEFAULT 'In-App',
    fulfilled_outcome TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Need Responses Table
CREATE TABLE IF NOT EXISTS need_responses (
    id TEXT PRIMARY KEY,
    need_id TEXT NOT NULL,
    responder_id TEXT NOT NULL,
    response_type TEXT DEFAULT 'OFFER_HELP', -- 'OFFER_HELP', 'QUESTION', 'SUGGEST_RESOURCE', 'MAKE_INTRO'
    message TEXT NOT NULL,
    suggested_resource TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'ACCEPTED', 'DECLINED'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (need_id) REFERENCES needs_offers(id) ON DELETE CASCADE,
    FOREIGN KEY (responder_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Leads CRM Table
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    lead_type TEXT DEFAULT 'Opportunity', -- 'Opportunity', 'Referral Request', 'Provider Recommendation', 'Warm Intro Request'
    lead_name TEXT NOT NULL,
    company TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    industry_category TEXT,
    location_reach TEXT DEFAULT 'Pan India',
    requirement TEXT NOT NULL,
    deadline DATETIME,
    consent_obtained INTEGER DEFAULT 1,
    estimated_value REAL DEFAULT 0.0,
    source TEXT DEFAULT 'Community',
    status TEXT NOT NULL DEFAULT 'NEW', -- 'NEW', 'ACKNOWLEDGED', 'INTRODUCTION_REQUESTED', 'INTRODUCED', 'IN_DISCUSSION', 'WON', 'NOT_PROCEEDING', 'CLOSED'
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Referrals Table
CREATE TABLE IF NOT EXISTS referrals (
    id TEXT PRIMARY KEY,
    referrer_id TEXT NOT NULL,
    referred_member_id TEXT NOT NULL,
    client_name TEXT NOT NULL,
    requirement TEXT NOT NULL,
    estimated_value REAL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'ACCEPTED', 'CONVERTED', 'CLOSED'
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (referred_member_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Business Deals Table (Recorded Business Generated)
CREATE TABLE IF NOT EXISTS business_deals (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    referral_id TEXT,
    deal_title TEXT NOT NULL,
    client_name TEXT NOT NULL,
    amount REAL NOT NULL,
    source TEXT NOT NULL DEFAULT 'Founder for Founder',
    deal_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verified_by_admin INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (referral_id) REFERENCES referrals(id) ON DELETE SET NULL
);

-- Events Table
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'Founder / Business', -- 'Sports & Movement', 'Outdoor & Adventure', 'Food & Dining', 'Games & Socials', 'Creative Learning', 'Founder / Business', 'Behind-the-scenes', 'Culture', 'Wellbeing & Reflection', 'Community Contribution', 'Trips & Retreats'
    signature_format TEXT DEFAULT 'The Founder Table', -- 'The Founder Table', 'Founder Playbook', 'First Light Club', 'The Inner Circle Roundtable', 'After Hours', 'Off the Clock', 'Founder Field Trip', 'Give First', 'The Founder Challenge', 'Members Host'
    description TEXT NOT NULL,
    event_date DATETIME NOT NULL,
    time_str TEXT NOT NULL,
    venue TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    google_maps_url TEXT,
    host_name TEXT DEFAULT 'Founder for Founder Team',
    banner_url TEXT,
    capacity INTEGER DEFAULT 50,
    rsvp_deadline DATETIME,
    eligibility TEXT DEFAULT 'All Active Members',
    what_is_included TEXT DEFAULT 'Full session access, curated networking, refreshments',
    price_amount REAL DEFAULT 0.0, -- 0 for included in membership, >0 if separately paid experience
    cancellation_terms TEXT DEFAULT 'Free cancellation up to 24 hours prior to event.',
    status TEXT NOT NULL DEFAULT 'UPCOMING', -- 'UPCOMING', 'COMPLETED', 'CANCELLED'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Event RSVPs Table
CREATE TABLE IF NOT EXISTS event_rsvps (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ATTENDING', -- 'ATTENDING', 'WAITLIST', 'CANCELLED'
    payment_status TEXT NOT NULL DEFAULT 'NOT_REQUIRED', -- 'NOT_REQUIRED', 'PENDING', 'PAID'
    payment_id TEXT,
    amount_paid REAL DEFAULT 0.0,
    feedback TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(event_id, user_id)
);

-- Event Attendance Table
CREATE TABLE IF NOT EXISTS event_attendance (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    attended INTEGER NOT NULL DEFAULT 1,
    marked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(event_id, user_id)
);

-- Meeting Reports Table
CREATE TABLE IF NOT EXISTS meeting_reports (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    highlights TEXT NOT NULL,
    next_meeting_date DATETIME,
    published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- Monthly Challenges Table
CREATE TABLE IF NOT EXISTS challenges (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT DEFAULT 'Business Execution', -- 'Business Execution', 'Introductions', 'Learning', 'Fitness', 'Skill Sharing'
    description TEXT NOT NULL,
    target_value REAL NOT NULL,
    unit TEXT NOT NULL DEFAULT 'INR', -- 'INR', 'Leads', 'Introductions', 'Km'
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    rules TEXT NOT NULL,
    reward TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE', -- 'UPCOMING', 'ACTIVE', 'COMPLETED'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Challenge Submissions Table
CREATE TABLE IF NOT EXISTS challenge_submissions (
    id TEXT PRIMARY KEY,
    challenge_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    progress_value REAL NOT NULL DEFAULT 0.0,
    evidence_notes TEXT,
    verified_by_admin INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Founder Introduction Videos Table
CREATE TABLE IF NOT EXISTS founder_videos (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    business_name TEXT NOT NULL,
    bio TEXT NOT NULL,
    talking_points TEXT NOT NULL,
    video_url TEXT,
    consent_given INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'SUBMITTED', -- 'SUBMITTED', 'EDITORIAL_REVIEW', 'CAPTION_DRAFTED', 'APPROVED_BY_FOUNDER', 'PUBLISHED', 'WITHDRAWN'
    draft_caption TEXT,
    published_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    link TEXT,
    is_read INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Email Logs Table
CREATE TABLE IF NOT EXISTS email_logs (
    id TEXT PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_content TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'SENT', -- 'SENT', 'FAILED'
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- WhatsApp Notification Logs Table
CREATE TABLE IF NOT EXISTS whatsapp_logs (
    id TEXT PRIMARY KEY,
    phone_number TEXT NOT NULL,
    message TEXT NOT NULL,
    notification_type TEXT NOT NULL, -- 'MEETING', 'EVENT', 'RENEWAL', 'PAYMENT_FAILED', 'GENERAL'
    status TEXT NOT NULL DEFAULT 'SENT', -- 'SCHEDULED', 'SENT', 'DELIVERED', 'FAILED'
    provider_id TEXT,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CMS Testimonials Table
CREATE TABLE IF NOT EXISTS testimonials (
    id TEXT PRIMARY KEY,
    author_name TEXT NOT NULL,
    author_title TEXT NOT NULL,
    business_name TEXT NOT NULL,
    quote TEXT NOT NULL,
    photo_url TEXT,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CMS Instagram Reels Table
CREATE TABLE IF NOT EXISTS instagram_reels (
    id TEXT PRIMARY KEY,
    reel_url TEXT NOT NULL,
    title TEXT NOT NULL,
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CMS YouTube Embeds Table
CREATE TABLE IF NOT EXISTS youtube_videos (
    id TEXT PRIMARY KEY,
    video_url TEXT NOT NULL,
    youtube_id TEXT NOT NULL,
    title TEXT NOT NULL,
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CMS Hero Banners Table
CREATE TABLE IF NOT EXISTS hero_banners (
    id TEXT PRIMARY KEY,
    heading TEXT NOT NULL,
    subheading TEXT NOT NULL,
    cta_text TEXT NOT NULL DEFAULT 'SHOW INTEREST',
    cta_url TEXT NOT NULL DEFAULT '#show-interest',
    banner_image_url TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CMS Event Gallery Table (Past Event Photos)
CREATE TABLE IF NOT EXISTS event_gallery (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    caption TEXT,
    image_url TEXT NOT NULL,
    event_date DATETIME,
    display_order INTEGER DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CMS FAQs Table
CREATE TABLE IF NOT EXISTS faqs (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    display_order INTEGER DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Site Settings Table (API Keys, Business Config, Social Links)
CREATE TABLE IF NOT EXISTS site_settings (
    key_name TEXT PRIMARY KEY,
    key_value TEXT NOT NULL,
    description TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    actor_id TEXT,
    action TEXT NOT NULL,
    target_entity TEXT NOT NULL,
    target_id TEXT,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 1-to-1 Founder Meetings Tracker Table
CREATE TABLE IF NOT EXISTS one_on_one_meetings (
    id TEXT PRIMARY KEY,
    host_id TEXT NOT NULL,
    partner_id TEXT,
    partner_name TEXT NOT NULL,
    partner_company TEXT,
    partner_avatar TEXT,
    meeting_date DATETIME NOT NULL,
    meeting_type TEXT DEFAULT 'In-Person',
    location_venue TEXT,
    agenda_topic TEXT NOT NULL,
    discussion_notes TEXT,
    collaboration_outcome TEXT DEFAULT 'Synergy Explored',
    rating INTEGER DEFAULT 5,
    status TEXT NOT NULL DEFAULT 'COMPLETED',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (partner_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Founders Collective Community Chat Table
CREATE TABLE IF NOT EXISTS community_chat_messages (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'collective',
    message TEXT NOT NULL,
    reply_to_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Performance Indexes for Rapid Sub-Millisecond Queries
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_memberships_user_status ON memberships(user_id, status);
CREATE INDEX IF NOT EXISTS idx_memberships_status ON memberships(status);

CREATE INDEX IF NOT EXISTS idx_member_profiles_user ON member_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_member_profiles_created ON member_profiles(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_member_profiles_category ON member_profiles(business_category);
CREATE INDEX IF NOT EXISTS idx_member_profiles_stage ON member_profiles(business_stage);
CREATE INDEX IF NOT EXISTS idx_member_profiles_city ON member_profiles(city);

CREATE INDEX IF NOT EXISTS idx_events_status_date ON events(status, event_date);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date);
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_event_gallery_active ON event_gallery(is_active, display_order, created_at);
CREATE INDEX IF NOT EXISTS idx_event_rsvps_lookup ON event_rsvps(event_id, user_id);
CREATE INDEX IF NOT EXISTS idx_event_rsvps_status ON event_rsvps(event_id, status);
CREATE INDEX IF NOT EXISTS idx_event_rsvps_user ON event_rsvps(user_id);
CREATE INDEX IF NOT EXISTS idx_event_attendance_lookup ON event_attendance(event_id, user_id);
CREATE INDEX IF NOT EXISTS idx_event_attendance_user ON event_attendance(user_id);

CREATE INDEX IF NOT EXISTS idx_needs_status ON needs_offers(status, created_at);
CREATE INDEX IF NOT EXISTS idx_needs_creator ON needs_offers(creator_id);
CREATE INDEX IF NOT EXISTS idx_needs_type_cat ON needs_offers(type, category, urgency);
CREATE INDEX IF NOT EXISTS idx_need_responses_need ON need_responses(need_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_need_responses_responder ON need_responses(responder_id);

CREATE INDEX IF NOT EXISTS idx_leads_user ON leads(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_user_status ON leads(user_id, status);
CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referred ON referrals(referred_member_id);
CREATE INDEX IF NOT EXISTS idx_deals_verified ON business_deals(verified_by_admin);
CREATE INDEX IF NOT EXISTS idx_deals_user_verified ON business_deals(user_id, verified_by_admin);

CREATE INDEX IF NOT EXISTS idx_one_on_one_meetings_host ON one_on_one_meetings(host_id, meeting_date);
CREATE INDEX IF NOT EXISTS idx_one_on_one_meetings_partner ON one_on_one_meetings(partner_id, meeting_date);

CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status, created_at);
CREATE INDEX IF NOT EXISTS idx_applications_email ON applications(email);
CREATE INDEX IF NOT EXISTS idx_notifications_user_date ON notifications(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_date ON audit_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_otp_email_verified ON otp_records(email, verified_at);
CREATE INDEX IF NOT EXISTS idx_chat_channel ON community_chat_messages(channel, created_at);
CREATE INDEX IF NOT EXISTS idx_site_settings_key ON site_settings(key_name);
CREATE INDEX IF NOT EXISTS idx_testimonials_active ON testimonials(is_active, display_order);
CREATE INDEX IF NOT EXISTS idx_faqs_active ON faqs(is_active, display_order);



