# One Shortcut

Retail store daily operation tools for Apple Retail Thailand.

## Files

- `staff-tool.html` - launcher page
- `price-battle.html` - price comparison hub
- `education-price.html` - education pricing lookup
- `vat-refund.html` - VAT refund calculator
- `belkin-claim.html` - Belkin screen claim QR page
- `deploy_ShortcutTools.sh` - publish all HTML files to one gist

## Workflow

1. Edit the HTML files locally.
2. Run `./deploy_ShortcutTools.sh`.
3. Use the printed raw gist URL for `staff-tool.html` in the iOS Shortcut.
4. Open the launcher in Safari from Shortcuts.

## Notes

- Each tool is a standalone HTML file.
- `price-battle.html` is the hub for the split Price Battle tools.
- The launcher derives sibling tool URLs from the same raw gist base.
- The repo is intentionally framework-free and uses only static HTML/CSS/JS.
