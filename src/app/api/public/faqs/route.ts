export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { query } from '@/lib/db';

export async function GET() {
  try {
    const faqs = query('SELECT * FROM faqs WHERE is_active = 1 ORDER BY display_order ASC');
    return NextResponse.json({ faqs: faqs || [] });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
