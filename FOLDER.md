# FOLDER - the tree, file by file

`context/MEMORY.md` is the one file a reader opens first: the facts that are true before any topic is
opened. Then `context/MUST-KNOW.md`, then the one topic the task touches, then stop. `skeleton/` holds the
**shells** a host fills; `port/` holds the text they are filled from, and the files that cannot be a shell.
`MANIFEST.md` maps one to the other. `CONCEPT.md` argues for the shape; this file only maps it.

## Repo root - the documents, the pin, the tests and the CI, and none of them a node of the memory

- `FOLDER.md` - this map: what each file is, when it loads, and what edits it; read first.
- `CONCEPT.md` - the six-value argument that decides a placement; on demand, when a placement is in question.
- `README.md` - the short entry: the tree, the load slots, what this repo does not carry yet; on demand.
- `GATES.md` - **what keeps the tree correct**: the eight gates with their assertion, finding and cadence, the four defaults and the four opt-ins, the three decided questions, and what is deliberately unchecked; read when a check surprises you or before adding one.
- `MANIFEST.md` - **the install contract**: the placeholder invariant, the rank and the port target, the three artefact kinds, install in seven steps, the marker vocabulary; read while adopting, never by a session.
- `ADOPT.md` - the runbook an agent follows to put the tree on a host repo, fresh or add-on; when adopting, and never again.
- `AGENTIC-SYSTEM.md` - how a harness connects at all: the authoring map (§0 - where each artefact is edited), the three connection layers in order with what each silently does without, per harness the file that must exist, the write contract, the dispute order, and one worked arrival; when the wiring is in question.
- `MECHANISM.md` - **how the tree is used**: the five stages with the file each writes and its mutability, the operations at each turn, who may perform each one without asking (`act` / `ask` / `owner`), one worked session; on demand, when the operation or a write's authority is in question, never loaded by a session.
- `VERSION` - `1.0.1`; read by tooling and humans, never by a session. What the first release contains, and the decisions behind it: `LOCKED.md`.
- `.gitattributes` - `* text=auto eol=lf`, with `.ps1` at CRLF; read by git, never by a session. It is load-bearing rather than tidy: a CRLF `port/hooks/pre-commit.sh` fails under bash with `$'\r': command not found`, which is a hook that looks installed and cannot run.
- `.gitignore` - `__pycache__/` and `*.py[cod]`, plus the two tool caches; read by git, never by a session. A committed `.pyc` is a diff nobody reads and a file every run rewrites.
- `LOCKED.md` - the owner's rulings, the release record and the step decisions behind them; a human audit trail, never loaded by a session.
- `context.config.json` - **this repo's own config**: every path points under `skeleton/context/`, `installed` and `ported` are disabled (the shipped shells hold markers), `verified` is advisory. The host's starting config is the separate file inside `skeleton/`, copied with it.
- `tests/` - `test_gates.py`: `python -m unittest discover -s tests`; every gate fails on its own defect fixture and passes on a clean tree. Not copied to a host: it tests the tool, not the memory tree.
- `.github/workflows/context.yml` - this repo's own CI: `skeleton/scripts/contextctl.py check --all` over the shipped tree, then the tests. A host copies `port/hooks/ci.yml` instead.

## skeleton/ - the shells a host fills

Holds files that are **correct in shape** in a host: each harness owns its own dot-folder, so they cannot
collide and nothing is translated at install. Their bodies are **shells** - a `<!-- PORT: … -->` marker
where the shared text goes, legal here and nowhere else.

