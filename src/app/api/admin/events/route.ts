export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const body = await req.json();
    const evtId = crypto.randomUUID();
    const venue = (body.venue || '').trim();
    const city = (body.city || 'Pan India').trim();
    let googleMapsUrl = (body.google_maps_url || '').trim();

    if (!googleMapsUrl && venue) {
      googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
        `${venue} ${city}`.trim()
      )}`;
    }

    run(
      `INSERT INTO events (
        id, title, category, signature_format, description, event_date, time_str,
        venue, city, google_maps_url, host_name, capacity, eligibility, what_is_included,
        price_amount, cancellation_terms, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'UPCOMING')`,
      [
        evtId,
        body.title || 'Founder Gathering',
        body.category || 'Executive Networking',
        body.signature_format || 'Curated Dinner & Peer Roundtable',
        body.description || '',
        body.event_date || new Date().toISOString().replace('T', ' ').substring(0, 19),
        body.time_str || '7:30 PM - 10:30 PM',
        venue || 'Private Dining Room',
        city,
        googleMapsUrl,
        body.host_name || 'Founder for Founder Chapter Host',
        parseInt(body.capacity || 25, 10),
        body.eligibility || 'Active Founders & Verified Members Only',
        body.what_is_included || 'Private Dining & Strategic Networking',
        parseFloat(body.price_amount || 0),
        body.cancellation_terms || 'Non-refundable within 48 hours of gathering.',
      ]
    );

    return NextResponse.json({
      success: true,
      message: 'New gathering event published successfully!',
      event_id: evtId,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
