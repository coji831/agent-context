#!/bin/sh
# EXAMPLE ONLY - copy to .git/hooks/pre-commit and chmod +x. Nothing here is installed by adopting the tree.
#
# Intent: gate the commit. The structural defects a memory tree can ship are exactly the ones invisible in
# review - a register row with no folder, a leaf no index names, a citation that resolves to nothing - and
# a commit is the last moment they are cheap to fix.
#
# Skip with `git commit --no-verify`. Say so once rather than leaving it to be discovered.

set -e

if [ ! -f scripts/contextctl.py ]; then
  echo "pre-commit: scripts/contextctl.py is not in this repo - nothing to check." >&2
  exit 0
fi

python scripts/contextctl.py check
