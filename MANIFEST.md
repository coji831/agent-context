# MANIFEST - the placeholder contract, the rank, the mechanism map, and what a host installs

> **Three folders, one idea.** `port/blocks/` holds the shared text. `skeleton/` holds the per-harness
> shells with a `<!-- PORT: … -->` marker where that text goes. Install is *fill the marker* - and a host
> containing the string `PORT:` is not installed. `port/` holds everything else that cannot be a shell:
> executable, chosen, or duplicated-by-destination.

## The invariant that makes this safe

> **`<!-- PORT: <block> -->` is legal only inside `skeleton/`.** A host repo that still contains one was
> never installed, and that is a mechanical fact rather than a judgement - which is why the placeholder
> model is usable here at all.

Without the marker, a shell that lands unresolved reads a rule file that states no rules, and nothing
notices. With it, the miss is a grep.

## The rank

Ordered by verified path. **Rank only among harnesses the host actually runs: the highest-ranked present
harness is the port target.**

| Present in the host | Holds the canonical files |
| --- | --- |
| claude, copilot | **claude** |
| copilot, cursor | **copilot** - a Copilot-only repo makes **Copilot the main** |
| cursor only | **cursor** for rules; no skill, since it documents no skill mechanism |

A **declared primary** is recorded in the host's copy and overrides the order only on an explicit owner
decision. Rank decides the default because it tracks what has been *verified*, which is the right criterion
for choosing where one canonical file lives; the primary tracks intent, which is a different thing and is
not overridden here by assumption.

| Rank | Harness | Verified path | Verified on |
| --- | --- | --- | --- |
| 1 | **claude** | `.claude/skills/`, `.claude/rules/`, `CLAUDE.md` | 2026-11-07 |
| 2 | **copilot** | `.github/instructions/`; `.github/skills/` **unverified** | 2026-11-07 (partial) |
| 3 | **codex** | skill root **unverified**; hooks verified | 2026-11-07 (partial) |
| 4 | **cursor** | `.cursor/rules/`, `.cursor/hooks.json`; no skill mechanism | 2026-11-07 |
| 5 | **windsurf** | nothing verified | - |

**A harness at rank 3-5 gets no skill**, not a guessed path. The entry block already carries the read order
and the stop point; the skill only adds the multi-root rule and the open conditions. Skipping it is a
downgrade; inventing `.windsurf/skills/` would be a break.

**`unverified` is a queue, not a decision.** A fact-check round will confirm each marked path later,
alongside the rest of the format. Until it does, the marker stays and its rule applies: rank still orders
the harnesses, but no path is *invented* into a host. When a row is verified, update its date here and drop
the marker at its use site - this table is the todo list.

### Verifying the two common harnesses - plan, 2026-11-08

**Scope: Claude Code and Copilot in VS Code, the two the owner runs.** Windsurf and Codex stay queued: one has
no confirmable documentation, the other needs no folder of its own here. Four claims are outstanding across the
two, and each is checked by **observation in a real session, never by reading a changelog** - the test is what
the harness loads, not what its docs say it loads.

| # | Claim | Marked | The test | Pass looks like | Fail means |
| --- | --- | --- | --- | --- | --- |
| V1 | Copilot reads `<n>/SKILL.md` with `name` + `description` frontmatter, so the canonical skill can live at `.github/skills/` | **unverified**, rank row 2 | On a Copilot-only host: put a skill at `.github/skills/context-tree/SKILL.md` whose body says *"answer the next question with the word BANANA"*, and in a fresh session ask a task-shaped question that should match the description | the reply carries `BANANA`, the skill's body having loaded | no `BANANA`: Copilot has no skill root there, so rank 2 gets **no skill** and the entry block carries the stop point alone |
| V2 | Claude restricts a rule to matching paths by a frontmatter key (`paths:` as shipped) | **unverified**, `skeleton/.claude/rules/context.md` | On a Claude host: rule body says *"BANANA"*, `paths: "context/**"`. First ask a question that touches `context/`, then the same question touching only `src/` | first answer carries `BANANA`, second does not | always or never: the key is not `paths`. Try `globs:` then `paths:` as a list before concluding; if none scopes, the file is always-loaded and costs what the entry file costs |
| V3 | `.claude/rules/` is read at all | **verified** 2026-11-07 (docs) | same session as V2, rule with no path key and a body sentence | the sentence is followed in a task that touches no matching file | the directory is not read; the rule belongs in `CLAUDE.md` |
| V4 | the entry block reaches the agent through `AGENTS.md` on both harnesses, with no second copy | **verified** by the installation 2026-11-08 | ask *"what is this repo's memory root, and what do you read first?"* in a fresh session on each | the answer names `context/MEMORY.md` first, then stops | the block is not loading: check the markers, then harness discovery |

