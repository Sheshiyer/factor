#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Factor — Language / Langue
# @raycast.mode silent
# @raycast.packageName Factor
# @raycast.icon circle.fill
# @raycast.argument1 { "type": "dropdown", "placeholder": "Language / Langue", "optional": false, "data": [{"title": "English", "value": "en"}, {"title": "Français", "value": "fr"}] }
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
path_file="$HOME/Library/Application Support/Factor/company.path"
if [ ! -f "$path_file" ]; then
  echo "Choose a company in the Mac menu / Choisissez une entreprise dans le menu Mac." >&2
  exit 2
fi
company=$(head -n 1 "$path_file" | tr -d '\r')
exec python3 "$root/scripts/onboard.py" --company "$company" --set-language "${1:-}"
