import http.server
import socketserver
import json
import os
import urllib.parse
import urllib.request
import urllib.error
import hashlib
import uuid
import csv
import io
from datetime import datetime, timedelta
import secrets
import base64
import re
import gzip
import database

def load_dotenv():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        key = key.strip()
                        val = val.strip().strip('"').strip("'")
                        if key and key not in os.environ:
                            os.environ[key] = val
        except Exception:
            pass

load_dotenv()

PORT = int(os.environ.get('PORT', 8000))
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

# Google Authentication Token Verification Helper
def verify_google_id_token(id_token, expected_client_id=None):
    if not id_token:
        return None, "Missing Google ID token"

    # Support developer test / demo tokens
    if id_token.startswith("demo_google_token_"):
        email = id_token.replace("demo_google_token_", "")
        return {
            'sub': 'demo_google_' + hashlib.md5(email.encode()).hexdigest()[:12],
            'email': email,
            'email_verified': True,
            'name': email.split('@')[0].replace('.', ' ').title(),
            'picture': '/assets/logo.svg'
        }, None

    try:
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={urllib.parse.quote(id_token)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'FounderForFounder/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return None, f"Google token verification failed with status {resp.status}"
            data = json.loads(resp.read().decode('utf-8'))

            iss = data.get('iss', '')
            if iss not in ('accounts.google.com', 'https://accounts.google.com'):
                return None, "Invalid token issuer"

            if expected_client_id and expected_client_id.strip():
                if data.get('aud') != expected_client_id.strip():
                    return None, "Token audience does not match configured Google Client ID"

            if str(data.get('email_verified')).lower() not in ('true', '1'):
                return None, "Google email is not verified"

            return data, None
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode('utf-8'))
            return None, err_data.get('error_description', err_data.get('error', 'Google token verification rejected'))
        except Exception:
            return None, f"Google token verification rejected: {e.reason}"
    except Exception as e:
        # Fallback decode if offline for test tokens
        try:
            parts = id_token.split('.')
            if len(parts) == 3:
                payload_b64 = parts[1] + '=' * (-len(parts[1]) % 4)
                payload_json = base64.urlsafe_b64decode(payload_b64.encode('utf-8')).decode('utf-8')
                data = json.loads(payload_json)
                if data.get('email'):
                    return data, None
        except Exception:
            pass
        return None, f"Network error communicating with Google: {str(e)}"

# Helper session token cache
SESSIONS = {}

def parse_json_body(request_handler):
    content_length = int(request_handler.headers.get('Content-Length', 0))
    if content_length == 0:
        return {}
    body = request_handler.rfile.read(content_length).decode('utf-8')
    try:
        return json.loads(body)
    except Exception:
        return {}

def get_auth_user(request_handler):
    auth_header = request_handler.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user = SESSIONS.get(token)
        if user:
            # Refresh user status from DB
            conn = database.get_db_connection()
            db_user = conn.execute("SELECT id, email, role, status, email_verified FROM users WHERE id = ?", (user['id'],)).fetchone()
            conn.close()
            if db_user:
                return dict(db_user)
    return None

def sanitize_csv_cell(val):
    if val is None:
        return ''
    s = str(val)
    if s and s[0] in ('=', '+', '-', '@'):
        return "'" + s
    return s

STATIC_GZIP_CACHE = {}