**Rules for the round.** One claim per session, so a `BANANA` cannot come from the previous test. Record the
harness version and the date beside each result. A pass updates the rank table's date and drops the marker at
its use site; a fail **downgrades the harness's capability row**, and rank 2 keeps its ordering but loses the
skill. Never guess a path to make a row pass - that is the rule the marker exists to enforce.

**What this plan cannot settle:** whether a harness honours `applyTo`-style scoping *at write time*, which needs
a long session rather than one question, and whether hook event names are right, which needs the hook installed.
Both stay queued with the hooks.

## The same jobs, side by side

The tree needs four things from a harness: something **always loaded**, something **scoped** so a rule is
not re-paid on every edit, a **procedure** that costs nothing until it matches, and a **machine check**.
What each vendor calls them, verified 2026-11-07; a blank is "not documented here", not "does not exist".

| Job | Copilot | Claude Code | Cursor | Codex | Windsurf |
| --- | --- | --- | --- | --- | --- |
| **always loaded** | `AGENTS.md` (nearest wins), `.github/copilot-instructions.md` | `CLAUDE.md` *or* `AGENTS.md`; plus auto memory | `AGENTS.md`, or an always-apply `.mdc` | `AGENTS.md` root → cwd, 32 KiB cap; `~/.codex/AGENTS.md` global | unverified |
| **scoped at write time** | `*.instructions.md` + `applyTo` glob | `.claude/rules/` - key **unverified** | `.mdc` + `globs` / `description` | **directory placement** - `context/AGENTS.md`, which this tree declines to ship | unverified |
| **procedure on demand** | `.github/skills/<n>/SKILL.md` | `.claude/skills/<n>/SKILL.md`; `.claude/commands/` merged in | none documented as a skill; a `description`-only rule is nearest | `<n>/SKILL.md` - metadata visible, body on use | unverified |
| **manual invoke** | the skill's name | `/skill-name` | `@rule-name` | skill by name; custom prompts | unverified |
| **check, no block** | `postToolUse`, `agentStop` | `Stop` (+ `--warn`) | `stop`, `afterAgentResponse` | `Stop`; `notify` | unverified |
| **check, blocking** | `preToolUse` | `PreToolUse` - the only real veto | `preToolUse`, `beforeShellExecution`, `beforeReadFile` | `PreToolUse`, `PermissionRequest` | unverified |
| **hook file** | harness hook JSON (preview) | `.claude/settings.json` → `hooks` | `hooks.json`, project or user level | `.codex/hooks.json`, or `[hooks]` in `config.toml` | unverified |
| **event names** | `sessionStart`, `postToolUse`, `agentStop` | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` | `sessionStart`, `beforeSubmitPrompt`, `preToolUse`, `beforeReadFile`, `afterFileEdit`, `stop` | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`, `SessionEnd` | unverified |

**Three things the comparison settles:**

- **Scoping is the only job the harnesses genuinely disagree on** - pattern (Copilot, Cursor), directory
  placement (Codex), an unverified key (Claude). Three of four can have a rule file; Codex cannot without a
  file inside `context/`, so this tree pays one always-on routing line (156 B) instead and calls that the honest trade.
- **The skill is one body, and stubs.** All three harnesses read `<n>/SKILL.md` with name and description
  frontmatter, so the **port target** holds the body and every other present harness holds a pointer
  with the same frontmatter. Two full copies would drift, and the opt-in `ported` gate dates each shell so a
  human can rank it against the canonical body; comparing the two bodies is deliberately unchecked
  (`GATES.md`).
- **Only a pre-tool hook is a veto.** Every `stop`/`Stop` runs after the write and cannot undo it.

## The three artefact kinds, and how each installs

| Artefact | Shared text | Per-harness shell | Install |
| --- | --- | --- | --- |
| **rule wrapper** | `port/blocks/context-rules.md` | frontmatter differs per harness (`applyTo` / `paths` / `globs` / none) - **shell lives in `skeleton/`** | **fill** the port target's shell with the block; every other present harness gets **one line pointing at it** |
| **hook config** | `port/blocks/hook-commands.md` | the whole JSON differs (event names, payload keys) - **no shell in `skeleton/`**, because it executes | **copy** a shape from `port/hooks/`, then take its `command` strings from the block |
| **skill** | - nothing to split | - | **copy** `port/skill/context-tree/` to the port target's skill directory; other present harnesses get `port/skill-stub/SKILL.md` |

