# EXAMPLE ONLY - copy to .git/hooks/pre-commit (git does not read a .ps1 name; use this as the body of
# `pre-commit`, or call it from that file). Nothing here is installed by adopting the tree.
#
# Intent: gate the commit. The structural defects a memory tree can ship are the ones invisible in
# review - a register row with no folder, a leaf no index names, a citation that resolves to nothing -
# and a commit is the last moment they are cheap to fix.
#
# Skip with `git commit --no-verify`.

$ErrorActionPreference = 'Stop'

if (-not (Test-Path 'scripts/contextctl.py')) {
    Write-Host 'pre-commit: scripts/contextctl.py is not in this repo - nothing to check.'
    exit 0
}

python scripts/contextctl.py check
exit $LASTEXITCODE