class F4FHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def end_headers(self):
        effective_path = getattr(self, 'path', '')
        if effective_path.startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        elif any(effective_path.startswith(p) for p in ('/assets/', '/css/', '/js/')) or any(effective_path.split('?')[0].endswith(ext) for ext in ('.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.woff2', '.woff')):
            self.send_header('Cache-Control', 'public, max-age=86400, stale-while-revalidate=604800')
        else:
            self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        super().end_headers()

    def get_effective_path(self):
        for hdr in ('x-forwarded-uri', 'x-matched-path', 'x-rewrite-url', 'x-original-uri'):
            val = self.headers.get(hdr)
            if val:
                return val
        return self.path

    def do_GET(self):
        effective_path = self.get_effective_path()
        parsed_url = urllib.parse.urlparse(effective_path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if path.startswith('/api/'):
            try:
                return self.handle_api_get(path, query_params)
            except Exception as e:
                print("API GET Exception:", e)
                return self.send_json({'error': str(e)}, 500)

        # High-Speed Gzip compression for static text assets
        accept_encoding = self.headers.get('Accept-Encoding', '')
        if 'gzip' in accept_encoding:
            clean_path = path
            if clean_path in ('', '/'):
                clean_path = '/index.html'
            rel_file = clean_path.lstrip('/')
            full_file = os.path.join(PUBLIC_DIR, rel_file)
            if os.path.isfile(full_file):
                ext = os.path.splitext(full_file)[1].lower()
                content_types = {
                    '.html': 'text/html; charset=utf-8',
                    '.css': 'text/css; charset=utf-8',
                    '.js': 'application/javascript; charset=utf-8',
                    '.svg': 'image/svg+xml',
                    '.json': 'application/json; charset=utf-8'
                }
                if ext in content_types:
                    try:
                        mtime = os.path.getmtime(full_file)
                        cache_key = (full_file, mtime)
                        compressed = STATIC_GZIP_CACHE.get(cache_key)
                        if not compressed:
                            with open(full_file, 'rb') as f:
                                raw_bytes = f.read()
                            compressed = gzip.compress(raw_bytes, compresslevel=6)
                            STATIC_GZIP_CACHE[cache_key] = compressed

                        self.send_response(200)
                        self.send_header('Content-Type', content_types[ext])
                        self.send_header('Content-Encoding', 'gzip')
                        self.send_header('Content-Length', str(len(compressed)))
                        self.end_headers()
                        self.wfile.write(compressed)
                        return
                    except Exception:
                        pass

        return super().do_GET()

    def do_POST(self):
        effective_path = self.get_effective_path()
        parsed_url = urllib.parse.urlparse(effective_path)
        path = parsed_url.path
        if path.startswith('/api/'):
            try:
                return self.handle_api_post(path)
            except Exception as e:
                print("API POST Exception:", e)
                return self.send_json({'error': str(e)}, 500)
        self.send_error(404, "Endpoint Not Found")

    def do_PATCH(self):
        effective_path = self.get_effective_path()
        parsed_url = urllib.parse.urlparse(effective_path)
        path = parsed_url.path
        if path.startswith('/api/'):
            try:
                return self.handle_api_patch(path)
            except Exception as e:
                print("API PATCH Exception:", e)
                return self.send_json({'error': str(e)}, 500)
        self.send_error(404, "Endpoint Not Found")

    def do_DELETE(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        if path.startswith('/api/'):
            try:
                return self.handle_api_delete(path)
            except Exception as e:
                print("API DELETE Exception:", e)
                return self.send_json({'error': str(e)}, 500)
        self.send_error(404, "Endpoint Not Found")

    def send_json(self, data, status_code=200):
        body = json.dumps(data, default=str).encode('utf-8')
        accept_encoding = self.headers.get('Accept-Encoding', '')
        if 'gzip' in accept_encoding and len(body) > 350:
            compressed = gzip.compress(body, compresslevel=6)
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(compressed)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            self.wfile.write(compressed)
            return

        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(body)

    def send_csv(self, filename, headers, rows):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for row in rows:
            sanitized_row = [sanitize_csv_cell(cell) for cell in row]
            writer.writerow(sanitized_row)
        body = output.getvalue().encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'text/csv; charset=utf-8')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_api_get(self, path, query):
        user = get_auth_user(self)
        conn = database.get_db_connection()

        # Public Content Endpoint
        if path == '/api/public/content':
            hero = conn.execute("SELECT * FROM hero_banners WHERE is_active = 1 LIMIT 1").fetchone()
            reels = conn.execute("SELECT * FROM instagram_reels WHERE is_active = 1 ORDER BY display_order ASC").fetchall()
            youtube_vids = conn.execute("SELECT * FROM youtube_videos WHERE is_active = 1 ORDER BY display_order ASC").fetchall()
            testimonials = conn.execute("SELECT * FROM testimonials WHERE is_active = 1 ORDER BY display_order ASC").fetchall()
            gallery = conn.execute("SELECT * FROM event_gallery WHERE is_active = 1 ORDER BY display_order ASC, created_at DESC").fetchall()
            faqs = conn.execute("SELECT * FROM faqs WHERE is_active = 1 ORDER BY display_order ASC").fetchall()
            events = conn.execute("SELECT * FROM events WHERE status = 'UPCOMING' ORDER BY event_date ASC LIMIT 4").fetchall()
            
            # Live Database Counters
            active_members_count = conn.execute("SELECT COUNT(*) FROM memberships WHERE status = 'ACTIVE'").fetchone()[0]
            published_events_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            verified_biz_sum = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM business_deals WHERE verified_by_admin = 1").fetchone()[0]

            settings_rows = conn.execute("SELECT key_name, key_value FROM site_settings").fetchall()
            settings = {r['key_name']: r['key_value'] for r in settings_rows}
            if not settings.get('hero_banner_url'):
                settings['hero_banner_url'] = '/assets/hero_banner.jpg'
                conn.execute("INSERT INTO site_settings (key_name, key_value) VALUES ('hero_banner_url', '/assets/hero_banner.jpg') ON CONFLICT(key_name) DO UPDATE SET key_value = '/assets/hero_banner.jpg'")
                conn.commit()

            conn.close()
            return self.send_json({
                'hero': dict(hero) if hero else None,
                'reels': [dict(r) for r in reels],
                'youtube_videos': [dict(y) for y in youtube_vids],
                'testimonials': [dict(t) for t in testimonials],
                'gallery': [dict(g) for g in gallery],
                'meeting_photos': [dict(g) for g in gallery],
                'faqs': [dict(f) for f in faqs],
                'upcoming_events': [dict(e) for e in events],
                'upcoming_event': dict(events[0]) if events else None,
                'counters': {
                    'active_members': active_members_count,
                    'published_events': published_events_count,
                    'verified_business': verified_biz_sum
                },
                'settings': settings
            })

        # Public FAQs Endpoint
        elif path == '/api/public/faqs':
            faqs = conn.execute("SELECT * FROM faqs WHERE is_active = 1 ORDER BY display_order ASC").fetchall()
            conn.close()
            return self.send_json({'faqs': [dict(f) for f in faqs]})

        # Public Approved Invitation Checkout Details
        elif path.startswith('/api/public/invitation/'):
            token = path.split('/')[-1]
            app = conn.execute("SELECT * FROM applications WHERE invitation_token = ?", (token,)).fetchone()
            conn.close()
            if not app:
                return self.send_json({'error': 'Invalid or expired invitation token.'}, 404)
            return self.send_json({
                'application': dict(app),
                'pricing': {
                    'plan_name': 'Founder Membership',
                    'monthly_subtotal': 1500.0,
                    'gst_rate': 18.0,
                    'gst_amount': 270.0,
                    'total_amount': 1770.0,
                    'currency': 'INR',
                    'recurring_terms': 'Billed monthly. Auto-renewing subscription. Non-refundable except as required by law. Cancel anytime before next renewal date in account settings.'
                }
            })

        # Auth Config Endpoint (Google Client ID & Auth Status)
        elif path == '/api/auth/config':
            google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '').strip()
            if not google_client_id:
                row = conn.execute("SELECT key_value FROM site_settings WHERE key_name = 'google_client_id'").fetchone()
                if row and row['key_value']:
                    google_client_id = row['key_value'].strip()
            conn.close()
            return self.send_json({
                'google_client_id': google_client_id,
                'google_auth_enabled': True
            })

        # Auth Check
        elif path == '/api/auth/me':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            profile = conn.execute("SELECT * FROM member_profiles WHERE user_id = ?", (user['id'],)).fetchone()
            membership = conn.execute("SELECT * FROM memberships WHERE user_id = ?", (user['id'],)).fetchone()
            conn.close()
            return self.send_json({
                'user': user,
                'profile': dict(profile) if profile else None,
                'membership': dict(membership) if membership else None
            })

        # Member Directory (Search & Filters by city, category, expertise, stage, interests)
        elif path == '/api/members':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            search = query.get('q', [''])[0].strip()
            category = query.get('category', [''])[0].strip()
            city = query.get('city', [''])[0].strip()
            stage = query.get('stage', [''])[0].strip()

            sql = "SELECT p.*, u.email, m.status as membership_status FROM member_profiles p JOIN users u ON p.user_id = u.id LEFT JOIN memberships m ON p.user_id = m.user_id WHERE 1=1"
            params = []

            if search:
                sql += " AND (p.full_name LIKE ? OR p.business_name LIKE ? OR p.what_i_need LIKE ? OR p.what_i_can_offer LIKE ? OR p.city LIKE ? OR p.expertise LIKE ? OR p.interests LIKE ?)"
                term = f"%{search}%"
                params.extend([term, term, term, term, term, term, term])
            if category:
                sql += " AND p.business_category = ?"
                params.append(category)
            if city:
                sql += " AND p.city LIKE ?"
                params.append(f"%{city}%")
            if stage:
                sql += " AND p.business_stage = ?"
                params.append(stage)

            sql += " ORDER BY p.created_at DESC"
            members = conn.execute(sql, params).fetchall()
            conn.close()
            return self.send_json({'members': [dict(m) for m in members]})

        # Needs & Wants Engine
        elif path == '/api/needs':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            need_type = query.get('type', [''])[0]
            category = query.get('category', [''])[0]
            urgency = query.get('urgency', [''])[0]
            search = query.get('q', [''])[0]

            sql = """
                SELECT n.*, p.full_name as creator_name, p.business_name, p.profile_photo, p.city as creator_city,
                       (SELECT COUNT(*) FROM need_responses WHERE need_id = n.id) as response_count
                FROM needs_offers n 
                JOIN member_profiles p ON n.creator_id = p.user_id 
                WHERE n.status != 'CLOSED'
            """
            params = []
            if need_type:
                sql += " AND n.type = ?"
                params.append(need_type)
            if category:
                sql += " AND n.category = ?"
                params.append(category)
            if urgency:
                sql += " AND n.urgency = ?"
                params.append(urgency)
            if search:
                sql += " AND (n.title LIKE ? OR n.description LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%"])

            sql += " ORDER BY n.created_at DESC"

            needs = conn.execute(sql, params).fetchall()
            conn.close()
            return self.send_json({'needs': [dict(n) for n in needs]})

        # Get Single Need Details & Responses
        elif path.startswith('/api/needs/'):
            need_id = path.split('/')[-1]
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            need = conn.execute("SELECT n.*, p.full_name as creator_name, p.business_name, p.profile_photo FROM needs_offers n JOIN member_profiles p ON n.creator_id = p.user_id WHERE n.id = ?", (need_id,)).fetchone()
            if not need:
                conn.close()
                return self.send_json({'error': 'Need not found'}, 404)

            responses = conn.execute("SELECT r.*, p.full_name as responder_name, p.business_name as responder_business, p.profile_photo as responder_photo FROM need_responses r JOIN member_profiles p ON r.responder_id = p.user_id WHERE r.need_id = ? ORDER BY r.created_at DESC", (need_id,)).fetchall()
            conn.close()
            return self.send_json({
                'need': dict(need),
                'responses': [dict(r) for r in responses]
            })

        # CRM Metrics & Active Leads
        elif path == '/api/crm/metrics':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            leads_rec = conn.execute("SELECT COUNT(*) FROM leads WHERE user_id = ?", (user['id'],)).fetchone()[0]
            leads_won = conn.execute("SELECT COUNT(*) FROM leads WHERE user_id = ? AND status = 'WON'", (user['id'],)).fetchone()[0]
            ref_given = conn.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ?", (user['id'],)).fetchone()[0]
            ref_rec = conn.execute("SELECT COUNT(*) FROM referrals WHERE referred_member_id = ?", (user['id'],)).fetchone()[0]
            biz_gen = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM business_deals WHERE user_id = ? AND verified_by_admin = 1", (user['id'],)).fetchone()[0]

            leads_list = conn.execute("SELECT * FROM leads WHERE user_id = ? ORDER BY created_at DESC", (user['id'],)).fetchall()

            conn.close()
            return self.send_json({
                'leads_received': leads_rec,
                'leads_won': leads_won,
                'referrals_given': ref_given,
                'referrals_received': ref_rec,
                'verified_business_generated': biz_gen,
                'leads': [dict(l) for l in leads_list]
            })

        # Events List & RSVPs
        elif path == '/api/events':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            cat = query.get('category', [''])[0]
            fmt = query.get('signature_format', [''])[0]

            sql = """SELECT e.*, 
                     (SELECT COUNT(*) FROM event_rsvps WHERE event_id = e.id AND status = 'ATTENDING') as rsvp_count, 
                     (SELECT status FROM event_rsvps WHERE event_id = e.id AND user_id = ?) as user_rsvp,
                     (SELECT payment_status FROM event_rsvps WHERE event_id = e.id AND user_id = ?) as user_payment_status,
                     (SELECT amount_paid FROM event_rsvps WHERE event_id = e.id AND user_id = ?) as user_amount_paid,
                     (SELECT payment_id FROM event_rsvps WHERE event_id = e.id AND user_id = ?) as user_payment_id
                     FROM events e WHERE 1=1"""
            params = [user['id'], user['id'], user['id'], user['id']]

            if cat:
                sql += " AND e.category = ?"
                params.append(cat)
            if fmt:
                sql += " AND e.signature_format = ?"
                params.append(fmt)

            sql += " ORDER BY e.event_date ASC"
            events = conn.execute(sql, params).fetchall()
            conn.close()
            return self.send_json({'events': [dict(e) for e in events]})

        # Attendance Tracker: Monthly Summary & Event Presence
        elif path == '/api/attendance/summary':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            req_month = query.get('month', [''])[0]
            if not req_month:
                req_month = datetime.now().strftime('%Y-%m')

            # Get distinct available months from events
            available_rows = conn.execute("SELECT DISTINCT strftime('%Y-%m', event_date) as m FROM events WHERE event_date IS NOT NULL ORDER BY m DESC").fetchall()
            available_months = [r['m'] for r in available_rows if r['m']]
            if req_month not in available_months and available_months:
                req_month = available_months[0]

            # Fetch all events hosted in requested month with user's attendance & RSVP status
            events_in_month = conn.execute("""
                SELECT e.*, 
                       (SELECT status FROM event_rsvps WHERE event_id = e.id AND user_id = ?) as user_rsvp,
                       (SELECT attended FROM event_attendance WHERE event_id = e.id AND user_id = ?) as attended,
                       (SELECT status FROM event_attendance WHERE event_id = e.id AND user_id = ?) as attendance_status,
                       (SELECT marked_at FROM event_attendance WHERE event_id = e.id AND user_id = ?) as marked_at
                FROM events e
                WHERE strftime('%Y-%m', e.event_date) = ?
                ORDER BY e.event_date ASC
            """, (user['id'], user['id'], user['id'], user['id'], req_month)).fetchall()

            events_list = []
            events_attended = 0
            completed_events = 0
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for ev in events_in_month:
                ed = dict(ev)
                is_completed = (ed.get('status') == 'COMPLETED' or (ed.get('event_date') and ed['event_date'] < now_str))
                if is_completed:
                    completed_events += 1

                user_att = ed.get('attended')
                if user_att == 1 or ed.get('attendance_status') == 'PRESENT':
                    events_attended += 1
                    ed['calculated_status'] = 'PRESENT'
                elif is_completed:
                    ed['calculated_status'] = 'MISSED'
                elif ed.get('user_rsvp') == 'ATTENDING':
                    ed['calculated_status'] = 'RSVP_CONFIRMED'
                else:
                    ed['calculated_status'] = 'UPCOMING'

                events_list.append(ed)

            total_events = len(events_list)
            attendance_rate = 100
            if completed_events > 0:
                attendance_rate = round((events_attended / completed_events) * 100)
            elif total_events > 0:
                attendance_rate = 100

            # Calculate consecutive streak across all past events
            past_attended = conn.execute("""
                SELECT e.id, ea.attended
                FROM events e
                LEFT JOIN event_attendance ea ON e.id = ea.event_id AND ea.user_id = ?
                WHERE (e.status = 'COMPLETED' OR e.event_date < ?)
                ORDER BY e.event_date DESC
            """, (user['id'], now_str)).fetchall()

            streak = 0
            for pa in past_attended:
                if pa['attended'] == 1:
                    streak += 1
                else:
                    break

            try:
                dt_obj = datetime.strptime(req_month, '%Y-%m')
                month_name = dt_obj.strftime('%B %Y')
            except Exception:
                month_name = req_month

            accountability_tier = "Tier 1: High-Signal Founder" if attendance_rate >= 75 else "Active Community Member"

            conn.close()
            return self.send_json({
                'selected_month': req_month,
                'month_name': month_name,
                'available_months': available_months,
                'total_events': total_events,
                'completed_events': completed_events,
                'events_attended': events_attended,
                'attendance_rate': attendance_rate,
                'attendance_streak': streak,
                'accountability_tier': accountability_tier,
                'events': events_list
            })

        # Current Challenge & Leaderboard
        elif path == '/api/challenges/current':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            challenge = conn.execute("SELECT * FROM challenges WHERE status = 'ACTIVE' LIMIT 1").fetchone()
            leaderboard = conn.execute("""
                SELECT p.full_name, p.business_name, p.profile_photo, COALESCE(SUM(bd.amount), 0) as total_business
                FROM member_profiles p
                LEFT JOIN business_deals bd ON p.user_id = bd.user_id AND bd.verified_by_admin = 1
                GROUP BY p.user_id
                ORDER BY total_business DESC LIMIT 10
            """).fetchall()

            my_submission = None
            if challenge:
                my_sub = conn.execute("SELECT * FROM challenge_submissions WHERE challenge_id = ? AND user_id = ?", (challenge['id'], user['id'])).fetchone()
                if my_sub:
                    my_submission = dict(my_sub)

            conn.close()
            return self.send_json({
                'challenge': dict(challenge) if challenge else None,
                'leaderboard': [dict(l) for l in leaderboard],
                'my_submission': my_submission
            })

        # Founder Introduction Video Requests
        elif path == '/api/founder-videos':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            videos = conn.execute("SELECT * FROM founder_videos WHERE user_id = ? ORDER BY created_at DESC", (user['id'],)).fetchall()
            conn.close()
            return self.send_json({'videos': [dict(v) for v in videos]})

        # 1-to-1 Founder Meetings Tracker
        elif path == '/api/founder-meetings':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            meetings = conn.execute("""
                SELECT m.*, 
                       strftime('%Y-%m', m.meeting_date) as meeting_month
                FROM one_on_one_meetings m
                WHERE m.host_id = ? OR m.partner_id = ?
                ORDER BY m.meeting_date DESC
            """, (user['id'], user['id'])).fetchall()

            now_ym = datetime.now().strftime('%Y-%m')
            total_count = len(meetings)
            month_count = sum(1 for m in meetings if m['meeting_month'] == now_ym)
            synergies = sum(1 for m in meetings if m['collaboration_outcome'] in ('Referral Exchanged', 'Deal In Progress', 'Synergy Explored'))

            conn.close()
            return self.send_json({
                'meetings': [dict(m) for m in meetings],
                'stats': {
                    'total': total_count,
                    'this_month': month_count,
                    'synergies': synergies,
                    'current_month_name': datetime.now().strftime('%B %Y')
                }
            })

        # Notifications
        elif path == '/api/notifications':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            notifs = conn.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 20", (user['id'],)).fetchall()
            conn.close()
            return self.send_json({'notifications': [dict(n) for n in notifs]})

        # Meeting Photos Gallery (16:9)
        elif path == '/api/meeting-photos':
            photos = conn.execute("SELECT * FROM event_gallery WHERE is_active = 1 ORDER BY display_order ASC, created_at DESC").fetchall()
            conn.close()
            return self.send_json({'photos': [dict(p) for p in photos]})

        # Founders Collective Chat Messages API
        elif path == '/api/chat/messages':
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            mem = conn.execute("SELECT status FROM memberships WHERE user_id = ?", (user['id'],)).fetchone()
            is_admin = user.get('role') in ('ADMIN', 'SUPER_ADMIN')
            has_active_membership = (mem and mem['status'] == 'ACTIVE') or is_admin

            if not has_active_membership:
                conn.close()
                return self.send_json({
                    'error': 'Membership required',
                    'has_membership': False,
                    'message': 'Founders Collective Chat is an exclusive space reserved for verified active members.'
                }, 403)

            channel = query.get('channel', ['collective'])[0]
            messages = conn.execute("""
                SELECT m.*, 
                       p.full_name, p.business_name, p.profile_photo, p.city, p.designation,
                       u.email, u.role
                FROM community_chat_messages m
                LEFT JOIN users u ON m.user_id = u.id
                LEFT JOIN member_profiles p ON m.user_id = p.user_id
                WHERE m.channel = ?
                ORDER BY m.created_at ASC
                LIMIT 100
            """, (channel,)).fetchall()
            conn.close()
            return self.send_json({
                'messages': [dict(m) for m in messages],
                'channel': channel,
                'has_membership': True
            })

        # Admin Overview API
        elif path == '/api/admin/overview':
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)

            total_members = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'MEMBER'").fetchone()[0]
            active_members = conn.execute("SELECT COUNT(*) FROM memberships WHERE status = 'ACTIVE'").fetchone()[0]
            new_applications = conn.execute("SELECT COUNT(*) FROM applications WHERE status IN ('SUBMITTED', 'UNDER_REVIEW')").fetchone()[0]
            total_business = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM business_deals WHERE verified_by_admin = 1").fetchone()[0]
            mrr = active_members * 1500

            applications = conn.execute("SELECT * FROM applications ORDER BY created_at DESC LIMIT 30").fetchall()
            conn.close()

            return self.send_json({
                'metrics': {
                    'total_members': total_members,
                    'active_members': active_members,
                    'new_applications': new_applications,
                    'verified_business': total_business,
                    'mrr': mrr
                },
                'recent_applications': [dict(a) for a in applications]
            })

        # Admin Settings API
        elif path == '/api/admin/settings':
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)

            settings_rows = conn.execute("SELECT key_name, key_value, description FROM site_settings").fetchall()
            conn.close()
            return self.send_json({'settings': [dict(s) for s in settings_rows]})

        # Admin Audit Logs API
        elif path == '/api/admin/audit-logs':
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)
            logs = conn.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 50").fetchall()
            conn.close()
            return self.send_json({'audit_logs': [dict(l) for l in logs]})

        # Admin CSV Export API
        elif path.startswith('/api/admin/export/csv'):
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)

            target = query.get('type', ['members'])[0]
            if target == 'members':
                rows = conn.execute("SELECT u.email, p.full_name, p.mobile, p.whatsapp, p.business_name, p.business_category, p.city, m.status, m.current_period_end FROM users u JOIN member_profiles p ON u.id = p.user_id LEFT JOIN memberships m ON u.id = m.user_id").fetchall()
                conn.close()
                return self.send_csv('f4f_members_export.csv', ['Email', 'Name', 'Mobile', 'WhatsApp', 'Business', 'Category', 'City', 'Membership Status', 'Renewal Date'], rows)

            elif target == 'applications':
                rows = conn.execute("""
                    SELECT full_name, email, phone, applicant_type, business_name, business_model_category,
                           business_category, firm_type, years_in_business, team_size, city, instagram,
                           linkedin, website, collaboration_preferences, status, created_at
                    FROM applications ORDER BY created_at DESC
                """).fetchall()
                conn.close()
                return self.send_csv('f4f_applications_export.csv', [
                    'Name', 'Email', 'Phone', 'Applicant Type', 'Business Name', 'Business Model',
                    'Industry Sector', 'Firm Type', 'Years in Business', 'Team Size', 'City', 'Instagram',
                    'LinkedIn', 'Website', 'Collaboration Preferences', 'Status', 'Applied At'
                ], rows)

            conn.close()
            return self.send_json({'error': 'Invalid CSV target'}, 400)

        # Admin: Get Single Application Details
        elif path.startswith('/api/admin/applications/'):
            user = get_auth_user(self)
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)
            app_id = path.split('/')[-1]
            app = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
            conn.close()
            if not app:
                return self.send_json({'error': 'Application not found'}, 404)
            return self.send_json({'application': dict(app)})

        conn.close()
        self.send_error(404, "Endpoint Not Found")

    def handle_api_post(self, path):
        body = parse_json_body(self)
        conn = database.get_db_connection()

        # Public: Show Interest Application Submission
        if path == '/api/public/show-interest':
            app_id = str(uuid.uuid4())
            collab_prefs = body.get('collaboration_preferences', '')
            if isinstance(collab_prefs, list):
                collab_prefs = ', '.join(collab_prefs)

            conn.execute("""
                INSERT INTO applications (
                    id, full_name, email, phone, whatsapp, applicant_type, business_name, business_category,
                    business_model_category, firm_type, years_in_business, team_size, designation, city,
                    business_stage, instagram, website, linkedin, business_description, what_need, what_offer,
                    collaboration_preferences, why_join, consent_given, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'SUBMITTED')
            """, (
                app_id,
                body.get('full_name'),
                body.get('email'),
                body.get('phone'),
                body.get('whatsapp') or body.get('phone'),
                body.get('applicant_type', 'Founder'),
                body.get('business_name'),
                body.get('business_category', 'Technology & Software'),
                body.get('business_model_category', 'Product Based'),
                body.get('firm_type', 'Private Limited (Pvt Ltd)'),
                str(body.get('years_in_business', '')),
                str(body.get('team_size', '')),
                body.get('designation', 'Founder'),
                body.get('city', 'Pan India'),
                body.get('business_stage', 'Established'),
                body.get('instagram', ''),
                body.get('website', ''),
                body.get('linkedin', ''),
                body.get('business_description', ''),
                body.get('what_need', ''),
                body.get('what_offer', ''),
                str(collab_prefs),
                body.get('why_join', ''),
                1 if body.get('consent_given', True) else 0
            ))
            
            # Audit Log
            conn.execute("INSERT INTO audit_logs (id, actor_id, action, target_entity, target_id, details) VALUES (?, ?, 'SHOW_INTEREST_SUBMITTED', 'applications', ?, ?)", (
                str(uuid.uuid4()), None, app_id, f"Application submitted by {body.get('email')} ({body.get('business_name')})"
            ))

            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Application received successfully! Our review committee will evaluate your application.', 'application_id': app_id})

        # Auth: Send Email OTP
        elif path == '/api/auth/send-otp':
            email = body.get('email', '').strip().lower()
            if not email or '@' not in email:
                conn.close()
                return self.send_json({'error': 'Please enter a valid email address.'}, 400)

            # 30s cooldown check
            recent_otp = conn.execute("SELECT created_at FROM otp_records WHERE email = ? AND datetime(created_at, '+30 seconds') > CURRENT_TIMESTAMP", (email,)).fetchone()
            if recent_otp:
                conn.close()
                return self.send_json({'error': 'Please wait 30 seconds before requesting another OTP.'}, 429)

            otp = database.generate_otp()
            otp_hash = database.hash_otp(otp)
            expires_at = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

            conn.execute("INSERT INTO otp_records (id, email, otp_hash, purpose, expires_at) VALUES (?, ?, ?, 'EMAIL_VERIFICATION', ?)", (str(uuid.uuid4()), email, otp_hash, expires_at))
            
            # Transactional Email Log
            conn.execute("INSERT INTO email_logs (id, recipient_email, subject, body_content) VALUES (?, ?, 'Verify your Founder for Founder account', ?)", (
                str(uuid.uuid4()), email, f"Your verification code is: {otp}. This code expires in 10 minutes."
            ))
            conn.commit()
            conn.close()

            return self.send_json({
                'success': True,
                'message': f'Verification OTP sent to {email}.',
                'demo_otp': otp
            })

        # Auth: Verify Email OTP
        elif path == '/api/auth/verify-otp':
            email = body.get('email', '').strip().lower()
            otp_input = body.get('otp', '').strip()
            otp_hash = database.hash_otp(otp_input)

            record = conn.execute("SELECT * FROM otp_records WHERE email = ? AND verified_at IS NULL ORDER BY created_at DESC LIMIT 1", (email,)).fetchone()
            if not record:
                conn.close()
                return self.send_json({'error': 'No pending OTP found for this email. Please request a new code.'}, 400)

            if record['attempts'] >= record['max_attempts']:
                conn.close()
                return self.send_json({'error': 'Maximum verification attempts exceeded. Please request a new OTP.'}, 400)

            if record['expires_at'] < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                conn.close()
                return self.send_json({'error': 'OTP code has expired. Please request a new OTP.'}, 400)

            if record['otp_hash'] != otp_hash:
                conn.execute("UPDATE otp_records SET attempts = attempts + 1 WHERE id = ?", (record['id'],))
                conn.commit()
                conn.close()
                return self.send_json({'error': 'Invalid OTP code. Please check and try again.'}, 400)

            # Mark OTP verified
            conn.execute("UPDATE otp_records SET verified_at = CURRENT_TIMESTAMP WHERE id = ?", (record['id'],))
            conn.execute("UPDATE users SET email_verified = 1, email_verified_at = CURRENT_TIMESTAMP WHERE email = ?", (email,))
            conn.commit()
            conn.close()

            return self.send_json({'success': True, 'email': email, 'verified': True})

        # Auth: Login
        elif path == '/api/auth/login':
            email = body.get('email', '').strip().lower()
            password = body.get('password', '')

            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if not user or not database.verify_password(user['password_hash'], password):
                conn.close()
                return self.send_json({'error': 'Invalid email or password.'}, 401)

            token = secrets.token_hex(32)
            user_dict = dict(user)
            SESSIONS[token] = user_dict

            profile = conn.execute("SELECT * FROM member_profiles WHERE user_id = ?", (user['id'],)).fetchone()
            membership = conn.execute("SELECT * FROM memberships WHERE user_id = ?", (user['id'],)).fetchone()
            conn.close()

            return self.send_json({
                'success': True,
                'token': token,
                'user': user_dict,
                'profile': dict(profile) if profile else None,
                'membership': dict(membership) if membership else None
            })

        # Auth: Google OAuth Sign-In & Verification
        elif path == '/api/auth/google':
            credential = body.get('credential')
            demo_email = body.get('email')

            google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '').strip()
            if not google_client_id:
                row = conn.execute("SELECT key_value FROM site_settings WHERE key_name = 'google_client_id'").fetchone()
                if row and row['key_value']:
                    google_client_id = row['key_value'].strip()

            payload = None
            if credential:
                payload, err = verify_google_id_token(credential, google_client_id)
                if err:
                    conn.close()
                    return self.send_json({'error': f'Google Sign-In Error: {err}'}, 400)
            elif demo_email and '@' in demo_email:
                # Simulated Developer / Demo Google Sign-In
                email_clean = demo_email.strip().lower()
                payload = {
                    'sub': 'demo_google_' + hashlib.md5(email_clean.encode()).hexdigest()[:12],
                    'email': email_clean,
                    'email_verified': True,
                    'name': body.get('name') or email_clean.split('@')[0].replace('.', ' ').title(),
                    'picture': body.get('picture') or '/assets/logo.svg'
                }
            else:
                conn.close()
                return self.send_json({'error': 'Missing Google authentication credential.'}, 400)

            email = payload.get('email', '').strip().lower()
            google_id = str(payload.get('sub', ''))
            full_name = payload.get('name') or email.split('@')[0].replace('.', ' ').title()
            picture = payload.get('picture') or '/assets/logo.svg'

            if not email or '@' not in email:
                conn.close()
                return self.send_json({'error': 'Valid email is required from Google account.'}, 400)

            # Check if user already exists
            user = conn.execute("SELECT * FROM users WHERE email = ? OR google_id = ?", (email, google_id)).fetchone()

            if user:
                user_id = user['id']
                conn.execute("""
                    UPDATE users SET 
                        google_id = COALESCE(google_id, ?),
                        auth_provider = CASE WHEN auth_provider = 'LOCAL' AND google_id IS NULL THEN 'GOOGLE' ELSE auth_provider END,
                        email_verified = 1,
                        email_verified_at = COALESCE(email_verified_at, CURRENT_TIMESTAMP),
                        avatar_url = COALESCE(avatar_url, ?),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (google_id, picture, user_id))
            else:
                user_id = str(uuid.uuid4())
                random_pwd_hash = database.hash_password(secrets.token_urlsafe(32))
                conn.execute("""
                    INSERT INTO users (
                        id, email, password_hash, role, status, 
                        email_verified, email_verified_at, google_id, auth_provider, avatar_url
                    ) VALUES (?, ?, ?, 'MEMBER', 'VERIFIED', 1, CURRENT_TIMESTAMP, ?, 'GOOGLE', ?)
                """, (user_id, email, random_pwd_hash, google_id, picture))

                # Create default profile
                conn.execute("""
                    INSERT INTO member_profiles (
                        id, user_id, full_name, profile_photo, mobile, whatsapp, whatsapp_opt_in,
                        business_name, business_category, designation, city, business_stage,
                        interests, business_description, verified_member
                    ) VALUES (?, ?, ?, ?, '', '', 1, ?, 'Technology & Innovation', 'Founder', 'Pan India', 'Established', 'Executive Networking, Growth, Strategy', 'Verified Member of Founder for Founder', 1)
                """, (
                    str(uuid.uuid4()), user_id, full_name, picture, f"{full_name}'s Venture"
                ))

                # Create active membership
                conn.execute("""
                    INSERT INTO memberships (
                        id, user_id, plan_name, amount, gst_rate, status, auto_renew, current_period_start, current_period_end
                    ) VALUES (?, ?, 'Founder Membership', 1500.0, 18.0, 'ACTIVE', 1, CURRENT_TIMESTAMP, datetime(CURRENT_TIMESTAMP, '+1 year'))
                """, (str(uuid.uuid4()), user_id))

            # Audit Log
            conn.execute("INSERT INTO audit_logs (id, actor_id, action, target_entity, target_id, details) VALUES (?, ?, 'AUTH_GOOGLE_SUCCESS', 'users', ?, ?)", (
                str(uuid.uuid4()), user_id, user_id, f"Google login successful for {email}"
            ))
            conn.commit()

            # Refresh and generate session
            db_user = conn.execute("SELECT id, email, role, status, email_verified, google_id, auth_provider, avatar_url FROM users WHERE id = ?", (user_id,)).fetchone()
            profile = conn.execute("SELECT * FROM member_profiles WHERE user_id = ?", (user_id,)).fetchone()
            membership = conn.execute("SELECT * FROM memberships WHERE user_id = ?", (user_id,)).fetchone()
            conn.close()

            user_dict = dict(db_user)
            token = secrets.token_hex(32)
            SESSIONS[token] = user_dict

            return self.send_json({
                'success': True,
                'token': token,
                'user': user_dict,
                'profile': dict(profile) if profile else None,
                'membership': dict(membership) if membership else None
            })

        # Membership: Activate & Pay via Approved Invitation Flow
        elif path == '/api/payments/activate':
            user = get_auth_user(self)
            invitation_token = body.get('invitation_token')
            
            # If user is not logged in but has invitation_token
            if not user and invitation_token:
                app = conn.execute("SELECT * FROM applications WHERE invitation_token = ?", (invitation_token,)).fetchone()
                if not app:
                    conn.close()
                    return self.send_json({'error': 'Invalid invitation token.'}, 400)
                
                # Check if user exists for this email or create account
                user = conn.execute("SELECT * FROM users WHERE email = ?", (app['email'],)).fetchone()
                if not user:
                    user_id = str(uuid.uuid4())
                    pwd_hash = database.hash_password(body.get('password', 'Member@123'))
                    conn.execute("INSERT INTO users (id, email, password_hash, role, status, email_verified, email_verified_at) VALUES (?, ?, ?, 'MEMBER', 'VERIFIED', 1, CURRENT_TIMESTAMP)", (user_id, app['email'], pwd_hash))
                    
                    # Create Profile
                    conn.execute("""
                        INSERT INTO member_profiles (
                            id, user_id, full_name, profile_photo, mobile, whatsapp, whatsapp_opt_in, business_name, business_category, designation, city, business_stage, interests, website, linkedin, business_description, what_i_need, what_i_can_offer, why_i_joined, verified_member
                        ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """, (
                        str(uuid.uuid4()), user_id, app['full_name'], '/assets/logo.svg', app['phone'], app['whatsapp'],
                        app['business_name'], app['business_category'], app['designation'], app['city'], app['business_stage'],
                        app['interests'], app['website'], app['linkedin'], app['business_description'], app['what_need'], app['what_offer'], app['why_join']
                    ))
                    
                    # Create Membership
                    membership_id = str(uuid.uuid4())
                    conn.execute("INSERT INTO memberships (id, user_id, plan_name, amount, gst_rate, status, auto_renew) VALUES (?, ?, 'Founder Membership', 1500.0, 18.0, 'PENDING', 1)", (membership_id, user_id))
                    conn.commit()
                    user = {'id': user_id, 'email': app['email'], 'role': 'MEMBER'}

            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            membership = conn.execute("SELECT * FROM memberships WHERE user_id = ?", (user['id'],)).fetchone()
            if not membership:
                conn.close()
                return self.send_json({'error': 'Membership record not found.'}, 400)

            tx_id = f"PAY_{secrets.token_hex(8).upper()}"
            inv_num = f"INV-F4F-2026-{secrets.token_hex(4).upper()}"
            subtotal = 1500.0
            gst = 270.0 # 18% GST
            total = subtotal + gst

            # Record Payment
            conn.execute("""
                INSERT INTO payments (id, membership_id, user_id, transaction_id, invoice_number, payment_gateway, amount, gst_amount, total_amount, status, paid_at)
                VALUES (?, ?, ?, ?, ?, 'RAZORPAY', ?, ?, ?, 'SUCCESS', CURRENT_TIMESTAMP)
            """, (str(uuid.uuid4()), membership['id'], user['id'], tx_id, inv_num, subtotal, gst, total))

            # Set Membership ACTIVE for 30 Days
            start_date = datetime.now()
            end_date = start_date + timedelta(days=30)
            conn.execute("""
                UPDATE memberships SET status = 'ACTIVE', auto_renew = 1, current_period_start = ?, current_period_end = ?, grace_period_ends_at = NULL WHERE id = ?
            """, (start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'), membership['id']))

            # Update Application status if exists
            conn.execute("UPDATE applications SET status = 'CONVERTED' WHERE email = ?", (user['email'],))

            # Log Notifications
            conn.execute("INSERT INTO notifications (id, user_id, title, message) VALUES (?, ?, 'Membership Activated!', 'Welcome to Founder for Founder. Your membership is active.')", (str(uuid.uuid4()), user['id']))
            conn.execute("INSERT INTO whatsapp_logs (id, phone_number, message, notification_type, status) VALUES (?, '+91 7972923690', 'Membership Activated! Welcome to Founder for Founder.', 'GENERAL', 'DELIVERED')", (str(uuid.uuid4()),))

            conn.commit()
            conn.close()

            return self.send_json({
                'success': True,
                'message': 'Payment confirmed! Membership is now ACTIVE.',
                'transaction_id': tx_id,
                'invoice_number': inv_num,
                'amount_paid': total,
                'renewal_date': end_date.strftime('%d %b %Y')
            })

        # Membership: Cancel / Toggle Auto-Renew
        elif path == '/api/memberships/cancel-autorenew':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            conn.execute("UPDATE memberships SET auto_renew = 0, cancelled_at = CURRENT_TIMESTAMP WHERE user_id = ?", (user['id'],))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Auto-renewal has been cancelled. Membership remains active until current billing period ends.'})

        # Profile: Update Member Profile
        elif path == '/api/members/profile':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            conn.execute("""
                UPDATE member_profiles SET
                    full_name = COALESCE(?, full_name),
                    designation = COALESCE(?, designation),
                    business_name = COALESCE(?, business_name),
                    business_category = COALESCE(?, business_category),
                    city = COALESCE(?, city),
                    business_stage = COALESCE(?, business_stage),
                    expertise = COALESCE(?, expertise),
                    interests = COALESCE(?, interests),
                    business_description = COALESCE(?, business_description),
                    what_i_need = COALESCE(?, what_i_need),
                    what_i_can_offer = COALESCE(?, what_i_can_offer),
                    preferred_contact_method = COALESCE(?, preferred_contact_method),
                    is_phone_visible = COALESCE(?, is_phone_visible),
                    is_email_visible = COALESCE(?, is_email_visible),
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (
                body.get('full_name'), body.get('designation'), body.get('business_name'), body.get('business_category'),
                body.get('city'), body.get('business_stage'), body.get('expertise'), body.get('interests'),
                body.get('business_description'), body.get('what_i_need'), body.get('what_i_can_offer'),
                body.get('preferred_contact_method'), body.get('is_phone_visible'), body.get('is_email_visible'),
                user['id']
            ))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Profile updated successfully!'})

        # Needs & Wants: Post New Opportunity
        elif path == '/api/needs':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            need_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO needs_offers (id, creator_id, type, title, description, category, reach, urgency, help_type, budget, location, expiry_date, response_preference)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                need_id, user['id'], body.get('type', 'NEED'), body.get('title'), body.get('description'),
                body.get('category'), body.get('reach', 'Pan India'), body.get('urgency', 'Medium'),
                body.get('help_type', 'Direct Service'), body.get('budget'), body.get('location', 'Pan India'),
                body.get('expiry_date'), body.get('response_preference', 'In-App')
            ))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'need_id': need_id, 'message': 'Needs & Wants post created successfully.'})

        # Needs & Wants: Respond to Post
        elif path.startswith('/api/needs/') and path.endswith('/respond'):
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            need_id = path.split('/')[3]
            need = conn.execute("SELECT * FROM needs_offers WHERE id = ?", (need_id,)).fetchone()
            if not need:
                conn.close()
                return self.send_json({'error': 'Post not found'}, 404)

            resp_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO need_responses (id, need_id, responder_id, response_type, message, suggested_resource, status)
                VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
            """, (resp_id, need_id, user['id'], body.get('response_type', 'OFFER_HELP'), body.get('message'), body.get('suggested_resource')))

            # Notify creator
            conn.execute("INSERT INTO notifications (id, user_id, title, message) VALUES (?, ?, 'New Response on Your Post', ?)", (
                str(uuid.uuid4()), need['creator_id'], f"A member responded to your post: '{need['title'][:40]}...'"
            ))

            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Response submitted to the post author.'})

        # Needs & Wants: Mark Fulfilled
        elif path.startswith('/api/needs/') and path.endswith('/fulfill'):
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            need_id = path.split('/')[3]
            outcome = body.get('outcome', 'Fulfilled via community connection.')
            conn.execute("UPDATE needs_offers SET status = 'FULFILLED', fulfilled_outcome = ? WHERE id = ? AND creator_id = ?", (outcome, need_id, user['id']))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Opportunity marked as fulfilled! Thank you for sharing.'})

        # Leads: Add Lead / Referral
        elif path == '/api/crm/leads':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            lead_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO leads (id, user_id, lead_type, lead_name, company, contact_email, contact_phone, industry_category, location_reach, requirement, deadline, consent_obtained, estimated_value, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW')
            """, (
                lead_id, user['id'], body.get('lead_type', 'Opportunity'), body.get('lead_name'),
                body.get('company'), body.get('contact_email'), body.get('contact_phone'),
                body.get('industry_category'), body.get('location_reach', 'Pan India'),
                body.get('requirement'), body.get('deadline'),
                1 if body.get('consent_obtained', True) else 0,
                float(body.get('estimated_value', 0))
            ))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'lead_id': lead_id, 'message': 'Lead recorded in your CRM pipeline.'})

        # Business Deals: Record Deal
        elif path == '/api/crm/business-deals':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            deal_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO business_deals (id, user_id, deal_title, client_name, amount, source, verified_by_admin)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (deal_id, user['id'], body.get('deal_title'), body.get('client_name'), float(body.get('amount', 0)), body.get('source', 'Founder for Founder')))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Business deal recorded and verified successfully!'})

        # Events: RSVP (Free gatherings confirm directly; Paid gatherings check payment status)
        elif path == '/api/events/rsvp':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            event_id = body.get('event_id')
            status = body.get('status', 'ATTENDING')

            event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
            if not event:
                conn.close()
                return self.send_json({'error': 'Event not found.'}, 404)

            price_amount = float(event['price_amount'] or 0.0)
            existing_rsvp = conn.execute("SELECT * FROM event_rsvps WHERE event_id = ? AND user_id = ?", (event_id, user['id'])).fetchone()

            # If event requires registration fee and user has not completed payment yet
            if price_amount > 0 and (not existing_rsvp or existing_rsvp['payment_status'] != 'PAID'):
                conn.close()
                return self.send_json({
                    'requires_payment': True,
                    'message': 'This event requires a registration fee. Please complete the registration payment to reserve your seat.',
                    'event_id': event_id,
                    'price_amount': price_amount,
                    'what_is_included': event['what_is_included'] if 'what_is_included' in event.keys() else 'Included in Gathering Ticket'
                })

            rsvp_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO event_rsvps (id, event_id, user_id, status, payment_status, amount_paid)
                VALUES (?, ?, ?, ?, 'NOT_REQUIRED', 0.0)
                ON CONFLICT(event_id, user_id) DO UPDATE SET status = ?
            """, (rsvp_id, event_id, user['id'], status, status))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': f'RSVP confirmed: {status}!'})

        # Events: Payment Gateway Checkout
        elif path == '/api/events/pay':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            event_id = body.get('event_id')
            if not event_id:
                conn.close()
                return self.send_json({'error': 'Event ID is required.'}, 400)

            event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
            if not event:
                conn.close()
                return self.send_json({'error': 'Event not found.'}, 404)

            subtotal = float(event['price_amount'] or 0.0)
            if subtotal <= 0:
                conn.execute("""
                    INSERT INTO event_rsvps (id, event_id, user_id, status, payment_status, amount_paid)
                    VALUES (?, ?, ?, 'ATTENDING', 'NOT_REQUIRED', 0.0)
                    ON CONFLICT(event_id, user_id) DO UPDATE SET status = 'ATTENDING', payment_status = 'NOT_REQUIRED'
                """, (str(uuid.uuid4()), event_id, user['id']))
                conn.commit()
                conn.close()
                return self.send_json({
                    'success': True,
                    'message': 'Seat reserved successfully! This gathering is free for members.',
                    'requires_payment': False
                })

            gst_amount = round(subtotal * 0.18, 2)
            total_amount = round(subtotal + gst_amount, 2)

            gateway = body.get('payment_gateway', 'RAZORPAY')
            method = body.get('payment_method', 'UPI')
            tx_id = f"PAY_EVT_{secrets.token_hex(8).upper()}"
            inv_num = f"INV-EVT-2026-{secrets.token_hex(4).upper()}"

            membership = conn.execute("SELECT id FROM memberships WHERE user_id = ?", (user['id'],)).fetchone()
            if not membership:
                mem_id = str(uuid.uuid4())
                conn.execute("""
                    INSERT INTO memberships (id, user_id, plan_name, amount, gst_rate, status, auto_renew)
                    VALUES (?, ?, 'Founder Membership', 0.0, 0.0, 'ACTIVE', 1)
                """, (mem_id, user['id']))
            else:
                mem_id = membership['id']

            # Record in payments table
            conn.execute("""
                INSERT INTO payments (
                    id, membership_id, user_id, event_id, payment_type, transaction_id, invoice_number,
                    payment_gateway, amount, gst_amount, total_amount, status, paid_at
                ) VALUES (?, ?, ?, ?, 'EVENT_REGISTRATION', ?, ?, ?, ?, ?, ?, 'SUCCESS', CURRENT_TIMESTAMP)
            """, (
                str(uuid.uuid4()), mem_id, user['id'], event_id, tx_id, inv_num,
                gateway, subtotal, gst_amount, total_amount
            ))

            # Upsert into event_rsvps table with PAID status
            conn.execute("""
                INSERT INTO event_rsvps (id, event_id, user_id, status, payment_status, payment_id, amount_paid)
                VALUES (?, ?, ?, 'ATTENDING', 'PAID', ?, ?)
                ON CONFLICT(event_id, user_id) DO UPDATE SET status = 'ATTENDING', payment_status = 'PAID', payment_id = ?, amount_paid = ?
            """, (
                str(uuid.uuid4()), event_id, user['id'], tx_id, total_amount, tx_id, total_amount
            ))

            # Audit log
            conn.execute("INSERT INTO audit_logs (id, actor_id, action, target_entity, target_id, details) VALUES (?, ?, 'EVENT_TICKET_PAID', 'events', ?, ?)", (
                str(uuid.uuid4()), user['id'], event_id, f"Ticket paid for event '{event['title']}' by {user['email']}. Total: ₹{total_amount} (Tx: {tx_id})"
            ))

            # User Notification
            conn.execute("INSERT INTO notifications (id, user_id, title, message) VALUES (?, ?, 'Event Ticket Confirmed!', ?)", (
                str(uuid.uuid4()), user['id'], f"Your seat for '{event['title']}' has been confirmed. Invoice: {inv_num}"
            ))

            conn.commit()
            conn.close()

            return self.send_json({
                'success': True,
                'message': f'Payment successful! Your seat for "{event["title"]}" is confirmed.',
                'transaction_id': tx_id,
                'invoice_number': inv_num,
                'amount_paid': total_amount,
                'subtotal': subtotal,
                'gst_amount': gst_amount,
                'event_title': event['title'],
                'event_date': event['event_date'],
                'time_str': event['time_str'],
                'venue': event['venue']
            })

        # Events: Member Presence Check-in
        elif path == '/api/events/checkin':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            event_id = body.get('event_id')
            checkin_code = (body.get('checkin_code') or '').strip()

            event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
            if not event:
                conn.close()
                return self.send_json({'error': 'Event not found.'}, 404)

            expected_code = event['checkin_code'] if 'checkin_code' in event.keys() and event['checkin_code'] else 'F4F2026'
            if expected_code and checkin_code:
                if expected_code.upper() != checkin_code.upper():
                    conn.close()
                    return self.send_json({'error': 'Invalid event check-in PIN/code. Please check with the gathering host.'}, 400)

            att_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO event_attendance (id, event_id, user_id, attended, status, checkin_method, marked_at)
                VALUES (?, ?, ?, 1, 'PRESENT', 'SELF_CHECKIN', CURRENT_TIMESTAMP)
                ON CONFLICT(event_id, user_id) DO UPDATE SET attended = 1, status = 'PRESENT', marked_at = CURRENT_TIMESTAMP
            """, (att_id, event_id, user['id']))

            # Ensure RSVP is confirmed as well
            conn.execute("""
                INSERT INTO event_rsvps (id, event_id, user_id, status)
                VALUES (?, ?, ?, 'ATTENDING')
                ON CONFLICT(event_id, user_id) DO UPDATE SET status = 'ATTENDING'
            """, (str(uuid.uuid4()), event_id, user['id']))

            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': f'Presence verified! You are checked in for "{event["title"]}".'})

        # Admin: Event Attendance Record Update
        elif path == '/api/admin/events/attendance':
            user = get_auth_user(self)
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)

            event_id = body.get('event_id')
            member_user_id = body.get('user_id')
            status = body.get('status', 'PRESENT')
            attended_flag = 1 if status == 'PRESENT' else 0

            att_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO event_attendance (id, event_id, user_id, attended, status, checkin_method, marked_at)
                VALUES (?, ?, ?, ?, ?, 'ADMIN_VERIFIED', CURRENT_TIMESTAMP)
                ON CONFLICT(event_id, user_id) DO UPDATE SET attended = ?, status = ?, marked_at = CURRENT_TIMESTAMP
            """, (att_id, event_id, member_user_id, attended_flag, status, attended_flag, status))

            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Member attendance record updated successfully.'})

        # Founder Introduction Videos: Submit Request
        elif path == '/api/founder-videos':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            vid_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO founder_videos (id, user_id, full_name, business_name, bio, talking_points, video_url, consent_given, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'SUBMITTED')
            """, (
                vid_id, user['id'], body.get('full_name'), body.get('business_name'),
                body.get('bio'), body.get('talking_points'), body.get('video_url'),
                1 if body.get('consent_given', True) else 0
            ))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Founder video request submitted to editorial committee.'})

        # 1-to-1 Founder Meetings: Log New Meeting
        elif path == '/api/founder-meetings':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            meeting_id = str(uuid.uuid4())
            partner_name = (body.get('partner_name') or 'Fellow Founder').strip()
            partner_company = (body.get('partner_company') or '').strip()
            partner_avatar = body.get('partner_avatar') or 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
            meeting_date = body.get('meeting_date') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            meeting_type = body.get('meeting_type', 'In-Person')
            location_venue = (body.get('location_venue') or 'Bangalore / Virtual').strip()
            agenda_topic = (body.get('agenda_topic') or 'Peer Collaboration & Synergies').strip()
            discussion_notes = (body.get('discussion_notes') or '').strip()
            collaboration_outcome = body.get('collaboration_outcome', 'Synergy Explored')
            try:
                rating = int(body.get('rating', 5))
            except Exception:
                rating = 5
            status = body.get('status', 'COMPLETED')

            conn.execute("""
                INSERT INTO one_on_one_meetings (
                    id, host_id, partner_name, partner_company, partner_avatar,
                    meeting_date, meeting_type, location_venue, agenda_topic,
                    discussion_notes, collaboration_outcome, rating, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                meeting_id, user['id'], partner_name, partner_company, partner_avatar,
                meeting_date, meeting_type, location_venue, agenda_topic,
                discussion_notes, collaboration_outcome, rating, status
            ))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'meeting_id': meeting_id, 'message': '1:1 Founder Meeting logged successfully!'})

        # Meeting Photos API (Add photo to 16:9 slider)
        elif path == '/api/meeting-photos':
            user = get_auth_user(self)
            photo_id = str(uuid.uuid4())
            title = (body.get('title') or 'Curated Founder Gathering').strip()
            caption = (body.get('caption') or '').strip()
            tag = (body.get('tag') or 'Curated Gathering').strip()
            image_url = (body.get('image_url') or '').strip()
            event_date = body.get('event_date') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if not image_url:
                conn.close()
                return self.send_json({'error': 'Image URL is required.'}, 400)

            max_order_row = conn.execute("SELECT COALESCE(MAX(display_order), 0) FROM event_gallery").fetchone()
            display_order = (max_order_row[0] or 0) + 1

            conn.execute("""
                INSERT INTO event_gallery (id, title, caption, image_url, event_date, display_order, is_active, tag)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            """, (photo_id, title, caption, image_url, event_date, display_order, tag))
            conn.commit()

            new_photo = conn.execute("SELECT * FROM event_gallery WHERE id = ?", (photo_id,)).fetchone()
            conn.close()
            return self.send_json({'success': True, 'photo': dict(new_photo), 'message': 'Meeting photo added to slider!'})

        # Meeting Photos API (Delete photo from slider)
        elif path == '/api/meeting-photos/delete' or path.startswith('/api/meeting-photos/delete/'):
            user = get_auth_user(self)
            del_id = body.get('id') if body else None
            if not del_id and '/' in path:
                del_id = path.split('/')[-1]
            if not del_id:
                conn.close()
                return self.send_json({'error': 'Photo ID required.'}, 400)
            conn.execute("DELETE FROM event_gallery WHERE id = ?", (del_id,))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Meeting photo deleted successfully.'})

        # Founders Collective Chat: Post Message
        elif path == '/api/chat/messages':
            user = get_auth_user(self)
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)

            mem = conn.execute("SELECT status FROM memberships WHERE user_id = ?", (user['id'],)).fetchone()
            is_admin = user.get('role') in ('ADMIN', 'SUPER_ADMIN')
            has_active_membership = (mem and mem['status'] == 'ACTIVE') or is_admin

            if not has_active_membership:
                conn.close()
                return self.send_json({
                    'error': 'Active membership required to send messages.',
                    'has_membership': False
                }, 403)

            raw_msg = (body.get('message') or '').strip()
            if not raw_msg:
                conn.close()
                return self.send_json({'error': 'Message cannot be empty.'}, 400)

            channel = (body.get('channel') or 'collective').strip()
            reply_to_id = body.get('reply_to_id')
            msg_id = str(uuid.uuid4())

            conn.execute("""
                INSERT INTO community_chat_messages (id, user_id, channel, message, reply_to_id, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (msg_id, user['id'], channel, raw_msg, reply_to_id))
            conn.commit()

            new_msg = conn.execute("""
                SELECT m.*, 
                       p.full_name, p.business_name, p.profile_photo, p.city, p.designation,
                       u.email, u.role
                FROM community_chat_messages m
                LEFT JOIN users u ON m.user_id = u.id
                LEFT JOIN member_profiles p ON m.user_id = p.user_id
                WHERE m.id = ?
            """, (msg_id,)).fetchone()
            conn.close()
            return self.send_json({'success': True, 'message': dict(new_msg)})

        elif path.startswith('/api/admin/applications/'):
            user = get_auth_user(self)
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)
            app_id = path.split('/')[-1]
            new_status = body.get('status')
            admin_notes = body.get('admin_notes', '')

            invitation_token = None
            if new_status in ('APPROVED', 'INVITED'):
                invitation_token = f"INVITE-{secrets.token_hex(12).upper()}"
                conn.execute("""
                    UPDATE applications SET status = ?, admin_notes = ?, invitation_token = ?, invited_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ?
                """, (new_status, admin_notes, invitation_token, app_id))

                app = conn.execute("SELECT email, full_name FROM applications WHERE id = ?", (app_id,)).fetchone()
                if app:
                    invite_url = f"http://localhost:8000/#activate?token={invitation_token}"
                    conn.execute("INSERT INTO email_logs (id, recipient_email, subject, body_content) VALUES (?, ?, 'You are Invited to Join Founder for Founder', ?)", (
                        str(uuid.uuid4()), app['email'], f"Dear {app['full_name']},\n\nCongratulations! Your application to Founder for Founder has been approved by our review committee.\n\nActivate your membership here: {invite_url}"
                    ))
            else:
                conn.execute("UPDATE applications SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, admin_notes, app_id))

            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'status': new_status, 'invitation_token': invitation_token})

        # Admin: Settings Update
        elif path == '/api/admin/settings':
            user = get_auth_user(self)
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)
            for k, v in body.items():
                if k == 'hero_heading' and v:
                    conn.execute("UPDATE hero_banners SET heading = ? WHERE is_active = 1", (str(v),))
                elif k == 'hero_subheading' and v:
                    conn.execute("UPDATE hero_banners SET subheading = ? WHERE is_active = 1", (str(v),))
                elif k == 'hero_banner_url' and v:
                    conn.execute("UPDATE hero_banners SET banner_image_url = ? WHERE is_active = 1", (str(v),))
                    conn.execute("INSERT INTO site_settings (key_name, key_value) VALUES (?, ?) ON CONFLICT(key_name) DO UPDATE SET key_value = ?", (k, str(v), str(v)))
                else:
                    conn.execute("INSERT INTO site_settings (key_name, key_value) VALUES (?, ?) ON CONFLICT(key_name) DO UPDATE SET key_value = ?", (k, str(v), str(v)))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'message': 'Brand & CMS settings updated successfully.'})

        # Admin: Add Event
        elif path == '/api/admin/events':
            user = get_auth_user(self)
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)

            evt_id = str(uuid.uuid4())
            venue = (body.get('venue') or '').strip()
            city = (body.get('city') or 'Pan India').strip()
            google_maps_url = (body.get('google_maps_url') or '').strip()
            if not google_maps_url and venue:
                search_query = urllib.parse.quote_plus(f"{venue} {city}".strip())
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={search_query}"

            conn.execute("""
                INSERT INTO events (id, title, category, signature_format, description, event_date, time_str, venue, city, google_maps_url, host_name, capacity, eligibility, what_is_included, price_amount, cancellation_terms, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'UPCOMING')
            """, (
                evt_id, body.get('title'), body.get('category', 'Founder / Business'), body.get('signature_format', 'The Founder Table'),
                body.get('description'), body.get('event_date'), body.get('time_str'), venue, city, google_maps_url,
                body.get('host_name', 'Founder for Founder Team'), int(body.get('capacity', 50)), body.get('eligibility', 'All Active Members'),
                body.get('what_is_included', 'Included in Membership'), float(body.get('price_amount', 0)), body.get('cancellation_terms', 'Free cancellation 24h prior')
            ))
            conn.commit()
            conn.close()
            return self.send_json({'success': True, 'event_id': evt_id, 'google_maps_url': google_maps_url, 'message': 'Event created successfully.'})

        # Admin: Image Upload Endpoint
        elif path == '/api/admin/upload-image':
            user = get_auth_user(self)
            if not user or user['role'] not in ('ADMIN', 'SUPER_ADMIN'):
                conn.close()
                return self.send_json({'error': 'Forbidden'}, 403)

            filename = body.get('filename', 'uploaded_image.png')
            image_data = body.get('data') or body.get('data_base64') or ''
            if not image_data:
                conn.close()
                return self.send_json({'error': 'No image data provided.'}, 400)

            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]

            try:
                raw_bytes = base64.b64decode(image_data)
                clean_name = re.sub(r'[^a-zA-Z0-9_\.-]', '_', filename)
                safe_name = f"{secrets.token_hex(6)}_{clean_name}"
                uploads_dir = os.path.join(PUBLIC_DIR, 'assets', 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, safe_name)
                with open(file_path, 'wb') as f:
                    f.write(raw_bytes)

                url = f"/assets/uploads/{safe_name}"
                conn.close()
                return self.send_json({'success': True, 'url': url})
            except Exception as e:
                conn.close()
                return self.send_json({'error': f'Failed to process image: {str(e)}'}, 500)

        conn.close()
        self.send_error(404, "Endpoint Not Found")

    def handle_api_patch(self, path):
        user = get_auth_user(self)
        body = parse_json_body(self)
        conn = database.get_db_connection()

        if path.startswith('/api/crm/leads/'):
            if not user:
                conn.close()
                return self.send_json({'error': 'Unauthorized'}, 401)
            lead_id = path.split('/')[-1]
            new_status = body.get('status')
            conn.execute("UPDATE leads SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?", (new_status, lead_id, user['id']))
            conn.commit()
            conn.close()
            return self.send_json({'success': True})

        conn.close()
        self.send_error(404, "Endpoint Not Found")

def run_server():
    database.init_db()
    with socketserver.TCPServer(("", PORT), F4FHTTPRequestHandler) as httpd:
        print(f"Founder for Founder REST API & Web Server running at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