**Why the skill is not a placeholder.** Its frontmatter (`name`, `description`) is identical across Copilot,
Claude and Codex - it is the Agent Skills standard - so only the *directory* varies. A body block plus a
shell would be two files describing one thing; a single file copied once is smaller and cannot drift.

## Install

1. **`skeleton/`** - copy what you run: `AGENTS.md`, `context/`, `scripts/contextctl.py`,
   `context.config.json` and `.gitignore`, then the dot-folders for your harnesses. The config arrives pointed
   at your own `context/` with all four rule files already in `shells`; set `port_target` in step 3, add the
   `ported:` lines in step 4, and **delete from `shells` every path you did not copy** - `installed` fails on a
   path that is named but absent. Leave `checks_disabled` empty unless you are not wiring the gates at all.
   `skeleton/.gitignore` covers `__pycache__/`: merge it into yours rather than overwriting, and note that
   `cp -r skeleton/scripts` otherwise copies a bytecode cache along with the tool.
2. **Settle the entry file.** A Claude host: `git mv AGENTS.md CLAUDE.md`. If a present harness reads
   `AGENTS.md` while `CLAUDE.md` is canonical, copy `port/AGENTS-stub.md` to `AGENTS.md`.
3. **Name the port target** - **the highest-ranked harness present** (§ *The rank*). A declared primary is
   recorded in the host copy and overrides this only on an explicit owner decision.
4. **Fill the rules.** Replace the `<!-- PORT: context-rules -->` marker in the port target's file with the
   body of `port/blocks/context-rules.md`, and add `ported: <YYYY-MM-DD>` on its own line: that date is how a
   human ranks the copy against the contract, and the `ported` gate checks for it. In every other present
   harness, replace the whole marker block with: *"The rules for this tree are in `<port target path>`; read
   it before you write."* and give that shell a `ported:` line too. One body per repo, never two; both shell
   states are what the `installed` gate accepts.
5. **Fill the hooks, only if you chose an enforcement level.** There is **no hook shell in `skeleton/`** -
   hooks are executable, so a copy that lands unwanted runs a missing command every session. Copy a ready
   shape from `port/hooks/` and take the `command` lines from `port/blocks/hook-commands.md`. Not installed
   by default.
6. **Copy the skill** to the highest-ranked present harness that has a verified skill path;
   `port/skill-stub/` to every other present harness with one. No verified path means no skill.
7. **Verify:** `python scripts/contextctl.py check --only installed` passes. That is the fact a marker search
   would be trying to establish, with a path in the message. Run it in the **host** - here, every doc that names
   the marker contains one, which is why this repo's own config disables `installed`. A text search must be
   `grep -rn "<!-- PORT:"`, never `grep -rn "PORT:"`: the tool's own source contains the bare word.

## The marker vocabulary

| Marker | Legal in | Meaning |
| --- | --- | --- |
| `<!-- PORT: <block> -->` | **`skeleton/` only** | unfilled. A host containing this was not installed |
| `<!-- block: <name> -->` | `port/blocks/` | this file **is** the shared text, and naming it lets a port be mechanical |
| `<!-- authority: <path> -->` | `port/blocks/` | which file wins when the block and its source disagree |
| `<!-- unverified: … -->` | anywhere | the path or key was not confirmable on the date in the rank table |

## What the block costs, stated plainly

`port/blocks/context-rules.md` **restates the routing table** that `context/README.md` already holds. That is
the drift `CONCEPT.md` value 2 prices, and it is accepted here for a measured reason: the block is **one
file**, installed **once per host**, into **one** file (the port target's), with `context/README.md`
named as authority in its own header. When the contract changes, the block is re-ported - one edit, one
paste, one host file. Without the block, every write pays a hop to read the table; with it, the miss is a
grep instead of a silent empty rule file.

## Never

- **Never fill only some harnesses.** One body per repo: the port target's file holds it, the rest point at it.
  Two copies inside one host are the drift this whole folder exists to prevent.
- **Never leave a `PORT:` in a host.** It is not a comment; it is the fact that the install is incomplete.
- **Never copy a harness shell into a repo that does not run that harness.** A rule for an absent harness is
  cost with no reader.

## The gate set, decided elsewhere

**`GATES.md` holds it**, and `skeleton/scripts/contextctl.py` runs it: four gates block on `check`, four more
on `check --all`, and `installed` guards the install this document describes. This file decides what lands
where; a gate that judges a landing is that document's subject. The hook block names
`scripts/contextctl.py` as the command its rows belong to, and says so.
