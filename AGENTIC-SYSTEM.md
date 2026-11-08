# AGENTIC-SYSTEM - how a harness or an agent connects to this tree

> [`skeleton/`](skeleton) holds the **shells** - per-harness frontmatter plus a `<!-- PORT: … -->` marker,
> which is legal there and nowhere else. [`port/`](port) holds the text that fills them, plus the files
> that cannot be a shell; [`MANIFEST.md`](MANIFEST.md) maps one to the other.
> This document answers one question: **what has to exist outside that tree for a session
> to read it at the start and write to it before it stops.** It describes the connection, not the pattern:
> `CONCEPT.md` ranks the values, `FOLDER.md` maps the files, `LOCKED.md` says what is frozen. The gate runner
> `scripts/contextctl.py` and its `context.config.json` now ship (see `GATES.md`); `brief` and `resolve` are
> still later steps, and their absence is deliberate.

## 0. The authoring map - where each thing is edited

**Every artefact has exactly one place to edit.** That is the claim this document exists to support, so it
is stated before the layers rather than after them.

| Artefact | Authoring home - edit here | Installed as |
| --- | --- | --- |
| **entry block** | `skeleton/AGENTS.md` | that file, or renamed to `CLAUDE.md`; `port/AGENTS-stub.md` for a second reader |
| **rules body** | `port/blocks/context-rules.md` | filled into the **port target**'s shell |
| **rules frontmatter** | `skeleton/.<harness>/…` | that shell, unchanged |
| **skill body** | `port/skill/context-tree/SKILL.md` | copied to the port target's skill directory |
| **hook commands** | `port/blocks/hook-commands.md` | filled into a harness hook config |
| **hook config** | `port/hooks/<harness>-hooks.json` | copied to that harness's own hook path |

**Three things are not "one home", and each is deliberate.**

1. **The rules body.** `context/README.md` is the **authority** and `port/blocks/context-rules.md` a summary
   of it, installed into one file per host. The block's own header says so, and §4 is the order to apply when
   they part company.
2. **`port/AGENTS-stub.md`** carries a *reduced* form of the read order rather than a pointer: an entry file
   is read at the start of **every** session, so a hop there is paid constantly, while the same hop in a
   skill is paid only on a match.
3. **The skill restates the read order**, because a skill that only pointed at the entry file would be a
   procedure with no procedure - and the skill may never load at all, so the entry cannot be the only carrier.
   The skill is a superset: it adds `## Now` / `## Failed`, the leaf conditions and the multi-root rule.

Everything else - rules, skill body, hook commands, hook config - has exactly one place to edit and no second
copy.

## 1. The three connection layers, in order

| # | Layer | What it carries | Portable? | Where it ships |
| --- | --- | --- | --- | --- |
| 1 | **entry file** | the memory rule, the read order, where to stop, one line naming the skill | **yes - the only universal layer** | `skeleton/AGENTS.md`, placed in step 5 of `ADOPT.md` |
| 2 | **`applyTo` scoping** | the write-time trigger, carrying the filled rules block | no | `skeleton/.<harness>/`, a shell - **Codex has none**: it pays a clause in `AGENTS.md` instead |
| 3 | **hook injection** | the entry block delivered at session start, or a check run when a turn ends | no | `port/hooks/` - executable, so never installed by default |

**1 - entry file.** Every harness loads *some* file at session start; only the filename differs. It is
universal because it asks nothing of the harness beyond the file it already reads. **Silently fails
without it:** the session never learns the tree exists - it answers from the chat, writes nothing, and the
tree stays as the last human edit left it. No error, no missing-file warning, nothing to notice.

**2 - `applyTo` scoping.** The rules ship as a rule file whose frontmatter names the paths it governs, so
a rule about `context/**` is not re-paid for every edit elsewhere. Not portable: `applyTo` is one vendor's
spelling, glob and description-matching semantics differ, and a harness without scoped rules has no home
for these rules short of the always-loaded file. **Silently fails without it:** the rules either load into
every request as standing cost, or - the commoner case - load on no request at all, so the agent knows it
should write but not *where*, and the write lands in the chat, the handoff, or a file the index never
names. The shell here is **frontmatter plus a `PORT:` marker**: the body is one shared block in
`port/blocks/`, filled into the port target only, because a second filled copy in one repo is exactly
the drift this pattern prices.

