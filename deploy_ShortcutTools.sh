#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_owner="${PAGES_REPO_OWNER:-}"
repo_name="${PAGES_REPO_NAME:-One-Shorcut}"
branch="${PAGES_REPO_BRANCH:-main}"
description="One Shortcut tools GitHub Pages"
html_files=(
  index.html
  staff-tool.html
  price-battle.html
  highlight.html
  support.html
  other.html
  edu-price.html
  education-price.html
  vat-refund.html
  belkin-claim.html
)

if ! command -v gh >/dev/null 2>&1; then
  printf 'gh CLI is required. Install it and run gh auth login first.\n' >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  printf 'gh is not authenticated. Run gh auth login first.\n' >&2
  exit 1
fi

if [[ -z "$repo_owner" ]]; then
  repo_owner="$(gh api user --jq .login)"
fi

deploy_repo="$repo_owner/$repo_name"

for file in "${html_files[@]}"; do
  if [[ ! -f "$repo_root/$file" ]]; then
    printf 'Missing deployable file: %s\n' "$file" >&2
    exit 1
  fi
done

if ! gh repo view "$deploy_repo" >/dev/null 2>&1; then
  gh repo create "$deploy_repo" --public --description "$description" --disable-issues --disable-wiki
fi

workdir="$(mktemp -d "${TMPDIR:-/tmp}/one-shorcut-pages.XXXXXX")"
trap 'rm -rf "$workdir"' EXIT

git clone "https://github.com/$deploy_repo.git" "$workdir" >/dev/null 2>&1

cd "$workdir"
git checkout -B "$branch" >/dev/null 2>&1
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +

for file in "${html_files[@]}"; do
  cp "$repo_root/$file" "$workdir/$file"
done

git add .

if git diff --cached --quiet; then
  printf 'No changes to deploy.\n'
else
  git commit -m "Deploy: $(date +%Y-%m-%d\ %H:%M)" >/dev/null
  git push -u origin "$branch" >/dev/null
fi

if ! gh api "repos/$deploy_repo/pages" >/dev/null 2>&1; then
  gh api --method POST "repos/$deploy_repo/pages" -f "source[branch]=$branch" -f 'source[path]=/' >/dev/null
fi

pages_url="https://$repo_owner.github.io/$repo_name/"

printf '\nPublished GitHub Pages repo: %s\n' "$deploy_repo"
printf 'Pages URL:\n'
printf '  %s\n' "$pages_url"
