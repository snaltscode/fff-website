export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser, createSession, hashPassword } from '@/lib/auth';
import { get, run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    const body = await req.json();
    const invitationToken = body.invitation_token;

    let targetUserId = user ? user.id : null;
    let targetEmail = user ? user.email : '';
    let applicantName = '';
    let app: any = null;

    if (!targetUserId && invitationToken) {
      app = get('SELECT * FROM applications WHERE invitation_token = ?', [invitationToken]);
      if (!app) {
        return NextResponse.json(
          { error: 'Invalid invitation token. Please check your invitation link.' },
          { status: 400 }
        );
      }
      targetEmail = app.email;
      applicantName = app.full_name;

      let existingUser = get('SELECT id FROM users WHERE email = ?', [targetEmail]);
      if (existingUser) {
        targetUserId = existingUser.id;
      } else {
        targetUserId = crypto.randomUUID();
        const initialPwdHash = hashPassword(body.password || 'Founder@2026');
        run(
          `INSERT INTO users (id, email, password_hash, role, status, email_verified, email_verified_at)
           VALUES (?, ?, ?, 'MEMBER', 'VERIFIED', 1, CURRENT_TIMESTAMP)`,
          [targetUserId, targetEmail, initialPwdHash]
        );

        run(
          `INSERT INTO member_profiles (
            id, user_id, full_name, profile_photo, mobile, whatsapp, whatsapp_opt_in,
            business_name, business_category, designation, city, website, linkedin,
            business_description, years_in_business, what_i_need, what_i_can_offer,
            why_i_joined, verified_member, business_stage
          ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)`,
          [
            crypto.randomUUID(),
            targetUserId,
            app.full_name,
            '/assets/logo.svg',
            app.phone || '',
            app.whatsapp || app.phone || '',
            app.business_name || '',
            app.business_category || 'Technology & Innovation',
            app.designation || 'Founder',
            app.city || 'Pan India',
            app.website || '',
            app.linkedin || '',
            app.business_description || '',
            app.years_in_business || '3',
            app.what_need || '',
            app.what_offer || '',
            app.why_join || '',
            app.business_stage || 'Established',
          ]
        );
      }
    }

    if (!targetUserId) {
      return NextResponse.json(
        { error: 'Authentication or valid invitation token required.' },
        { status: 400 }
      );
    }

    const subtotal = 1500.0;
    const gstRate = 18.0;
    const gstAmount = Math.round(subtotal * (gstRate / 100) * 100) / 100;
    const total = subtotal + gstAmount;

    const paymentId = 'pay_' + crypto.randomBytes(8).toString('hex');
    const orderId = 'order_' + crypto.randomBytes(8).toString('hex');

    run(
      `INSERT INTO payments (id, user_id, amount, gst_amount, currency, provider, transaction_id, status)
       VALUES (?, ?, ?, ?, 'INR', 'Razorpay', ?, 'COMPLETED')`,
      [crypto.randomUUID(), targetUserId, total, gstAmount, paymentId]
    );

    const now = new Date();
    const endDate = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
    const endStr = endDate.toISOString().replace('T', ' ').substring(0, 19);

    run(
      `INSERT INTO memberships (
        id, user_id, plan_name, amount, gst_rate, status, auto_renew,
        current_period_start, current_period_end, payment_provider, subscription_id
      ) VALUES (?, ?, 'Founder Membership', ?, ?, 'ACTIVE', 1, CURRENT_TIMESTAMP, ?, 'Razorpay', ?)
      ON CONFLICT(user_id) DO UPDATE SET
        status = 'ACTIVE',
        auto_renew = 1,
        current_period_start = CURRENT_TIMESTAMP,
        current_period_end = ?,
        updated_at = CURRENT_TIMESTAMP`,
      [
        crypto.randomUUID(),
        targetUserId,
        subtotal,
        gstRate,
        endStr,
        orderId,
        endStr,
      ]
    );

    if (app && app.id) {
      run("UPDATE applications SET status = 'APPROVED' WHERE id = ?", [app.id]);
    }

    const dbUser = get('SELECT id, email, role, status, email_verified, avatar_url FROM users WHERE id = ?', [
      targetUserId,
    ]);
    const profile = get('SELECT * FROM member_profiles WHERE user_id = ?', [targetUserId]);
    const membership = get('SELECT * FROM memberships WHERE user_id = ?', [targetUserId]);

    const token = createSession(dbUser);

    const monthNames = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
    ];
    const renewalFormatted = `${endDate.getDate()} ${monthNames[endDate.getMonth()]} ${endDate.getFullYear()}`;

    return NextResponse.json({
      success: true,
      message: 'Membership activated successfully! Welcome to Founder for Founder.',
      token,
      user: dbUser,
      profile: profile || null,
      membership: membership || null,
      payment_id: paymentId,
      amount_paid: total,
      renewal_date: renewalFormatted,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
