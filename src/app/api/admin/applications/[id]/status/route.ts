export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const appId = params.id;
    const body = await req.json();
    const newStatus = body.status;

    let invitationToken: string | null = null;
    if (newStatus === 'APPROVED') {
      invitationToken = 'inv_' + crypto.randomBytes(16).toString('hex');
      run(
        `UPDATE applications 
         SET status = 'APPROVED', invitation_token = ?, invited_at = CURRENT_TIMESTAMP 
         WHERE id = ?`,
        [invitationToken, appId]
      );
    } else {
      run('UPDATE applications SET status = ? WHERE id = ?', [newStatus, appId]);
    }

    return NextResponse.json({
      success: true,
      status: newStatus,
      invitation_token: invitationToken,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
