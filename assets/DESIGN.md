# Profile design system

This repository is a **GitHub-native engineering portfolio**, not a generic GitHub stats template. The README is the entry point; SVG files in `assets/` are versioned artwork.

## Design intent

- **Editorial engineering:** clear typography, precise spacing, signal/trace motifs, deliberate color accents
- **Evidence over hype:** distinguish production platforms, reproducible software tests and work that still requires physical validation
- **No third-party image renderers:** portfolio artwork resolves from this repository; avoid external analytics cards and counters that can disappear or mislead
- **Light and dark themes:** `hero-*.svg` and `engineering-map-*.svg` are theme-paired; project cards use a consistent dark surface for brand continuity
- **Accessible fallbacks:** every README image has alt text, artwork includes a title or `aria-label`, and important content exists as selectable README text

## Visual tokens

| Usage | Dark | Light |
| --- | --- | --- |
| Background | `#0A1524` | `#F6F8FB` |
| Main ink | `#F1F7FF` | `#15273B` |
| Accent / software | `#65C8FF` | `#136CAC` |
| Accent / embedded | `#7BE7D3` | `#098D82` |
| Accent / agent systems | `#F1BD79` | `#B77934` |
| Muted text | `#A1BBCE` | `#50677C` |

Project-card accent hues are intentionally different to aid scanning; all share one geometry and footer treatment.

## Components

| File | Purpose |
| --- | --- |
| `hero-dark.svg`, `hero-light.svg` | Branded portfolio cover |
| `engineering-map-dark.svg`, `engineering-map-light.svg` | Three capability pipelines, not a real network topology |
| `card-*.svg` | Selected project artwork |
| `signal-footer.svg` | Signature engineering motif |

## Content maintenance

When a project changes, update its README description and status only after checking its public source-of-truth. A prototype must not silently become a deployed product. Keep project links stable; avoid fabricated activity, test, uptime or user-count claims.

Run `python scripts/check_profile_assets.py` before committing. The `profile-quality.yml` workflow validates local SVG references, XML, responsive viewBoxes, accessibility labels and external SVG dependencies.

GitHub Markdown controls layout and does not provide custom CSS media queries. The two-column project table is designed to be readable on typical desktop widths; all information remains available as text and links.
