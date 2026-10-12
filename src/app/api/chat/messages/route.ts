export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { get, query, run } from '@/lib/db';

export async function GET(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const isAdmin = ['ADMIN', 'SUPER_ADMIN'].includes(user.role);
    let hasActiveMembership = isAdmin;

    if (!hasActiveMembership) {
      const mem = get('SELECT status FROM memberships WHERE user_id = ?', [user.id]);
      hasActiveMembership = Boolean(mem && mem.status === 'ACTIVE');
    }

    if (!hasActiveMembership) {
      return NextResponse.json(
        {
          error: 'Membership required',
          has_membership: false,
          message:
            'Founders Collective Chat is an exclusive space reserved for verified active members.',
        },
        { status: 403 }
      );
    }

    const { searchParams } = new URL(req.url);
    const channel = searchParams.get('channel') || 'collective';

    const messages = query(
      `SELECT m.*, 
              p.full_name, p.business_name, p.profile_photo, p.city, p.designation,
              u.email, u.role
       FROM community_chat_messages m
       LEFT JOIN users u ON m.user_id = u.id
       LEFT JOIN member_profiles p ON m.user_id = p.user_id
       WHERE m.channel = ?
       ORDER BY m.created_at ASC
       LIMIT 100`,
      [channel]
    );

    return NextResponse.json({
      messages: messages || [],
      channel,
      has_membership: true,
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

    const isAdmin = ['ADMIN', 'SUPER_ADMIN'].includes(user.role);
    let hasActiveMembership = isAdmin;

    if (!hasActiveMembership) {
      const mem = get('SELECT status FROM memberships WHERE user_id = ?', [user.id]);
      hasActiveMembership = Boolean(mem && mem.status === 'ACTIVE');
    }

    if (!hasActiveMembership) {
      return NextResponse.json(
        {
          error: 'Active membership required to send messages.',
          has_membership: false,
        },
        { status: 403 }
      );
    }

    const body = await req.json();
    const rawMsg = (body.message || '').trim();
    if (!rawMsg) {
      return NextResponse.json({ error: 'Message cannot be empty.' }, { status: 400 });
    }

    const channel = (body.channel || 'collective').trim();
    const replyToId = body.reply_to_id || null;
    const msgId = crypto.randomUUID();

    run(
      `INSERT INTO community_chat_messages (id, user_id, channel, message, reply_to_id, created_at)
       VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`,
      [msgId, user.id, channel, rawMsg, replyToId]
    );

    const newMsg = get(
      `SELECT m.*, 
              p.full_name, p.business_name, p.profile_photo, p.city, p.designation,
              u.email, u.role
       FROM community_chat_messages m
       LEFT JOIN users u ON m.user_id = u.id
       LEFT JOIN member_profiles p ON m.user_id = p.user_id
       WHERE m.id = ?`,
      [msgId]
    );

    return NextResponse.json({ success: true, message: newMsg });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
