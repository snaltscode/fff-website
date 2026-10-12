export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { get, query } from '@/lib/db';

let _cachedContent: any = null;
let _cachedTime = 0;
const CACHE_TTL = 30000; // 30 seconds

export async function GET() {
  const now = Date.now();
  if (_cachedContent && now - _cachedTime < CACHE_TTL) {
    return NextResponse.json(_cachedContent, {
      headers: {
        'Cache-Control': 'public, max-age=30, s-maxage=60, stale-while-revalidate=300',
      },
    });
  }

  try {
    const hero = get('SELECT * FROM hero_banners WHERE is_active = 1 LIMIT 1');
    const reels = query('SELECT * FROM instagram_reels WHERE is_active = 1 ORDER BY display_order ASC');
    const youtubeVideos = query('SELECT * FROM youtube_videos WHERE is_active = 1 ORDER BY display_order ASC');
    const testimonials = query('SELECT * FROM testimonials WHERE is_active = 1 ORDER BY display_order ASC');
    const gallery = query('SELECT * FROM event_gallery WHERE is_active = 1 ORDER BY display_order ASC, created_at DESC');
    const faqs = query('SELECT * FROM faqs WHERE is_active = 1 ORDER BY display_order ASC');
    const events = query("SELECT * FROM events WHERE status = 'UPCOMING' ORDER BY event_date ASC LIMIT 4");

    const countersRow = get(`
      SELECT 
        (SELECT COUNT(*) FROM memberships WHERE status = 'ACTIVE') as active_members,
        (SELECT COUNT(*) FROM events) as published_events,
        (SELECT COALESCE(SUM(amount), 0) FROM business_deals WHERE verified_by_admin = 1) as verified_business
    `);

    const settingsRows = query('SELECT key_name, key_value FROM site_settings');
    const settings: Record<string, string> = {};
    for (const r of settingsRows) {
      settings[r.key_name] = r.key_value;
    }
    if (!settings.hero_banner_url) {
      settings.hero_banner_url = '/assets/hero_banner.jpg';
    }
    settings.google_client_id = process.env.GOOGLE_CLIENT_ID || settings.google_client_id || '';

    const payload = {
      hero: hero || null,
      reels: reels || [],
      youtube_videos: youtubeVideos || [],
      testimonials: testimonials || [],
      gallery: gallery || [],
      meeting_photos: gallery || [],
      faqs: faqs || [],
      upcoming_events: events || [],
      upcoming_event: events && events.length > 0 ? events[0] : null,
      counters: {
        active_members: countersRow ? countersRow.active_members : 0,
        published_events: countersRow ? countersRow.published_events : 0,
        verified_business: countersRow ? countersRow.verified_business : 0,
      },
      settings,
    };

    _cachedContent = payload;
    _cachedTime = now;

    return NextResponse.json(payload, {
      headers: {
        'Cache-Control': 'public, max-age=30, s-maxage=60, stale-while-revalidate=300',
      },
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Failed to fetch public content' }, { status: 500 });
  }
}
