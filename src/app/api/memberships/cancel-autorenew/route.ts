export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    run(
      'UPDATE memberships SET auto_renew = 0, cancelled_at = CURRENT_TIMESTAMP WHERE user_id = ?',
      [user.id]
    );

    return NextResponse.json({
      success: true,
      message:
        'Auto-renewal has been cancelled. Membership remains active until current billing period ends.',
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
