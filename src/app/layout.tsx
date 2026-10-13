import type { Metadata, Viewport } from 'next';
import './globals.css';

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  themeColor: '#064E3B',
};

export const metadata: Metadata = {
  title: 'Founder for Founder | Curated Business Network for Founders',
  description:
    'A curated business network connecting founders, entrepreneurs, business owners, and professionals across India. Create. Connect. Collaborate.',
  icons: {
    icon: '/assets/logo.svg',
    apple: '/assets/logo.svg',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,600&family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap"
          rel="stylesheet"
        />
        <script src="https://cdn.tailwindcss.com"></script>
        <script
          id="tailwind-config"
          dangerouslySetInnerHTML={{
            __html: `
              tailwind.config = {
                corePlugins: { preflight: false },
                darkMode: "class",
                theme: {
                  extend: {
                    colors: {
                      "canvas-cream": "#FAF8F5",
                      "canvas-ivory": "#FBF9F6",
                      "surface-subtle": "#F5F2EC",
                      "card-border": "#E8E4DC",
                      "border-hairline": "#EDE9E1",
                      "primary-dark": "#064E3B",
                      "primary-emerald": "#043E2E",
                      "primary-light": "#0B664C",
                      "text-main": "#1A1A1A",
                      "text-muted": "#5A6260",
                      "text-subtle": "#7E8784",
                      "gold-accent": "#B89047",
                      "stitch-emerald": "#047857",
                      "stitch-emerald-hover": "#065F46",
                      "stitch-green": "#10B981",
                      "stitch-green-tint": "#ECFDF5",
                      "stitch-gold": "#C9A227",
                      "stitch-heading": "#0B1F17",
                      "stitch-body": "#4B5B53",
                      "stitch-border": "#E5EDE8",
                      "stitch-surface": "#FFFFFF",
                      "stitch-surface-subtle": "#F7FAF8",
                      "on-primary-container": "#80bea6",
                      "background": "#F7FAF8",
                      "surface-container": "#f4ece8",
                      "tertiary-fixed-dim": "#4edea3",
                      "on-secondary": "#ffffff",
                      "secondary-container": "#fed488",
                      "error-container": "#ffdad6",
                      "primary-fixed": "#b0f0d6",
                      "on-error-container": "#93000a",
                      "on-secondary-container": "#785a1a",
                      "on-background": "#1e1b19",
                      "on-primary-fixed": "#002117",
                      "gold-light": "#F5EFEB",
                      "surface-container-high": "#eee7e3",
                      "inverse-on-surface": "#f7efeb",
                      "surface-tint": "#2b6954",
                      "inverse-surface": "#33302d",
                      "secondary": "#775a19",
                      "on-surface": "#1e1b19",
                      "inverse-primary": "#95d3ba",
                      "tertiary-container": "#004f34",
                      "surface": "#fff8f5",
                      "error": "#ba1a1a",
                      "on-surface-variant": "#404944",
                      "surface-bright": "#fff8f5",
                      "outline-variant": "#bfc9c3",
                      "primary-container": "#064e3b",
                      "tertiary": "#003623",
                      "surface-dim": "#e0d8d5",
                      "text-tertiary": "#6B7280",
                      "canvas-ivory": "#FBFBFA",
                      "surface-variant": "#e9e1dd",
                      "secondary-fixed": "#ffdea5",
                      "primary": "#003527",
                      "primary-fixed-dim": "#95d3ba",
                      "on-primary": "#ffffff",
                      "text-primary": "#111827",
                      "surface-card": "#FFFFFF",
                      "surface-container-low": "#faf2ee",
                      "outline": "#707974",
                      "border-strong": "#D5D2CB",
                      "surface-subtle": "#F4F3F0",
                      "on-secondary-fixed-variant": "#5d4201",
                      "surface-container-lowest": "#ffffff",
                      "on-primary-fixed-variant": "#0b513d",
                      "border-hairline": "#EAE8E4",
                      "emerald-deep": "#043E2E",
                      "surface-container-highest": "#e9e1dd",
                      "on-error": "#ffffff",
                      "on-tertiary": "#ffffff",
                      "on-tertiary-fixed": "#002113",
                      "text-secondary": "#4B5563",
                      "on-tertiary-container": "#31c98f",
                      "on-secondary-fixed": "#261900",
                      "tertiary-fixed": "#6ffbbe",
                      "on-tertiary-fixed-variant": "#005236",
                      "secondary-fixed-dim": "#e9c176"
                    },
                    borderRadius: {
                      DEFAULT: "0.125rem",
                      lg: "0.25rem",
                      xl: "0.5rem",
                      full: "0.75rem"
                    },
                    spacing: {
                      gutter: "1.5rem",
                      "margin-md": "3rem",
                      "space-xs": "0.25rem",
                      "space-lg": "1.75rem",
                      "space-xl": "3rem",
                      "space-md": "1rem",
                      "gutter-lg": "2.5rem",
                      "space-sm": "0.5rem",
                      "margin-lg": "6rem",
                      margin: "1.5rem"
                    },
                    fontFamily: {
                      serif: ['"Playfair Display"', 'Georgia', 'serif'],
                      sans: ['"Plus Jakarta Sans"', 'system-ui', '-apple-system', 'sans-serif'],
                      "headline-lg-mobile": ["Fraunces", "Playfair Display", "serif"],
                      "body-lg": ["Inter", "Plus Jakarta Sans", "sans-serif"],
                      "label-caps": ["Inter", "Plus Jakarta Sans", "sans-serif"],
                      "numeric-stat": ["Fraunces", "Playfair Display", "serif"],
                      "headline-md": ["Fraunces", "Playfair Display", "serif"],
                      "body-md": ["Inter", "Plus Jakarta Sans", "sans-serif"],
                      "body-sm": ["Inter", "Plus Jakarta Sans", "sans-serif"],
                      "display-hero": ["Fraunces", "Playfair Display", "serif"],
                      "label-md": ["Inter", "Plus Jakarta Sans", "sans-serif"],
                      "subhead-lg": ["Inter", "Plus Jakarta Sans", "sans-serif"],
                      "headline-sm": ["Fraunces", "Playfair Display", "serif"],
                      "headline-lg": ["Fraunces", "Playfair Display", "serif"],
                      "display-hero-mobile": ["Fraunces", "Playfair Display", "serif"]
                    },
                    fontSize: {
                      "headline-lg-mobile": ["32px", { lineHeight: "40px", letterSpacing: "-0.01em", fontWeight: "600" }],
                      "body-lg": ["17px", { lineHeight: "28px", letterSpacing: "0em", fontWeight: "400" }],
                      "label-caps": ["11px", { lineHeight: "16px", letterSpacing: "0.12em", fontWeight: "700" }],
                      "numeric-stat": ["48px", { lineHeight: "52px", letterSpacing: "-0.02em", fontWeight: "700" }],
                      "headline-md": ["28px", { lineHeight: "36px", letterSpacing: "-0.01em", fontWeight: "600" }],
                      "body-md": ["15px", { lineHeight: "24px", letterSpacing: "0em", fontWeight: "400" }],
                      "body-sm": ["13px", { lineHeight: "20px", letterSpacing: "0.005em", fontWeight: "400" }],
                      "display-hero": ["64px", { lineHeight: "72px", letterSpacing: "-0.02em", fontWeight: "600" }],
                      "label-md": ["14px", { lineHeight: "20px", letterSpacing: "0.01em", fontWeight: "600" }],
                      "subhead-lg": ["20px", { lineHeight: "30px", letterSpacing: "-0.01em", fontWeight: "400" }],
                      "headline-sm": ["22px", { lineHeight: "30px", letterSpacing: "0em", fontWeight: "500" }],
                      "headline-lg": ["44px", { lineHeight: "52px", letterSpacing: "-0.02em", fontWeight: "600" }],
                      "display-hero-mobile": ["40px", { lineHeight: "48px", letterSpacing: "-0.015em", fontWeight: "600" }]
                    }
                  }
                }
              };
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
