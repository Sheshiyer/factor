#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Factor — Français
# @raycast.mode silent
# @raycast.packageName Factor
# @raycast.icon circle.fill
# @raycast.argument1 { "type": "text", "placeholder": "Tâche", "percentEncoded": false }
# @raycast.argument2 { "type": "dropdown", "placeholder": "Pièce", "optional": false, "data": [{"title": "Contenu", "value": "content"}, {"title": "Chiffres", "value": "numbers"}, {"title": "Croissance", "value": "growth"}, {"title": "Publicités", "value": "ads"}, {"title": "Partenaires", "value": "partners"}, {"title": "Finances", "value": "money"}] }
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
if [ ! -f "$HOME/Library/Application Support/Factor/company.path" ]; then
  echo "Choisissez d’abord une entreprise dans le menu Mac." >&2
  exit 2
fi
if [ -z "${1:-}" ]; then
  echo "Décrivez la tâche." >&2
  exit 2
fi
exec bash "$root/surfaces/raycast/factor.sh" "$@"
