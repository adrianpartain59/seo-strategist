#!/usr/bin/env bash
# Smoke tests: scripts compile, the fixture lints with 0 errors, a broken copy is caught, the report builds.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; K="$HERE/../skills/seo-strategist/scripts"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
python3 -m py_compile "$K"/*.py
cp -R "$HERE/fixtures/example.com" "$TMP/site"
python3 "$K/lint_plans.py" "$TMP/site" > "$TMP/lint.txt" || { cat "$TMP/lint.txt"; echo "FAIL: clean fixture has lint errors"; exit 1; }
sed -i.bak 's/The number grows on the home screen\./The number grows — fast!/' "$TMP/site/plans/habit-streak-tracker.md"
if python3 "$K/lint_plans.py" "$TMP/site" > "$TMP/lint2.txt"; then echo "FAIL: dash and ! not caught"; exit 1; fi
grep -q "em dash" "$TMP/lint2.txt" && grep -q "exclamation" "$TMP/lint2.txt"
python3 "$K/build_report.py" "$TMP/site" >/dev/null
test -s "$TMP/site/index.html" && test -s "$TMP/site/plans/habit-streak-tracker.html"
echo "ok: all smoke tests passed"
