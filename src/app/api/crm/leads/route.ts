export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const leadId = crypto.randomUUID();

    run(
      `INSERT INTO leads (
        id, user_id, lead_type, lead_name, company, contact_email, contact_phone,
        industry_category, location_reach, requirement, deadline, consent_obtained,
        estimated_value, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW')`,
      [
        leadId,
        user.id,
        body.lead_type || 'Opportunity',
        body.lead_name || '',
        body.company || '',
        body.contact_email || '',
        body.contact_phone || '',
        body.industry_category || 'General',
        body.location_reach || 'Pan India',
        body.requirement || '',
        body.deadline || '',
        body.consent_obtained ? 1 : 0,
        parseFloat(body.estimated_value || 0),
      ]
    );

    return NextResponse.json({
      success: true,
      lead_id: leadId,
      message: 'Lead recorded in your CRM pipeline.',
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
