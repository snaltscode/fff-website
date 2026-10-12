export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { get, query } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const metricsRow = get(`
      SELECT 
        (SELECT COUNT(*) FROM users WHERE role = 'MEMBER') as total_members,
        (SELECT COUNT(*) FROM memberships WHERE status = 'ACTIVE') as active_members,
        (SELECT COUNT(*) FROM applications WHERE status IN ('SUBMITTED', 'UNDER_REVIEW')) as new_applications,
        (SELECT COALESCE(SUM(amount), 0) FROM business_deals WHERE verified_by_admin = 1) as verified_business
    `);

    const totalMembers = metricsRow ? metricsRow.total_members : 0;
    const activeMembers = metricsRow ? metricsRow.active_members : 0;
    const newApplications = metricsRow ? metricsRow.new_applications : 0;
    const totalBusiness = metricsRow ? metricsRow.verified_business : 0;
    const mrr = activeMembers * 1500;

    const applications = query('SELECT * FROM applications ORDER BY created_at DESC LIMIT 30');

    return NextResponse.json({
      metrics: {
        total_members: totalMembers,
        active_members: activeMembers,
        new_applications: newApplications,
        verified_business: totalBusiness,
        mrr,
      },
      recent_applications: applications || [],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
