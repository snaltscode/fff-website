---
name: Founder-to-Founder Fintech
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daef'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8fd'
  surface-container-highest: '#dce2f7'
  on-surface: '#141b2b'
  on-surface-variant: '#3f4942'
  inverse-surface: '#293040'
  inverse-on-surface: '#edf0ff'
  outline: '#6f7a72'
  outline-variant: '#bec9c0'
  surface-tint: '#096c49'
  primary: '#005034'
  on-primary: '#ffffff'
  primary-container: '#046a47'
  on-primary-container: '#92e7bb'
  inverse-primary: '#83d7ac'
  secondary: '#735c00'
  on-secondary: '#ffffff'
  secondary-container: '#fed65b'
  on-secondary-container: '#745c00'
  tertiary: '#064f39'
  on-tertiary: '#ffffff'
  tertiary-container: '#28674f'
  on-tertiary-container: '#a2e3c5'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9ff4c7'
  primary-fixed-dim: '#83d7ac'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005235'
  secondary-fixed: '#ffe088'
  secondary-fixed-dim: '#e9c349'
  on-secondary-fixed: '#241a00'
  on-secondary-fixed-variant: '#574500'
  tertiary-fixed: '#aff0d2'
  tertiary-fixed-dim: '#94d4b6'
  on-tertiary-fixed: '#002115'
  on-tertiary-fixed-variant: '#0a513b'
  background: '#f9f9ff'
  on-background: '#141b2b'
  surface-variant: '#dce2f7'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-tablet: 2rem
  margin-desktop: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes a high-trust, modern consumer fintech aesthetic tailored specifically for a founder-to-founder ecosystem. The brand personality blends institutional reliability with entrepreneurial agility: polished, confident, approachable, and razor-focused on execution.

The visual mood draws direct inspiration from high-growth modern fintech platforms:
- **Clean Minimalism:** Open breathing room, crisp white foundations, structured informational hierarchy, and minimal visual noise.
- **Purposeful Color Economy:** Deep emerald green is treated with surgical restraint—strictly reserved for key conversions, status indicators, and pill badges—preventing visual fatigue and maintaining high conversion clarity.
- **Heritage Distinction:** A dedicated metallic gold accent is reserved exclusively for the signature knot emblem mark, imbuing the brand with discreet prestige and trust without bleeding into utilitarian UI controls.
- **Mobile-First Ergonomics:** Touch targets, thumb-accessible sheet interactions, and fluid typographic scaling ensure a native-app-like mobile browser experience.

## Colors

The palette is engineered around clean whites and soft grey structural layers, highlighted by deep emerald and a prestige gold touchpoint.

- **Primary (`#046A47`):** Deep Emerald Green. Used selectively for primary action buttons, verified indicators, active navigational states, and focus halos.
- **Secondary (`#D4AF37`):** Warm Prestige Gold. Exclusively applied to the knot insignia, luxury milestone seals, and membership badges. Never used for standard text or generic interactive buttons.
- **Tertiary (`#054E38`):** Deep Forest Shadow. Serves as dark-mode contrast accents, dark hero containers, footer banners, and pressed button states.
- **Neutral Dark (`#111827`):** Primary headline and body typography color, providing crisp contrast without harsh pure black. Secondary copy uses `#4B5563`.
- **Surfaces & Backgrounds:**
  - Base canvas: `#FFFFFF`
  - Subtle layer container: `#F8F9FA`
  - Elevated card background: `#F4F5F7`
  - Hairline borders: `#E5E7EB`

## Typography

The typographic hierarchy pairs **Plus Jakarta Sans** for prominent headings with **Inter** for UI, numerical data, and body copy.

- **Plus Jakarta Sans** introduces subtle geometric warmth, distinct friendly apertures, and punchy modern weights (700 and 800) ideal for high-impact fintech proposition headers and metric figures.
- **Inter** handles high-density data, tabular financial numbers, button labels, and transactional lists with neutral legibility and rigorous vertical alignment.
- **Scaling Rules:** Mobile viewport headers (`< 640px`) automatically downscale using `-mobile` definitions to maintain comfortable two-line wraps on typical devices without horizontal overflow.

## Layout & Spacing

