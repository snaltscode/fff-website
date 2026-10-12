export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { query, run } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const settingsRows = query('SELECT key_name, key_value, description FROM site_settings');
    return NextResponse.json({ settings: settingsRows || [] });
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

    for (const [k, v] of Object.entries(body)) {
      if (k === 'hero_heading' && v) {
        run('UPDATE hero_banners SET heading = ? WHERE is_active = 1', [String(v)]);
      } else if (k === 'hero_subheading' && v) {
        run('UPDATE hero_banners SET subheading = ? WHERE is_active = 1', [String(v)]);
      } else if (k === 'hero_banner_url' && v) {
        run('UPDATE hero_banners SET banner_image_url = ? WHERE is_active = 1', [String(v)]);
        run(
          'INSERT INTO site_settings (key_name, key_value) VALUES (?, ?) ON CONFLICT(key_name) DO UPDATE SET key_value = ?',
          [k, String(v), String(v)]
        );
      } else {
        run(
          'INSERT INTO site_settings (key_name, key_value) VALUES (?, ?) ON CONFLICT(key_name) DO UPDATE SET key_value = ?',
          [k, String(v), String(v)]
        );
      }
    }

    return NextResponse.json({
      success: true,
      message: 'Brand & CMS settings updated successfully.',
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
