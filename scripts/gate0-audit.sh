#!/usr/bin/env bash
# gate0-audit.sh: one plain-text report of everything worth checking before Wave 1.
# Run from the repo root:   bash gate0-audit.sh > audit.txt 2>&1
# Then paste audit.txt (or its contents) to Claude.
#
# Mostly read-only. It DOES run `just check` and `just freeze`, which write
# build output (dist/). It never prints file contents of untracked files,
# .env files, or secrets; it lists names only. Remote URLs are redacted.

export GIT_PAGER=cat PAGER=cat NO_COLOR=1 TERM=dumb LC_ALL=C.UTF-8 2>/dev/null

section() { printf '\n===== %s =====\n' "$1"; }

# run <max_lines> <cmd...>  : print command, last N lines of output, exit code
run() {
  local n="$1"; shift
  printf '$ %s\n' "$*"
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$out" | tail -n "$n"
  printf '[exit %s]\n' "$rc"
}

have() { command -v "$1" >/dev/null 2>&1; }

section "META"
date -u '+%Y-%m-%d %H:%M:%S UTC'
printf 'cwd: %s\n' "$PWD"
if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "NOT A GIT REPO. Run this from the repo root."; exit 1
fi
printf 'repo root: %s\n' "$(git rev-parse --show-toplevel)"
printf 'branch: %s\n' "$(git branch --show-current)"
printf 'tools: just=%s uv=%s gh=%s python=%s\n' \
  "$(have just && echo yes || echo NO)" "$(have uv && echo yes || echo NO)" \
  "$(have gh && echo yes || echo no)" "$(python3 --version 2>&1)"

section "GIT STATE"
run 80 git status --short
printf 'untracked count: %s\n' "$(git ls-files --others --exclude-standard | wc -l)"
run 15 git log --oneline --decorate -15
run 10 git tag --list
run 30 git diff --stat

section "REMOTE + VISIBILITY (urls redacted)"
git remote -v 2>&1 | sed -E 's#(https?://)[^/@]*@#\1***@#'
if have gh; then
  run 5 gh repo view --json visibility,url,isPrivate
else
  echo "gh not installed: check repo visibility manually on GitHub"
fi

section "docs/ai LAYOUT"
for f in README.md master-context.md orchestrator-prompt.md STATE.md NEEDS.md \
         RECON.md CONTRACT.md MOTION.md archive/OLD-VS-NEW.md \
         archive/master-context.old.md inputs/lyra-doodle-transparent.png \
         inputs/piiiiink-a11y.json; do
  if [ -e "docs/ai/$f" ]; then printf '  [ok]      docs/ai/%s\n' "$f"
  else printf '  [MISSING] docs/ai/%s\n' "$f"; fi
done
echo "-- everything under docs/ai (names only):"
find docs/ai -maxdepth 3 -not -path '*/.git/*' 2>/dev/null | sort | head -80
printf 'docs/ai tracked files: %s\n' "$(git ls-files docs/ai | wc -l)"
echo "-- docs/ai git status:"
git status --short docs/ai | head -40
echo "-- duplicate master-context copies (should be exactly one):"
find . -maxdepth 4 -iname 'master-context*.md' -not -path './.git/*' \
  -not -path './node_modules/*' -not -path './.venv/*' 2>/dev/null | sort
echo "-- leftover kit folder (should be absent or empty):"
ls -A lyra-portfolio-kit 2>/dev/null || echo "  (none)"

section "OLD-VS-NEW (first 60 lines; may quote your OLD master context, delete this section before pasting if it holds anything private)"
if [ -f docs/ai/archive/OLD-VS-NEW.md ]; then head -n 60 docs/ai/archive/OLD-VS-NEW.md
else echo "(no OLD-VS-NEW.md found)"; fi

section "STATE.md (first 50 lines)"
if [ -f docs/ai/STATE.md ]; then head -n 50 docs/ai/STATE.md; else echo "(no STATE.md found)"; fi

section "just check (last 70 lines)"
if have just; then run 70 just check; else echo "just not installed"; fi

section "just freeze + dist"
if have just; then run 25 just freeze; else echo "just not installed"; fi
if [ -d dist ]; then
  echo "-- dist tree (depth 2):"
  find dist -maxdepth 2 | sort | head -60
  echo "-- expected outputs:"
  for pat in 'index.html' '404.html' 'resume*' 'cv*' 'sitemap*' '*rss*' 'robots.txt'; do
    n=$(find dist -iname "$pat" 2>/dev/null | wc -l)
    printf '  %-14s %s match(es)\n' "$pat" "$n"
  done
else
  echo "(no dist/ directory)"
fi

section "CONTRAST MATRIX + TODOs"
if [ -f scripts/check_contrast.py ] && have uv; then run 40 uv run python scripts/check_contrast.py
else echo "(scripts/check_contrast.py or uv missing)"; fi
if [ -f scripts/check_todos.py ] && have uv; then run 40 uv run python scripts/check_todos.py
else echo "(scripts/check_todos.py or uv missing)"; fi

section "PROJECT FILE MAP (names only)"
find src content scripts tests -maxdepth 3 -type f \
  -not -name '*.pyc' -not -path '*/__pycache__/*' 2>/dev/null | sort | head -150

section "PRIVACY LEAK CHECKS (file names only, never matched text)"
echo "-- private terms in public-facing sources / docs (expect NOTHING):"
git grep -I -i -l -E 'raizen|arriola|jeremy' -- src content docs/ai/master-context.md 2>/dev/null | head -20
echo "-- private terms in built output (expect NOTHING):"
[ -d dist ] && grep -rIil -E 'raizen|arriola|jeremy' dist 2>/dev/null | head -20
echo "-- possible secrets in tracked files (expect NOTHING):"
git grep -I -l -E 'AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|(api[_-]?key|secret|token)[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{12,}' 2>/dev/null | head -20
echo "-- tracked .env files (expect only .env.example):"
git ls-files | grep -E '(^|/)\.env' | head
echo "-- global-context leakage hints in repo (expect NOTHING):"
git grep -I -l -E '\.config/lyra|agy-context' 2>/dev/null | head -10

section "END (paste everything above to Claude)"
printf 'lines in this report: see: wc -l audit.txt\n'