**3 - hook injection.** The harness runs a command on a lifecycle event and prepends the entry block, or
runs a check as the turn ends. Not portable in the strongest sense: event names, JSON field names, the
injection cap and whether stdout is read at all are vendor-specific, and sharing a hook file location
between harnesses establishes nothing. **Silently fails without it:** an adopted repo whose start file
must not be edited is unreachable, and no check ever runs at the moment a write is made - a stale pointer
is then only ever found by a human who opens the file it points at.

The order is load-bearing: layers 2 and 3 exist to compensate for what layer 1 cannot say. Without 1,
neither helps - there is no start file to scope and no event to hang a hook on.

## 2. Per harness: the file that must exist

The per-harness table came from the adoption runbook (`agent/WIRING.md`, still readable from `54ba837`),
which warned that **the paths move; the shape does not**. Each path below is either re-verified against
the vendor's own documentation on 2026-11-07, or marked unverified - nothing is asserted and then hidden.

| Harness | File that must exist | Where | Path-scoped rules | Silently, without it | Verified |
| --- | --- | --- | --- | --- | --- |
| VS Code / Copilot | `AGENTS.md` (nearest in the directory tree wins), or `.github/copilot-instructions.md` | repo root / `.github/` | `*.instructions.md` with `applyTo` frontmatter, in or below `.github/instructions/` | the session never learns `context/` exists: it answers from the chat, writes nothing, and reports no error | 2026-11-07, GitHub Copilot docs |
| Claude Code | `CLAUDE.md`, or `AGENTS.md`, which Claude Code reads **in place of** it | repo root; also a user-level home | `.claude/rules/` - the glob key is **unverified** | it starts from an empty window with nothing pointing at the tree, and every session re-derives what the last one knew | 2026-11-07, Claude Code docs |
| Cursor | `AGENTS.md`, or `.cursor/rules/*.mdc` - a plain `.md` there is **ignored**, having no frontmatter | `.cursor/rules/` | the `.mdc` frontmatter: `globs` (apply-to-files) or `description` (apply-intelligently) | a rule written at a plausible path is never loaded, because Agent reads only what it recognises - the file looks installed and is inert | 2026-11-07, Cursor docs |
| Codex / CLI agents | `AGENTS.md`, concatenated root-downward, one per directory, capped at `project_doc_max_bytes` (32 KiB default) | repo root - and **no folder of its own here**: a nested one would mean a thirteenth file inside the frozen `context/` | **none - scoping is by directory placement only.** The root `AGENTS.md` carries the routing clause with its moment instead (one always-on line, 156 B) | it re-derives the read order, re-tries a `## Failed` approach, and writes nothing durable before stopping | 2026-11-07, Codex docs |
| Windsurf | **unverified** - `.windsurfrules` and `.windsurf/rules/` are the historically documented pair | - | unverified | **unverified** - cannot be named from here | **unverified**: `docs.windsurf.com` now redirects to a different vendor's customisation page |
| no harness (a human) | `AGENTS.md` | repo root | not applicable | nothing - a human who opens `context/MEMORY.md` first is a legitimate wiring | by construction |

A harness missing from this table is unmeasured, not unsupported. **Any harness that loads a file at session
start can be wired**, in four steps:

1. **Find the file it reads.** Its own documentation, or the file it already has - never a guessed path.
2. **Put the entry block there**, between `<!-- context:begin -->` and `<!-- context:end -->`. Upsert if the
   file exists; create it if not. This alone is a working wiring: the session learns the tree exists, the
   read order, and where to stop.
3. **If it also reads path-scoped or glob-scoped rules**, add a shell in that harness's own frontmatter
   dialect under `skeleton/`, and record the path in [`MANIFEST.md`](MANIFEST.md)'s rank table.
4. **If it documents no scoping at all**, put the filled block in the always-loaded file instead and accept
   the always-on cost - that is what Codex's row does.

Each row's folder is `skeleton/.<harness>/` - the harness root as the host has it, not an invented one;
Codex has none by design, and its scoping loss is the price of leaving the frozen tree alone.
[`MANIFEST.md`](MANIFEST.md) is the map to correct when a path moves, and it carries the
mechanism-by-mechanism comparison.

## 3. The write contract

**Write inside `context/`, in the one file the kind of knowledge owns, in the same turn** - a leaf is
named in its topic `README.md` as it is created, `HANDOFF.md` is rewritten and never appended, `JOURNEY.md`
is appended and never edited. Nothing durable goes in the chat, the commit message, or a file outside the
tree.

