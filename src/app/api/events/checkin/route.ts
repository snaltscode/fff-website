export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const eventId = body.event_id;
    if (!eventId) {
      return NextResponse.json({ error: 'Event ID required' }, { status: 400 });
    }

    const targetUserId = body.user_id || user.id;

    run(
      `INSERT INTO event_attendance (id, event_id, user_id, attended, status, marked_at)
       VALUES (?, ?, ?, 1, 'PRESENT', CURRENT_TIMESTAMP)
       ON CONFLICT(event_id, user_id) DO UPDATE SET attended = 1, status = 'PRESENT', marked_at = CURRENT_TIMESTAMP`,
      [crypto.randomUUID(), eventId, targetUserId]
    );

    return NextResponse.json({ success: true, message: 'Check-in recorded successfully!' });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
