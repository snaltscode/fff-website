export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { query } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const cat = searchParams.get('category') || '';
    const fmt = searchParams.get('signature_format') || '';

    let sql = `
      SELECT e.*, 
             COALESCE(rc.rsvp_count, 0) as rsvp_count, 
             r.status as user_rsvp,
             r.payment_status as user_payment_status,
             r.amount_paid as user_amount_paid,
             r.payment_id as user_payment_id
      FROM events e
      LEFT JOIN event_rsvps r ON r.event_id = e.id AND r.user_id = ?
      LEFT JOIN (
          SELECT event_id, COUNT(*) as rsvp_count 
          FROM event_rsvps 
          WHERE status = 'ATTENDING' 
          GROUP BY event_id
      ) rc ON rc.event_id = e.id
      WHERE 1=1
    `;
    const params: any[] = [user.id];

    if (cat) {
      sql += ' AND e.category = ?';
      params.push(cat);
    }
    if (fmt) {
      sql += ' AND e.signature_format = ?';
      params.push(fmt);
    }

    sql += ' ORDER BY e.event_date ASC';

    const events = query(sql, params);
    return NextResponse.json({ events: events || [] });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
