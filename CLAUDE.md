# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Antigravity — EasyPlay

A staff tool for Apple Retail Thailand, built as a single self-contained HTML file deployed via iOS Shortcuts "Show Web Page" action. No server, no build step, no package manager.

**App name:** EasyPlay (previously "Staff Tool")  
**Owner:** Wan — Lead ISE (In-Store Experience), Apple Retail Thailand

---

## File structure

```
/
├── staff-tool.html           active file — primary deliverable
├── deploy_ShortcutTools.sh   active deploy script
├── .gist-id-shortcut         gist ID for staff-tool.html
├── CLAUDE.md
├── archive/
│   ├── index.html            original Price List (source reference only)
│   ├── VAT Refun.html        original VAT Calculator (source reference only)
│   ├── deploy_PriceList.sh   legacy deploy script for index.html
│   └── .gist-id              gist ID for index.html
├── docs/
│   ├── Implement.md          original planning document
│   ├── antigravity-staff-tool-context.md  project context reference
│   └── Price List.xlsx       source pricing data
└── scratch/
    ├── integrate_vat.py
    └── integrate_vat_robust.py
```

All development happens in **`staff-tool.html`**.

---

## Architecture

Single HTML file: all CSS in `<style>`, all JS in `<script>`, all data embedded as JS constants. No external frameworks. One external CDN dependency: `QRCode.js` from cdnjs (used for the Belkin claim QR code).

**Screen navigation:** `showScreen('screen-id')` — hides all `<div>` sections, shows the target, scrolls to top. No page reloads. When navigating to `screen-edu-price`, also calls `syncColHeader()` via `requestAnimationFrame` to pin the column header below the sticky tab bar.

**App structure:**
```
Landing Menu
├── 1.1 Education Price   — dynamic product dashboard (Mac/iPad/Watch/Accessories/Display)
├── 1.2 VAT Refund        — airport VAT refund calculator
├── 1.3 Tech Spec         — external link
├── 2.1 APU & Online Order — external link
└── 2.2 Claim Belkin      — QR code + external link
```

**External links:** use `window.location.href` in the HTML file context; use `window.open(url, '_blank')` when running as a hosted artifact.

**Visual design:** Dark theme matching Apple's iOS dark mode palette — `#000` background, `#1c1c1e` surface cards, `rgba(255,255,255,0.1)` borders. All inner screens use `.sticky-header` with `backdrop-filter: blur` pinned at top. Accent colors: `#0a84ff` (blue), `#30d158` (green), `#ff9f0a` (education orange).

---

## VAT Refund logic

- `total < ฿2,000` → not eligible
- `฿2,000 – ฿199,999` → lookup `vat_priceRanges` table
- `total >= ฿200,000` → `total * 0.061` (6.1% flat rate)

---

## Versioning

`const VERSION = 'vX.X'` is declared at the top of the `<script>` block. On every launch, the app fetches the live gist raw URL with `cache: 'no-store'`, extracts the VERSION via regex, and shows an orange dismissible banner if it differs from the embedded version.

- **Version check URL:** `https://gist.githubusercontent.com/i3udokai/f98d4345a77ce9d8b919c4f3047a5a1f/raw/staff-tool.html`
- To release an update: bump `VERSION` and run `./deploy_ShortcutTools.sh`
- Network failure is silent — the tool works offline

---

## Price List data

Product data is embedded as a JS constant (`priceData`). Categories (tab order): MacBook, Mac Desktop, iPad, Apple Watch, Accessories, Display.

`priceData` mirrors `archive/index.html`'s `data` object exactly (key `'Mac Desktop'` instead of `'MacDesktop'` to match tab buttons). Notable fields:
- `adapterTo` — triggers adapter display in the detail panel (not `adapterFrom`)
- `nanoPrice` / `nanoEdu` — optional Nano-Texture add-on pricing (MacBook Pro, iMac)
- `acEdu` — AppleCare+ EDU price; present on all Watch models

**Education Price screen layout:**
- Sticky blur header with category tabs
- Sticky 6-column header row below tabs (`.col-header`): Model / Regular / EDU ✦ / AC+ / AC+ EDU / Save
- `syncColHeader()` measures the tab header's `offsetHeight` at render time and sets `col-header` `top` dynamically
- `renderPriceList()` generates 6-column `.row` elements; tapping a row toggles `.detail` inline below it
- Configuration badges on row labels: **Cell** (green), **Nano** (blue)
- Detail cards are color-coded: Education (orange), Savings (green), AppleCare+ (blue)
- Detail includes "With Nano-Texture Display" compare table (when `nanoPrice` present) and "With AppleCare+" compare table
- Responsive: on narrow viewports the 6-column grid collapses to 2-column with labelled cells; `.col-header` is hidden

---

## Deployment

Requires: `gh` CLI (`brew install gh && gh auth login`)

| Script | Deploys | Gist ID stored in |
|---|---|---|
| `./deploy_ShortcutTools.sh` | `staff-tool.html` | `.gist-id-shortcut` |
| `archive/deploy_PriceList.sh` | `archive/index.html` | `archive/.gist-id` |

**`deploy_ShortcutTools.sh`** is the active deploy script. Run it from the project root after editing `staff-tool.html`. It prints a timestamped Raw URL to paste into the iOS Shortcut's "Get Contents of URL" action.

**iOS Shortcut setup:**
1. "Get Contents of URL" → Gist Raw URL
2. "Show Web Page" → connected to step 1 output
3. Add to Home Screen for app-like experience
