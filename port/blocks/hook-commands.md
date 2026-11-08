<!-- block: hook-commands -->
<!-- authority: port/hooks/README.md - the four intents and what each enforcement level costs. -->

These are the only commands a hook ever needs. Copy the row your harness's event needs.

| Intent | Command | Blocks? |
| --- | --- | --- |
| **keep the digest current** | `python scripts/contextctl.py brief` | no |
| **remind** | `python scripts/contextctl.py check --all --warn` | no - every finding prints, exit 0 |
| **gate the commit** | `python scripts/contextctl.py check` | yes |
| **gate the merge** | `python scripts/contextctl.py check --all` | yes |

Read `--warn` as the default and `check` as the deliberate choice: a gate that behaves the same whether it
is advisory or blocking is a gate someone disables.

**Both `brief` forms exist and neither does anything yet.** `brief` is a stub: it writes no digest, compares
none, prints why to stderr and exits `0` - deliberately, because a failing session-start hook blocks the
session it is starting. Read the row as the intent, not as a renderer: until one exists the register is the
copy.
