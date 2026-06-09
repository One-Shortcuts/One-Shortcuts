# CLAUDE.md

This file gives working guidance for this repository.

## Project

**One Shortcut** is a single HTML launcher that contains the retail store daily operation tools.

The only entry point is `staff-tool.html`. iOS Shortcuts should open the raw gist URL in Safari.

## Files

```
/
├── staff-tool.html
├── deploy_ShortcutTools.sh
├── .gist-id-shortcut
└── README.md
```

## Architecture

- Pure static HTML, CSS, and vanilla JavaScript.
- No build step and no package manager.
- All tool views live inside `staff-tool.html` and switch without leaving the page.
- Price Battle still opens the legacy comparison sheets, but from inside the single launcher page.
- One external dependency remains: `QRCode.js` from cdnjs for the Belkin claim page.

## Deployment

Run `./deploy_ShortcutTools.sh` from the repo root.

Requirements:
- `gh` CLI installed
- authenticated GitHub session via `gh auth login`

The script publishes `staff-tool.html` into one public gist, stores the gist ID in `.gist-id-shortcut`, and prints the raw URL for the launcher.

## Visual style

- Dark Apple-like palette
- iOS-friendly spacing and sticky headers where needed
- Use the existing CSS variable style if you extend a page

## Behavioral expectations

- `staff-tool.html` is the launcher and the tool container.
- The page should work when opened directly from a raw gist URL or locally from the repo folder.
- Keep the content self-contained and avoid external app dependencies unless already required.
