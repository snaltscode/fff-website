export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { query } from '@/lib/db';

function sanitizeCell(val: any): string {
  if (val === null || val === undefined) return '""';
  let s = String(val).replace(/"/g, '""');
  if (['=', '+', '-', '@'].includes(s[0])) {
    s = "'" + s;
  }
  return `"${s}"`;
}

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user || !['ADMIN', 'SUPER_ADMIN'].includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const { searchParams } = new URL(req.url);
    const target = searchParams.get('type') || 'members';

    if (target === 'members') {
      const rows = query(`
        SELECT u.email, p.full_name, p.mobile, p.whatsapp, p.business_name,
               p.business_category, p.city, m.status, m.current_period_end
        FROM users u 
        JOIN member_profiles p ON u.id = p.user_id 
        LEFT JOIN memberships m ON u.id = m.user_id
      `);

      const headers = ['Email', 'Name', 'Mobile', 'WhatsApp', 'Business', 'Category', 'City', 'Membership Status', 'Renewal Date'];
      let csvContent = headers.join(',') + '\n';

      for (const r of rows || []) {
        csvContent += [
          sanitizeCell(r.email),
          sanitizeCell(r.full_name),
          sanitizeCell(r.mobile),
          sanitizeCell(r.whatsapp),
          sanitizeCell(r.business_name),
          sanitizeCell(r.business_category),
          sanitizeCell(r.city),
          sanitizeCell(r.status),
          sanitizeCell(r.current_period_end),
        ].join(',') + '\n';
      }

      return new NextResponse(csvContent, {
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="f4f_members_export.csv"',
        },
      });
    } else if (target === 'applications') {
      const rows = query(`
        SELECT full_name, email, phone, applicant_type, business_name, business_model_category,
               business_category, firm_type, years_in_business, team_size, city, instagram,
               linkedin, website, collaboration_preferences, status, created_at
        FROM applications 
        ORDER BY created_at DESC
      `);

      const headers = [
        'Name', 'Email', 'Phone', 'Applicant Type', 'Business Name', 'Business Model',
        'Industry Sector', 'Firm Type', 'Years in Business', 'Team Size', 'City', 'Instagram',
        'LinkedIn', 'Website', 'Collaboration Preferences', 'Status', 'Applied At',
      ];
      let csvContent = headers.join(',') + '\n';

      for (const r of rows || []) {
        csvContent += [
          sanitizeCell(r.full_name),
          sanitizeCell(r.email),
          sanitizeCell(r.phone),
          sanitizeCell(r.applicant_type),
          sanitizeCell(r.business_name),
          sanitizeCell(r.business_model_category),
          sanitizeCell(r.business_category),
          sanitizeCell(r.firm_type),
          sanitizeCell(r.years_in_business),
          sanitizeCell(r.team_size),
          sanitizeCell(r.city),
          sanitizeCell(r.instagram),
          sanitizeCell(r.linkedin),
          sanitizeCell(r.website),
          sanitizeCell(r.collaboration_preferences),
          sanitizeCell(r.status),
          sanitizeCell(r.created_at),
        ].join(',') + '\n';
      }

      return new NextResponse(csvContent, {
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="f4f_applications_export.csv"',
        },
      });
    }

    return NextResponse.json({ error: 'Invalid CSV target' }, { status: 400 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
