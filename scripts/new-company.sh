#!/bin/sh
# Copy the blank company glove to a new directory.
# Usage: scripts/new-company.sh <slug> <dest>
set -eu

if [ "$#" -ne 2 ]; then
  echo "usage: scripts/new-company.sh <slug> <dest>" >&2
  exit 2
fi

slug=$1
dest=$2

printf '%s' "$slug" | grep -Eq '^[a-z][a-z0-9-]{0,62}$' || {
  echo "slug must be lowercase letters, digits, and hyphens, starting with a letter" >&2
  exit 2
}

if [ -e "$dest" ]; then
  echo "dest already exists: $dest" >&2
  exit 2
fi

root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
mkdir -p "$dest"
cp -R "$root/company/." "$dest/"
find "$dest" -type f -print | while IFS= read -r file; do
  tmp="$file.tmp"
  sed "s/__COMPANY__/$slug/g" "$file" > "$tmp"
  mv "$tmp" "$file"
done

echo "$dest"
echo "Fill context/*.md until scripts/check_company.py passes."
echo "Then: hermes -p factor config set skills.config.factor.company_root $dest"
