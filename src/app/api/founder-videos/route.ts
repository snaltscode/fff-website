export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { query, run } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    const videos = query('SELECT * FROM founder_videos WHERE user_id = ? ORDER BY created_at DESC', [
      user.id,
    ]);
    return NextResponse.json({ videos: videos || [] });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    const body = await req.json();
    const vidId = crypto.randomUUID();

    run(
      `INSERT INTO founder_videos (id, user_id, video_url, video_type, status)
       VALUES (?, ?, ?, ?, 'PENDING')`,
      [vidId, user.id, body.video_url || '', body.video_type || 'Introduction']
    );

    return NextResponse.json({ success: true, message: 'Founder video submitted for review.' });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
