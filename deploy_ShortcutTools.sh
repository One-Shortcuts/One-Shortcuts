#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
gist_id_file="$repo_root/.gist-id-shortcut"
file="$repo_root/staff-tool.html"

if [[ ! -f "$file" ]]; then
  printf 'Missing file: %s\n' "$file" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  printf 'gh CLI is required. Install it and run gh auth login first.\n' >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  printf 'gh is not authenticated. Run gh auth login first.\n' >&2
  exit 1
fi

gist_ref=""
if [[ -f "$gist_id_file" ]]; then
  gist_ref="$(tr -d '[:space:]' < "$gist_id_file" || true)"
fi

if [[ -z "$gist_ref" ]]; then
  create_output="$(gh gist create "$file" -d "One Shortcut tools" -p)"
  gist_ref="${create_output##*/}"
  printf '%s\n' "$gist_ref" > "$gist_id_file"
else
  gist_id="${gist_ref##*/}"
  for legacy in price-battle.html education-price.html vat-refund.html belkin-claim.html; do
    gh gist edit "$gist_id" --remove "$legacy" >/dev/null 2>&1 || true
  done
  gh gist edit "$gist_id" --filename "$(basename "$file")" "$file"
fi

gist_id="${gist_ref##*/}"
owner="$(gh api user --jq .login)"
raw_base="https://gist.githubusercontent.com/$owner/$gist_id/raw"

printf '\nPublished gist: %s\n' "$gist_id"
printf 'Raw URLs:\n'
printf '  staff-tool.html      %s/staff-tool.html\n' "$raw_base"
