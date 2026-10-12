export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { query, run } from '@/lib/db';

export async function GET() {
  try {
    const photos = query(
      'SELECT * FROM event_gallery WHERE is_active = 1 ORDER BY display_order ASC, created_at DESC'
    );
    return NextResponse.json({ photos: photos || [] });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const body = await req.json();
    const photoId = crypto.randomUUID();

    run(
      `INSERT INTO event_gallery (id, title, image_url, display_order, is_active)
       VALUES (?, ?, ?, ?, 1)`,
      [
        photoId,
        body.title || 'Founder Meeting Moment',
        body.image_url || '/assets/hero_banner.jpg',
        parseInt(body.display_order || 0, 10),
      ]
    );

    return NextResponse.json({
      success: true,
      message: 'Photo added to meeting gallery!',
      photo_id: photoId,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
