export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const appId = crypto.randomUUID();

    let collabPrefs = body.collaboration_preferences || '';
    if (Array.isArray(collabPrefs)) {
      collabPrefs = collabPrefs.join(', ');
    }

    run(
      `INSERT INTO applications (
        id, full_name, email, phone, whatsapp, applicant_type, business_name, business_category,
        business_model_category, firm_type, years_in_business, team_size, designation, city,
        business_stage, instagram, website, linkedin, business_description, what_need, what_offer,
        collaboration_preferences, why_join, consent_given, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'SUBMITTED')`,
      [
        appId,
        body.full_name || '',
        body.email || '',
        body.phone || '',
        body.whatsapp || body.phone || '',
        body.applicant_type || 'Founder',
        body.business_name || '',
        body.business_category || 'Technology & Software',
        body.business_model_category || 'Product Based',
        body.firm_type || 'Private Limited (Pvt Ltd)',
        String(body.years_in_business || ''),
        String(body.team_size || ''),
        body.designation || 'Founder',
        body.city || 'Pan India',
        body.business_stage || 'Established',
        body.instagram || '',
        body.website || '',
        body.linkedin || '',
        body.business_description || '',
        body.what_need || '',
        body.what_offer || '',
        String(collabPrefs),
        body.why_join || '',
        body.consent_given ? 1 : 0,
      ]
    );

    // Audit log
    run(
      `INSERT INTO audit_logs (id, actor_id, action, target_entity, target_id, details) VALUES (?, ?, 'SHOW_INTEREST_SUBMITTED', 'applications', ?, ?)`,
      [
        crypto.randomUUID(),
        null,
        appId,
        `Application submitted by ${body.email} (${body.business_name})`,
      ]
    );

    return NextResponse.json({
      success: true,
      message: 'Application received successfully! Our review committee will evaluate your application.',
      application_id: appId,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || 'Failed to submit application.' }, { status: 500 });
  }
}
