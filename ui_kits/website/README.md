# ABSOLUT Sport — Website UI Kit

## Overview
Interactive click-through prototype of the **absolut-sport.com.br** website.
Built with React + Babel. No backend — all data is static.

## Design Width
**1280px** desktop-first. Not yet responsive (mobile breakpoints TBD).

## Screens
| Screen | How to reach |
|--------|-------------|
| **Home** | Default / click logo |
| **Eventos** | Nav → Eventos, or "Ver Todos os Eventos" CTA |
| **Event Detail** | Click any event card |
| **Sobre Nós** | Nav → Sobre Nós |

## Components (Components.jsx)
| Component | Description |
|-----------|-------------|
| `Logo` | Wordmark + mark lockup. Props: `dark`, `size` |
| `LogoMark` | SVG mark only. Props: `size`, `dark` |
| `Badge` | Status pill. Variants: `red`, `gold`, `white`, `success` |
| `Button` | CTA button. Variants: `primary`, `secondary`, `gold`, `ghost`. Sizes: `sm`, `md`, `lg` |
| `Navbar` | Sticky top nav with active state + CTA |
| `StatStrip` | "+500 Eventos, +10K Viagens" strip |
| `EventCard` | Event package card with hover animation |
| `FeatureList` | Benefit list with red check icons |
| `Footer` | Full footer with columns + CONMEBOL badge |

## Tokens (../../colors_and_type.css)
All CSS vars defined at project root. Key vars:
- `--color-red: #E3001B`
- `--color-gold: #C9A84C`
- `--font-display: 'Barlow Condensed'`
- `--font-body: 'Barlow'`

## Persistence
Current page is stored in `localStorage` under key `as_page` — refresh preserves navigation state.
