export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { get } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const profile = get('SELECT * FROM member_profiles WHERE user_id = ?', [user.id]);
    const membership = get('SELECT * FROM memberships WHERE user_id = ?', [user.id]);

    return NextResponse.json({
      user,
      profile: profile || null,
      membership: membership || null,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
