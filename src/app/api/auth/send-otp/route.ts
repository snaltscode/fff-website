export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { get, run } from '@/lib/db';
import { generateOtp, hashOtp } from '@/lib/auth';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const email = (body.email || '').trim().toLowerCase();

    if (!email || !email.includes('@')) {
      return NextResponse.json({ error: 'Please enter a valid email address.' }, { status: 400 });
    }

    // 30s cooldown check
    const recentOtp = get(
      "SELECT created_at FROM otp_records WHERE email = ? AND datetime(created_at, '+30 seconds') > CURRENT_TIMESTAMP",
      [email]
    );

    if (recentOtp) {
      return NextResponse.json(
        { error: 'Please wait 30 seconds before requesting another OTP.' },
        { status: 429 }
      );
    }

    const otp = generateOtp();
    const otpHash = hashOtp(otp);
    const expiresAt = new Date(Date.now() + 10 * 60000).toISOString().replace('T', ' ').substring(0, 19);

    run(
      "INSERT INTO otp_records (id, email, otp_hash, purpose, expires_at) VALUES (?, ?, ?, 'EMAIL_VERIFICATION', ?)",
      [crypto.randomUUID(), email, otpHash, expiresAt]
    );

    // Transactional email log
    run(
      'INSERT INTO email_logs (id, recipient_email, subject, body_content) VALUES (?, ?, ?, ?)',
      [
        crypto.randomUUID(),
        email,
        'Verify your Founder for Founder account',
        `Your verification code is: ${otp}. This code expires in 10 minutes.`,
      ]
    );

    return NextResponse.json({
      success: true,
      message: `Verification OTP sent to ${email}.`,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Failed to send OTP.' }, { status: 500 });
  }
}
