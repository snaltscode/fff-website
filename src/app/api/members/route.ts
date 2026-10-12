export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { query } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const search = (searchParams.get('q') || '').trim();
    const category = (searchParams.get('category') || '').trim();
    const city = (searchParams.get('city') || '').trim();
    const stage = (searchParams.get('stage') || '').trim();

    let sql = `
      SELECT p.*, u.email, m.status as membership_status 
      FROM member_profiles p 
      JOIN users u ON p.user_id = u.id 
      LEFT JOIN memberships m ON p.user_id = m.user_id 
      WHERE 1=1
    `;
    const params: any[] = [];

    if (search) {
      sql += ` AND (
        p.full_name LIKE ? OR 
        p.business_name LIKE ? OR 
        p.what_i_need LIKE ? OR 
        p.what_i_can_offer LIKE ? OR 
        p.city LIKE ? OR 
        p.expertise LIKE ? OR 
        p.interests LIKE ?
      )`;
      const term = `%${search}%`;
      params.push(term, term, term, term, term, term, term);
    }

    if (category) {
      sql += ' AND p.business_category = ?';
      params.push(category);
    }

    if (city) {
      sql += ' AND p.city LIKE ?';
      params.push(`%${city}%`);
    }

    if (stage) {
      sql += ' AND p.business_stage = ?';
      params.push(stage);
    }

    sql += ' ORDER BY p.created_at DESC LIMIT 200';

    const members = query(sql, params);
    return NextResponse.json({ members: members || [] });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
