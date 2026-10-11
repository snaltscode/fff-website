"""
generate_master_docx.py
Generates a complete, comprehensive, beautifully formatted Word document (.docx)
containing the Master System Specification Prompt for the "Founder for Founder" website.
Includes Attendance Tracker, 1-to-1 Meetings Tracker, 16:9 Steady Meeting Photos Slider,
Official Social Profiles, 12-Question Comprehensive Admissions Questionnaire, Dynamic CMS,
and Animated UI/UX Specifications.
Built with pure Python 3 standard library (zipfile, xml.sax.saxutils).
"""

import os
import zipfile
import html

def xml_escape(text):
    if text is None:
        return ""
    return html.escape(str(text), quote=True)

class DocxBuilder:
    def __init__(self):
        self.body_elements = []

    def add_title(self, title_text, subtitle_text=None, meta_text=None):
        p = f'''<w:p>
          <w:pPr>
            <w:jc w:val="center"/>
            <w:spacing w:before="360" w:after="120"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:b/>
              <w:sz w:val="52"/>
              <w:color w:val="064E3B"/>
            </w:rPr>
            <w:t>{xml_escape(title_text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

        if subtitle_text:
            p_sub = f'''<w:p>
              <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:before="0" w:after="180"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                  <w:sz w:val="26"/>
                  <w:color w:val="047857"/>
                </w:rPr>
                <w:t>{xml_escape(subtitle_text)}</w:t>
              </w:r>
            </w:p>'''
            self.body_elements.append(p_sub)

        if meta_text:
            p_meta = f'''<w:p>
              <w:pPr>
                <w:jc w:val="center"/>
                <w:pBdr>
                  <w:bottom w:val="single" w:sz="12" w:space="8" w:color="A7F3D0"/>
                </w:pBdr>
                <w:spacing w:before="60" w:after="360"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                  <w:sz w:val="18"/>
                  <w:color w:val="6B7280"/>
                </w:rPr>
                <w:t>{xml_escape(meta_text)}</w:t>
              </w:r>
            </w:p>'''
            self.body_elements.append(p_meta)

    def add_heading_1(self, text):
        p = f'''<w:p>
          <w:pPr>
            <w:pBdr>
              <w:left w:val="single" w:sz="24" w:space="8" w:color="047857"/>
            </w:pBdr>
            <w:shd w:val="clear" w:color="auto" w:fill="F3FBF7"/>
            <w:spacing w:before="400" w:after="140"/>
            <w:ind w:left="160"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:b/>
              <w:sz w:val="32"/>
              <w:color w:val="064E3B"/>
            </w:rPr>
            <w:t>{xml_escape(text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

    def add_heading_2(self, text):
        p = f'''<w:p>
          <w:pPr>
            <w:spacing w:before="260" w:after="100"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:b/>
              <w:sz w:val="26"/>
              <w:color w:val="047857"/>
            </w:rPr>
            <w:t>{xml_escape(text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

    def add_heading_3(self, text):
        p = f'''<w:p>
          <w:pPr>
            <w:spacing w:before="180" w:after="60"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:b/>
              <w:sz w:val="22"/>
              <w:color w:val="111827"/>
            </w:rPr>
            <w:t>{xml_escape(text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

    def add_paragraph(self, text, bold_prefix=None):
        r_prefix = ""
        if bold_prefix:
            r_prefix = f'''<w:r>
              <w:rPr>
                <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                <w:b/>
                <w:sz w:val="21"/>
                <w:color w:val="064E3B"/>
              </w:rPr>
              <w:t xml:space="preserve">{xml_escape(bold_prefix)} </w:t>
            </w:r>'''
        p = f'''<w:p>
          <w:pPr>
            <w:spacing w:before="40" w:after="100" w:line="280" w:lineRule="auto"/>
          </w:pPr>
          {r_prefix}
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:sz w:val="21"/>
              <w:color w:val="1F2937"/>
            </w:rPr>
            <w:t>{xml_escape(text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

    def add_bullet(self, text, bold_prefix=None, level=1):
        indent = level * 360
        r_prefix = ""
        if bold_prefix:
            r_prefix = f'''<w:r>
              <w:rPr>
                <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                <w:b/>
                <w:sz w:val="21"/>
                <w:color w:val="047857"/>
              </w:rPr>
              <w:t xml:space="preserve">{xml_escape(bold_prefix)} </w:t>
            </w:r>'''
        bullet_char = "•  " if level == 1 else "–  "
        p = f'''<w:p>
          <w:pPr>
            <w:ind w:left="{indent}" w:hanging="220"/>
            <w:spacing w:before="20" w:after="60" w:line="260" w:lineRule="auto"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:b/>
              <w:color w:val="10B981"/>
            </w:rPr>
            <w:t>{bullet_char}</w:t>
          </w:r>
          {r_prefix}
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:sz w:val="21"/>
              <w:color w:val="1F2937"/>
            </w:rPr>
            <w:t>{xml_escape(text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

    def add_callout(self, text, title=None, callout_type="emerald"):
        bg_color = "E4F7EE" if callout_type == "emerald" else "FEF3C7"
        border_color = "047857" if callout_type == "emerald" else "D97706"
        title_color = "064E3B" if callout_type == "emerald" else "92400E"

        title_run = ""
        if title:
            title_run = f'''<w:r>
              <w:rPr>
                <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                <w:b/>
                <w:sz w:val="22"/>
                <w:color w:val="{title_color}"/>
              </w:rPr>
              <w:t>{xml_escape(title)}</w:t>
              <w:br/>
            </w:r>'''

        p = f'''<w:p>
          <w:pPr>
            <w:pBdr>
              <w:left w:val="single" w:sz="36" w:space="12" w:color="{border_color}"/>
            </w:pBdr>
            <w:shd w:val="clear" w:color="auto" w:fill="{bg_color}"/>
            <w:spacing w:before="120" w:after="160"/>
            <w:ind w:left="200" w:right="200"/>
          </w:pPr>
          {title_run}
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
              <w:sz w:val="20"/>
              <w:color w:val="111827"/>
            </w:rPr>
            <w:t>{xml_escape(text)}</w:t>
          </w:r>
        </w:p>'''
        self.body_elements.append(p)

    def add_code_block(self, code_text):
        lines = code_text.split('\n')
        for i, line in enumerate(lines):
            space_attr = ' xml:space="preserve"' if line.startswith(' ') or line.endswith(' ') else ''
            before_sp = "60" if i == 0 else "0"
            after_sp = "80" if i == len(lines)-1 else "0"
            p = f'''<w:p>
              <w:pPr>
                <w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/>
                <w:pBdr>
                  <w:left w:val="single" w:sz="12" w:space="8" w:color="CBD5E1"/>
                </w:pBdr>
                <w:spacing w:before="{before_sp}" w:after="{after_sp}"/>
                <w:ind w:left="180"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                  <w:sz w:val="18"/>
                  <w:color w:val="0F172A"/>
                </w:rPr>
                <w:t{space_attr}>{xml_escape(line)}</w:t>
              </w:r>
            </w:p>'''
            self.body_elements.append(p)

    def add_divider(self):
        p = '''<w:p>
          <w:pPr>
            <w:pBdr>
              <w:bottom w:val="single" w:sz="8" w:space="12" w:color="E2E8F0"/>
            </w:pBdr>
            <w:spacing w:before="200" w:after="200"/>
          </w:pPr>
        </w:p>'''
        self.body_elements.append(p)

    def build_docx(self, output_path):
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

        document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {''.join(self.body_elements)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', content_types)
            z.writestr('_rels/.rels', rels)
            z.writestr('word/document.xml', document_xml)

def generate_full_master_document(docx_path):
    builder = DocxBuilder()

    # Document Header
    builder.add_title(
        "FOUNDER FOR FOUNDER (f4f)",
        subtitle_text="Master System Specification & AI Rebuild Prompt",
        meta_text="Version 3.3 • Powered by snalts.co • Enterprise Full-Stack Blueprint with Attendance, 1:1 Meetings, 16:9 Steady Photo Slider & 12-Question Admissions Architecture"
    )

    builder.add_callout(
        "This master document consolidates every architectural decision, visual design constraint, database schema, API endpoint, dynamic CMS requirement, copy deck, monthly attendance accountability engine, founder 1-to-1 meeting tracking framework, official social profile ecosystem, 16:9 steady right-to-left meeting photos slider, 12-question admissions questionnaire with multi-select collaboration options, and ultra-dynamic animated frontend built for the Founder for Founder community platform. Any senior software engineer or AI coding assistant can ingest this specification to reconstruct the identical, fully functional production system from scratch.",
        title="EXECUTIVE SUMMARY & SYSTEM SCOPE",
        callout_type="emerald"
    )

    # SECTION 1
    builder.add_heading_1("SECTION 1: THE MASTER AI RECONSTRUCTION PROMPT")
    builder.add_paragraph(
        "Use the following master instruction prompt verbatim when commanding an AI agent to regenerate the entire website and backend server:"
    )

    master_prompt_text = """Act as an elite Principal Full-Stack Engineer, Product Architect, and UI/UX Designer.
Build a complete, standalone, production-ready community and collaboration platform for "Founder for Founder" (powered by snalts.co) — a vetted, high-trust network of ambitious startup founders and scale-up leaders across India.

The solution must be fully self-contained in a single project directory with zero complex build tools or heavy framework overhead. Use a clean, robust Python 3 standard library HTTP backend with SQLite database persistence, paired with a modern Vanilla HTML5, CSS3, and JavaScript Single Page Application (SPA).

KEY SYSTEM MANDATES:
1. STRICT DESIGN SYSTEM:
   - Palette: Deep Forest Emerald (#064E3B, #047857), Mint accents (#10B981, #34D399, #A7F3D0), Warm Mint Tint (#F3FBF7, #E4F7EE), Deep Ink (#0B0F0D).
   - Rich Gradients: Replace flat colors with emerald gradients (linear-gradient(135deg, #064E3B 0%, #047857 50%, #059669 100%)) on banner highlights, counter strips, and key CTA accents.
   - Typography: 'DM Serif Display' for headings, 'Plus Jakarta Sans' for body and interface elements.
   - ABSOLUTE PROHIBITION OF ITALIC/SLANTED TEXT: All text must be strictly upright ('font-style: normal !important;'). Never use slanted or italic styling anywhere.
   - Button Corners: Strict 6px corner radius ('border-radius: 6px !important;'). Never use pill-shaped rounded-full buttons.
   - High-Contrast Hero Banner: Prominent background photography with high-contrast text and directional scrim for perfect readability.
   - NO BOXES OVER CARD PHOTOS: In 'Ways We Collaborate', 'Core Philosophy', 'Curated Experiences', and 'Meeting Photos', photos must never be covered by opaque, frosted, or tinted rectangular boxes. Content sits directly over the imagery with a subtle bottom gradient shadow and high-contrast dual text-shadows (0 2px 4px rgba(0,0,0,0.8), 0 4px 12px rgba(0,0,0,0.6)).
   - Card Badges: Crisp Mint Emerald (#A7F3D0) headers with subtle luminous glow, ensuring high contrast against dark photography.

2. BUSINESS PROOF STRIP & MARQUEE:
   - Live verified counters: '1,528+ Verified Founders & Operators', '27 Curated Gatherings & Private Experiences', '4.9/5 Peer Trust Rating'.
   - DO NOT display 'verified business generated' metric on the public landing strip.
   - Display a dedicated heading: 'Businesses Connected With Us' positioned immediately above the continuously scrolling horizontal brand marquee strip.

3. DYNAMIC MEDIA & CONTENT MANAGEMENT SYSTEM (CMS):
   - Every single image on the website must be editable dynamically through an Admin CMS:
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

4. ATTENDANCE TRACKER & MONTHLY ACCOUNTABILITY:
   - Built-in monthly attendance tracker to monitor members' presence across all curated gatherings and private sessions hosted in any month.
   - Monthly selector dropdown (e.g., October 2026, September 2026, August 2026) with automatic KPI calculations:
     * Monthly Attendance Rate %: calculated accurately against *completed* events in that calendar month.
     * Events Attended vs Hosted count.
     * Consecutive Gathering Streak tracker.
     * Dynamic Progress Bar: visual color-coded progress indicator (Emerald for >=80%, Amber for 50-79%, Coral for <50%).
   - Event Presence Table: Complete list of monthly events with date, city, venue format, status badge (PRESENT, UPCOMING, MISSED), and verified check-in timestamp.
   - Host PIN Check-In System: Modal allowing attendees to enter the 6-digit Host Event Code (e.g., 'F4F2026') upon arrival at the venue to instantly record presence and mark status as PRESENT.
   - Admin Manual Override: Admin endpoint ('POST /api/admin/events/attendance') to manually verify or update member attendance.

5. FOUNDER 1-TO-1 MEETINGS TRACKER:
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

6. CURATED MEETING PHOTOS SLIDER (16:9 ASPECT RATIO & STEADY RIGHT-TO-LEFT MOTION):
   - Completely remove the former "As Seen on Instagram and Media" section.
   - Replace it with a dedicated Curated Meeting Photos Showcase featuring:
     * Continuous Right-to-Left Sliding Motion: The slider moves steadily from right to left using `@keyframes slideRightToLeft { from { transform: translateX(0); } to { transform: translateX(-50%); } }` with linear timing, smoothly pausing on mouse hover for comfortable reading.
     * Strict 16:9 Aspect Ratio: Every meeting photo card and image strictly enforces `aspect-ratio: 16 / 9;` (`object-fit: cover;`) for a uniform, cinematic, distortion-free presentation.
     * Direct Photography & Contrast: Format pill tags ('Closed-Door Salon', 'Founder Dinner', '1:1 Meeting', 'Mastermind', 'Experiential', 'Founder Retreat'), meeting titles, captions, and dates sit over subtle bottom gradient shadow scrims with dual text shadows. No obscuring frosted boxes.
     * Provision to Add & Manage Meeting Photos:
       - Public Landing Page is kept clean, uncluttered, and pristine with the 'Add Meeting Photo' button removed from the home page.
       - Administrators add and manage meeting photos directly inside the Admin Dashboard via a quick in-card upload form or admin modal with live 16:9 preview, format tag dropdown, title, caption, date, URL input, and file upload.
       - Admin Console Gallery card provides thumbnail inspection and instant photo deletion.
     * SQLite Persistence: Managed in `event_gallery` table (`id`, `title`, `caption`, `image_url`, `event_date`, `tag`, `display_order`, `is_active`).

7. OFFICIAL SOCIAL PROFILES FOOTER INTEGRATION:
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

8. 12-POINT COMPREHENSIVE ADMISSIONS QUESTIONNAIRE (SHOW INTEREST FUNNEL):
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

9. ULTRA-DYNAMIC & ANIMATED FRONTEND UI:
   - Fluid micro-interactions and smooth hardware-accelerated animations across the entire application:
     * CSS Keyframes: '@keyframes slideRightToLeft' for continuous steady meeting photo sliding; '@keyframes emeraldPulse' for live indicators; '@keyframes tabSlideIn' for seamless tab switching; '@keyframes floatSmooth' for hero floating cards.
     * Micro-Elevations: Cards and interactive modules elevate smoothly on hover ('transform: translateY(-4px); box-shadow: 0 12px 28px rgba(6,78,59,0.15)').
     * Button State Feedback: Subtle press bounce ('active: scale(0.98)'), smooth gradient transition, and luminous borders.
     * Dynamic Progress Visuals: Animated fill-up bars for attendance metrics and meeting synergy scores.
     * Zero page reload delays: Instant DOM updates and seamless modal dialogs with backdrop blur.

10. FULL PLATFORM FUNCTIONALITY & SELF-HEALING BACKEND:
   - Public Landing Page: Hero with dual CTAs, capsule collage, live counters strip, 'Businesses Connected With Us' marquee, 4 Core Philosophy cards, 5 Ways We Collaborate pillars, 6-step How It Works timeline, 6-tab interactive Feature Showcase, Upcoming Gatherings grid with seat reservations, Curated Meeting Photos 16:9 steady slider, FAQ accordion, footer with official social profile squares.
   - Admissions Hub: 12-question application modal, OTP verification capability, and instant database submission.
   - Admin Console: Application review table with full inspector modal, Site Settings Editor, Media Manager, Meeting Photos Manager.
   - Member Portal: Authenticated workspace featuring Member Directory, Needs & Wants Engine, Referral CRM, Private Gatherings RSVP, Monthly Attendance Tracker, and Founder 1:1 Meetings Tracker."""

    builder.add_code_block(master_prompt_text)
    builder.add_divider()

    # SECTION 2
    builder.add_heading_1("SECTION 2: BRAND IDENTITY & STRATEGIC POSITIONING")
    builder.add_paragraph("Founder for Founder (f4f) is a curated, high-trust closed-loop ecosystem designed for active venture-backed and profitable bootstrapped founders across India.", bold_prefix="Brand Essence:")
    builder.add_paragraph("Powered by snalts.co — an ecosystem builder driving peer-to-peer founder leverage.", bold_prefix="Parentage:")
    builder.add_paragraph("Not an open networking forum, generic coworking directory, or noisy WhatsApp group. It operates on mutual peer accountability, zero sales pitch tolerance, radical transparency, and tangible deal flow.", bold_prefix="Positioning:")
    
    builder.add_heading_2("Verified Public Community Metrics")
    builder.add_bullet("1,528+ Verified Founders & Operators across 12+ tech and industrial sectors.")
    builder.add_bullet("27 Curated Gatherings & Private Experiences executed to date.")
    builder.add_bullet("4.9 / 5.0 Peer Trust & Collaboration Score across closed pods.")
    builder.add_bullet("Strict Rule: Public counters strip must NOT mention 'verified business generated' to avoid sounding like a commercial lead agency.")

    builder.add_heading_2("Official Social Media Profiles")
    builder.add_bullet("LinkedIn Company Page: https://www.linkedin.com/company/founder-for-founder/")
    builder.add_bullet("Instagram Official Channel: https://www.instagram.com/founder_for_founder")
    builder.add_bullet("Facebook Community Handle: https://www.facebook.com/share/19ZnPNuhPb/")

    builder.add_heading_2("Section Headings & Eyebrows")
    builder.add_bullet("Brand Strip Header: 'Businesses Connected With Us' placed prominently above the scrolling brand marquee.")
    builder.add_bullet("Core Philosophy Eyebrow: 'FOUNDATION • UNCOMPROMISING PRINCIPLES'")
    builder.add_bullet("Ways We Collaborate Eyebrow: 'CURATED ENGAGEMENT • HIGH SIGNAL'")
    builder.add_bullet("How It Works Eyebrow: 'VETTED ADMISSION • SELECTIVE ONBOARDING'")
    builder.add_bullet("Platform Features Eyebrow: 'MEMBER PORTAL • PRIVATE ARCHITECTURE'")
    builder.add_bullet("Curated Meeting Photos Eyebrow: 'FOUNDER INTERACTIONS • MOMENTS OF LEVERAGE' (Section: 'Curated Founder Gatherings & Meeting Moments')")
    builder.add_bullet("Attendance Tracker Eyebrow: 'MEMBER ACCOUNTABILITY • MONTHLY PRESENCE'")
    builder.add_bullet("1:1 Meetings Tracker Eyebrow: 'PEER CONNECTIONS • SYNERGY ACCELERATOR'")

    builder.add_divider()

    # SECTION 3
    builder.add_heading_1("SECTION 3: STRICT DESIGN SYSTEM, ANIMATIONS & VISUAL SPECIFICATION")
    builder.add_callout(
        "Adherence to these visual guidelines is mandatory. Deviations ruin the sophisticated, executive tone of the platform.",
        title="DESIGN SYSTEM GUARDRAILS",
        callout_type="amber"
    )

    builder.add_heading_2("1. Color Palette Tokens")
    builder.add_bullet("--emerald-950: #042F2C (Ultra deep forest foundation)")
    builder.add_bullet("--emerald-900: #064E3B (Primary dark brand accent)")
    builder.add_bullet("--emerald-800: #065F46 (Card headers and active tab backgrounds)")
    builder.add_bullet("--emerald-700: #047857 (Primary interactive elements and buttons)")
    builder.add_bullet("--emerald-600: #059669 (Button hover and secondary accents)")
    builder.add_bullet("--emerald-500: #10B981 (Luminous green accent and live status badges)")
    builder.add_bullet("--emerald-400: #34D399 (Card hover borders and subtle glow outlines)")
    builder.add_bullet("--emerald-200: #A7F3D0 (Card format badges and pill text for maximum contrast)")
    builder.add_bullet("--emerald-100: #C9EFDD (Subtle container outlines)")
    builder.add_bullet("--emerald-50:  #E4F7EE (Pill badge backgrounds and light card fills)")
    builder.add_bullet("--bg-light:     #F3FBF7 (Soft mint tinted body background)")
    builder.add_bullet("--text-main:    #0B0F0D (Deep ink primary copy)")
    builder.add_bullet("--text-muted:   #4B5563 (Balanced neutral secondary copy)")

    builder.add_heading_2("2. Strict Gradient Specifications")
    builder.add_paragraph("Replace flat, solid color blocks with luxurious emerald gradients:")
    builder.add_bullet("Primary Brand Gradient: linear-gradient(135deg, #064E3B 0%, #047857 50%, #059669 100%)")
    builder.add_bullet("Hero Scrim Gradient: linear-gradient(180deg, rgba(6,78,59,0.78) 0%, rgba(4,120,87,0.85) 100%)")
    builder.add_bullet("Card Bottom Shadow Scrim: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(6,78,59,0.5) 45%, rgba(0,0,0,0.92) 100%)")
    builder.add_bullet("Soft Mint Card Accent: linear-gradient(145deg, #FFFFFF 0%, #F3FBF7 100%)")

    builder.add_heading_2("3. Typography & Anti-Italic Rules")
    builder.add_bullet("Heading Font: 'DM Serif Display', Georgia, serif — Used for all H1, H2, H3, H4 titles.")
    builder.add_bullet("Body & UI Font: 'Plus Jakarta Sans', system-ui, sans-serif — Used for buttons, forms, paragraphs, navigation.")
    builder.add_bullet("CRITICAL RULE — ZERO SLANTED TEXT: Ensure font-style: normal !important; is globally applied across * { font-style: normal !important; }. Neither headings nor captions may ever appear in italics.")

    builder.add_heading_2("4. Corner Radius & Button Architecture")
    builder.add_bullet("Corner Radius: Strictly 6px border radius (border-radius: 6px !important;) on all primary buttons, secondary buttons, inputs, and tab selectors.")
    builder.add_bullet("DO NOT use pill buttons (border-radius: 9999px) for primary actions.")
    builder.add_bullet("Large Cards: 12px border radius with subtle 1px border (#E4F7EE) and multi-layer box shadows.")

    builder.add_heading_2("5. Card Overlay Rules (NO BOXES OVER PHOTOS)")
    builder.add_paragraph("In sections featuring photographic backgrounds ('Ways We Collaborate', 'Core Philosophy', 'Curated Experiences', 'Meeting Photos'):")
    builder.add_bullet("NO FROSTED GLASS BOXES: Never place opaque, tinted, or frosted rectangular cards over the photos.")
    builder.add_bullet("DIRECT TYPOGRAPHY: The title, format badge, and description sit directly on the photo background.")
    builder.add_bullet("DUAL-LAYER TEXT SHADOW: Apply text-shadow: 0 2px 4px rgba(0,0,0,0.85), 0 4px 12px rgba(0,0,0,0.6) so copy is razor-sharp against any photo background.")
    builder.add_bullet("BADGE STYLING: Badges (.format-badge) use luminous Mint Emerald (#A7F3D0) text on translucent dark emerald backgrounds (rgba(6,78,59,0.75)) with 1px border (#10B981) and glowing box-shadow.")

    builder.add_heading_2("6. Curated Meeting Photos 16:9 Steady Slider Architecture")
    builder.add_paragraph("Replaces the old 'As Seen on Instagram and Media' section with an authentic showcase of real founder interactions:")
    builder.add_bullet("Strict 16:9 Aspect Ratio: Cards enforce aspect-ratio: 16 / 9; with width: 440px (desktop) or width: 320px (mobile). Inner images enforce object-fit: cover and 100% dimensions, eliminating distortion.")
    builder.add_bullet("Steady Right-to-Left Continuous Slide: Powered by @keyframes slideRightToLeft { from { transform: translateX(0); } to { transform: translateX(-50%); } }. The track duplicates the photo items in JavaScript to ensure an uninterrupted, seamless loop without white gaps.")
    builder.add_bullet("Linear Non-Stop Speed: Slower, steady 85s linear infinite duration (animation: slideRightToLeft 85s linear infinite;).")
    builder.add_bullet("Hover Pause: Pauses smoothly on hover (:hover { animation-play-state: paused; }) allowing founders to read titles, dates, and captions comfortably.")
    builder.add_bullet("Slider Edge Masking: The slider wrapper features edge masks using mask-image: linear-gradient(to right, transparent, black 4%, black 96%, transparent) for a smooth aesthetic fade at the screen margins.")
    builder.add_bullet("Direct Caption Scrim: Captions sit over linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(6,78,59,0.4) 40%, rgba(0,0,0,0.92) 100%) with dual text shadows.")
    builder.add_bullet("Pristine Executive Presentation: The home page header is cleanly centered with zero public action buttons; meeting photo management is strictly controlled via the Admin Dashboard to maintain brand curation and security.")

    builder.add_heading_2("7. Official Social Profile Component Specifications (Footer Only)")
    builder.add_bullet("Removed from Header & Hero: Social buttons are completely removed from the navbar and hero banner to keep focus on membership action and value proposition.")
    builder.add_bullet("Footer Integration: Placed in the 'Official Profiles' column of the home page footer.")
    builder.add_bullet("Geometry: Exactly square 44x44px buttons with slight curves (border-radius: 8px !important;).")
    builder.add_bullet("Theme Cohesion: Styled in website emerald colors — deep emerald glass background (rgba(6, 78, 59, 0.75)), 1px emerald border (#059669), and mint icons (#A7F3D0).")
    builder.add_bullet("Hover Micro-Interactions: Elevates by -3px (scale 1.06), transitions into linear-gradient(135deg, #047857, #059669) with #34D399 border glow and crisp white SVG icon.")
    builder.add_bullet("Minimalist Presentation: Strictly display the platform SVG logos (Instagram, Facebook, LinkedIn) without accompanying text labels.")

    builder.add_heading_2("8. Dynamic Form & Choice Card Styling (.collab-choice-grid)")
    builder.add_paragraph("The Show Interest application modal implements responsive multi-column layouts and interactive selection cards:")
    builder.add_bullet("Modal Dimensions: Expanded width (max-width: 780px) with responsive two-column (.form-row-2) and three-column (.form-row-3) grid groupings.")
    builder.add_bullet("Section Dividers: Numbered badge pills (.form-section-tag) and uppercase subheadings (.form-section-title) separating applicant identity, business operations, web links, value exchange, and connection choices.")
    builder.add_bullet("Choice Cards (.collab-choice-card): Flex cards featuring styled emerald checkboxes, bold titles, and subtext descriptions that highlight on hover and focus.")

    builder.add_heading_2("9. Dynamic Animation & Keyframe Specifications")
    builder.add_paragraph("Enhance user immersion through performant CSS keyframes:")
    builder.add_bullet("@keyframes slideRightToLeft: from { transform: translateX(0); } to { transform: translateX(-50%); } — Applied to the meeting photos slider track.")
    builder.add_bullet("@keyframes emeraldPulse: 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.4); } 70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } — Applied to live status pills and active check-in indicators.")
    builder.add_bullet("@keyframes tabSlideIn: from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } — Applied on portal tab switching for silky transitions.")
    builder.add_bullet("@keyframes floatSmooth: 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } — Applied to hero floating status capsules.")
    builder.add_bullet("Interactive Hover Elevation: Cards smoothly lift by -4px with transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1).")

    builder.add_divider()

    # SECTION 4
    builder.add_heading_1("SECTION 4: SYSTEM ARCHITECTURE & CODEBASE STRUCTURE")
    builder.add_paragraph("The application operates without complex npm build pipelines, Webpack/Vite bundlers, or third-party database dependencies. It runs directly via standard Python 3 and native browser APIs.")

    structure_tree = """Founder_for_Founder_Project/
├── server.py                  # Zero-dependency Python 3 HTTP Server & REST API router
├── database.py                # SQLite database manager, schema migrations & seed records
├── f4f_community.db           # SQLite database file (auto-initialized)
├── public/
│   ├── index.html             # Single Page Application entrypoint (Semantic HTML5)
│   ├── css/
│   │   └── styles.css         # Complete responsive design system, variables & animations
│   ├── js/
│   │   └── app.js             # Client SPA controller, dynamic image hydration, CMS, Attendance & Meetings
│   └── assets/
│       ├── images/            # Static brand assets & fallback photography
│       └── uploads/           # Server-side upload directory for dynamic CMS images
└── README.md                  # Setup & operational manual"""

    builder.add_code_block(structure_tree)

    builder.add_heading_2("Key Execution Requirements")
    builder.add_bullet("Command to run: 'python server.py'")
    builder.add_bullet("Default port: 8000 (accessible via http://localhost:8000)")
    builder.add_bullet("Persistent storage: Database creates f4f_community.db on first boot and automatically applies migrations and seeds without overwriting user-updated CMS settings.")
    builder.add_bullet("Uploads endpoint: Writes uploaded files to public/assets/uploads/ and serves them statically at /assets/uploads/<filename>.")

    builder.add_divider()

    # SECTION 5
    builder.add_heading_1("SECTION 5: COMPLETE SQLITE DATABASE SCHEMA")
    builder.add_paragraph("The database schema encompasses users, profiles, vetted applications, dynamic CMS settings, needs/wants, referrals, events, attendance records, founder 1:1 meetings, meeting gallery photos, and leaderboard points.")

    schema_sql = """-- 1. USERS & AUTHENTICATION
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'member', 'guest')) DEFAULT 'member',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. MEMBER PROFILES
CREATE TABLE IF NOT EXISTS member_profiles (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    company_name TEXT NOT NULL,
    designation TEXT NOT NULL,
    industry TEXT NOT NULL,
    stage TEXT NOT NULL,
    city TEXT NOT NULL,
    bio TEXT,
    linkedin_url TEXT,
    website TEXT,
    avatar_url TEXT,
    verified_status INTEGER DEFAULT 1,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. MEMBERSHIP APPLICATIONS & COMPREHENSIVE ONBOARDING
CREATE TABLE IF NOT EXISTS applications (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    applicant_type TEXT NOT NULL DEFAULT 'Founder',
    designation TEXT NOT NULL,
    city TEXT NOT NULL DEFAULT 'Pan India',
    business_name TEXT NOT NULL,
    business_model_category TEXT, -- 'Product Based', 'Service Based', 'Manufacturing', 'Hybrid', 'Other'
    firm_type TEXT, -- 'Private Limited', 'LLP', 'Partnership', 'Sole Proprietorship', 'Public Limited', 'OPC', 'Other'
    years_in_business TEXT,
    team_size TEXT,
    business_category TEXT NOT NULL,
    business_stage TEXT DEFAULT 'Established',
    business_description TEXT NOT NULL,
    website TEXT,
    linkedin TEXT,
    instagram TEXT,
    what_offer TEXT,
    what_need TEXT,
    collaboration_preferences TEXT, -- Multi-select values joined by comma
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

-- 4. DYNAMIC SYSTEM SETTINGS & MEDIA CMS
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. NEEDS & WANTS ENGINE
CREATE TABLE IF NOT EXISTS needs_wants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('need', 'want')) NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    urgency TEXT CHECK(urgency IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
    status TEXT CHECK(status IN ('open', 'in_progress', 'fulfilled', 'closed')) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. NEED RESPONSES & THREADS
CREATE TABLE IF NOT EXISTS need_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    need_id INTEGER NOT NULL,
    responder_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(need_id) REFERENCES needs_wants(id) ON DELETE CASCADE,
    FOREIGN KEY(responder_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 7. REFERRALS & DEALS CRM
CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_id INTEGER NOT NULL,
    referee_name TEXT NOT NULL,
    referee_company TEXT NOT NULL,
    deal_title TEXT NOT NULL,
    description TEXT,
    estimated_value TEXT,
    status TEXT CHECK(status IN ('intro_made', 'in_discussion', 'proposal_sent', 'deal_closed', 'passed')) DEFAULT 'intro_made',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(referrer_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 8. GATHERINGS & EXPERIENCES
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    event_date TEXT NOT NULL,
    location TEXT NOT NULL,
    city TEXT DEFAULT 'Bengaluru',
    google_maps_url TEXT,
    venue_type TEXT CHECK(venue_type IN ('in_person', 'virtual')) DEFAULT 'in_person',
    max_capacity INTEGER DEFAULT 12,
    price_amount REAL DEFAULT 0.0,
    what_is_included TEXT,
    checkin_code TEXT DEFAULT 'F4F2026',
    image_url TEXT,
    status TEXT DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. EVENT RSVPS
CREATE TABLE IF NOT EXISTS event_rsvps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rsvp_status TEXT DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id),
    FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 10. EVENT ATTENDANCE TRACKER
CREATE TABLE IF NOT EXISTS event_attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('PRESENT', 'ABSENT', 'EXCUSED')) DEFAULT 'PRESENT',
    checkin_method TEXT DEFAULT 'HOST_PIN',
    checkin_notes TEXT,
    attended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id),
    FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 11. FOUNDER 1-TO-1 MEETINGS TRACKER
CREATE TABLE IF NOT EXISTS one_on_one_meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_user_id INTEGER NOT NULL,
    partner_user_id INTEGER,
    partner_name TEXT NOT NULL,
    partner_company TEXT NOT NULL,
    meeting_date TEXT NOT NULL,
    meeting_type TEXT CHECK(meeting_type IN ('in_person', 'virtual', 'coffee', 'dinner')) DEFAULT 'in_person',
    agenda TEXT NOT NULL,
    collaboration_outcome TEXT,
    synergy_rating INTEGER DEFAULT 5,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(host_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 12. CURATED MEETING PHOTOS GALLERY (16:9 SLIDER)
CREATE TABLE IF NOT EXISTS event_gallery (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    caption TEXT,
    image_url TEXT NOT NULL,
    event_date TEXT,
    tag TEXT DEFAULT 'Curated Meeting',
    display_order INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. FOUNDERS COLLECTIVE CHAT MESSAGES
CREATE TABLE IF NOT EXISTS community_chat_messages (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'collective',
    message TEXT NOT NULL,
    reply_to_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 14. LEADERBOARD & REPUTATION
CREATE TABLE IF NOT EXISTS leaderboard (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0,
    referrals_given INTEGER DEFAULT 0,
    needs_resolved INTEGER DEFAULT 0,
    events_attended INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);"""

    builder.add_code_block(schema_sql)
    builder.add_divider()

    # SECTION 6
    builder.add_heading_1("SECTION 6: BACKEND SERVER & REST API SPECIFICATIONS")
    builder.add_paragraph("The backend server (`server.py`) extends `http.server.BaseHTTPRequestHandler` to provide a full REST API and static file serving with CORS and JSON responses.")

    builder.add_heading_2("Public Endpoints")
    builder.add_bullet("GET /api/public/content — Returns site metadata, live counters, dynamic image URLs from 'system_settings', published events, and curated meeting_photos.")
    builder.add_bullet("POST /api/public/show-interest — Accepts comprehensive 12-question application payload:")
    builder.add_bullet("  - full_name, email, phone, whatsapp, applicant_type, designation, city", level=2)
    builder.add_bullet("  - business_name, business_model_category (Product/Service/Mfg), firm_type, years_in_business, team_size, business_category, business_stage, business_description", level=2)
    builder.add_bullet("  - website, linkedin, instagram (optional links)", level=2)
    builder.add_bullet("  - what_offer (contribution superpower), what_need (asks & bottlenecks)", level=2)
    builder.add_bullet("  - collaboration_preferences (array/comma-separated connection choices)", level=2)
    builder.add_bullet("  - why_join, consent_given", level=2)
    builder.add_bullet("  - Returns { success: true, application_id } and logs audit entry.", level=2)
    builder.add_bullet("POST /api/public/verify-otp — Verifies submitted OTP against application record; marks status as 'otp_verified'.")
    builder.add_bullet("POST /api/auth/login — Validates user email & password; returns auth session token, user details, and role.")

    builder.add_heading_2("Curated Meeting Photos Endpoints (16:9 Steady Slider)")
    builder.add_bullet("GET /api/meeting-photos — Returns active meeting photos from 'event_gallery' sorted by display_order ASC.")
    builder.add_bullet("POST /api/meeting-photos — Direct admin photo addition endpoint. Accepts { title, caption, tag, image_url, event_date }. Generates unique UUID, persists photo in 'event_gallery', and returns created photo record. Also supports direct Base64 file uploads via /api/admin/upload-image.")
    builder.add_bullet("POST /api/meeting-photos/delete — Accepts { id } or DELETE via /api/meeting-photos/delete/<id>. Deletes or deactivates the meeting photo from the gallery.")

    builder.add_heading_2("Founders Collective Chat Endpoints (Active Membership Gated)")
    builder.add_bullet("GET /api/chat/messages?channel=<name> — Authenticated & Membership Gated. Verifies member has an active subscription (memberships.status == 'ACTIVE') or has role 'ADMIN'. If not active, returns 403 Forbidden with { has_membership: false, message: 'Exclusive to active members' } to trigger frontend gatecard. If active, returns last 100 messages joined with member profile name, business name, and avatar.")
    builder.add_bullet("POST /api/chat/messages — Authenticated & Membership Gated. Accepts { channel, message, reply_to_id }. Validates active membership, stores message in 'community_chat_messages', and returns created message with sender metadata.")

    builder.add_heading_2("Attendance Tracker Endpoints")
    builder.add_bullet("GET /api/attendance/summary?month=YYYY-MM — Returns monthly attendance statistics for the member:")
    builder.add_bullet("  - selected_month: 'YYYY-MM' format (e.g. '2026-10')", level=2)
    builder.add_bullet("  - month_name: Full display label (e.g. 'October 2026')", level=2)
    builder.add_bullet("  - total_events: Count of all hosted gatherings in target month", level=2)
    builder.add_bullet("  - completed_events: Events that have already taken place", level=2)
    builder.add_bullet("  - events_attended: Count of events where member status is 'PRESENT'", level=2)
    builder.add_bullet("  - attendance_rate: Attendance percentage based on completed events (e.g. 100%)", level=2)
    builder.add_bullet("  - attendance_streak: Consecutive gatherings attended count", level=2)
    builder.add_bullet("  - accountability_tier: Member trust status tier (e.g. 'Tier 1: High-Signal Founder')", level=2)
    builder.add_bullet("  - events: Array of monthly events with date, city, venue format, attendance status ('PRESENT', 'UPCOMING', 'MISSED', 'RSVP_CONFIRMED'), checkin code, and timestamp.", level=2)
    builder.add_bullet("POST /api/events/checkin — Accepts { event_id, pin_code, notes }. Validates host PIN (matches event 'checkin_code' or global 'F4F2026'). Records attendance record in 'event_attendance' with status='PRESENT', marks event_rsvps, and returns success confirmation.")
    builder.add_bullet("POST /api/admin/events/attendance — Admin override endpoint: accepts { event_id, user_id, status } to manually mark a member as PRESENT, ABSENT, or EXCUSED.")

    builder.add_heading_2("Founder 1-to-1 Meetings Endpoints")
    builder.add_bullet("GET /api/founder-meetings — Returns list of logged 1:1 meetings for authenticated user, ordered by meeting_date DESC, along with summary KPIs:")
    builder.add_bullet("  - total: Total lifetime 1:1 meetings logged", level=2)
    builder.add_bullet("  - this_month: Meetings logged in current calendar month", level=2)
    builder.add_bullet("  - synergies: Count of meetings with tangible collaboration outcomes", level=2)
    builder.add_bullet("  - current_month_name: e.g. 'October 2026'", level=2)
    builder.add_bullet("POST /api/founder-meetings — Accepts { partner_name, partner_company, meeting_date, meeting_type, agenda, collaboration_outcome, synergy_rating, notes }. Validates required fields, persists meeting in SQLite, and returns created meeting object.")

    builder.add_heading_2("Member Portal & Community Endpoints")
    builder.add_bullet("GET /api/members/directory — Returns verified members with search parameters: 'search', 'industry', 'stage', 'city'.")
    builder.add_bullet("GET /api/needs-wants — Returns active asks and offers with filter by 'type' (need/want) and 'urgency'.")
    builder.add_bullet("POST /api/needs-wants — Creates a new need or want linked to the authenticated user.")
    builder.add_bullet("POST /api/needs-wants/:id/respond — Posts a collaboration offer or response to a specific need.")
    builder.add_bullet("GET /api/referrals — Fetches user's referral pipeline, lead status, and estimated deal value.")
    builder.add_bullet("POST /api/referrals — Creates a new referral record.")
    builder.add_bullet("GET /api/events — Returns upcoming curated dinners and roundtables with current RSVP count.")
    builder.add_bullet("POST /api/events/:id/rsvp — Toggles RSVP confirmation for the authenticated user.")
    builder.add_bullet("GET /api/leaderboard — Returns member collaboration rankings, points, and badges.")

    builder.add_heading_2("Admin Management Endpoints (Role: admin)")
    builder.add_bullet("GET /api/admin/dashboard — Returns system KPIs and recent_applications list containing all 12 submitted founder answers.")
    builder.add_bullet("GET /api/admin/applications/:id — Returns single application record for detailed inspection modal.")
    builder.add_bullet("POST /api/admin/applications/:id — Updates status ('SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'INVITED', 'DECLINED', 'WAITLISTED') and generates one-time invite token.")
    builder.add_bullet("GET /api/admin/export/csv?type=applications — Exports full application dataset including Business Model, Firm Type, Years, Team, Links, and Collaboration Choices.")
    builder.add_bullet("GET /api/admin/settings & POST /api/admin/settings — Returns and updates dynamic CMS configuration.")
    builder.add_bullet("POST /api/admin/upload-image — Writes uploaded image to 'public/assets/uploads/' and returns relative URL.")

    builder.add_divider()

    # SECTION 7
    builder.add_heading_1("SECTION 7: DYNAMIC MEDIA & CONTENT MANAGEMENT (CMS)")
    builder.add_paragraph("A core system feature is the capability to modify every image across the platform without editing code, with persistent SQLite storage.")

    builder.add_heading_2("Dynamic Image Slots & Element IDs")
    builder.add_bullet("Hero Banner: id='img-hero-banner' • Background image of main hero section.")
    builder.add_bullet("Brand Logo: id='img-brand-logo' • Navbar branding logo.")
    builder.add_bullet("Capsule 1: id='img-capsule-1' • Founder discussion capsule in hero collage.")
    builder.add_bullet("Capsule 2: id='img-capsule-2' • Executive roundtable capsule in hero collage.")
    builder.add_bullet("Capsule 3: id='img-capsule-3' • Fireside chat capsule in hero collage.")
    builder.add_bullet("Philosophy 1: id='img-phil-1' • 'High-Trust Closed Circles' card photo.")
    builder.add_bullet("Philosophy 2: id='img-phil-2' • 'Unfiltered Playbooks' card photo.")
    builder.add_bullet("Philosophy 3: id='img-phil-3' • 'Reciprocal Deal Flow' card photo.")
    builder.add_bullet("Philosophy 4: id='img-phil-4' • 'Radical Transparency' card photo.")
    builder.add_bullet("Collab Pillar 1: id='img-collab-1' • 'Curated Founders Dinners' card photo.")
    builder.add_bullet("Collab Pillar 2: id='img-collab-2' • 'Closed-Door Mastermind Salons' card photo.")
    builder.add_bullet("Collab Pillar 3: id='img-collab-3' • 'Needs & Wants Engine' card photo.")
    builder.add_bullet("Collab Pillar 4: id='img-collab-4' • 'Peer Advisory Board' card photo.")
    builder.add_bullet("Collab Pillar 5: id='img-collab-5' • 'Annual Founder Retreats' card photo.")
    builder.add_bullet("Feature Tab 1: id='img-feat-needs' • Needs & Wants Matching showcase.")
    builder.add_bullet("Feature Tab 2: id='img-feat-directory' • Verified Directory showcase.")
    builder.add_bullet("Feature Tab 3: id='img-feat-events' • Curated Gatherings showcase.")
    builder.add_bullet("Feature Tab 4: id='img-feat-crm' • Warm Referral CRM showcase.")
    builder.add_bullet("Feature Tab 5: id='img-feat-circles' • Accountability Circles showcase.")
    builder.add_bullet("Feature Tab 6: id='img-feat-perks' • Founder Perks showcase.")
    builder.add_bullet("Meeting Photos Gallery: Managed in 'event_gallery' table and rendered in 16:9 ratio slider.")

    builder.add_heading_2("CMS Architecture & Implementation Flow")
    builder.add_paragraph("1. Database Schema: 'system_settings' table holds key-value pairs (e.g. key='img_collab_1', value='https://images.unsplash.com/...'). 'event_gallery' stores dynamic meeting photos with tags, captions, and 16:9 image URLs.", bold_prefix="Persistence:")
    builder.add_paragraph("2. Backend API: 'GET /api/public/content' merges default images with custom entries stored in SQLite. 'POST /api/admin/settings' saves changes. 'POST /api/admin/upload-image' writes uploaded files to 'public/assets/uploads/' and returns URL.", bold_prefix="API:")
    builder.add_paragraph("3. Client Hydration: In 'app.js', 'applyDynamicContent(content)' updates DOM element attributes ('src' or 'backgroundImage') according to element IDs.", bold_prefix="Hydration:")
    builder.add_paragraph("4. Admin Media Panel: Divided into 5 clear tabs (Hero & Brand, Capsule Collage, Core Philosophy, Ways We Collaborate, Platform Features) plus dedicated Meeting Photos Gallery card with file dropzone, URL text input, and live thumbnail preview.", bold_prefix="Admin UI:")

    builder.add_divider()

    # SECTION 8
    builder.add_heading_1("SECTION 8: PUBLIC LANDING PAGE SECTIONS & UI BREAKDOWN")
    
    sections_list = [
        ("1. Navigation Bar", "Fixed glassmorphism bar with brand badge ('Founder for Founder • powered by snalts.co'), smooth scroll anchor links, 'Sign In' trigger, and 'Apply for Membership' CTA button with emerald glow. (Free of social clutter to maintain high conversion focus)."),
        ("2. Hero Banner & Scrim", "Prominent photographic backdrop with emerald directional scrim. Headline: 'Where India's Ambitious Founders Build, Share & Scale Together'. Subhead emphasizing vetted peer intelligence and mutual leverage. Dual action buttons: 'Apply for Vetted Access' and 'Explore Directory'."),
        ("3. Capsule Collage", "3 floating portrait capsules with live status pills ('1,528+ Verified Members', 'Zero Sales Pitches', 'Closed Pods') exhibiting authentic founder interactions."),
        ("4. Live Proof Counters", "Gradient emerald strip featuring '1,528+ Verified Founders & Operators', '27 Curated Gatherings', and '4.9/5 Peer Trust Rating'. (No mention of 'verified business generated')."),
        ("5. Businesses Connected With Us", "Section label followed by an infinite auto-scrolling horizontal marquee displaying startup logos and brand names connected to the network."),
        ("6. Core Philosophy (4 Cards)", "Grid cards with authentic photography, zero covering boxes, dual-layer text shadows, and luminous mint header badges: 1. High-Trust Closed Circles, 2. Unfiltered Playbooks, 3. Reciprocal Deal Flow, 4. Radical Transparency."),
        ("7. Ways We Collaborate (5 Pillars)", "Full-bleed photographic cards with mint header tags and direct typography: 1. Curated Founders Dinners, 2. Closed-Door Mastermind Salons, 3. Needs & Wants Engine, 4. Peer Advisory Board, 5. Annual Founder Retreats."),
        ("8. How It Works (6-Step Timeline)", "Structured horizontal/vertical progression: 1. Apply Online -> 2. Peer Screening -> 3. Private Induction -> 4. Unlock Needs & Wants -> 5. Attend Dinners -> 6. Compound Mutual Leverage."),
        ("9. Interactive Feature Showcase", "6 tab buttons switching between high-resolution screenshots/visuals and feature bullet breakdowns."),
        ("10. Curated Gatherings Grid", "Upcoming private events with date badges, city location, guest capacity (max 12 seats), and 'Request Seat' action."),
        ("11. Curated Meeting Photos (16:9 Slower Steady Slider)", "Replaces former 'Instagram & Media' section. A dedicated showcase of real founder gatherings sliding slowly and steadily from right to left in a continuous marquee (reduced, relaxed sliding speed with 85s linear infinite duration). Strictly enforced 16:9 aspect ratio cards with mint format tags, titles, captions, dates, and interactive addition directly from the Admin Dashboard as well as via modal."),
        ("12. FAQ Accordion", "Interactive expandable accordions addressing vetting criteria, time commitments, confidentiality, zero spam policy, and membership governance."),
        ("13. Final CTA Band", "High-contrast action banner: 'Your next meaningful business connection starts here' with 'SHOW INTEREST' button."),
        ("14. Comprehensive Footer", "5-column executive footer: Brand identity & mission statement, Navigation links, Contact & Entity, Legal Disclosures, and dedicated 'Official Profiles' column featuring slightly curved square icon buttons (44x44px, 8px radius) matching the emerald theme for Instagram, Facebook, and LinkedIn.")
    ]

    for title, desc in sections_list:
        builder.add_paragraph(desc, bold_prefix=title + ":")

    builder.add_divider()

    # SECTION 9
    builder.add_heading_1("SECTION 9: 12-POINT ADMISSIONS QUESTIONNAIRE & REVIEW WORKFLOW")
    builder.add_paragraph("A high-trust founder community requires thorough vetting of business credibility, scale, alignment, and mutual value exchange. The Show Interest funnel captures all 12 key founder questions:")

    builder.add_heading_2("The 12 Mandated Admissions Questions")
    builder.add_bullet("1. Name of Business — Legal/brand name of the startup or enterprise.", bold_prefix="Q1:")
    builder.add_bullet("2. Brief About Business — Comprehensive description of products, services, value proposition, and customer base.", bold_prefix="Q2:")
    builder.add_bullet("3. Business Being Carried Out From How Many Years? — Track record options: Less than 1 Year, 1-2 Years, 3-5 Years, 5-10 Years, 10+ Years.", bold_prefix="Q3:")
    builder.add_bullet("4. Team Size — Operational scale options: Solo Founder, 2-10 Members, 11-50 Members, 51-200 Members, 200+ Members.", bold_prefix="Q4:")
    builder.add_bullet("5. Type of Firm — Corporate structure options: Private Limited (Pvt Ltd), Limited Liability Partnership (LLP), Partnership Firm, Sole Proprietorship, Public Limited, One Person Company (OPC), Other.", bold_prefix="Q5:")
    builder.add_bullet("6. Business Instagram Link (if any) — Official social channel for brand verification.", bold_prefix="Q6:")
    builder.add_bullet("7. LinkedIn of Founder (if any) — Professional profile URL for peer credentialing.", bold_prefix="Q7:")
    builder.add_bullet("8. Website of Business (if any) — Official digital storefront or SaaS application.", bold_prefix="Q8:")
    builder.add_bullet("9. Category of Business — Core operating model: Product Based, Service Based, Manufacturing, Hybrid (Product & Service), or Other.", bold_prefix="Q9:")
    builder.add_bullet("10. What They Can Contribute — Founder's unique superpower, domain expertise, mentorship, supplier intros, or technical assets.", bold_prefix="Q10:")
    builder.add_bullet("11. What They Are Looking For — Critical bottlenecks, client introductions, fundraising advisory, or scaling playbooks.", bold_prefix="Q11:")
    builder.add_bullet("12. Collaboration & Connection Preferences — Multi-select choice cards allowing applicants to pick how they wish to connect with community members:", bold_prefix="Q12:")
    builder.add_bullet("  - Curated Founders Dinners (Private dining & off-the-record growth talks)", level=2)
    builder.add_bullet("  - Executive Roundtables & Salons (Problem-solving masterminds & playbooks)", level=2)
    builder.add_bullet("  - Sports & Movement (Badminton, Pickleball, Golf, Morning Walks & Fitness)", level=2)
    builder.add_bullet("  - 1-to-1 Founder Coffee Meetings (Strategic deep-dive peer dialogues & mutual intros)", level=2)
    builder.add_bullet("  - Annual Weekend Retreats (3-day immersive offsites, wellness & strategy)", level=2)
    builder.add_bullet("  - Peer Advisory & Accountability Pods (Closed-pod monthly sprints & OKR reviews)", level=2)
    builder.add_bullet("  - Virtual Strategy Syncs (Focused online roundtables & lightning AMAs)", level=2)

    builder.add_heading_2("Admin Review & Application Inspection Hub")
    builder.add_bullet("Applications Review Table: Displays incoming applicants with badges for Role, Business, Business Model Category, Contact, and Status.")
    builder.add_bullet("Application Inspector Modal: Clicking 'View Details' opens a modal displaying all 12 answers, clickable social and website links, formatted contribution/need callouts, and collaboration preference tags.")
    builder.add_bullet("One-Click Approval: Clicking 'Approve' or 'Approve & Invite' generates a secure, one-time invitation token link (e.g. '/#activate?token=INVITE-XXX') with automated clipboard copy and notification log.")

    builder.add_divider()

    # SECTION 10
    builder.add_heading_1("SECTION 10: MEMBER PORTAL ARCHITECTURE & ADVANCED MODULES")
    builder.add_paragraph("Upon signing in, members access a dedicated single-page workspace with 8 core modules (with Founder Video Spotlights removed to maximize focus on direct peer interaction):")

    builder.add_heading_2("1. Monthly Event Attendance Tracker")
    builder.add_paragraph("High-trust communities thrive on mutual presence. The Attendance Tracker provides clear accountability for every gathering hosted in a calendar month:")
    builder.add_bullet("Month Filter Selector: Dropdown allowing members to view current or past months (e.g. October 2026, September 2026, August 2026).")
    builder.add_bullet("4 KPI Metric Cards: Monthly Attendance Rate (%), Events Attended vs Hosted, Attendance Streak (consecutive events), and Reliability Tier ('Anchor Member').")
    builder.add_bullet("Dynamic Attendance Progress Bar: Visual fill bar dynamically color-coded based on percentage (>=80% Emerald, 50-79% Amber, <50% Coral).")
    builder.add_bullet("Event Presence Log Table: Lists all dinners and roundtables for the selected month with Title, Date, City, Format, Status Badge ('PRESENT', 'UPCOMING', 'MISSED'), Check-in timestamp, and Action button.")
    builder.add_bullet("Host PIN Check-In Modal: Attendees enter the host's event PIN (e.g. 'F4F2026') to verify attendance and update status to 'PRESENT' immediately.")

    builder.add_heading_2("2. Founder 1-to-1 Meetings Tracker")
    builder.add_paragraph("Tracks private peer interactions, co-founder dialogues, and strategic syncs between founders:")
    builder.add_bullet("Summary Stats Header: Total 1:1 Meetings Logged, This Month's Meetings, Synergies & Deals Unlocked.")
    builder.add_bullet("'+ LOG 1:1 MEETING' Action Button: Launches the interactive meeting logger modal.")
    builder.add_bullet("Meeting Logger Modal Form: Partner Founder Name, Partner Company, Date, Meeting Format (Coffee, Dinner, In-Person, Virtual), Strategic Agenda, Collaboration Outcome, Synergy Rating (1-5 Stars), and Confidential Notes.")
    builder.add_bullet("Dynamic 1:1 Meetings Card Feed: Clean cards displaying partner name, company tag, meeting format pill, star rating (1-5 Gold SVG Stars), agenda summary, outcome badge, and notes.")

    builder.add_heading_2("3. Founders Collective Chat (Active Membership Gated — Single Unified Room)")
    builder.add_paragraph("A real-time, confidential discussion space exclusively reserved for verified active members and administrators to interact collectively in a single, unified founder lounge:")
    builder.add_bullet("Membership Access Control: Strict gating verifies memberships.status == 'ACTIVE'. Non-members or expired profiles are presented with an elegant lock gatecard ('Founders Collective Chat Requires an Active Membership') and CTA to activate membership.")
    builder.add_bullet("Unified Single Room: Streamlined single collective room for all members — eliminating fragmented channels to concentrate founder presence, deal flow, and peer collaborations in one high-signal stream.")
    builder.add_bullet("Interactive Stream & High-Contrast Typography: Messages display sender profile photo, full name, business badge, timestamp, and responsive chat bubble. Messages sent by the user render in a luminous mint bubble (#A7F3D0, border #34D399) with deep black font color (#000000 !important) for maximum crisp readability and contrast, while peer messages render in soft neutral cards (#F1F7F4, border #D1E7DD).")
    builder.add_bullet("Fast Composer: Textarea with auto-scroll to latest messages, Enter-to-send support, and live send confirmation.")

    builder.add_heading_2("4. Member Directory")
    builder.add_bullet("Real-time instant search by founder name, startup name, or expertise.")
    builder.add_bullet("Multi-select filter chips: Industry (Fintech, SaaS, D2C, Healthtech, AI), Stage (Bootstrapped, Seed, Series A), City (Bengaluru, Mumbai, Delhi-NCR, Hyderabad, Pune).")
    builder.add_bullet("Member Cards: Display profile photo, verified checkmark, company name, stage pill, founder bio, and 'Connect' trigger.")

    builder.add_heading_2("5. Needs & Wants Matching Engine")
    builder.add_bullet("Interactive Toggle: Filter between 'Needs' (Asks for talent, introductions, vendors, advice) and 'Wants' (Offers of advisory, software credits, hiring referrals).")
    builder.add_bullet("Post New Request Modal: Title, category, urgency badge (Low, Medium, High, Critical), detailed description, and preferred response format.")
    builder.add_bullet("Threaded Response System: Members can offer solutions or introductions directly on the card; notification alert sent to original requester.")

    builder.add_heading_2("6. Leads & Referrals CRM")
    builder.add_bullet("Pipeline Kanban / List View: Tracks warm introductions across stages: 'Intro Made' -> 'In Discussion' -> 'Proposal Sent' -> 'Deal Closed'.")
    builder.add_bullet("Value Metrics: Aggregate tracked referral volume and successful deal closures.")
    builder.add_bullet("Add Referral Modal: Submit introduction details, referee contact, and opportunity description.")

    builder.add_heading_2("7. Curated Gatherings, Optional Registration Fees & Payment Gateway")
    builder.add_bullet("Grid of upcoming private dinners, masterminds, and retreats.")
    builder.add_bullet("Seat counter: Displays confirmed attendee count vs maximum capacity (e.g., 9 / 12 seats claimed).")
    builder.add_bullet("Free Gatherings: Community events (₹0 entry fee) confirm instantly in 1 click via direct RSVP.")
    builder.add_bullet("Optional Event Registration Fees: Admins can optionally configure entry fees (₹ INR) and ticket inclusions in the Admin CMS. Paid gatherings display distinct price badges on the public landing page and member portal.")
    builder.add_bullet("Event Payment Gateway Modal: Active members registering for paid gatherings are directed to a dedicated checkout modal (#eventPaymentModal) with base fee, 18% GST calculation, total payable, and payment methods (UPI QR, Cards, NetBanking, Razorpay 1-Click Pay). Completing payment records the transaction, sets RSVP status to PAID and ATTENDING, and issues an instant verified tax invoice (INV-EVT-...) and transaction receipt (PAY_EVT-...).")
    builder.add_bullet("Google Maps Venue Location Integration: In the Admin event creation form, admins can enter the Venue, City, and an optional Google Maps location URL, with an 'Auto-Generate Link' helper and live test preview button. The backend auto-generates a search query URL if blank. On the public event showcase, member portal gathering cards, and payment gateway modal, clickable 'Google Maps' buttons open precise venue navigation in a new tab.")

    builder.add_heading_2("8. Admin Console & Direct Meeting Photos Manager")
    builder.add_bullet("Application review table with approve/reject actions and invite token generator.")
    builder.add_bullet("Dynamic Site Settings & Media CMS editor for all hero, philosophy, and collaboration visuals.")
    builder.add_bullet("Event Publishing with Optional Entry Fees & Google Maps: Configures title, category, format, date, venue, city, Google Maps location URL (with auto-generation helper), capacity, entry fee (₹), and inclusions.")
    builder.add_bullet("Direct Meeting Photos Manager: Direct in-card form allowing administrators to immediately upload or link 16:9 photos to the homepage slider without leaving the dashboard, plus thumbnail list with instant removal.")

    builder.add_divider()

    # SECTION 11
    builder.add_heading_1("SECTION 11: COMPLETE VERIFICATION & QUALITY CHECKLIST")
    builder.add_paragraph("Prior to deploying or presenting the rebuilt platform, verify all items on this checklist:")
    
    checklist = [
        ("Design System Compliance", "Verify font-style: normal !important is applied universally with zero italic/slanted fonts. Confirm 6px border-radius on all action buttons. Ensure no rectangular frosted boxes cover card photography."),
        ("12-Question Admissions Questionnaire", "Submit a test application from the Show Interest modal. Confirm all 12 answers (Business Name, Brief Description, Years in Business, Team Size, Firm Type, Instagram Link, LinkedIn, Website, Business Model Category, Contribution Offer, Need Asks, and Multi-Select Collaboration Preferences) are saved in SQLite. Verify the Admin Application Inspector displays all answers with working links."),
        ("16:9 Meeting Photos Slower Steady Slider", "Verify continuous slow and steady glide from right to left (@keyframes slideRightToLeft 85s linear infinite) without stutter or wrap gaps. Verify strict 16:9 aspect ratio on cards and images. Confirm hover smoothly pauses the slider."),
        ("Admin Direct Photo Addition", "Test '+ Add to 16:9 Slider' directly on the Admin Dashboard card with title, tag, caption, and image URL or local upload. Confirm photo appears in the homepage slider immediately upon submit and persists in SQLite."),
        ("Founders Collective Chat (Single Unified Room)", "Verify that authenticated active members can read and post messages in the single unified collective chat room with zero sidebar distractions. Confirm that non-members receive a 403 Forbidden response and see the elegant membership lock gatecard prompting subscription activation. Confirm that Founder Video Spotlight has been removed from the member portal."),
        ("Removal of Instagram & Media", "Confirm the former 'As Seen on Instagram and Media' section is completely removed from the landing page."),
        ("Official Social Profile Buttons", "Verify official Instagram (https://www.instagram.com/founder_for_founder), Facebook (https://www.facebook.com/share/19ZnPNuhPb/), and LinkedIn (https://www.linkedin.com/company/founder-for-founder/) shortcut buttons are placed in the footer as slightly curved squares (8px radius) matching the emerald theme, and verified absent from header and hero banner."),
        ("Attendance Tracker Validation", "Confirm monthly selector filters gatherings correctly. Verify attendance rate % calculates against completed events. Test PIN check-in modal with 'F4F2026' and verify status updates to 'PRESENT'."),
        ("Founder 1:1 Meetings Validation", "Log a new 1:1 meeting via modal. Confirm meeting card appears in feed with correct partner, company, star rating, outcome tag, and notes. Verify KPI summary counts increment."),
        ("Brand Proof Alignment", "Confirm '1,528+ Verified Founders' and '27 Curated Gatherings' are active. Ensure 'verified business generated' is absent from public strip."),
        ("Brand Marquee Header", "Confirm 'Businesses Connected With Us' label is clearly rendered above the marquee."),
        ("Optional Event Registration Fees & Payment Gateway", "Verify admin can publish gatherings with optional entry fee and ticket inclusions. Verify free events confirm directly, while paid events route through #eventPaymentModal with 18% GST calculation, UPI/Cards/NetBanking/1-Click pay, and issue transaction and invoice receipts."),
        ("Google Maps Venue Location Provision", "Verify admin can provide custom Google Maps URLs or use the Auto-Generate Link helper. Verify fallback search URLs are automatically generated if left blank. Verify public landing page cards, member portal gathering cards, and payment modal render working Google Maps navigation links with vector pin icons."),
        ("Google Authentication", "Verify Google Sign-In with official Google Identity Services client button, backend token verification via Google tokeninfo, auto-provisioning of member accounts, active memberships, and developer test mode."),
        ("Vercel Serverless Ready", "Verify vercel.json rewrites, requirements.txt, api/index.py serverless handler, and /tmp auto-seeding SQLite path handler for instant global deployment."),
        ("Dynamic CMS Persistence", "Upload a new image in Admin Media Manager. Refresh the page and restart the server; verify the custom image remains active without reverting."),
        ("Database Self-Healing", "Verify SQLite database f4f_community.db initializes tables, migrations, and seeds without errors on a fresh run."),
        ("Full API Coverage", "Test all REST routes (/api/public/content, /api/public/show-interest, /api/admin/applications, /api/admin/events, /api/events, /api/events/rsvp, /api/events/pay, /api/meeting-photos, /api/chat/messages, /api/attendance/summary, /api/events/checkin, /api/founder-meetings, /api/needs-wants) to ensure 200 OK responses with proper JSON formatting."),
    ]

    for title, desc in checklist:
        builder.add_bullet(desc, bold_prefix="[ ] " + title + ":")

    builder.add_divider()
    builder.add_paragraph("End of Master Specification Document • Founder for Founder • powered by snalts.co", bold_prefix="Document Status:")

    builder.build_docx(docx_path)
    print(f"Master prompt document successfully written to: {docx_path}")

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Founder_for_Founder_Master_Prompt.docx")
    generate_full_master_document(target)
    print("Filesize:", os.path.getsize(target), "bytes")
