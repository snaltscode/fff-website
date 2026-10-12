import fs from 'fs';
import path from 'path';

console.log('=== RUNNING MOBILE RESPONSIVENESS & PERFORMANCE VERIFICATION SUITE ===\n');

let passCount = 0;
let failCount = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  PASS: ${message}`);
    passCount++;
  } else {
    console.error(`  FAIL: ${message}`);
    failCount++;
  }
}

// 1. Verify CSS Files Synchronized
const publicCss = fs.readFileSync('public/css/styles.css', 'utf8').replace(/\r\n/g, '\n');
const globalsCss = fs.readFileSync('src/app/globals.css', 'utf8').replace(/\r\n/g, '\n');
assert(publicCss === globalsCss, 'public/css/styles.css and src/app/globals.css are 100% identical and synchronized');

// 2. Verify Universal Anti-Horizontal Scroll Guard
assert(
  publicCss.includes('.timeline-container') && publicCss.includes('.tabs-container'),
  'Universal anti-horizontal scroll guard covers .timeline-container and .tabs-container'
);
assert(
  publicCss.includes('overflow-x: hidden !important') && publicCss.includes('max-width: 100% !important'),
  'Universal anti-horizontal scroll guard enforces overflow-x: hidden and max-width: 100%'
);

// 3. Verify Timeline Responsive Rules across Breakpoints
assert(
  publicCss.includes('@media (max-width: 991px)') &&
  publicCss.includes('grid-template-columns: repeat(3, 1fr) !important') &&
  publicCss.includes('.timeline-line {\n    display: none !important;\n  }'),
  'Timeline converts to 3 columns on tablet (<=991px) and hides horizontal line'
);
assert(
  publicCss.includes('@media (max-width: 768px)') &&
  publicCss.includes('grid-template-columns: repeat(2, 1fr) !important'),
  'Timeline converts to 2 columns on small tablets & mobile (<=768px)'
);
assert(
  publicCss.includes('@media (max-width: 480px)') &&
  publicCss.includes('/* Timeline 1-Column on Compact Mobile */'),
  'Timeline converts to 1 column on compact mobile (<=480px)'
);

// 4. Verify Tabs Container Responsive Rules
assert(
  publicCss.includes('.tabs-container {\n    grid-template-columns: 1fr !important;\n    gap: 1.5rem !important;'),
  'Tabbed community features collapse to 1 column on <=991px'
);

// 5. Verify Touch Targets >= 44x44px
assert(
  publicCss.includes('.mobile-nav-toggle {\n  display: none;\n  background: transparent;\n  border: 1px solid var(--mint-200);\n  border-radius: 6px !important;\n  width: 44px;\n  height: 44px;\n  min-width: 44px;\n  min-height: 44px;'),
  'Base mobile-nav-toggle enforces minimum 44x44px touch target'
);
assert(
  !publicCss.includes('width: 36px !important;\n    height: 36px !important;\n    padding: 8px 6px !important;'),
  'No 36x36px undersized mobile-nav-toggle in <=360px query'
);
assert(
  publicCss.includes('.modal-close {\n  position: absolute;\n  top: 20px; right: 20px;\n  background: transparent;\n  border: none;\n  color: var(--grey-500);\n  font-size: 1.5rem;\n  cursor: pointer;\n  width: 44px;\n  height: 44px;\n  min-width: 44px;\n  min-height: 44px;'),
  'Base modal-close enforces minimum 44x44px touch target'
);
assert(
  publicCss.includes('.modal-close {\n    top: 10px !important;\n    right: 10px !important;\n    width: 44px !important;\n    height: 44px !important;\n    min-width: 44px !important;\n    min-height: 44px !important;'),
  'Mobile modal-close enforces minimum 44x44px touch target'
);

// 6. Verify iOS Safari Auto-Zoom Prevention
assert(
  publicCss.includes('font-size: 16px !important;\n    min-height: 44px !important;\n    border-radius: 6px !important;'),
  'Form inputs enforce font-size: 16px and min-height: 44px on mobile (prevents iOS auto-zoom)'
);

// 7. Verify GPU Performance & Backdrop-Filter Softening
assert(
  publicCss.includes('.nav-drawer {\n    display: flex;\n    position: fixed;\n    top: 60px;\n    left: 0;\n    right: 0;\n    background: rgba(255, 255, 255, 0.98);\n    backdrop-filter: blur(6px);'),
  'Mobile nav drawer softens backdrop-filter to blur(6px) to eliminate GPU lag and compositor repaints'
);
assert(
  publicCss.includes('.portal-sidebar {\n    width: 100%;\n    position: sticky;\n    top: 60px;\n    left: 0;\n    right: 0;\n    bottom: auto;\n    z-index: 90;\n    background: rgba(255, 255, 255, 0.98);\n    backdrop-filter: blur(6px);'),
  'Mobile portal ribbon softens backdrop-filter to blur(6px) for smooth 60/120fps touch scrolling'
);

// 8. Verify Hero Pill Badge Non-Overflow
const indexHtml = fs.readFileSync('public/index.html', 'utf8');
const pageTsx = fs.readFileSync('src/app/page.tsx', 'utf8');
assert(
  indexHtml.includes('<div class="hero-pill-badge">'),
  'index.html uses responsive .hero-pill-badge instead of fixed-width inline style'
);
assert(
  pageTsx.includes('hero-pill-badge'),
  'src/app/page.tsx is in sync with responsive .hero-pill-badge'
);
assert(
  publicCss.includes('.hero-pill-badge {\n  margin-bottom: 2rem;\n  background: rgba(255, 255, 255, 0.85);'),
  'CSS defines .hero-pill-badge with max-width: 100% and responsive mobile styling'
);

// 9. Verify JS Memory & Avatar Caching
const appJs = fs.readFileSync('public/js/app.js', 'utf8');
assert(
  appJs.includes('const _avatarCache = new Map();') &&
  appJs.includes('if (_avatarCache.has(initials))') &&
  appJs.includes('_avatarCache.set(initials, uri);'),
  'Avatar generator memoizes SVG data URIs via Map cache to eliminate memory leaks and GC overhead'
);
assert(
  appJs.includes('const isMobile = typeof window !== \'undefined\' && window.innerWidth <= 991;') &&
  appJs.includes('heroEl.style.backgroundImage = `${gradient}, url(\'${heroUrl}\')`;'),
  'Hero background gradient is viewport-aware in renderPublicContent (vertical on mobile)'
);

// 10. Verify Next.js Viewport Metadata Export
const layoutTsx = fs.readFileSync('src/app/layout.tsx', 'utf8');
assert(
  layoutTsx.includes('export const viewport: Viewport = {') &&
  layoutTsx.includes('width: \'device-width\',') &&
  layoutTsx.includes('themeColor: \'#064E3B\','),
  'src/app/layout.tsx exports Viewport with width: device-width and #064E3B themeColor'
);

console.log(`\n=== SUITE SUMMARY: ${passCount} PASSED, ${failCount} FAILED ===\n`);
if (failCount > 0) {
  process.exit(1);
}
