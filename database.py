import sqlite3
import os
import shutil
import hashlib
import hmac
import secrets
import json
import uuid
from datetime import datetime, timedelta

def get_db_path():
    # If running in Vercel or AWS Lambda serverless environment
    if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        tmp_db = '/tmp/f4f_community.db'
        seed_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f4f_community.db')
        if not os.path.exists(tmp_db) and os.path.exists(seed_db):
            try:
                shutil.copy2(seed_db, tmp_db)
            except Exception as e:
                print("Could not copy seed DB to /tmp:", e)
        return tmp_db
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f4f_community.db')

DB_PATH = get_db_path()
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')

def get_db_connection():
    db_path = get_db_path()
    # Auto-initialize if db file doesn't exist
    if not os.path.exists(db_path):
        init_db()
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 30000;")
    if not os.environ.get('VERCEL') and not os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        try:
            conn.execute("PRAGMA journal_mode = WAL;")
        except Exception:
            pass
    return conn

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${key.hex()}"

def verify_password(stored_password_hash, password_candidate):
    try:
        salt, stored_key = stored_password_hash.split('$')
        candidate_hash = hashlib.pbkdf2_hmac('sha256', password_candidate.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return hmac.compare_digest(stored_key, candidate_hash)
    except Exception:
        return False

def hash_otp(otp_str):
    return hashlib.sha256(otp_str.encode('utf-8')).hexdigest()

def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

def ensure_table_columns(conn):
    """Safely add missing columns to any existing SQLite table."""
    migrations = [
        ("applications", "applicant_type", "TEXT DEFAULT 'Founder'"),
        ("applications", "business_stage", "TEXT DEFAULT 'Established'"),
        ("applications", "interests", "TEXT"),
        ("applications", "what_need", "TEXT"),
        ("applications", "what_offer", "TEXT"),
        ("applications", "consent_given", "INTEGER DEFAULT 1"),
        ("applications", "invitation_token", "TEXT"),
        ("applications", "invited_at", "DATETIME"),
        ("member_profiles", "business_stage", "TEXT DEFAULT 'Established'"),
        ("member_profiles", "expertise", "TEXT"),
        ("member_profiles", "interests", "TEXT"),
        ("member_profiles", "preferred_contact_method", "TEXT DEFAULT 'In-App'"),
        ("member_profiles", "is_phone_visible", "INTEGER DEFAULT 1"),
        ("member_profiles", "is_email_visible", "INTEGER DEFAULT 1"),
        ("payments", "invoice_number", "TEXT"),
        ("needs_offers", "reach", "TEXT DEFAULT 'Pan India'"),
        ("needs_offers", "target_date", "DATETIME"),
        ("needs_offers", "urgency", "TEXT DEFAULT 'Medium'"),
        ("needs_offers", "help_type", "TEXT DEFAULT 'Direct Service'"),
        ("needs_offers", "expiry_date", "DATETIME"),
        ("needs_offers", "response_preference", "TEXT DEFAULT 'In-App'"),
        ("needs_offers", "fulfilled_outcome", "TEXT"),
        ("need_responses", "response_type", "TEXT DEFAULT 'OFFER_HELP'"),
        ("need_responses", "suggested_resource", "TEXT"),
        ("leads", "lead_type", "TEXT DEFAULT 'Opportunity'"),
        ("leads", "industry_category", "TEXT"),
        ("leads", "location_reach", "TEXT DEFAULT 'Pan India'"),
        ("leads", "deadline", "DATETIME"),
        ("leads", "consent_obtained", "INTEGER DEFAULT 1"),
        ("events", "category", "TEXT NOT NULL DEFAULT 'Founder / Business'"),
        ("events", "signature_format", "TEXT DEFAULT 'The Founder Table'"),
        ("events", "host_name", "TEXT DEFAULT 'Founder for Founder Team'"),
        ("events", "eligibility", "TEXT DEFAULT 'All Active Members'"),
        ("events", "what_is_included", "TEXT DEFAULT 'Full session access, curated networking, refreshments'"),
        ("events", "price_amount", "REAL DEFAULT 0.0"),
        ("events", "cancellation_terms", "TEXT DEFAULT 'Free cancellation up to 24 hours prior to event.'"),
        ("event_rsvps", "feedback", "TEXT"),
        ("challenges", "category", "TEXT DEFAULT 'Business Execution'"),
        ("event_attendance", "status", "TEXT DEFAULT 'PRESENT'"),
        ("event_attendance", "checkin_method", "TEXT DEFAULT 'SELF_CHECKIN'"),
        ("event_attendance", "checkin_notes", "TEXT"),
        ("events", "city", "TEXT DEFAULT 'Pan India'"),
        ("events", "checkin_code", "TEXT DEFAULT 'F4F2026'"),
        ("event_gallery", "tag", "TEXT DEFAULT 'Curated Meeting'"),
        ("applications", "years_in_business", "TEXT"),
        ("applications", "team_size", "TEXT"),
        ("applications", "firm_type", "TEXT"),
        ("applications", "instagram", "TEXT"),
        ("applications", "business_model_category", "TEXT"),
        ("applications", "collaboration_preferences", "TEXT"),
        ("users", "google_id", "TEXT"),
        ("users", "auth_provider", "TEXT DEFAULT 'LOCAL'"),
        ("users", "avatar_url", "TEXT"),
        ("event_rsvps", "payment_status", "TEXT DEFAULT 'NOT_REQUIRED'"),
        ("event_rsvps", "payment_id", "TEXT"),
        ("event_rsvps", "amount_paid", "REAL DEFAULT 0.0"),
        ("payments", "event_id", "TEXT"),
        ("payments", "payment_type", "TEXT DEFAULT 'MEMBERSHIP'"),
        ("events", "google_maps_url", "TEXT")
    ]
    cursor = conn.cursor()
    for table, col, col_type in migrations:
        try:
            cursor.execute(f"SELECT {col} FROM {table} LIMIT 1")
        except sqlite3.OperationalError:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
                conn.commit()
            except Exception as ex:
                print(f"Migration note ({table}.{col}): {ex}")

def init_db():
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    ensure_table_columns(conn)
    conn.close()
    seed_default_data()

def seed_default_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Admin User
    cursor.execute("SELECT id FROM users WHERE email = 'admin@founderforfounder.in'")
    admin = cursor.fetchone()
    if not admin:
        admin_id = str(uuid.uuid4())
        pwd_hash = hash_password("Admin@123")
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, role, status, email_verified, email_verified_at)
            VALUES (?, 'admin@founderforfounder.in', ?, 'ADMIN', 'VERIFIED', 1, CURRENT_TIMESTAMP)
        """, (admin_id, pwd_hash))
        
        # Admin Profile
        cursor.execute("""
            INSERT INTO member_profiles (
                id, user_id, full_name, profile_photo, mobile, whatsapp, whatsapp_opt_in,
                business_name, business_category, designation, city, website, linkedin,
                business_description, years_in_business, what_i_need, what_i_can_offer, why_i_joined, verified_member,
                business_stage, expertise, interests, preferred_contact_method
            ) VALUES (
                ?, ?, 'Founder for Founder Admin', '/assets/logo.svg', '', '', 1,
                'snalts.co', 'Business Network', 'Community Director', 'Pan India', 'https://snalts.co',
                'https://www.linkedin.com/company/founder-for-founder/',
                'Founder for Founder is a curated business network connecting founders, entrepreneurs, business owners, and professionals across India.', 5,
                'Ambitious founders seeking genuine relationships, referrals, and strategic collaborations.',
                'Founder meetings, direct introductions, curated peer network, and referral tracking engine.',
                'To build a connected ecosystem of founders across India where ideas turn into action.', 1,
                'Scaling', 'Community Building, Strategic Partnerships', 'Fine Dining, Sports & Movement, Peer Advisory', 'In-App'
            )
        """, (str(uuid.uuid4()), admin_id))

        cursor.execute("""
            INSERT INTO memberships (id, user_id, plan_name, amount, gst_rate, status, auto_renew)
            VALUES (?, ?, 'Founder Membership (Admin)', 0.0, 0.0, 'ACTIVE', 1)
        """, (str(uuid.uuid4()), admin_id))

    # 2. Hero Banner
    cursor.execute("SELECT COUNT(*) FROM hero_banners")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO hero_banners (id, heading, subheading, cta_text, cta_url, is_active)
            VALUES (?, 'Beyond Networking. Into Real Connections.', 'Founder for Founder brings ambitious entrepreneurs, business owners, and professionals into one curated network. Share experiences, explore opportunities, exchange trusted referrals, and build lasting business relationships across India.', 'SHOW INTEREST', '#show-interest', 1)
        """, (str(uuid.uuid4()),))
    else:
        cursor.execute("UPDATE hero_banners SET heading = ?, subheading = ? WHERE is_active = 1", (
            'Beyond Networking. Into Real Connections.',
            'Founder for Founder brings ambitious entrepreneurs, business owners, and professionals into one curated network. Share experiences, explore opportunities, exchange trusted referrals, and build lasting business relationships across India.'
        ))

    # 3. Instagram Reels
    cursor.execute("SELECT COUNT(*) FROM instagram_reels")
    if cursor.fetchone()[0] == 0:
        reels = [
            ("https://www.instagram.com/reel/Dd13kqPQPGf/", "Curated Founder Gatherings", "Inside the Founder for Founder networking session.", 1),
            ("https://www.instagram.com/reel/DXmp93IgCFG/", "Create. Connect. Collaborate.", "How business leaders collaborate and build.", 2),
            ("https://www.instagram.com/reel/DdlvTw5hUKk/", "Generating Credible Business Referrals", "Real growth stories from business leaders across India.", 3)
        ]
        for url, title, cap, order in reels:
            cursor.execute("""
                INSERT INTO instagram_reels (id, reel_url, title, caption, display_order, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (str(uuid.uuid4()), url, title, cap, order))

    # 3.1 YouTube Videos
    cursor.execute("SELECT COUNT(*) FROM youtube_videos")
    if cursor.fetchone()[0] == 0:
        yt_videos = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Founder Spotlight: Scaling Business Across India", "Keynote address on strategic partnerships and peer referrals.", 1),
            ("https://www.youtube.com/watch?v=3JZ_D3ELwOQ", "3JZ_D3ELwOQ", "Building High-Trust Founder Networks", "Insights from our closed-door monthly founder meeting.", 2)
        ]
        for url, ytid, title, cap, order in yt_videos:
            cursor.execute("""
                INSERT INTO youtube_videos (id, video_url, youtube_id, title, caption, display_order, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (str(uuid.uuid4()), url, ytid, title, cap, order))

    # 3.5 Testimonials
    cursor.execute("SELECT COUNT(*) FROM testimonials")
    if cursor.fetchone()[0] == 0:
        testimonials = [
            ("Vikram K.", "Founder & CEO", "Apex Global Tech", "Founder for Founder is the network where every introduction leads to real business. Authentic relationships and high-signal collaborations.", 1),
            ("Ananya M.", "Managing Director", "Precision Industries", "The Needs & Wants engine helped us source key enterprise partners. The curated network environment is unmatched.", 2),
            ("Rohan S.", "Co-Founder", "Elevate Digital", "Monthly founder meetings are insightful and actionable. It has accelerated our peer referral network across cities.", 3)
        ]
        for name, title, biz, quote, order in testimonials:
            cursor.execute("""
                INSERT INTO testimonials (id, author_name, author_title, business_name, quote, display_order, is_active)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (str(uuid.uuid4()), name, title, biz, quote, order))

    # 3.6 Event Gallery (Meeting Photos 16:9)
    cursor.execute("SELECT COUNT(*) FROM event_gallery")
    if cursor.fetchone()[0] < 6:
        cursor.execute("DELETE FROM event_gallery")
        meeting_photos = [
            ("Private Executive Roundtable", "Scale-up founders debating international expansion playbooks and capital efficiency.", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1280&q=80", 1, "Closed-Door Salon"),
            ("Curated Founders Dinner — Bengaluru", "12 Tech founders sharing unfiltered growth bottlenecks over private fine dining.", "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1280&q=80", 2, "Founder Dinner"),
            ("1-to-1 Founder Synergy Session", "Strategic partnership dialogue, cross-selling intros, and shared technical advisory.", "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1280&q=80", 3, "1:1 Meeting"),
            ("Peer Advisory Council Meeting", "Quarterly advisory session evaluating unit economics and talent retention strategies.", "https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=1280&q=80", 4, "Mastermind"),
            ("Founder Field Trip & Strategy Walk", "Morning walk and strategy reflection before high-impact quarterly sprints.", "https://images.unsplash.com/photo-1511578314322-64af69704e6a?auto=format&fit=crop&w=1280&q=80", 5, "Experiential"),
            ("Annual Founder Retreat — Coorg", "Immersive 3-day retreat focused on mental resilience, scale milestones, and peer bonds.", "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=1280&q=80", 6, "Founder Retreat")
        ]
        for title, cap, url, order, tag in meeting_photos:
            cursor.execute("""
                INSERT INTO event_gallery (id, title, caption, image_url, display_order, is_active, tag)
                VALUES (?, ?, ?, ?, ?, 1, ?)
            """, (str(uuid.uuid4()), title, cap, url, order, tag))
        conn.commit()

    # 3.7 FAQs
    cursor.execute("SELECT COUNT(*) FROM faqs")
    if cursor.fetchone()[0] == 0:
        faq_items = [
            ("What is Founder for Founder?", "Founder for Founder is a curated, founder-led network for entrepreneurs, business owners, and business professionals across India. We focus on meaningful connections built through shared experiences, practical collaboration, trusted introductions, and conversations that go beyond conventional networking.", "General", 1),
            ("How does the curated application process work?", "Click 'SHOW INTEREST' on our website and fill in your details. Our membership review committee screens applications for fit, background, and contribution mindset. Approved candidates receive an invitation with activation details.", "Membership", 2),
            ("What types of experiences and activities are organized?", "Our activities span curated formats: Play Together (sports & movement), Explore Together (outdoor trails & retreats), Dine Together (curated lunches & dinners), Build Together (roundtables & execution sprints), and Celebrate Together (after hours & social gatherings).", "Experiences", 3),
            ("Is there an application or membership fee?", "The initial application is completely free. If your application is approved and you are invited to join, membership activation details and clear subscription terms are presented in your private invitation before you commit.", "Pricing", 4),
            ("How is member privacy handled?", "Member privacy and data security are strictly protected. Sensitive request details and personal contact information are not publicly exposed. Direct contact information is shared only after mutual consent or connection authorization.", "Privacy", 5)
        ]
        for q, a, cat, order in faq_items:
            cursor.execute("""
                INSERT INTO faqs (id, question, answer, category, display_order, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (str(uuid.uuid4()), q, a, cat, order))
    else:
        cursor.execute("""
            UPDATE faqs SET answer = 'Click ''SHOW INTEREST'' on our website and fill in your details. Our membership review committee screens applications for fit, background, and contribution mindset. Approved candidates receive an invitation with activation details.'
            WHERE question LIKE '%curated application process%'
        """)

    # 4. Site Settings
    settings = {
        'site_title': ('Founder for Founder', 'Platform title'),
        'club_tagline': ('Create. Connect. Collaborate.', 'Header badge / tagline'),
        'supporting_message': ('Business brings us together. Experiences bring us closer.', 'Brand supporting message'),
        'logo_url': ('/assets/logo.svg', 'Brand Logo URL'),
        'hero_banner_url': ('/assets/hero_banner.jpg', 'Hero Banner Background Image URL'),
        'hero_capsule_1_url': ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80', 'Hero Collage Image 1'),
        'hero_capsule_2_url': ('/assets/hero_banner.jpg', 'Hero Collage Image 2 (Center)'),
        'hero_capsule_3_url': ('https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=600&q=80', 'Hero Collage Image 3'),
        'philosophy_img_1': ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80', 'Core Philosophy: Curated Founder Circle Image'),
        'philosophy_img_2': ('https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=800&q=80', 'Core Philosophy: Shared Experiences Image'),
        'philosophy_img_3': ('https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80', 'Core Philosophy: Needs & Wants Engine Image'),
        'philosophy_img_4': ('https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80', 'Core Philosophy: Leads & Introductions Image'),
        'format_img_play': ('https://images.unsplash.com/photo-1554068865-24cecd4e34b8?auto=format&fit=crop&w=800&q=80', 'Ways We Connect: Play Together Image'),
        'format_img_explore': ('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80', 'Ways We Connect: Explore Together Image'),
        'format_img_dine': ('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80', 'Ways We Connect: Dine Together Image'),
        'format_img_build': ('https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80', 'Ways We Connect: Build Together Image'),
        'format_img_celebrate': ('https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=800&q=80', 'Ways We Connect: Celebrate Together Image'),
        'feature_img_network': ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80', 'Platform Feature: Curated Founder Network Image'),
        'feature_img_needs': ('https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80', 'Platform Feature: Needs & Wants Engine Image'),
        'feature_img_crm': ('https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80', 'Platform Feature: Leads & Referrals CRM Image'),
        'feature_img_meetings': ('https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=800&q=80', 'Platform Feature: Founder Experiences Image'),
        'feature_img_collaborations': ('https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=800&q=80', 'Platform Feature: Business Collaborations Image'),
        'feature_img_challenges': ('https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80', 'Platform Feature: Monthly Challenges Image'),
        'hero_heading': ('Beyond Networking. Into Real Connections.', 'Hero Headline'),
        'hero_subheading': ('Founder for Founder brings ambitious entrepreneurs, business owners, and professionals into one curated network. Share experiences, explore opportunities, exchange trusted referrals, and build lasting business relationships across India.', 'Hero Subheading'),
        'positioning': ('A curated business network for founders.', 'Brand positioning'),
        'vision': ('To build a connected ecosystem of founders across India where ideas turn into action, relationships open doors, and collaboration drives business forward.', 'Brand vision'),
        'legal_business_name': ('snalts.co', 'Legal entity name'),
        'powered_by': ('snalts.co', 'Attribution copy'),
        'registered_city': ('Pan India', 'Registered operating base'),
        'contact_email': ('connect.f4f@gmail.com', 'Official contact email'),
        'contact_phone': ('', 'Official contact phone'),
        'membership_fee': ('1500', 'Monthly fee in INR'),
        'gst_rate': ('18', 'GST percentage'),
        'instagram_url': ('https://www.instagram.com/founder_for_founder', 'Instagram profile URL'),
        'linkedin_url': ('https://www.linkedin.com/company/founder-for-founder/', 'LinkedIn company URL'),
        'facebook_url': ('https://www.facebook.com/share/19ZnPNuhPb/', 'Facebook page URL'),
        'youtube_url': ('https://www.youtube.com/@founderforfounder', 'YouTube channel URL'),
        'whatsapp_api_key': ('', 'Admin API key for WhatsApp Business service provider'),
        'whatsapp_phone_number_id': ('', 'WhatsApp Business Phone Number ID'),
        'payment_gateway_key': ('', 'Razorpay/Stripe API Key'),
        'payment_gateway_secret': ('', 'Razorpay/Stripe API Secret'),
        'email_provider_key': ('', 'Resend/SendGrid API Key'),
        'terms_policy': ('Founder for Founder Terms & Conditions: Membership is application-based and curated. Members agree to foster respectful, transparent business relationships. Zero spam or unauthorized commercial solicitation permitted.', 'Terms Policy'),
        'privacy_policy': ('Founder for Founder Privacy Policy: We respect your data privacy. Personal contact information remains private by default until connection requests are authorized by members.', 'Privacy Policy'),
        'refund_policy': ('Refund and Cancellation Policy: Membership fees paid are non-refundable after successful payment, except where required by applicable law. Auto-renewal can be cancelled anytime prior to the next billing cycle in account settings.', 'Refund Policy'),
        'community_guidelines': ('Community Guidelines: Respect fellow members, maintain confidentiality of closed-door discussions, share genuine opportunities, and honor peer referrals.', 'Community Guidelines')
    }

    for key, (val, desc) in settings.items():
        cursor.execute("SELECT key_name FROM site_settings WHERE key_name = ?", (key,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO site_settings (key_name, key_value, description) VALUES (?, ?, ?)", (key, val, desc))
        else:
            cursor.execute("UPDATE site_settings SET description = ? WHERE key_name = ?", (desc, key))

    # 5. Challenge Seed
    cursor.execute("SELECT COUNT(*) FROM challenges")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO challenges (id, title, category, description, target_value, unit, start_date, end_date, rules, reward, status)
            VALUES (?, 'Monthly Business Collaboration Challenge', 'Business Execution', 'Generate verified business through peer referrals and community opportunities this month.', 100000, 'INR', '2026-10-01', '2026-10-31', 'Record verified deals closed via community connections. Admin verification required.', 'Featured Founder Spotlight & Challenge Recognition', 'ACTIVE')
        """, (str(uuid.uuid4()),))

    # 6. Events Seed
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] < 4:
        events = [
            ("First Light Club — Sunrise Founder Walk & Coffee", "Outdoor & Adventure", "First Light Club", "Invigorating morning trail walk, mindful conversation, and coffee before the workday begins.", "2026-10-04 07:00:00", "07:00 AM - 09:00 AM", "Cubbon Park / City Trails", "Pan India", "F4F Community Host", 30, "All Active Members", "Coffee & Guided Trail Included", 0.0, "COMPLETED", "FLC1004"),
            ("The Inner Circle Roundtable — Enterprise Sales & Hiring Playbook", "Founder / Business", "The Inner Circle Roundtable", "Interactive peer advisory roundtable solving real execution bottlenecks in enterprise B2B sales and strategic partner acquisition.", "2026-10-12 18:00:00", "06:00 PM - 08:30 PM", "F4F Executive Suite & Zoom", "Pan India", "Senior Advisory Committee", 20, "All Active Members", "Included in Membership", 0.0, "COMPLETED", "TIC1012"),
            ("Founder Playbook — Talent Density & Leadership Scale", "Founder / Business", "Founder Playbook", "Tactical deep dive into scaling executive leadership, stock option compensation, and high-performance teams.", "2026-10-20 17:00:00", "05:00 PM - 07:30 PM", "Hybrid Lounge & Virtual", "Pan India", "F4F Leadership Council", 25, "All Active Members", "Included in Membership", 0.0, "COMPLETED", "FPB1020"),
            ("The Founder's Table — Pan-India Leadership Gathering & Dinner", "Food & Dining", "The Founder Table", "Monthly closed-door dinner meeting for Founder for Founder members. Agenda: Business Scoreboard, Founder Spotlight, Needs & Wants, Challenge Updates & Networking.", "2026-10-29 18:30:00", "06:30 PM - 09:30 PM", "Grand Hall & Private Dining Room", "Pan India", "F4F Community Team", 60, "All Active Members", "Curated Dinner & Drinks Included", 0.0, "UPCOMING", "F4F2026"),
            ("First Light Club — Sunrise Trail & Coffee (November)", "Outdoor & Adventure", "First Light Club", "Join fellow founders for an invigorating morning trail walk, mindful conversation, and coffee before the workday begins.", "2026-11-05 06:30:00", "06:30 AM - 09:00 AM", "Nandi Hills / Cubbon Park", "Pan India", "Community Host", 25, "All Active Members", "Coffee & Entry Included", 0.0, "UPCOMING", "FLC1105"),
            ("The Inner Circle Roundtable — Scaling B2B Sales (November)", "Founder / Business", "The Inner Circle Roundtable", "Interactive peer advisory roundtable focused on solving real execution bottlenecks in enterprise B2B sales and partner acquisition.", "2026-11-12 17:00:00", "05:00 PM - 07:30 PM", "F4F Executive Suite & Zoom", "Pan India", "Senior Advisory Committee", 20, "All Active Members", "Included in Membership", 0.0, "UPCOMING", "TIC1112"),
            ("Pickleball & Founder Networking Challenge", "Sports & Movement", "Members Host", "Friendly pickleball tournament and networking social for founders of all skill levels.", "2026-11-18 08:00:00", "08:00 AM - 11:00 AM", "Padel & Sports Club", "Pan India", "Member Host: Vikram K.", 30, "All Active Members", "Court & Equipment Included", 0.0, "UPCOMING", "PB1118")
        ]
        for title, cat, format_str, desc, edate, tstr, venue, city, host, cap, elig, incl, price, stat, code in events:
            cursor.execute("SELECT id FROM events WHERE title = ?", (title,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO events (id, title, category, signature_format, description, event_date, time_str, venue, city, host_name, capacity, eligibility, what_is_included, price_amount, status, checkin_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), title, cat, format_str, desc, edate, tstr, venue, city, host, cap, elig, incl, price, stat, code))

    # 7. Seed Attendance Records for Members
    cursor.execute("SELECT id FROM users WHERE role IN ('ADMIN', 'MEMBER')")
    users = cursor.fetchall()
    cursor.execute("SELECT id, status FROM events WHERE status = 'COMPLETED'")
    completed_events = cursor.fetchall()
    for u in users:
        for idx, ev in enumerate(completed_events):
            # Mark attendance for completed events
            cursor.execute("SELECT id FROM event_attendance WHERE event_id = ? AND user_id = ?", (ev['id'], u['id']))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO event_attendance (id, event_id, user_id, attended, status, checkin_method)
                    VALUES (?, ?, ?, 1, 'PRESENT', 'SELF_CHECKIN')
                """, (str(uuid.uuid4()), ev['id'], u['id']))
        # RSVP for upcoming dinner
        cursor.execute("SELECT id FROM events WHERE status = 'UPCOMING' LIMIT 1")
        up_ev = cursor.fetchone()
        if up_ev:
            cursor.execute("SELECT id FROM event_rsvps WHERE event_id = ? AND user_id = ?", (up_ev['id'], u['id']))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO event_rsvps (id, event_id, user_id, status)
                    VALUES (?, ?, ?, 'ATTENDING')
                """, (str(uuid.uuid4()), up_ev['id'], u['id']))

    # 8. 1-to-1 Founder Meetings Table & Seed
    cursor.execute("""
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
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM one_on_one_meetings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM users WHERE role = 'ADMIN' LIMIT 1")
        admin_row = cursor.fetchone()
        if admin_row:
            admin_uid = admin_row['id']
            sample_meetings = [
                (str(uuid.uuid4()), admin_uid, "Vikram K.", "Apex Global Tech", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80", "2026-10-06 11:00:00", "Coffee / Lunch", "Third Wave Coffee, Indiranagar", "Enterprise GTM & Cloud Co-selling", "Agreed to exchange 3 enterprise introductions in BFSI. Shared playbook on sales incentives.", "Referral Exchanged", 5, "COMPLETED"),
                (str(uuid.uuid4()), admin_uid, "Ananya M.", "Precision Industries", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80", "2026-10-14 15:30:00", "Virtual Video", "Google Meet Room", "Supply Chain Software Architecture", "Reviewed enterprise requirements and supplier integration points. Scheduled follow-up pilot demo.", "Deal In Progress", 5, "COMPLETED"),
                (str(uuid.uuid4()), admin_uid, "Rohan S.", "Elevate Digital", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80", "2026-10-21 16:00:00", "In-Person", "WeWork Galaxy, Residency Road", "Fractional CMO & Talent Acquisition", "Introduced vetted growth marketing lead. Brainstormed co-hosting a closed-door fintech salon.", "Follow-up Scheduled", 5, "COMPLETED")
            ]
            for mid, hid, pname, pcomp, pavatar, mdate, mtype, mloc, magenda, mnotes, mout, mrate, mstat in sample_meetings:
                cursor.execute("""
                    INSERT INTO one_on_one_meetings (id, host_id, partner_name, partner_company, partner_avatar, meeting_date, meeting_type, location_venue, agenda_topic, discussion_notes, collaboration_outcome, rating, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (mid, hid, pname, pcomp, pavatar, mdate, mtype, mloc, magenda, mnotes, mout, mrate, mstat))

    # 9. Founders Collective Chat Table & Seed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_chat_messages (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT 'collective',
            message TEXT NOT NULL,
            reply_to_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM community_chat_messages")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM users WHERE role = 'ADMIN' LIMIT 1")
        admin_row = cursor.fetchone()
        if admin_row:
            admin_uid = admin_row['id']
            cursor.execute("SELECT user_id FROM member_profiles WHERE user_id != ? LIMIT 2", (admin_uid,))
            member_rows = cursor.fetchall()
            uid1 = member_rows[0]['user_id'] if len(member_rows) > 0 else admin_uid
            uid2 = member_rows[1]['user_id'] if len(member_rows) > 1 else admin_uid

            sample_chats = [
                (str(uuid.uuid4()), admin_uid, 'collective', 'Welcome founders to the Founder for Founder Collective Chat! This is an exclusive, confidential space for active members across India to discuss bottlenecks, exchange deal flow, and collaborate. Drop a message to introduce yourself or ask a question.', '2026-10-10 10:00:00'),
                (str(uuid.uuid4()), uid1, 'collective', 'Excited to be part of the network! We recently scaled our B2B SaaS platform across India. Happy to exchange playbooks on enterprise GTM, SOC2 compliance, and sales compensation.', '2026-10-10 11:15:00'),
                (str(uuid.uuid4()), uid2, 'collective', 'Hey everyone! If any founder here is navigating pan-India supply chain logistics or cold-chain warehousing, happy to share our vetted vendor list and unit economics model.', '2026-10-10 14:30:00'),
                (str(uuid.uuid4()), admin_uid, 'collective', 'Reminder: Our upcoming Curated Founders Dinner in Bengaluru has only 3 seats remaining. Check the Experiences tab to reserve your seat!', '2026-10-10 16:45:00')
            ]
            for cid, uid, ch, msg, dt in sample_chats:
                cursor.execute("""
                    INSERT INTO community_chat_messages (id, user_id, channel, message, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (cid, uid, ch, msg, dt))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized and seeded successfully at f4f_community.db!")

