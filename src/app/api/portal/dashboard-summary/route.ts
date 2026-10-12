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
    const now = new Date();
    const nowStr = now.toISOString().replace('T', ' ').substring(0, 19);

    const year = now.getFullYear();
    const month = now.getMonth() + 1;
    const monthPad = String(month).padStart(2, '0');
    const startOfMonth = `${year}-${monthPad}-01 00:00:00`;

    const nextYear = month === 12 ? year + 1 : year;
    const nextMonth = month === 12 ? 1 : month + 1;
    const nextMonthPad = String(nextMonth).padStart(2, '0');
    const nextMonthStart = `${nextYear}-${nextMonthPad}-01 00:00:00`;

    // 1. Combined CRM & Meeting stats query (1 single indexed query)
    const crmStats = get(
      `SELECT 
        (SELECT COUNT(*) FROM leads WHERE user_id = ? AND status = 'WON') as leads_won,
        (SELECT COUNT(*) FROM referrals WHERE referred_member_id = ?) as ref_rec,
        (SELECT COUNT(*) FROM one_on_one_meetings 
         WHERE (host_id = ? OR partner_id = ?) 
           AND meeting_date >= ? AND meeting_date < ?) as this_month_meetings`,
      [uid, uid, uid, uid, startOfMonth, nextMonthStart]
    );

    const leadsWon = crmStats ? crmStats.leads_won : 0;
    const refRec = crmStats ? crmStats.ref_rec : 0;
    const thisMonthMeetings = crmStats ? crmStats.this_month_meetings : 0;

    // 2. Optimized Events for Current Month using LEFT JOINs
    const eventsInMonth = query(
      `SELECT e.id, e.status, e.event_date,
              r.status as user_rsvp,
              a.attended as attended,
              a.status as attendance_status
       FROM events e
       LEFT JOIN event_rsvps r ON r.event_id = e.id AND r.user_id = ?
       LEFT JOIN event_attendance a ON a.event_id = e.id AND a.user_id = ?
       WHERE e.event_date >= ? AND e.event_date < ?`,
      [uid, uid, startOfMonth, nextMonthStart]
    );

    let eventsAttended = 0;
    let completedEvents = 0;
    for (const ev of eventsInMonth) {
      const isCompleted = ev.status === 'COMPLETED' || (ev.event_date && ev.event_date < nowStr);
      if (isCompleted) {
        completedEvents++;
      }
      if (ev.attended === 1 || ev.attendance_status === 'PRESENT') {
        eventsAttended++;
      }
    }

    let attendanceRate = 100;
    if (completedEvents > 0) {
      attendanceRate = Math.round((eventsAttended / completedEvents) * 100);
    }

    // 3. Optimized streak query with LIMIT 30
    const pastAttended = query(
      `SELECT ea.attended
       FROM events e
       LEFT JOIN event_attendance ea ON e.id = ea.event_id AND ea.user_id = ?
       WHERE (e.status = 'COMPLETED' OR e.event_date < ?)
       ORDER BY e.event_date DESC
       LIMIT 30`,
      [uid, nowStr]
    );

    let streak = 0;
    for (const pa of pastAttended) {
      if (pa.attended === 1) {
        streak++;
      } else {
        break;
      }
    }

    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ];

    return NextResponse.json({
      crm: {
        referrals_received: refRec,
        leads_won: leadsWon,
      },
      attendance: {
        attendance_rate: attendanceRate,
        attendance_streak: streak,
      },
      meetings: {
        this_month: thisMonthMeetings,
        current_month_name: monthNames[now.getMonth()],
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
