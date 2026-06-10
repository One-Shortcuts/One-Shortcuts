# Repository Guidelines

## Project Structure & Module Organization

This repository is a framework-free static HTML tool suite for retail store daily operations. The production deployment is the public GitHub Pages repo `i3udokai/One-Shorcut`, served at `https://i3udokai.github.io/One-Shorcut/`.

The local source entry point is `staff-tool.html`, which contains the launcher and most active tool views. The GitHub Pages entry point is `index.html`, which redirects to `staff-tool.html`.

Supporting files:

- `deploy_ShortcutTools.sh` publishes deployable `.html` files to the public `i3udokai/One-Shorcut` GitHub Pages repo and enables Pages from the repo root when needed.
- `price-battle.html` is a same-site production page opened by the launcher.
- `education-price.html`, `vat-refund.html`, `belkin-claim.html`, `highlight.html`, `support.html`, `other.html`, and `edu-price.html` are deployable standalone/reference pages. Keep `noindex` tags in public HTML.
- `README.md` and `CLAUDE.md` document workflow.
- `.gist-id-shortcut` is a legacy Gist artifact and is not part of the current deployment flow.

There is no build directory, package manager, or test suite.

## Build, Test, and Development Commands

- `open staff-tool.html` opens the app locally in the default browser on macOS.
- `bash -n deploy_ShortcutTools.sh` checks the deploy script syntax.
- `git diff --check` catches whitespace and patch formatting issues.
- `node -e "const fs=require('fs'); const html=fs.readFileSync('staff-tool.html','utf8'); for (const m of html.matchAll(/<script(?![^>]*src)[^>]*>([\\s\\S]*?)<\\/script>/gi)) new Function(m[1]); console.log('inline scripts parse ok')"` validates inline JavaScript parsing.
- `./deploy_ShortcutTools.sh` publishes deployable HTML files to the public GitHub Pages repo. Requires authenticated `gh` CLI.

## Coding Style & Naming Conventions

Use plain HTML, CSS, and vanilla JavaScript. Keep styles and scripts inside `staff-tool.html` unless there is a strong reason to split files. Use two-space indentation. Prefer descriptive IDs and function names such as `renderPriceList`, `vat_calculate`, and `showScreen`.

Keep bilingual UI text in matching `data-en` and `data-th` attributes where the current language system uses them. Preserve the existing iPhone-first visual style and CSS variable palette.

## Testing Guidelines

There is no automated test framework. Before deploy, validate:

- inline script parsing with the `node -e` command above
- shell syntax with `bash -n deploy_ShortcutTools.sh`
- whitespace with `git diff --check`
- manual Safari behavior for tool taps, language switching, VAT input, Education Price tabs, and Belkin QR rendering
- after deployment, confirm `https://i3udokai.github.io/One-Shorcut/` returns HTTP 200 and the GitHub Pages status is built

## Commit & Pull Request Guidelines

Recent commits use short imperative summaries, for example `Fix single-page tool navigation` and `Restore education price table styling`. Keep commit messages focused on the behavior changed.

Pull requests should include a concise description, manual test notes, screenshots for UI changes, and the deployed GitHub Pages URL when deployment is part of the change.

## Deployment Notes

iOS Shortcuts should open `https://i3udokai.github.io/One-Shorcut/` directly. Do not Base64-encode the page for Shortcuts.

The public Pages repo should contain only deployable HTML files. Do not push this private source repo, docs, shell scripts, or git metadata into the public Pages repo.

Avoid raw Gist fetch/document-write navigation for internal tools. Embedded tools should use `showScreen(...)`; separate tools should open as same-site Pages files, such as `price-battle.html`.

All public HTML should include:

```html
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">
```
