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

    const uid = user.id;
    const leadsList = query('SELECT * FROM leads WHERE user_id = ? ORDER BY created_at DESC', [uid]);
    const leadsRec = leadsList ? leadsList.length : 0;
    const leadsWon = leadsList ? leadsList.filter((l) => l.status === 'WON').length : 0;

    const stats = get(
      `SELECT 
        (SELECT COUNT(*) FROM referrals WHERE referrer_id = ?) as ref_given,
        (SELECT COUNT(*) FROM referrals WHERE referred_member_id = ?) as ref_rec,
        (SELECT COALESCE(SUM(amount), 0) FROM business_deals WHERE user_id = ? AND verified_by_admin = 1) as biz_gen`,
      [uid, uid, uid]
    );

    return NextResponse.json({
      leads_received: leadsRec,
      leads_won: leadsWon,
      referrals_given: stats ? stats.ref_given : 0,
      referrals_received: stats ? stats.ref_rec : 0,
      verified_business_generated: stats ? stats.biz_gen : 0,
      leads: leadsList || [],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
