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

    const meetings = query(
      `SELECT m.*, 
              strftime('%Y-%m', m.meeting_date) as meeting_month
       FROM one_on_one_meetings m
       WHERE m.host_id = ? OR m.partner_id = ?
       ORDER BY m.meeting_date DESC`,
      [user.id, user.id]
    );

    const now = new Date();
    const nowYM = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    const totalCount = meetings ? meetings.length : 0;
    const monthCount = meetings ? meetings.filter((m) => m.meeting_month === nowYM).length : 0;
    const synergies = meetings
      ? meetings.filter((m) =>
          ['Referral Exchanged', 'Deal In Progress', 'Synergy Explored'].includes(
            m.collaboration_outcome
          )
        ).length
      : 0;

    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ];

    return NextResponse.json({
      meetings: meetings || [],
      stats: {
        total: totalCount,
        this_month: monthCount,
        synergies,
        current_month_name: `${monthNames[now.getMonth()]} ${now.getFullYear()}`,
      },
    });
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
    const meetId = crypto.randomUUID();

    run(
      `INSERT INTO one_on_one_meetings (
        id, host_id, partner_id, partner_name, meeting_date, meeting_type,
        meeting_venue, collaboration_outcome, discussion_topics, action_items
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        meetId,
        user.id,
        body.partner_id || null,
        body.partner_name || '',
        body.meeting_date || new Date().toISOString().replace('T', ' ').substring(0, 19),
        body.meeting_type || 'Virtual Video Call',
        body.meeting_venue || '',
        body.collaboration_outcome || 'Synergy Explored',
        body.discussion_topics || '',
        body.action_items || '',
      ]
    );

    return NextResponse.json({
      success: true,
      message: '1-to-1 Founder Meeting logged successfully!',
      meeting_id: meetId,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
