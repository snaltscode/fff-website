export const dynamic = 'force-dynamic';

import { NextRequest, NextResponse } from 'next/server';
import { getAuthUser } from '@/lib/auth';
import { run } from '@/lib/db';

export async function POST(req: NextRequest) {
  try {
    const user = await getAuthUser(req.headers.get('Authorization'));
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();

    run(
      `UPDATE member_profiles SET
        full_name = COALESCE(?, full_name),
        designation = COALESCE(?, designation),
        business_name = COALESCE(?, business_name),
        business_category = COALESCE(?, business_category),
        city = COALESCE(?, city),
        business_stage = COALESCE(?, business_stage),
        expertise = COALESCE(?, expertise),
        interests = COALESCE(?, interests),
        business_description = COALESCE(?, business_description),
        what_i_need = COALESCE(?, what_i_need),
        what_i_can_offer = COALESCE(?, what_i_can_offer),
        preferred_contact_method = COALESCE(?, preferred_contact_method),
        is_phone_visible = COALESCE(?, is_phone_visible),
        is_email_visible = COALESCE(?, is_email_visible),
        updated_at = CURRENT_TIMESTAMP
      WHERE user_id = ?`,
      [
        body.full_name || null,
        body.designation || null,
        body.business_name || null,
        body.business_category || null,
        body.city || null,
        body.business_stage || null,
        body.expertise || null,
        body.interests || null,
        body.business_description || null,
        body.what_i_need || null,
        body.what_i_can_offer || null,
        body.preferred_contact_method || null,
        body.is_phone_visible !== undefined ? body.is_phone_visible : null,
        body.is_email_visible !== undefined ? body.is_email_visible : null,
        user.id,
      ]
    );

    return NextResponse.json({ success: true, message: 'Profile updated successfully!' });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
