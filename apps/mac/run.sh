#!/bin/sh
# Launch the menu-bar tray. Unsigned and local.
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
export FACTOR_ROOT="$root"
export FACTOR_WRITE_INTENT="$root/scripts/write_intent.py"
cd "$root/apps/mac"
exec swift run
