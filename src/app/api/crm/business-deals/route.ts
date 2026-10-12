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
    const dealId = crypto.randomUUID();

    run(
      `INSERT INTO business_deals (id, user_id, deal_title, client_name, amount, source, verified_by_admin)
       VALUES (?, ?, ?, ?, ?, ?, 1)`,
      [
        dealId,
        user.id,
        body.deal_title || '',
        body.client_name || '',
        parseFloat(body.amount || 0),
        body.source || 'Founder for Founder',
      ]
    );

    return NextResponse.json({
      success: true,
      message: 'Business deal recorded and verified successfully!',
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
