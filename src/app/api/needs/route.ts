export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { query, run } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const needType = searchParams.get('type') || '';
    const category = searchParams.get('category') || '';
    const urgency = searchParams.get('urgency') || '';
    const search = searchParams.get('q') || '';

    let sql = `
      SELECT n.*, p.full_name as creator_name, p.business_name, p.profile_photo, p.city as creator_city,
             COALESCE(nr.response_count, 0) as response_count
      FROM needs_offers n 
      JOIN member_profiles p ON n.creator_id = p.user_id 
      LEFT JOIN (
          SELECT need_id, COUNT(*) as response_count 
          FROM need_responses 
          GROUP BY need_id
      ) nr ON nr.need_id = n.id
      WHERE n.status != 'CLOSED'
    `;
    const params: any[] = [];

    if (needType) {
      sql += ' AND n.type = ?';
      params.push(needType);
    }
    if (category) {
      sql += ' AND n.category = ?';
      params.push(category);
    }
    if (urgency) {
      sql += ' AND n.urgency = ?';
      params.push(urgency);
    }
    if (search) {
      sql += ' AND (n.title LIKE ? OR n.description LIKE ?)';
      params.push(`%${search}%`, `%${search}%`);
    }

    sql += ' ORDER BY n.created_at DESC';

    const needs = query(sql, params);
    return NextResponse.json({ needs: needs || [] });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const needId = crypto.randomUUID();

    run(
      `INSERT INTO needs_offers (id, creator_id, type, title, description, category, urgency, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, 'OPEN')`,
      [
        needId,
        user.id,
        body.type || 'NEED',
        body.title || '',
        body.description || '',
        body.category || 'General',
        body.urgency || 'MEDIUM',
      ]
    );

    return NextResponse.json({
      success: true,
      message: 'Need / Offer posted to community board!',
      need_id: needId,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
