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
    const eventId = body.event_id;
    const targetUserId = body.user_id;
    const status = body.status || 'PRESENT';
    const attended = status === 'PRESENT' ? 1 : 0;

    run(
      `INSERT INTO event_attendance (id, event_id, user_id, attended, status, marked_at)
       VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
       ON CONFLICT(event_id, user_id) DO UPDATE SET attended = ?, status = ?, marked_at = CURRENT_TIMESTAMP`,
      [crypto.randomUUID(), eventId, targetUserId, attended, status, attended, status]
    );

    return NextResponse.json({ success: true, message: 'Attendance status recorded.' });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
