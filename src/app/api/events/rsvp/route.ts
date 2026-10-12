export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { get, run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const eventId = body.event_id;
    const status = body.status || 'ATTENDING';

    const event = get('SELECT * FROM events WHERE id = ?', [eventId]);
    if (!event) {
      return NextResponse.json({ error: 'Event not found.' }, { status: 404 });
    }

    const priceAmount = parseFloat(event.price_amount || 0);
    const existingRsvp = get('SELECT * FROM event_rsvps WHERE event_id = ? AND user_id = ?', [
      eventId,
      user.id,
    ]);

    if (priceAmount > 0 && (!existingRsvp || existingRsvp.payment_status !== 'PAID')) {
      return NextResponse.json({
        requires_payment: true,
        message:
          'This event requires a registration fee. Please complete the registration payment to reserve your seat.',
        event_id: eventId,
        price_amount: priceAmount,
        what_is_included: event.what_is_included || 'Included in Gathering Ticket',
      });
    }

    const rsvpId = crypto.randomUUID();
    run(
      `INSERT INTO event_rsvps (id, event_id, user_id, status, payment_status, amount_paid)
       VALUES (?, ?, ?, ?, 'NOT_REQUIRED', 0.0)
       ON CONFLICT(event_id, user_id) DO UPDATE SET status = ?`,
      [rsvpId, eventId, user.id, status, status]
    );

    return NextResponse.json({ success: true, message: `RSVP confirmed: ${status}!` });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
