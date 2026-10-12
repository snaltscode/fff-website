export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { get } from '@/lib/db';
import { verifyPassword, createSession } from '@/lib/auth';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const email = (body.email || '').trim().toLowerCase();
    const password = body.password || '';

    const user = get('SELECT * FROM users WHERE email = ?', [email]);
    if (!user || !verifyPassword(user.password_hash, password)) {
      return NextResponse.json({ error: 'Invalid email or password.' }, { status: 401 });
    }

    const token = createSession(user);
    const profile = get('SELECT * FROM member_profiles WHERE user_id = ?', [user.id]);
    const membership = get('SELECT * FROM memberships WHERE user_id = ?', [user.id]);

    const userClean = { ...user };
    delete userClean.password_hash;

    return NextResponse.json({
      success: true,
      token,
      user: userClean,
      profile: profile || null,
      membership: membership || null,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Login failed.' }, { status: 500 });
  }
}
