import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'This Path is Off the Record (404) — Founder for Founder',
  description: 'The requested page could not be found on Founder for Founder.',
};

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#FAF8F5] text-[#1A1A1A] flex flex-col justify-between" style={{ fontStyle: 'normal' }}>
      {/* Top Navbar */}
      <header className="w-full border-b border-[#E8E4DC] py-3.5 px-6 bg-[#FAF8F5]/95 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 no-underline">
            <img
              src="/assets/logo.svg"
              alt="Founder for Founder Logo"
              className="w-9 h-9 rounded-full object-cover border border-[#E8E4DC]"
              width="36"
              height="36"
            />
            <div>
              <div className="font-bold text-sm tracking-tight text-[#064E3B]" style={{ fontFamily: "'Domine', serif" }}>
                FOUNDER FOR FOUNDER
              </div>
              <div className="text-[10px] tracking-wider text-[#5A6260] font-medium uppercase">
                by snalts.co
              </div>
            </div>
          </Link>
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#064E3B] hover:text-[#0B664C] transition-colors"
          >
            &larr; Back to Home
          </Link>
        </div>
      </header>

      {/* Main 404 Hero Container */}
      <main className="flex-1 flex items-center justify-center px-6 py-16 bg-[#FAF8F5]">
        <div className="max-w-lg w-full text-center bg-[#FBF9F6] border border-[#E8E4DC] rounded-xl p-8 sm:p-12 shadow-[0_20px_40px_-15px_rgba(6,78,59,0.08)]">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#ECFDF5] border border-[#A7F3D0] text-[#064E3B] text-xs font-bold uppercase tracking-wider mb-5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span>
            Error 404 &bull; Path Off the Record
          </div>

          <h1
            className="text-3xl sm:text-4xl font-bold text-[#064E3B] mb-3 tracking-tight"
            style={{ fontFamily: "'Domine', serif" }}
          >
            This path is off the record.
          </h1>

          <p className="text-sm text-[#5A6260] mb-8 leading-relaxed max-w-md mx-auto" style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
            The page or resource you&apos;re looking for might have been moved, archived, or is restricted to active cohort members.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/"
              className="inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-[6px] text-xs font-bold uppercase tracking-wide bg-[#064E3B] hover:bg-[#003527] text-[#FAF8F5] shadow-sm transition-all"
            >
              Return to Sovereign Hub &rarr;
            </Link>
            <Link
              href="/#admissions"
              className="inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-[6px] text-xs font-bold uppercase tracking-wide bg-[#FBF9F6] border border-[#064E3B] text-[#064E3B] hover:bg-[#ECFDF5] transition-all"
            >
              Apply for Admissions
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-[#E8E4DC] py-5 px-6 bg-[#FAF8F5] text-center text-xs text-[#5A6260]">
        &copy; 2026 Founder for Founder. All rights reserved. Powered by snalts.co
      </footer>
    </div>
  );
}