A mobile-first fluid grid approach anchors the layout:
- **Mobile (`< 640px`):** 4-column layout, `1rem` outer canvas padding, `1rem` column gutters. Components span full width (4 columns) or stack in pairs (2 columns) for key metric pairs.
- **Tablet (`640px – 1024px`):** 8-column layout, `2rem` margins, `1.25rem` gutters.
- **Desktop (`> 1024px`):** 12-column layout max-width constrained to `1200px`, centered with `3rem` margins and `1.5rem` gutters.

Vertical rhythm relies on multiples of `8px` (`0.5rem`). Sections maintain generous vertical padding (`3rem` to `4rem` on mobile, `5rem` to `6rem` on desktop) to evoke an airy, premium finish.

## Elevation & Depth

Visual hierarchy uses **tonal layer stacking** accented by soft, tinted ambient shadows:

- **Level 0 (Canvas):** Crisp `#FFFFFF` base or solid `#F8F9FA` alternate backdrop.
- **Level 1 (Card & Module Surface):** Surface fill `#FFFFFF` over `#F8F9FA` canvas with hairline boundary (`1px solid #E5E7EB`). Ambient elevation: `0 4px 20px -2px rgba(17, 24, 39, 0.04)`.
- **Level 2 (Interactive Floating Elements & Modals):** `0 12px 32px -4px rgba(4, 106, 71, 0.08), 0 4px 12px -2px rgba(17, 24, 39, 0.05)`. A slight green-tinted undertone keeps elevated surfaces grounded in the brand colorway.
- **Level 3 (Sticky Navigation & Bottom Sheets):** Semi-transparent `#FFFFFF` (90% opacity) with `backdrop-filter: blur(12px)` and a subtle bottom hairline divider (`#E5E7EB`).

## Shapes

The design system embraces a friendly, pill-influenced fintech curvature:
- **Cards & Visual Containers:** `16px` (`rounded-lg`) on mobile devices, transitioning up to `24px` (`rounded-xl`) for featured containers and hero showcase cards.
- **Buttons & Interactive Badges:** `9999px` (full pill shape) for callouts, micro-badges, icon wrappers, and primary CTAs, matching consumer-grade mobile friendliness.
- **Input Fields & Small Controls:** `12px` to `16px` corner curvature, delivering a soft, non-intrusive container feel.

## Components

### Buttons
- **Primary:** Full pill border radius (`rounded-full`), background `#046A47`, text `#FFFFFF`, font weight `600`. Hover/active transforms subtly to `#054E38`.
- **Secondary / Ghost:** White background `#FFFFFF`, subtle outline `1px solid #E5E7EB`, text `#111827`. Hover displays `#F8F9FA`.
- **Accent Link:** Emerald `#046A47` text with an accompanying right-facing directional chevron.

### Badges & Pill Chips
- **Feature Badges:** Subtle emerald tint background (`rgba(4, 106, 71, 0.08)`), emerald `#046A47` typography, `12px` font size with uppercase letter spacing, accompanied by a small green live status dot.
- **Membership / Emblem Badges:** Gold border (`#D4AF37`) with faint gold sheen background (`rgba(212, 175, 55, 0.08)`), reserved for founder tier status or the brand knot emblem mark.

### Cards
- **Content Cards:** Flat white `#FFFFFF` surface placed on `#F8F9FA` page sections, framed with `1px solid #E5E7EB` and rounded to `16px` or `20px`.
- **Feature Icon Wells:** Squircle or circle containers sized `40px` to `48px`, filled with muted emerald tint (`rgba(4, 106, 71, 0.1)`) housing `#046A47` stroke icons.

### Inputs & Form Elements
- **Field Styling:** Height `48px` to `52px` for mobile tap ease, background `#F8F9FA`, border `1px solid #E5E7EB`, rounded to `12px`.
- **Focus State:** Transitions to `#FFFFFF` background, solid emerald border (`#046A47`), and a soft `3px` glow (`rgba(4, 106, 71, 0.15)`).

### Bottom Sheet & Mobile App Bar
- Bottom sticky navigation or action bar featuring `#FFFFFF` with glassmorphic backdrop blur, ensuring high-frequency founder actions stay directly under thumb reach.