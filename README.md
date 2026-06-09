# One Shortcut

Retail store daily operation tools for Apple Retail Thailand.

## Files

- `staff-tool.html` - single-file launcher and tool views
- `deploy_ShortcutTools.sh` - publish `staff-tool.html` to one gist

## Workflow

1. Edit the HTML files locally.
2. Run `./deploy_ShortcutTools.sh`.
3. Use the printed raw gist URL for `staff-tool.html` in the iOS Shortcut.
4. Open the launcher in Safari from Shortcuts.

## Notes

- `staff-tool.html` contains the launcher, Price Battle hub, Education Price, VAT Refund, and Belkin claim views.
- The iOS Shortcut should open only `staff-tool.html`.
- The repo is intentionally framework-free and uses only static HTML/CSS/JS.
