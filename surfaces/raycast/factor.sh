#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Factor
# @raycast.mode silent
# @raycast.packageName Factor
# @raycast.icon circle.fill
# @raycast.argument1 { "type": "text", "placeholder": "Job", "percentEncoded": false }
# @raycast.argument2 { "type": "dropdown", "placeholder": "Room", "optional": false, "data": [{"title": "Content", "value": "content"}, {"title": "Numbers", "value": "numbers"}, {"title": "Growth", "value": "growth"}, {"title": "Ads", "value": "ads"}, {"title": "Partners", "value": "partners"}, {"title": "Money", "value": "money"}] }

# Raycast script command. Add this folder in Raycast → Settings → Extensions → Script Commands.
# No keys live here. The company folder is the same file the menu bar uses.

set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
path_file="$HOME/Library/Application Support/Factor/company.path"
if [ ! -f "$path_file" ]; then
  echo "Choose a company folder in the menu bar first." >&2
  exit 2
fi
company=$(head -n 1 "$path_file" | tr -d '\r')
sentence=${1:-}
room=${2:-}
if [ -z "$sentence" ]; then
  echo "Say the job." >&2
  exit 2
fi
exec python3 "$root/scripts/write_intent.py" "$company" \
  --sentence "$sentence" \
  --room "$room" \
  --door raycast
