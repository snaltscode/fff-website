const port = process.env.PORT || 3000;
const BASE = `http://localhost:${port}`;

async function runTests() {
  console.log('=== RUNNING END-TO-END VERIFICATION SUITE ===\n');
  let passCount = 0;
  let failCount = 0;

  function assert(cond, msg) {
    if (cond) {
      console.log(`  PASS: ${msg}`);
      passCount++;
    } else {
      console.error(`  FAIL: ${msg}`);
      failCount++;
    }
  }

  // 1. GET /api/public/content
  try {
    const res = await fetch(`${BASE}/api/public/content`);
    const data = await res.json();
    assert(res.status === 200, 'GET /api/public/content returns HTTP 200');
    assert(Array.isArray(data.testimonials) && data.testimonials.length === 0, 'No fake testimonials returned (0 active fake reviews)');
    assert(Array.isArray(data.gallery) && data.gallery.length === 0, 'No demo Unsplash gallery photos returned');
    assert(data.counters && typeof data.counters.active_members === 'number', 'Counters return authentic database counts');
    assert(!JSON.stringify(data).includes('Apex Global Tech'), 'Response contains zero references to Apex Global Tech');
    assert(!JSON.stringify(data).includes('Precision Industries'), 'Response contains zero references to Precision Industries');
    assert(!JSON.stringify(data).includes('Elevate Digital'), 'Response contains zero references to Elevate Digital');
    assert(!JSON.stringify(data).includes('unsplash.com'), 'Response contains zero Unsplash stock image URLs');
  } catch (e) {
    assert(false, `GET /api/public/content threw error: ${e.message}`);
  }

  // 2. OTP Security Test (GET / POST /api/auth/send-otp)
  try {
    const res = await fetch(`${BASE}/api/auth/send-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'admin@founderforfounder.in' })
    });
    const data = await res.json();
    assert(res.status === 200, 'POST /api/auth/send-otp returns HTTP 200');
    assert(!('demo_otp' in data), 'SECURITY: demo_otp is NOT leaked in the API response');
    assert(data.success === true, 'OTP generated successfully for legitimate email');
  } catch (e) {
    assert(false, `POST /api/auth/send-otp threw error: ${e.message}`);
  }

  // 3. Google Auth Security Test
  try {
    const res = await fetch(`${BASE}/api/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'admin@founderforfounder.in', name: 'Fake Admin' })
    });
    assert(res.status === 400 || res.status === 401, 'SECURITY: Fake unauthenticated Google login payload is rejected');
  } catch (e) {
    assert(false, `Google auth security test threw error: ${e.message}`);
  }

  // 4. Admin Login with Credentials
  let adminToken = '';
  try {
    const res = await fetch(`${BASE}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'admin@founderforfounder.in', password: 'Admin@123' })
    });
    const data = await res.json();
    assert(res.status === 200 && data.token, 'Admin login with valid password succeeds');
    adminToken = data.token;
  } catch (e) {
    assert(false, `Admin login threw error: ${e.message}`);
  }

  // 5. Authenticated Member Directory with Privacy Enforcement
  if (adminToken) {
    try {
      const res = await fetch(`${BASE}/api/members`, {
        headers: { 'Authorization': `Bearer ${adminToken}` }
      });
      const data = await res.json();
      assert(res.status === 200 && Array.isArray(data.members), 'GET /api/members returns member list');
      const hasDemoUser = (data.members || []).some(m => (m.email && m.email.includes('demo')) || (m.full_name && m.full_name.includes('Demo')));
      assert(!hasDemoUser, 'Member directory excludes demo accounts');
      const hasTestExample = (data.members || []).some(m => m.email && m.email.includes('@example.com'));
      assert(!hasTestExample, 'Member directory excludes @example.com test fixture accounts');
    } catch (e) {
      assert(false, `GET /api/members threw error: ${e.message}`);
    }
  }

  // 6. Member Portal Dashboard Summary & Auth Me
  if (adminToken) {
    try {
      const res = await fetch(`${BASE}/api/portal/dashboard-summary`, {
        headers: { 'Authorization': `Bearer ${adminToken}` }
      });
      const data = await res.json();
      assert(res.status === 200 && data.crm && data.attendance && data.meetings, 'GET /api/portal/dashboard-summary returns metrics object');

      const meRes = await fetch(`${BASE}/api/auth/me`, {
        headers: { 'Authorization': `Bearer ${adminToken}` }
      });
      const meData = await meRes.json();
      assert(meRes.status === 200 && meData.user && meData.user.email === 'admin@founderforfounder.in', 'GET /api/auth/me returns authentic user object');
    } catch (e) {
      assert(false, `Dashboard summary threw error: ${e.message}`);
    }
  }

  // 7. Security: Admin Upload Validation (Size & Type Restriction)
  if (adminToken) {
    try {
      const res = await fetch(`${BASE}/api/admin/upload-image`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${adminToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          image_data: 'data:application/x-executable;base64,TVqQAAMAAAAEAAAA',
          folder: 'general'
        })
      });
      assert(res.status === 400, 'SECURITY: Upload of non-image MIME type is rejected (HTTP 400)');
    } catch (e) {
      assert(false, `Upload security test threw error: ${e.message}`);
    }
  }

  console.log(`\n=== SUITE SUMMARY: ${passCount} PASSED, ${failCount} FAILED ===`);
  if (failCount > 0) {
    process.exit(1);
  }
}

runTests();
