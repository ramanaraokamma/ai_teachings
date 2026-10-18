#!/usr/bin/env bash
set -euo pipefail
week_arg="${1:?Pass a week number or lesson ID such as ai-2/1}"
if [[ "$week_arg" == */* ]]; then level_id="${week_arg%/*}"; week_number="${week_arg##*/}"; else level_id="ai-1"; week_number="$week_arg"; fi
[[ "$week_number" =~ ^[0-9]+$ ]] || exit 64
[[ "$level_id" =~ ^(ai-[1-7]|python-bridge)$ ]] || exit 64
lesson_id="${level_id}/${week_number}"
if [[ "$level_id" == "ai-1" ]]; then report_prefix="week${week_number}"; else report_prefix="${level_id}-week${week_number}"; fi
export CONNECTED_LEVEL="$level_id"
# Local builds parse the complete curriculum; keep explicit caller options.
export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=8192}"
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"
log_dir="work/week1-presentation"
mkdir -p "$log_dir"
export ACADEMY_PLAYWRIGHT_MODULE="${ACADEMY_PLAYWRIGHT_MODULE:-file://${root_dir}/work/render-tools/node_modules/playwright-core/index.mjs}"
python3 tools/sync_connected_labs.py "$lesson_id" > "$log_dir/${report_prefix}-labs.log" 2>&1
python3 tools/render_programme.py > "$log_dir/${report_prefix}-render.log" 2>&1
CHECK_WEEKS="${lesson_id}" work/curriculum-python/bin/python tools/export_word.py > "$log_dir/${report_prefix}-word.log" 2>&1
node tools/export_formatted_week.mjs "${lesson_id}" > "$log_dir/${report_prefix}-pdf.log" 2>&1
node scripts/import-complete-programme.mjs --root > "$log_dir/${report_prefix}-import.log" 2>&1
node tests/connected-workbook-keys.mjs > "$log_dir/${report_prefix}-keys.log" 2>&1
npm run build > "$log_dir/${report_prefix}-build.log" 2>&1
CONNECTED_WEEK="$week_number" node --loader ./tests/cloudflare-loader.mjs tests/connected-week-browser.mjs > "$log_dir/${report_prefix}-browser.log" 2>&1
node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs > "$log_dir/${report_prefix}-access.log" 2>&1
python3 tools/validate_content.py > "$log_dir/${report_prefix}-content.log" 2>&1
python3 tools/check_connected_reasoning.py > "$log_dir/${report_prefix}-reasoning.log" 2>&1
python3 tools/check_connected_python.py > "$log_dir/${report_prefix}-python.log" 2>&1
CHECK_WEEKS="${lesson_id}" work/curriculum-python/bin/python tools/validate_downloads.py > "$log_dir/${report_prefix}-downloads.log" 2>&1
CONNECTED_WEEK="$week_number" node tests/connected-week-offline.mjs > "$log_dir/${report_prefix}-offline.log" 2>&1
python3 tools/validate_links.py > "$log_dir/${report_prefix}-links.log" 2>&1
python3 tools/build_connected_review.py "$lesson_id"
python3 tools/finalize_connected_review.py "$lesson_id"

python3 tools/build_connected_review_index.py
