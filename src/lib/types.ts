// TypeScript Data Models & Types for Founder for Founder

export interface User {
  id: string;
  email: string;
  password_hash?: string;
  role: 'MEMBER' | 'ADMIN' | 'SUPER_ADMIN';
  status: 'PENDING' | 'VERIFIED' | 'SUSPENDED';
  google_id?: string | null;
  auth_provider: 'LOCAL' | 'GOOGLE';
  avatar_url?: string | null;
  email_verified: number | boolean;
  email_verified_at?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface MemberProfile {
  id: string;
  user_id: string;
  full_name: string;
  profile_photo: string;
  mobile?: string;
  whatsapp?: string;
  whatsapp_opt_in?: number;
  business_name: string;
  business_category: string;
  designation: string;
  city: string;
  website?: string;
  linkedin?: string;
  business_description: string;
  years_in_business?: number | string;
  what_i_need?: string;
  what_i_can_offer?: string;
  why_i_joined?: string;
  verified_member?: number;
  business_stage?: string;
  expertise?: string;
  interests?: string;
  preferred_contact_method?: string;
  created_at?: string;
  updated_at?: string;
  email?: string;
  membership_status?: string;
}

export interface Membership {
  id: string;
  user_id: string;
  plan_name: string;
  amount: number;
  gst_rate: number;
  status: 'ACTIVE' | 'CANCELLED' | 'EXPIRED' | 'PAUSED';
  auto_renew: number | boolean;
  current_period_start?: string;
  current_period_end?: string;
  cancelled_at?: string;
  created_at?: string;
}

export interface Application {
  id: string;
  full_name: string;
  email: string;
  phone?: string;
  whatsapp?: string;
  applicant_type: string;
  business_name: string;
  business_category: string;
  business_model_category?: string;
  firm_type?: string;
  years_in_business?: string;
  team_size?: string;
  designation?: string;
  city?: string;
  business_stage?: string;
  instagram?: string;
  website?: string;
  linkedin?: string;
  business_description?: string;
  what_need?: string;
  what_offer?: string;
  collaboration_preferences?: string;
  why_join?: string;
  consent_given?: number;
  status: 'SUBMITTED' | 'UNDER_REVIEW' | 'APPROVED' | 'REJECTED';
  invitation_token?: string | null;
  invited_at?: string | null;
  rejected_at?: string | null;
  created_at?: string;
}

export interface EventItem {
  id: string;
  title: string;
  category: string;
  signature_format?: string;
  description?: string;
  event_date: string;
  time_str?: string;
  venue?: string;
  city?: string;
  google_maps_url?: string;
  host_name?: string;
  capacity?: number;
  eligibility?: string;
  what_is_included?: string;
  price_amount?: number;
  cancellation_terms?: string;
  status: 'UPCOMING' | 'COMPLETED' | 'CANCELLED';
  rsvp_count?: number;
  user_rsvp?: string | null;
  user_payment_status?: string | null;
  user_amount_paid?: number;
  user_payment_id?: string | null;
  created_at?: string;
}

export interface NeedOffer {
  id: string;
  creator_id: string;
  type: 'NEED' | 'OFFER';
  title: string;
  description: string;
  category: string;
  urgency: 'HIGH' | 'MEDIUM' | 'NORMAL';
  status: 'OPEN' | 'IN_PROGRESS' | 'FULFILLED' | 'CLOSED';
  fulfilled_outcome?: string;
  creator_name?: string;
  business_name?: string;
  profile_photo?: string;
  creator_city?: string;
  response_count?: number;
  created_at?: string;
}

export interface Lead {
  id: string;
  user_id: string;
  lead_type: string;
  lead_name: string;
  company?: string;
  contact_email?: string;
  contact_phone?: string;
  industry_category?: string;
  location_reach?: string;
  requirement?: string;
  deadline?: string;
  consent_obtained?: number;
  estimated_value?: number;
  status: 'NEW' | 'CONTACTED' | 'IN_DISCUSSION' | 'WON' | 'LOST';
  created_at?: string;
  updated_at?: string;
}

export interface OneOnOneMeeting {
  id: string;
  host_id: string;
  partner_id?: string;
  partner_name?: string;
  meeting_date: string;
  meeting_type?: string;
  meeting_venue?: string;
  collaboration_outcome?: string;
  discussion_topics?: string;
  action_items?: string;
  created_at?: string;
}

export interface ChatMessage {
  id: string;
  user_id: string;
  channel: string;
  message: string;
  reply_to_id?: string | null;
  full_name?: string;
  business_name?: string;
  profile_photo?: string;
  city?: string;
  designation?: string;
  email?: string;
  role?: string;
  created_at?: string;
}

export interface Testimonial {
  id: string;
  author_name: string;
  author_company: string;
  quote: string;
  photo_url?: string;
  display_order?: number;
  is_active?: number;
}

export interface FAQ {
  id: string;
  question: string;
  answer: string;
  category?: string;
  display_order?: number;
  is_active?: number;
}

export interface GalleryPhoto {
  id: string;
  title: string;
  image_url: string;
  display_order?: number;
  is_active?: number;
}

export interface SiteSettings {
  [key: string]: string;
}

export interface PublicContentPayload {
  hero: any;
  reels: any[];
  youtube_videos: any[];
  testimonials: Testimonial[];
  gallery: GalleryPhoto[];
  meeting_photos: GalleryPhoto[];
  faqs: FAQ[];
  upcoming_events: EventItem[];
  upcoming_event: EventItem | null;
  counters: {
    active_members: number;
    published_events: number;
    verified_business: number;
  };
  settings: SiteSettings;
}

export interface DashboardSummaryPayload {
  crm: {
    referrals_received: number;
    leads_won: number;
  };
  attendance: {
    attendance_rate: number;
    attendance_streak: number;
  };
  meetings: {
    this_month: number;
    current_month_name: string;
  };
}
