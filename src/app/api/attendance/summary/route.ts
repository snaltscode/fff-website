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
    const now = new Date();
    const currentYM = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    let reqMonth = searchParams.get('month') || currentYM;

    // Get distinct available months from events
    const availableRows = query(
      "SELECT DISTINCT substr(event_date, 1, 7) as m FROM events WHERE event_date IS NOT NULL ORDER BY m DESC LIMIT 24"
    );
    const availableMonths = (availableRows || []).map((r) => r.m).filter(Boolean);
    if (!availableMonths.includes(reqMonth) && availableMonths.length > 0) {
      reqMonth = availableMonths[0];
    }

    // Calculate date bounds
    const parts = reqMonth.split('-');
    const y = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10);

    const monthStart = `${y}-${String(m).padStart(2, '0')}-01 00:00:00`;
    const nextY = m === 12 ? y + 1 : y;
    const nextM = m === 12 ? 1 : m + 1;
    const monthEnd = `${nextY}-${String(nextM).padStart(2, '0')}-01 00:00:00`;

    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ];
    const monthName = `${monthNames[m - 1]} ${y}`;

    // Fetch events in month via indexed LEFT JOINs
    const eventsInMonth = query(
      `SELECT e.*, 
              r.status as user_rsvp,
              a.attended as attended,
              a.status as attendance_status,
              a.marked_at as marked_at
       FROM events e
       LEFT JOIN event_rsvps r ON r.event_id = e.id AND r.user_id = ?
       LEFT JOIN event_attendance a ON a.event_id = e.id AND a.user_id = ?
       WHERE e.event_date >= ? AND e.event_date < ?
       ORDER BY e.event_date ASC`,
      [user.id, user.id, monthStart, monthEnd]
    );

    const eventsList: any[] = [];
    let eventsAttended = 0;
    let completedEvents = 0;
    const nowStr = now.toISOString().replace('T', ' ').substring(0, 19);

    for (const ev of eventsInMonth || []) {
      const ed = { ...ev };
      const isCompleted = ed.status === 'COMPLETED' || (ed.event_date && ed.event_date < nowStr);
      if (isCompleted) {
        completedEvents++;
      }

      if (ed.attended === 1 || ed.attendance_status === 'PRESENT') {
        eventsAttended++;
        ed.calculated_status = 'PRESENT';
      } else if (isCompleted) {
        ed.calculated_status = 'MISSED';
      } else if (ed.user_rsvp === 'ATTENDING') {
        ed.calculated_status = 'RSVP_CONFIRMED';
      } else {
        ed.calculated_status = 'UPCOMING';
      }

      eventsList.push(ed);
    }

    const totalEvents = eventsList.length;
    let attendanceRate = 100;
    if (completedEvents > 0) {
      attendanceRate = Math.round((eventsAttended / completedEvents) * 100);
    }

    // Streak calculation across all past events
    const pastAttended = query(
      `SELECT e.id, ea.attended
       FROM events e
       LEFT JOIN event_attendance ea ON e.id = ea.event_id AND ea.user_id = ?
       WHERE (e.status = 'COMPLETED' OR e.event_date < ?)
       ORDER BY e.event_date DESC
       LIMIT 50`,
      [user.id, nowStr]
    );

    let streak = 0;
    for (const pa of pastAttended || []) {
      if (pa.attended === 1) {
        streak++;
      } else {
        break;
      }
    }

    const accountabilityTier =
      attendanceRate >= 75 ? 'Tier 1: High-Signal Founder' : 'Active Community Member';

    return NextResponse.json({
      selected_month: reqMonth,
      month_name: monthName,
      available_months: availableMonths,
      total_events: totalEvents,
      completed_events: completedEvents,
      events_attended: eventsAttended,
      attendance_rate: attendanceRate,
      attendance_streak: streak,
      accountability_tier: accountabilityTier,
      events: eventsList,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
