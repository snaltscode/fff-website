export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { get } from '@/lib/db';

export async function GET() {
  try {
    const setting = get("SELECT key_value FROM site_settings WHERE key_name = 'google_client_id'");
    const googleClientId = process.env.GOOGLE_CLIENT_ID || (setting ? setting.key_value : '');

    return NextResponse.json({
      google_client_id: googleClientId,
      google_auth_enabled: true,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
