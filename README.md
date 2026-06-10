# One Shortcut

Retail store daily operation tools for Apple Retail Thailand.

## Files

- `index.html` - GitHub Pages entry point that redirects to `staff-tool.html`
- `staff-tool.html` - single-file launcher and tool views
- `price-battle.html` - same-site Price Battle page for GitHub Pages
- `deploy_ShortcutTools.sh` - legacy helper to publish `staff-tool.html` to one gist

## Workflow

1. Edit the HTML files locally.
2. Push the repo to GitHub.
3. Enable GitHub Pages for the repo branch.
4. Use the GitHub Pages URL in the iOS Shortcut.

For the old Gist workflow, run `./deploy_ShortcutTools.sh` and use the printed raw gist URL for `staff-tool.html`.

## Notes

- `staff-tool.html` contains the launcher, Price Battle hub, Education Price, VAT Refund, and Belkin claim views.
- The iOS Shortcut should open the GitHub Pages URL, not a Base64-encoded copy.
- Pages include `noindex` meta tags to discourage search indexing. This is not access control.
- The repo is intentionally framework-free and uses only static HTML/CSS/JS.
