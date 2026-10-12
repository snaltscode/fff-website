export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { get, run } from '@/lib/db';
import { hashOtp, createSession } from '@/lib/auth';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const email = (body.email || '').trim().toLowerCase();
    const otpInput = (body.otp || '').trim();
    const otpHash = hashOtp(otpInput);

    const record = get(
      'SELECT * FROM otp_records WHERE email = ? AND verified_at IS NULL ORDER BY created_at DESC LIMIT 1',
      [email]
    );

    if (!record) {
      return NextResponse.json(
        { error: 'No pending OTP found for this email. Please request a new code.' },
        { status: 400 }
      );
    }

    if (record.attempts >= record.max_attempts) {
      return NextResponse.json(
        { error: 'Maximum verification attempts exceeded. Please request a new OTP.' },
        { status: 400 }
      );
    }

    const nowStr = new Date().toISOString().replace('T', ' ').substring(0, 19);
    if (record.expires_at < nowStr) {
      return NextResponse.json(
        { error: 'OTP code has expired. Please request a new OTP.' },
        { status: 400 }
      );
    }

    if (record.otp_hash !== otpHash) {
      run('UPDATE otp_records SET attempts = attempts + 1 WHERE id = ?', [record.id]);
      return NextResponse.json(
        { error: 'Invalid OTP code. Please check and try again.' },
        { status: 400 }
      );
    }

    // Mark OTP verified
    run('UPDATE otp_records SET verified_at = CURRENT_TIMESTAMP WHERE id = ?', [record.id]);
    run('UPDATE users SET email_verified = 1, email_verified_at = CURRENT_TIMESTAMP WHERE email = ?', [email]);

    const user = get('SELECT * FROM users WHERE email = ?', [email]);
    let token = null;
    let profile = null;
    let membership = null;
    let userClean = null;

    if (user) {
      token = createSession(user);
      profile = get('SELECT * FROM member_profiles WHERE user_id = ?', [user.id]);
      membership = get('SELECT * FROM memberships WHERE user_id = ?', [user.id]);
      userClean = { ...user };
      delete userClean.password_hash;
    }

    return NextResponse.json({
      success: true,
      email,
      verified: true,
      token,
      user: userClean,
      profile: profile || null,
      membership: membership || null,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'OTP verification failed.' }, { status: 500 });
  }
}
