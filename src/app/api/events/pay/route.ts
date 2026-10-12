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
    if (!eventId) {
      return NextResponse.json({ error: 'Event ID is required.' }, { status: 400 });
    }

    const event = get('SELECT * FROM events WHERE id = ?', [eventId]);
    if (!event) {
      return NextResponse.json({ error: 'Event not found.' }, { status: 404 });
    }

    const subtotal = parseFloat(event.price_amount || 0);
    if (subtotal <= 0) {
      run(
        `INSERT INTO event_rsvps (id, event_id, user_id, status, payment_status, amount_paid)
         VALUES (?, ?, ?, 'ATTENDING', 'NOT_REQUIRED', 0.0)
         ON CONFLICT(event_id, user_id) DO UPDATE SET status = 'ATTENDING', payment_status = 'NOT_REQUIRED'`,
        [crypto.randomUUID(), eventId, user.id]
      );
      return NextResponse.json({
        success: true,
        message: 'Seat reserved successfully! This gathering is free for members.',
        requires_payment: false,
      });
    }

    const gstRate = 18.0;
    const gstAmount = Math.round(subtotal * (gstRate / 100) * 100) / 100;
    const totalAmount = subtotal + gstAmount;

    const paymentId = 'pay_evt_' + crypto.randomBytes(8).toString('hex');
    const orderId = 'order_evt_' + crypto.randomBytes(8).toString('hex');

    run(
      `INSERT INTO payments (id, user_id, amount, gst_amount, currency, provider, transaction_id, status)
       VALUES (?, ?, ?, ?, 'INR', 'Razorpay', ?, 'COMPLETED')`,
      [crypto.randomUUID(), user.id, totalAmount, gstAmount, paymentId]
    );

    run(
      `INSERT INTO event_rsvps (id, event_id, user_id, status, payment_status, amount_paid, payment_id)
       VALUES (?, ?, ?, 'ATTENDING', 'PAID', ?, ?)
       ON CONFLICT(event_id, user_id) DO UPDATE SET status = 'ATTENDING', payment_status = 'PAID', amount_paid = ?, payment_id = ?`,
      [crypto.randomUUID(), eventId, user.id, totalAmount, paymentId, totalAmount, paymentId]
    );

    return NextResponse.json({
      success: true,
      message: 'Registration fee confirmed. Your seat is officially reserved!',
      payment_id: paymentId,
      order_id: orderId,
      amount_paid: totalAmount,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
