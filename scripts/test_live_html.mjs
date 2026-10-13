async function testLiveHtml() {
  const port = process.env.PORT || 3000;
  const res = await fetch(`http://localhost:${port}/`);
  const html = await res.text();
  console.log('HTTP Status:', res.status);
  console.log('HTML Length:', html.length);
  
  const checks = [
    ['tab-admin ID', html.includes('id="tab-admin"')],
    ['Stitch Header Banner', html.includes('FOUNDER FOR FOUNDER • EXECUTIVE OPERATING SYSTEM')],
    ['adminMetricsGrid ID', html.includes('id="adminMetricsGrid"')],
    ['applications-section ID', html.includes('id="applications-section"')],
    ['LIVE IMMUTABLE LEDGER badge', html.includes('LIVE IMMUTABLE LEDGER')],
    ['16:9 Meeting Photos Manager', html.includes('16:9 Meeting Photos Gallery Manager')],
    ['Dynamic Media CMS', html.includes('Dynamic Media &amp; Website Images CMS') || html.includes('Dynamic Media & Website Images CMS')],
    ['event-publisher-section ID', html.includes('id="event-publisher-section"')],
    ['Tailwind CDN script', html.includes('cdn.tailwindcss.com')],
    ['Playfair Display Font', html.includes('Playfair+Display')],
    ['Material Symbols Outlined Font', html.includes('Material+Symbols+Outlined')],
    ['adminQuickAddPhotoForm ID', html.includes('id="adminQuickAddPhotoForm"')],
    ['adminMeetingPhotosList ID', html.includes('id="adminMeetingPhotosList"')],
    ['adminSettingsForm ID', html.includes('id="adminSettingsForm"')],
    ['adminCreateEventForm ID', html.includes('id="adminCreateEventForm"')]
  ];

  let passed = 0;
  for (const [name, ok] of checks) {
    console.log(`  ${ok ? 'PASS' : 'FAIL'}: ${name}`);
    if (ok) passed++;
  }
  console.log(`\nVerified ${passed}/${checks.length} checks successfully.`);
}

testLiveHtml();
