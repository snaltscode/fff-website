export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const needId = params.id;
    const body = await req.json();
    const outcome = body.outcome || 'Fulfilled via community connection.';

    run(
      "UPDATE needs_offers SET status = 'FULFILLED', fulfilled_outcome = ? WHERE id = ? AND creator_id = ?",
      [outcome, needId, user.id]
    );

    return NextResponse.json({
      success: true,
      message: 'Opportunity marked as fulfilled! Thank you for sharing.',
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
