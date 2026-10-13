import Link from 'next/link';

export const metadata = {
  title: 'Page Not Found — Founder for Founder',
  description: 'The requested page could not be found on Founder for Founder.',
};

export default function NotFound() {
  return (
    <div className="min-h-screen bg-white text-[#0B1F17] flex flex-col justify-between">
      {/* Minimal Top Brand Bar */}
      <header className="w-full border-b border-[#E5EDE8] py-4 px-6 bg-white/95 backdrop-blur">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 text-decoration-none">
            <img
              src="/assets/logo.svg"
              alt="Founder for Founder Logo"
              className="w-10 h-10 rounded-lg border border-[#E5EDE8]"
            />
            <div>
              <div className="font-bold text-sm tracking-wider text-[#0B1F17]">FOUNDER FOR FOUNDER</div>
              <div className="text-[10px] tracking-widest text-[#047857] font-semibold">CREATE. CONNECT. COLLABORATE.</div>
            </div>
          </Link>
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#047857] hover:text-[#065F46] transition"
          >
            ← Back to Home
          </Link>
        </div>
      </header>

      {/* Main 404 Hero Container */}
      <main className="flex-1 flex items-center justify-center px-6 py-20 bg-[#F7FAF8]">
        <div className="max-w-xl w-full text-center bg-white border border-[#E5EDE8] rounded-2xl p-10 sm:p-14 shadow-sm">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#ECFDF5] border border-[#A7F3D0] text-[#047857] text-xs font-bold uppercase tracking-wider mb-6">
            Error 404 • Page Not Found
          </div>

          <h1
            className="text-4xl sm:text-5xl font-semibold text-[#0B1F17] mb-4 tracking-tight"
            style={{ fontFamily: "'Fraunces', Georgia, serif" }}
          >
            Looking for a Founder Connection?
          </h1>

          <p className="text-base text-[#4B5B53] mb-8 leading-relaxed">
            The page or resource you are seeking does not exist or may have been moved. Return to the curated community platform to explore verified members and experiences.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-sm font-bold uppercase tracking-wide bg-[#047857] hover:bg-[#065F46] text-white shadow-sm transition-all"
            >
              Return Home →
            </Link>
            <Link
              href="/#events"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-sm font-bold uppercase tracking-wide bg-white border border-[#047857] text-[#047857] hover:bg-[#ECFDF5] transition-all"
            >
              Explore Experiences
            </Link>
          </div>
        </div>
      </main>

      {/* Minimal Footer */}
      <footer className="border-t border-[#E5EDE8] py-6 px-6 bg-white text-center text-xs text-[#4B5B53]">
        © 2026 Founder for Founder. All rights reserved. Powered by snalts.co
      </footer>
    </div>
  );
}
