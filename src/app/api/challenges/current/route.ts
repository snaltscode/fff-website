export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { get, query } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const challenge = get("SELECT * FROM challenges WHERE status = 'ACTIVE' LIMIT 1");
    const leaderboard = query(
      `SELECT p.full_name, p.business_name, p.profile_photo, COALESCE(SUM(bd.amount), 0) as total_business
       FROM member_profiles p
       LEFT JOIN business_deals bd ON p.user_id = bd.user_id AND bd.verified_by_admin = 1
       GROUP BY p.user_id
       ORDER BY total_business DESC LIMIT 10`
    );

    let mySubmission = null;
    if (challenge) {
      mySubmission = get(
        'SELECT * FROM challenge_submissions WHERE challenge_id = ? AND user_id = ?',
        [challenge.id, user.id]
      );
    }

    return NextResponse.json({
      challenge: challenge || null,
      leaderboard: leaderboard || [],
      my_submission: mySubmission || null,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
