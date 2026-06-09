#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
gist_id_file="$repo_root/.gist-id-shortcut"
files=(
  "$repo_root/staff-tool.html"
  "$repo_root/price-battle.html"
  "$repo_root/education-price.html"
  "$repo_root/vat-refund.html"
  "$repo_root/belkin-claim.html"
)

for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    printf 'Missing file: %s\n' "$file" >&2
    exit 1
  fi
done

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
  create_output="$(gh gist create "${files[@]}" -d "One Shortcut tools" -p)"
  gist_ref="${create_output##*/}"
  printf '%s\n' "$gist_ref" > "$gist_id_file"
else
  gist_id="${gist_ref##*/}"
  for file in "${files[@]}"; do
    gh gist edit "$gist_id" --filename "$(basename "$file")" "$file"
  done
fi

gist_id="${gist_ref##*/}"
owner="$(gh api user --jq .login)"
raw_base="https://gist.githubusercontent.com/$owner/$gist_id/raw"

printf '\nPublished gist: %s\n' "$gist_id"
printf 'Raw URLs:\n'
printf '  staff-tool.html      %s/staff-tool.html\n' "$raw_base"
printf '  price-battle.html    %s/price-battle.html\n' "$raw_base"
printf '  education-price.html  %s/education-price.html\n' "$raw_base"
printf '  vat-refund.html      %s/vat-refund.html\n' "$raw_base"
printf '  belkin-claim.html    %s/belkin-claim.html\n' "$raw_base"
