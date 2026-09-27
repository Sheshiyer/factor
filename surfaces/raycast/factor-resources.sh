#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Factor — Learn / Découvrir
# @raycast.mode silent
# @raycast.packageName Factor
# @raycast.icon circle.fill
# @raycast.argument1 { "type": "dropdown", "placeholder": "Resource / Ressource", "optional": false, "data": [{"title": "Framework guide / Guide", "value": "framework-guide"}, {"title": "Operator guide / Opérations", "value": "operator-guide"}, {"title": "Slides / Présentation (FR)", "value": "framework-slides"}, {"title": "Workflow / Parcours (FR)", "value": "operations-slides"}, {"title": "Video / Vidéo (FR)", "value": "overview-video"}, {"title": "Architecture (FR)", "value": "architecture-infographic"}, {"title": "Learning / Apprentissage (FR)", "value": "learning-infographic"}] }
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
path_file="$HOME/Library/Application Support/Factor/company.path"
if [ -f "$path_file" ]; then
  company=$(head -n 1 "$path_file" | tr -d '\r')
  exec python3 "$root/scripts/onboard.py" --company "$company" --open-resource "${1:-}"
fi
exec python3 "$root/scripts/onboard.py" --open-resource "${1:-}"