- `AGENTS.md` - **the canon**, and the only entry file: the memory rule, the read order, where to stop, one line naming the skill, and the routing clause with its moment (*read the contract before you write*), between `<!-- context:begin -->` and `<!-- context:end -->`; **injected at the start of every session, before anything else** - the one unconditional cost: 664 B as this file ships, of which the marked block a host upserts is 625 B; long-term. **The only copy of the block** - a Claude host renames this file to `CLAUDE.md`; it is never copied.
- `context/` - the memory root, mapped below.
- `context.config.json` - **the host's starting config**: its paths are the host's own, `shells` names all four rule files, and `port_target` starts null, so `check --only installed` fails until the fill. **Trim `shells` to the harness folders you copied** - a named-but-absent path fails `installed`. The repo's own config is the separate file at the repo root.
- `.gitignore` - `__pycache__/` and `*.py[cod]`, plus the two tool caches; copied to a host root, or merged into an existing file. Without it a `cp -r` of `scripts/` can carry a bytecode cache into the host's first commit.
- `scripts/contextctl.py` - the **gate runner**, the only copy: `check` (four default gates), `check --all` (plus the four opt-in), `--warn`, `--only`, `--skip`, `--json`, and `brief` as a **stub** that writes nothing and exits 0 so a hook has something real to call; it reads and reports and **writes nothing else**. Copied to the host's own `scripts/contextctl.py`, where the hook commands have always pointed; inert until invoked, so it is a skeleton file and not a `port/` one.
- `.github/instructions/context.instructions.md` - the write-time **trigger**, as a **shell**: `applyTo` frontmatter only, then a `<!-- PORT: context-rules -->` marker. Install fills that marker from `port/blocks/context-rules.md`; injected only when a governed path is touched.
- `.claude/rules/context.md` - the same shell in Claude frontmatter (`paths:`, not `applyTo:`; both keys documented by the harness vendors - see `AGENTIC-SYSTEM.md`'s sources); at write time.
- `.cursor/rules/context.mdc` - the same shell as `.mdc`, because a plain `.md` here is ignored; at write time.
- `.windsurf/rules/context.md` - the same shell, **path and frontmatter unverified**; at write time if the path holds.

**Codex has no folder here, and that is the design.** It scopes by directory placement only, which would
mean a thirteenth file inside the frozen `context/`; instead the root `AGENTS.md` carries the routing clause
always-on (one 156 B routing line) and Codex is served with no file of its own. Hooks are executable, so their shapes live in
`port/hooks/` and their shared command text in `port/blocks/hook-commands.md` - no hook file sits here at all.

## port/ - the text that fills the shells, and what cannot be a shell

Holds files that would be **wrong or harmful** in a host: executable (an unused hook fails every session),
mutually exclusive (a second entry file is dead text), or one body for several destinations (three copies
drift).

- `README.md` - the test that sorts skeleton from port, the block authority rule, and how to verify an install; read when installing.
- `blocks/context-rules.md` - **the shared rule text**: the routing table plus the two timing rules, filled into the port target's shell. `context/README.md` is named authority in its header; changes when the contract does.
- `blocks/hook-commands.md` - **the shared hook text**: the four intents as one-line commands and which block; changes when the tooling does.
- `skill/context-tree/SKILL.md` - the read order, the stop point, which tree applies - and nothing else; only its `description` is always paid, the body loads on match; **the canonical copy**, installed into the port target's skill directory only.
- `skill-stub/SKILL.md` - the pointer a non-canonical harness gets when it reads its own skill directory: same frontmatter so it still loads, then the canonical path and a stop-if-missing rule; here because it exists only when a host runs two skill-reading harnesses.
- `AGENTS-stub.md` - the pointer at `CLAUDE.md` for a harness that reads `AGENTS.md` while `CLAUDE.md` is canonical; here because Claude reads one **instead of** the other, never both.
- `hooks/README.md` - the four hook **intents** and what each level costs; read when choosing enforcement; stable.
- `hooks/pre-commit.sh`, `pre-commit.ps1`, `ci.yml` - the intents as shapes to adapt: gate the commit, gate the merge; **never installed by default**; change only when the tooling does.
- `hooks/copilot-vscode-hooks.json` - the Copilot hook intent, here because **no repository-level hook path could be verified**; a guess inside `skeleton/` would be trusted and then not load.
- `hooks/cursor-hooks.json` - `sessionStart` / `stop` for Cursor; event names verified, payload schema not; here because it **executes**.
- `hooks/codex-hooks.json` - `SessionStart` / `Stop` for Codex; event names verified, object shape not; here because it **executes**, and a non-managed hook needs a human to trust it first.

## skeleton/context/ - the memory root; three files, and the contract is the biggest of them

- `MEMORY.md` - cross-cutting facts only: what this repo is, conventions that span topics, where an external system lives; one line each, never an aggregate of the topics; **at start, step 1**; long-term, edited when a fact changes.
- `MUST-KNOW.md` - the constraints that apply to every topic, ≤10, admission-tested and ordered by blast radius; **at start, step 2**; long-term, pruned.
- `README.md` - the contract: where a thing goes, what loads and when, a topic is not a task, what a topic holds, leaf identity, nesting, drain; **on demand**, when a rule is unclear; stable, edited only when the pattern changes.

### skeleton/context/topics/ - one folder per live topic, depth <=3, fan-out ~10

- `INDEX.md` - the register: one row per topic with its path, a one-line what, and a `Verified:` date; **on demand**; a folder with no row and a row with no folder are both findings.

### skeleton/context/topics/widget/ - one topic folder, shipped as the worked shape; delete it and its row on adoption

- `README.md` - the topic entry: purpose, reading order, `Verified:` date, and a `## Leaves` table of `id` · leaf · brief; **on the topic's trigger, first**; edited when a leaf is added.
- `MUST-KNOW.md` - the constraints that hold for this area only, mock-shipped; **on the topic's trigger, second**; pruned, created with the first earned rule.
- `HANDOFF.md` - the snapshot (`Now · State · Test · Next · Blockers · Failed · Refs`), `## Now` required; **on the topic's trigger, last**; one-time use - rewritten whole at each wrap-up, never appended.
- `JOURNEY.md` - append-only `J-` entries recording what happened in a turn, reasoning included, ending at the leaf `id` or `D-####` it produced; **never read by an agent**; long-term, appended per turn, never corrected.
- `L-0001-widget-throughput.md` - a leaf: `id`, `brief`, then one conclusion with its evidence and the option rejected; **on demand**, only when the README's brief is not enough; long-term, rewritten as the finding sharpens.
- `decisions.md` - mock-shipped; `D-####` rows of decision, why, and what it ruled out, no cap; **on demand**, only when a choice is being relitigated; long-term, appended per choice.

### skeleton/context/topics/widget/research/ and plan/ - the two leaf families, each a sub-index

- `research/README.md` - background and prior art, written before commitment; **on demand**; names its own leaves, and the topic README names the folder.
- `plan/README.md` - plan, phases, tasks, written during and rewritten freely; **on demand**; names its own leaves the same way.

### skeleton/context/archive/ - where a drained topic's files go; created by the first drain, absent until then

- `<topic>-<original name>` - one flat folder at the tree root, holding the leaves, `decisions.md` and `JOURNEY.md` of every drained topic, each file prefixed with its topic name so two topics cannot collide; **never read by an agent** unless a shim sends it there, and **never inside `topics/`** - every gate scopes to `topics_dir`, so an archive folder there reads as a live topic and its leaves as live ones, failing `register` and `leaf-index` on a correct drain.

## A correct new topic, from this document and `CONCEPT.md` alone

The register and the folder must agree in both directions, so create them in one turn:

1. `context/topics/billing-export/README.md` - a title and one-line purpose, `Verified: 2026-11-07`, a reading order, an empty `## Leaves` table (`id` · leaf · brief), and no *Families* list until a family holds a leaf.
2. `context/topics/billing-export/L-0001-export-rate.md` - starting `id: L-0001` and `brief: what the export run measured, and the verdict`, then the evidence, the verdict, and the option rejected.
3. The same `README.md` - the leaf named in `## Leaves` in that same turn: `| L-0001 | L-0001-export-rate.md | what the export run measured, and the verdict |`.
4. `context/topics/INDEX.md` - one new row: the path, a one-line what, and `2026-11-07` - the date **identical** to the README's `Verified:`, and never a second row for the same topic.

Only as the work needs them:

- `HANDOFF.md` - written at wrap-up, `## Now` present; its absence means "not yet wrapped up", not a defect.
- `decisions.md` - the first time a choice needs a reason that outlives the turn.
- `MUST-KNOW.md` - when an area constraint earns it.
- `JOURNEY.md` - one appended entry per turn, from `J-0001`, saying what happened and naming the id it produced.
- `research/` or `plan/` - when the first leaf of that family exists; each gets a `README.md` sub-index naming its leaves, and the topic README names the folder.

## Not in this tree yet

The entry file, the shells, the skill, the hook shapes and the gate runner are here. What is still absent:

- a generated `briefing.md`; `brief` exists as a stub that writes nothing and says so, and the register is
  the copy until a renderer exists;
- `resolve --where` and `.context-root` - the marker earns its place only when a workspace nests two trees,
  and with it the `.gitignore` for a derived `state/` that nothing writes yet;
- `inbox.md` is not designed and nothing routes to it: a thought that cannot be filed yet has no home, and
  is not durable;
- any hook actually installed - `port/hooks/` holds shapes and says so.

`skeleton/scripts/contextctl.py` runs the gates in `GATES.md` over the tree its `context.config.json` names,
and it moves no file. Three config keys change what it looks at: `leaf_pattern` (what counts as a leaf),
`accepted_absent` (citations a clone cannot resolve) and `extra_checks` (the host's own checks, run under
`--all`). Gates run at a milestone or when the owner asks, never as a turn-end ritual; this repo's
own config disables `installed` and `ported` (its shells hold markers by design) and holds `verified` advisory.

## What the tree does not contain

No root decision record - a decision is a leaf of the topic that made it. No task tracker, no requirement
record, no embeddings, daemon or network, no transcript, no task per topic, and no aggregate of the topics
at the root. Open next: `CONCEPT.md` for the why, then `skeleton/context/README.md` for a topic's rules.
