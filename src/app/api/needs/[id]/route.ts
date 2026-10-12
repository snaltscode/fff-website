export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { get, query } from '@/lib/db';

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const needId = params.id;
    const need = get(
      `SELECT n.*, p.full_name as creator_name, p.business_name, p.profile_photo 
       FROM needs_offers n 
       JOIN member_profiles p ON n.creator_id = p.user_id 
       WHERE n.id = ?`,
      [needId]
    );

    if (!need) {
      return NextResponse.json({ error: 'Need not found' }, { status: 404 });
    }

    const responses = query(
      `SELECT r.*, p.full_name as responder_name, p.business_name as responder_business, p.profile_photo as responder_photo 
       FROM need_responses r 
       JOIN member_profiles p ON r.responder_id = p.user_id 
       WHERE r.need_id = ? 
       ORDER BY r.created_at DESC`,
      [needId]
    );

    return NextResponse.json({
      need,
      responses: responses || [],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
