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

**Only the `check` commands exist so far.** `brief` is not written, so a sessionStart hook fails loudly on
its first run, which is correct and not a bug to silence with `|| true`.
