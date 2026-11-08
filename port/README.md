# port - the text that fills the shells, and the files that are not shells

> Two kinds of thing live here, and they install differently.
>
> **`blocks/`** is the shared text. `skeleton/` holds a per-harness shell with a `<!-- PORT: … -->` marker
> where that text goes; filling the marker with a block is the install. The text exists here **once**, so
> editing it once is the whole update.
>
> **Everything else** is a file that cannot be a shell - executable, chosen by the host, or one body for
> several destinations.

## blocks/ - the shared text

| Block | Fills | Extent |
| --- | --- | --- |
| `context-rules.md` | the body of the port target's rule file | the routing table + the two timing rules. `context/README.md` is named as authority in its header |
| `hook-commands.md` | the `command` strings in a harness hook config | the four intents as one-line commands, and which of them block |

Each block opens with `<!-- block: <name> -->` and `<!-- authority: <path> -->`. The second is the answer to
"these two disagree" - the block is a *summary*, and the authority wins.

## Everything else

| File here | Lands at | Why it is not in `skeleton/` |
| --- | --- | --- |
| `skill/context-tree/SKILL.md` | the **port target**'s skill directory - `.claude/skills/`, or `.github/skills/` on a Copilot-only repo (**unverified**) | **one body, one home.** Which directory depends on which harnesses the host runs |
| `skill-stub/SKILL.md` | every other present harness with a verified skill path | **a pointer, not a copy.** Two 41-line bodies drift, and the `ported` gate dates a shell rather than comparing the bodies (`GATES.md`) |
| `AGENTS-stub.md` | `<repo>/AGENTS.md` - only when `CLAUDE.md` is canonical and a present harness reads `AGENTS.md` | **a pointer.** Claude reads `CLAUDE.md` *instead of* `AGENTS.md`; a second full copy is dead text |
| `hooks/pre-commit.sh`, `pre-commit.ps1` | `.git/hooks/pre-commit` | not a repo file at all, and a **choice** |
| `hooks/ci.yml` | `.github/workflows/context.yml` | a workflow is one line of intent per repo |
| `hooks/copilot-vscode-hooks.json` | your harness's own hook path - **unverified** | **executable.** No repository-level path could be confirmed; a guess in `skeleton/` would be trusted and then not load |
| `hooks/cursor-hooks.json` | `.cursor/hooks.json` | **executable** - a host that wants no checks should not have one that runs them |
| `hooks/codex-hooks.json` | `.codex/hooks.json` | **executable**, and needs a human to trust it before it runs |
| `hooks/README.md` | nowhere | the policy behind the four intents; read by a human choosing a level |

## The test

| Question | If yes → |
| --- | --- |
| Is the harness **run** by the host? | `skeleton/` as a shell - if not, do not copy it at all |
| Does it need a **choice** at install? | `port/` - the skeleton cannot decide for the host |
| Does the harness **execute** it? | `port/` - an unused rule costs nothing, an unused hook fails every session |
| Is it the **same text** for N harnesses? | `port/blocks/`, once, filled into shells |
| Is it the **same body** for N destinations? | `port/`, once, plus a stub per destination |

A file that passes none of these is correct wherever it lands, and belongs in `skeleton/` at the path its
harness reads.

## Why this is not the drift it looks like

`context-rules.md` restates a table that `context/README.md` already holds. Three things keep that honest:

1. **One copy.** The text exists in `port/blocks/` only; the shells in `skeleton/` are empty of it.
2. **One host file.** Install fills the *port target*'s file and points the rest at it - never two
   copies inside one repo.
3. **Named authority.** The block's own header says the contract wins. `AGENTIC-SYSTEM.md` §4 already
   settles that order.

The remaining cost is real and stated: when the pattern's rules change, a host re-ports the block instead of
inheriting an edit. That is the price of having the rules visible at the moment of writing instead of one
hop away.

## Verify an install

```
cd <host repo> && python scripts/contextctl.py check --only installed
```

Passing means every path in `shells` exists and none still holds a marker. For a text search, match the marker
and not the word - `grep -rn "<!-- PORT:" . --exclude-dir=.git` - because the copied `scripts/contextctl.py`
contains `PORT:` in its own source, so `grep -rn "PORT:"` is non-empty on a perfect install. Run either in the
host, never here, where every doc that names the marker contains one.
