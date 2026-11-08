# EXAMPLE hooks - the shared slot, copied only when you choose a level

> **These are examples, not installers.** Adopting the tree wires nothing up. A hook is the one part of an
> agent system that cannot be portable: event names, payload shapes and failure semantics differ per
> harness, so the *shared* part is the intent and the scripts, and the *per-harness* part is the wiring -
> `../copilot/hooks/` for a Copilot-shaped host, and nothing else here assumes one.
>
> **Every command below calls `scripts/contextctl.py`, which ships its `check` commands and not `brief`.**
> Read the ones it cannot run as the intended shape; a hook that runs a missing command fails loudly, which
> is correct and not a bug to silence with a `|| true`.

## The portable part is the intent, not the event

Decide *what* you want before *where*: these four are harness-independent and survive a change of editor.

| Intent | Runs | Call | Blocks? |
| --- | --- | --- | --- |
| **remind** | session end, or as a pre-commit note | `check --all --warn` | no - every finding prints, exit 0 |
| **gate the commit** | pre-commit | `check` | yes |
| **gate the merge** | CI | `check --all` | yes |
| **keep the digest current** | session start | `brief`, then `brief --check` | no |

`--warn` exists because a gate that behaves the same whether it is advisory or blocking is a gate someone
disables: the soft version is a one-word change at the call site, not a second script.

## What each level costs

| Level | You gain | You give up |
| --- | --- | --- |
| none | nothing to maintain | the check runs only when someone remembers |
| **1. run it yourself** | visibility, zero wiring | nothing enforced |
| **2. git pre-commit** | a block that survives any editor change | skipped with `--no-verify`; runs on every commit, so it must stay fast |
| **3. harness event** | the agent sees the finding mid-work | per-harness wiring; a stop event cannot undo what already ran |
| **4. CI** | the only level that cannot be skipped locally | feedback arrives after the push |

Adopt downward from 1 and stop when the pain is covered. **Recommend level 2 and nothing else**: one file,
harness-independent, survives every editor change.

## Two traps

- **A stop hook that blocks is an outage.** Staleness is information; run it with `--warn` and let the
  commit gate be the thing that stops.
- **A harness hook installed before the habit exists** gets disabled at the first false positive, taking
  the habit with it.

Tell the human `git commit --no-verify` exists. They will find it anyway, and an undocumented escape
hatch becomes the default.
