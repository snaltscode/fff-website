export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { get } from '@/lib/db';

export async function GET(req: NextRequest, { params }: { params: { token: string } }) {
  const token = params.token;
  try {
    const app = get('SELECT * FROM applications WHERE invitation_token = ?', [token]);
    if (!app) {
      return NextResponse.json({ error: 'Invalid or expired invitation token.' }, { status: 404 });
    }
    return NextResponse.json({
      application: app,
      pricing: {
        plan_name: 'Founder Membership',
        monthly_subtotal: 1500.0,
        gst_rate: 18.0,
        gst_amount: 270.0,
        total_monthly_amount: 1770.0,
        currency: 'INR',
        recurring_terms:
          'Billed monthly. Auto-renewing subscription. Non-refundable except as required by law. Cancel anytime before next renewal date in account settings.',
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
