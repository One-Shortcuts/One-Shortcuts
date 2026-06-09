# CLAUDE.md

This file gives working guidance for this repository.

## Project

**One Shortcut** is a set of standalone HTML tools for retail store daily operations.

The launcher is `staff-tool.html`. Each tool has its own HTML file and is published together into one GitHub Gist. iOS Shortcuts should open the raw gist URL in Safari.

## Files

```
/
├── staff-tool.html
├── price-battle.html
├── education-price.html
├── vat-refund.html
├── belkin-claim.html
├── deploy_ShortcutTools.sh
├── .gist-id-shortcut
└── README.md
```

## Architecture

- Pure static HTML, CSS, and vanilla JavaScript.
- No build step and no package manager.
- The launcher derives sibling tool URLs from its own raw gist URL by replacing the filename after `/raw/`.
- `price-battle.html` is a hub page that opens the legacy Price Battle and Domestic Price Battle gist URLs.
- Tool pages use the same pattern for a back link to `staff-tool.html`.
- One external dependency remains: `QRCode.js` from cdnjs for the Belkin claim page.

## Deployment

Run `./deploy_ShortcutTools.sh` from the repo root.

Requirements:
- `gh` CLI installed
- authenticated GitHub session via `gh auth login`

The script publishes all five HTML files into one public gist, stores the gist ID in `.gist-id-shortcut`, and prints the raw URLs for each page.

## Visual style

- Dark Apple-like palette
- iOS-friendly spacing and sticky headers where needed
- Use the existing CSS variable style if you extend a page

## Behavioral expectations

- `staff-tool.html` is only a launcher.
- Each tool page should work when opened directly from a raw gist URL or locally from the repo folder.
- Keep the content self-contained and avoid external app dependencies unless already required.
