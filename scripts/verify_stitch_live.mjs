async function verifyLive() {
  const port = process.env.PORT || 3000;
  const res = await fetch(`http://localhost:${port}/`);
  const html = await res.text();
  const checks = [
    ['F4F Logo / Monogram', html.includes('>F4F<')],
    ['Beyond Networking. Into Real Connections.', html.includes('Beyond Networking.') && html.includes('Into Real Connections.')],
    ['Curated founder network across India', html.includes('Founder for Founder brings ambitious entrepreneurs')],
    ['Marquee Ticker', html.includes('animate-marquee')],
    ['What We Offer section', html.includes('What We Offer')],
    ['Platform Architecture section', html.includes('Platform Architecture') && html.includes('Structured For Active Value')],
    ['Experiences Photo Carousel', html.includes('Experiences') && html.includes('id="experiences-track"')],
    ['How To Join Timeline', html.includes('How To Join') && html.includes('Show Interest')],
    ['Active Community Needs & Offers', html.includes('Active Community Needs &amp; Offers') || html.includes('Active Community Needs & Offers')],
    ['Founder Perspectives', html.includes('Founder Perspectives')],
    ['Closing Banner CTA', html.includes('Your next meaningful business') && html.includes('connection starts here.')],
    ['Stitch Footer with Contact & Legal', html.includes('connect.f4f@gmail.com') && html.includes('snalts.co')]
  ];
  let passed = 0;
  checks.forEach(([title, ok]) => {
    console.log((ok ? '  PASS: ' : '  FAIL: ') + title);
    if (ok) passed++;
  });
  console.log(`\nVerified ${passed}/${checks.length} public Stitch Screen 13 components.`);
}
verifyLive();
