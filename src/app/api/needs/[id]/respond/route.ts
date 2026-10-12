export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { get, run } from '@/lib/db';

export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const needId = params.id;
    const need = get('SELECT * FROM needs_offers WHERE id = ?', [needId]);
    if (!need) {
      return NextResponse.json({ error: 'Post not found' }, { status: 404 });
    }

    const body = await req.json();
    const respId = crypto.randomUUID();

    run(
      `INSERT INTO need_responses (id, need_id, responder_id, response_type, message, suggested_resource, status)
       VALUES (?, ?, ?, ?, ?, ?, 'PENDING')`,
      [
        respId,
        needId,
        user.id,
        body.response_type || 'OFFER_HELP',
        body.message || '',
        body.suggested_resource || '',
      ]
    );

    // Notify creator
    run(
      'INSERT INTO notifications (id, user_id, title, message) VALUES (?, ?, ?, ?)',
      [
        crypto.randomUUID(),
        need.creator_id,
        'New Response on Your Post',
        `A member responded to your post: '${(need.title || '').substring(0, 40)}...'`,
      ]
    );

    return NextResponse.json({ success: true, message: 'Response submitted to the post author.' });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
