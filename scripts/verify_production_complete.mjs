import assert from 'node:assert';

const BASE_URL = 'https://founderforfounder.in';

async function runVerification() {
  console.log('====================================================');
  console.log('🚀 FOUNDER FOR FOUNDER - PRODUCTION VERIFICATION SUITE');
  console.log(`🌐 Base URL: ${BASE_URL}`);
  console.log('====================================================\n');

  const results = [];

  // 1. Verify Homepage
  console.log('--- 1. Testing Homepage ---');
  try {
    const res = await fetch(`${BASE_URL}/`);
    assert.strictEqual(res.status, 200, `Homepage HTTP status: ${res.status}`);
    const html = await res.text();
    assert(html.length > 200000, `Homepage HTML length: ${html.length}`);
    assert(html.includes('Playfair Display'), 'Missing Playfair Display font');
    assert(html.includes('Plus Jakarta Sans'), 'Missing Plus Jakarta Sans font');
    assert(html.includes('Executive Guild'), 'Missing Executive Guild positioning');
    assert(html.includes('showInterestModal'), 'Missing admissions questionnaire modal');
    assert(html.includes('loginModal'), 'Missing login modal');
    assert(html.includes('Curated Gatherings'), 'Missing Curated Gatherings format section');
    assert(html.includes('5 Pillars') || html.includes('Pillars'), 'Missing 5 Pillars section');
    console.log('✅ Homepage: Status 200, Stitch Design Verified, Length:', html.length);
    results.push({ test: 'Homepage Stitch Design', passed: true });
  } catch (e) {
    console.error('❌ Homepage failed:', e.message);
    results.push({ test: 'Homepage Stitch Design', passed: false, error: e.message });
  }

  // 2. Verify Legal Pages
  console.log('\n--- 2. Testing Legal Transparency Pages ---');
  const legalRoutes = [
    { path: '/terms', title: 'Terms And Conditions' },
    { path: '/terms-and-conditions', title: 'Terms And Conditions' },
    { path: '/privacy-policy', title: 'Privacy Policy' },
    { path: '/refund-policy', title: 'Refund' },
    { path: '/refund-and-cancellation-policy', title: 'Refund' },
    { path: '/community-guidelines', title: 'Community Guidelines' },
    { path: '/guidelines', title: 'Community Guidelines' }
  ];

  for (const lr of legalRoutes) {
    try {
      const res = await fetch(`${BASE_URL}${lr.path}`);
      assert.strictEqual(res.status, 200, `Route ${lr.path} status ${res.status}`);
      const text = await res.text();
      assert(text.length > 10000, `Route ${lr.path} content length ${text.length}`);
      assert(text.includes('Founder for Founder') || text.includes('Legal Transparency'), `Route ${lr.path} missing brand title`);
      console.log(`✅ ${lr.path.padEnd(35)} -> HTTP 200 (Length: ${text.length})`);
      results.push({ test: `Legal route ${lr.path}`, passed: true });
    } catch (e) {
      console.error(`❌ ${lr.path} failed:`, e.message);
      results.push({ test: `Legal route ${lr.path}`, passed: false, error: e.message });
    }
  }

  // 3. Verify Serverless API Endpoints
  console.log('\n--- 3. Testing Serverless APIs ---');
  try {
    const res = await fetch(`${BASE_URL}/api`);
    assert.strictEqual(res.status, 200, `/api status ${res.status}`);
    const json = await res.json();
    assert.strictEqual(json.status, 'ok', 'Status not ok');
    console.log('✅ /api Healthcheck -> HTTP 200, Version:', json.version, 'Environment:', json.environment);
    results.push({ test: 'API Healthcheck /api', passed: true });
  } catch (e) {
    console.error('❌ /api failed:', e.message);
    results.push({ test: 'API Healthcheck /api', passed: false, error: e.message });
  }

  try {
    const res = await fetch(`${BASE_URL}/api/public/content`);
    assert.strictEqual(res.status, 200, `/api/public/content status ${res.status}`);
    const json = await res.json();
    assert(json.hero, 'Missing hero in public content');
    assert(json.settings, 'Missing settings in public content');
    assert(json.testimonials, 'Missing testimonials in public content');
    assert(json.faqs, 'Missing faqs in public content');
    console.log('✅ /api/public/content -> HTTP 200, Received keys:', Object.keys(json).join(', '));
    results.push({ test: 'API /api/public/content', passed: true });
  } catch (e) {
    console.error('❌ /api/public/content failed:', e.message);
    results.push({ test: 'API /api/public/content', passed: false, error: e.message });
  }

  try {
    const res = await fetch(`${BASE_URL}/api/auth/config`);
    assert.strictEqual(res.status, 200, `/api/auth/config status ${res.status}`);
    const json = await res.json();
    console.log('✅ /api/auth/config -> HTTP 200, Config:', json);
    results.push({ test: 'API /api/auth/config', passed: true });
  } catch (e) {
    console.error('❌ /api/auth/config failed:', e.message);
    results.push({ test: 'API /api/auth/config', passed: false, error: e.message });
  }

  // Summary
  console.log('\n====================================================');
  const allPassed = results.every(r => r.passed);
  const passedCount = results.filter(r => r.passed).length;
  console.log(`Verification Summary: ${passedCount} / ${results.length} tests passed.`);
  if (allPassed) {
    console.log('🎉 ALL PRODUCTION VERIFICATION TESTS PASSED SUCCESSFULLY!');
  } else {
    console.log('⚠️ Some tests failed. Review logs above.');
  }
  console.log('====================================================');
}

runVerification();