**The one file it may not touch is whatever the host calls a requirement** - a spec, a locked brief. That
is host-supplied, the tree is never authority for it, and a change is a **new revision**, never an edit.

**Also not a write target:** the generated digest, which a renderer overwrites, and the contract's own
rules, which change only when the pattern changes and only with the reason stated.

## 4. Two files disagree

First rule that applies:

1. **The code wins over any document about it.** A `HANDOFF.md` that contradicts the code is stale; the
   contradiction is a finding to record, not something to reconcile silently.
2. **A host-supplied requirement wins over the tree.** The tree holds working state and drains; it never
   becomes the record. Disagreement is a new revision, or a finding.
3. **Between two tree files, the pointed-at file is right.** The entry file carries pointers and must not
   restate the contract, so when it disagrees with what it points at, the pointer is the stale copy. A
   topic snapshot likewise yields to the contract, which states rules and never the topic roster.
4. **A filled rule shell yields to the contract.** `port/blocks/context-rules.md` is a *summary* of
   `context/README.md`, and its own header names the contract as authority. So when a host's filled shell
   and the contract disagree, the shell is the stale copy - the summary was correct when it was ported and
   the pattern has moved since. Re-port the block; never edit the host's copy to match.

Stated rather than discovered because two copies drift and the copy nobody loads is the one that gets
edited: a disagreement means one copy is stale, and an agent asked to adjudicate it mid-task is inventing
authority it does not have. One stated order is checkable; a case-by-case judgement is not.

## 5. One worked arrival

A session starts in an adopted repo of this shape; the task touches `widget`. In order:

1. **The harness's entry file** - `AGENTS.md`, or `CLAUDE.md` on a Claude host (one, never both; `AGENTS.md`
   may exist as a stub pointing at `CLAUDE.md` for a second reader). The marked block: memory is `context/`,
   read in this order, then stop, and one line naming the skill.
2. **`context/MEMORY.md`** - the start read, step 1: facts true before any topic is opened.
3. **`context/MUST-KNOW.md`** - the start read, step 2: the root constraints, already pruned.
4. **`context/topics/widget/README.md`** - on the topic's trigger, first: purpose, reading order, and the
   `## Leaves` table saying which leaves exist and what each one answers.
5. **`context/topics/widget/MUST-KNOW.md`** - on the trigger, second: constraints for that area only.
6. **`context/topics/widget/HANDOFF.md`** - on the trigger, last: `## Now` is the first action, `## Failed`
   is what not to retry.

**Reading stops at step 6.** `JOURNEY.md` is never read by an agent. `decisions.md` opens only when a
choice in this topic is being relitigated. A leaf opens only when the README's `brief` is not enough - the
table exists so the leaf can *not* be read. `context/README.md` is not a step before step 1: it opens when
a rule is unclear. A task touching no topic opens none; opening topics "for context" is how a one-screen
start becomes an expensive one.

**If the task names no topic**, the on-demand read is `context/topics/INDEX.md` - the register, one row
per topic with a one-line what and a `Verified:` date. It is not a start-read and it is not a step
between 3 and 4: it is what you open instead of guessing, and its date is the thing to distrust if a
row describes a folder you cannot find.

**The seventh thing that happens, and it is the point of the block.** At the moment the agent first *edits*
something under `context/`, the scoped rule fires - and because the port target's copy was filled at
install, the routing table is **already in the file that just loaded**. There is no fetch and no second
read: the rules arrive exactly when they are needed, at the cost of one path being touched. On
any other harness the rule fires and points at the port target's copy instead - one hop, never a stale
second body.

Where an adopted repo also ships a generated digest, it is read with the start read and never edited; this
tree ships none yet (`README.md` §4).

**Block drift, resolved 2026-11-08.** The block is a *summary*, so a host that never re-ports it drifts from
the contract silently: the one failure the `PORT:` marker cannot catch, because the marker is gone once the
fill succeeded. The ruling is a **`ported: <YYYY-MM-DD>` line in every filled shell**, written at install and
guarded by the opt-in `ported` gate for presence; there is no comparison against the block. A hash gate would
need `port/blocks/context-rules.md` beside the host, which a host does not install, and a pointer-only fill is
a legal, byte-different body. The date is what a human ranks the copy by; the comparison still happens, at a
dispute, which is what section 4's fourth rule is for. Full reasoning: `GATES.md` § *The three owed decisions*.
