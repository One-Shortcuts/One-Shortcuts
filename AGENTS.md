# Repository Guidelines

## Project Structure & Module Organization

This repository is a framework-free static HTML tool suite for retail store daily operations. The production entry point is `staff-tool.html`, which contains the launcher and all active tool views.

Supporting files:

- `deploy_ShortcutTools.sh` publishes `staff-tool.html` to the configured GitHub Gist.
- `.gist-id-shortcut` stores the target gist ID.
- `education-price.html`, `vat-refund.html`, `belkin-claim.html`, and `price-battle.html` are legacy/reference pages. Do not treat them as the active iOS Shortcut entry point unless the architecture changes.
- `README.md` and `CLAUDE.md` document workflow.

There is no build directory, package manager, or test suite.

## Build, Test, and Development Commands

- `open staff-tool.html` opens the app locally in the default browser on macOS.
- `bash -n deploy_ShortcutTools.sh` checks the deploy script syntax.
- `git diff --check` catches whitespace and patch formatting issues.
- `node -e "const fs=require('fs'); const html=fs.readFileSync('staff-tool.html','utf8'); for (const m of html.matchAll(/<script(?![^>]*src)[^>]*>([\\s\\S]*?)<\\/script>/gi)) new Function(m[1]); console.log('inline scripts parse ok')"` validates inline JavaScript parsing.
- `./deploy_ShortcutTools.sh` publishes the latest `staff-tool.html` to the gist. Requires authenticated `gh` CLI.

## Coding Style & Naming Conventions

Use plain HTML, CSS, and vanilla JavaScript. Keep styles and scripts inside `staff-tool.html` unless there is a strong reason to split files. Use two-space indentation. Prefer descriptive IDs and function names such as `renderPriceList`, `vatCalculate`, and `showView`.

Keep UI text in the `I18N` object and update both English and Thai strings together. Preserve the existing dark, iPhone-first visual style and CSS variable palette.

## Testing Guidelines

There is no automated test framework. Before deploy, validate:

- inline script parsing with the `node -e` command above
- shell syntax with `bash -n deploy_ShortcutTools.sh`
- whitespace with `git diff --check`
- manual Safari behavior for tool taps, language switching, VAT input, Education Price tabs, and Belkin QR rendering

## Commit & Pull Request Guidelines

Recent commits use short imperative summaries, for example `Fix single-page tool navigation` and `Restore education price table styling`. Keep commit messages focused on the behavior changed.

Pull requests should include a concise description, manual test notes, screenshots for UI changes, and the deployed gist URL when deployment is part of the change.

## Deployment Notes

iOS Shortcuts should open only the raw gist URL for `staff-tool.html`. Avoid linking the launcher to sibling raw HTML files; encoded/base64 Safari launches have previously rendered raw source instead of usable pages.
