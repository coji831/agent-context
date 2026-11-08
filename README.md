# agent-context - a memory tree for an agent, as a folder

A repo-shaped pattern for an agent's durable memory: a small tree of markdown files a session reads at the
start and writes to before it stops. This repo carries one working copy of that tree,
[`skeleton/context/`](skeleton/context) - twelve files - one entry file every harness reads, and a dot-folder
per harness at the path it really uses. [`skeleton/`](skeleton) is a repo a host could open tomorrow;
[`port/`](port) holds the shared text the shells are filled from, plus the files that cannot be shells.
[`MANIFEST.md`](MANIFEST.md) maps one to the other. Nothing here is a framework; the pattern is prose you
copy.

The shape in one line: **the tree is the memory, the chat is not.** A session ends and a window is
compacted; a file is not. So every kind of knowledge has one home, and the home is chosen by *when* the
knowledge has to load.

## Run it in thirty seconds

```bash
git clone https://github.com/coji831/agent-context && cd agent-context
python skeleton/scripts/contextctl.py check --all   # the gates over the shipped tree
python -m unittest discover -s tests                # 76 tests for the gates themselves
```

**Adopt it:** copy `skeleton/` into your repo root, then follow [`ADOPT.md`](ADOPT.md) - eight steps, and
`check --only installed` is the one that tells you whether the copy arrived. It is disabled in this repo's own
config, because the shells shipped here still carry their `PORT:` markers by design; the config you copy with
`skeleton/` has it enabled.

**Read it:** [`CONCEPT.md`](CONCEPT.md) for what it is for, [`FOLDER.md`](FOLDER.md) for what is in it,
[`GATES.md`](GATES.md) for what is checked and what is deliberately not.

---

## 1. The tree

```
skeleton/context/
  MEMORY.md         start 1 - facts true before any topic is opened; never an aggregate of the topics
  MUST-KNOW.md      start 2 - constraints that apply to every topic, ≤10
  README.md         the contract - routing, load slots, topic artefacts, leaf identity, drain
  topics/
    INDEX.md        the register - one row per topic and its verified date
    widget/         the worked topic; delete it and its row on adoption
      README.md     topic entry: purpose, reading order, leaf index, Verified date
      MUST-KNOW.md  area constraints only - second read step
      HANDOFF.md    the snapshot - rewritten at wrap-up, never appended
      JOURNEY.md    append-only: what happened each turn, no consumer
      L-0001-….md   a leaf: id, brief, one conclusion with its evidence
      decisions.md  D-#### rows: decision, why, what it ruled out
      research/     sub-index - prior art, written before commitment
      plan/         sub-index - plan and tasks, written during
```

Around it, one file - the only one a session loads before any work - and one dot-folder per harness, named
exactly as the host has it:

```
skeleton/                     the shells a host fills
  AGENTS.md         THE CANON - the only entry file: read order, stop point, routing + its moment
  context/          the twelve files above
  .github/          Copilot - instructions/ shell
  .claude/          Claude Code - rules/ shell
  .cursor/          Cursor - rules/ shell
  .windsurf/        Windsurf - rules/ shell (path unverified)

port/                         the shared text, and what cannot be a shell
  blocks/           context-rules.md · hook-commands.md - the text, once
  skill/            context-tree/SKILL.md - the canonical body (port target only)
  skill-stub/       SKILL.md - the pointer every other present harness gets
  AGENTS-stub.md    the pointer at CLAUDE.md, for a harness that reads AGENTS.md
```

The skeleton root **is** the union of every harness's real shape, so nothing is translated at install: copy
`AGENTS.md`, `context/`, and the dot-folders you run, then fill each shell from `port/blocks/`.

**A shell is frontmatter plus a `<!-- PORT: … -->` marker** - nothing else. Filling that marker from the
one shared block *is* the install, so the text exists once and a host that still contains a `PORT:` was never
installed. The **port target** - the highest-ranked harness present - receives
the block; every other present harness gets one line pointing at it. Codex needs no folder of its own: the
root `AGENTS.md` pays one always-on routing line (156 B) instead.

Why each layer exists and what fails silently without it: [`AGENTIC-SYSTEM.md`](AGENTIC-SYSTEM.md). The
harness map, the markers and what is ported where: [`MANIFEST.md`](MANIFEST.md).

There is no root decision record: a decision is a leaf of the topic that made it. File by file, with the
trigger that loads each one: [`FOLDER.md`](FOLDER.md). How a harness connects at all:
[`AGENTIC-SYSTEM.md`](AGENTIC-SYSTEM.md). Putting it on a host repo: [`ADOPT.md`](ADOPT.md). How the tree
is used end to end - the stages, the writes at each turn, and which of them need a human: [`MECHANISM.md`](MECHANISM.md).

## 2. What decides a file's job

Not importance - **what makes it load**:

| Slot | Ships | Loads when |
| --- | --- | --- |
| start read | `MEMORY.md` | once, at start |
| root rules | `MUST-KNOW.md` | with the tree |
| on demand | `context/README.md` | a rule is unclear |
| on demand | a topic's `README.md`, then the leaf it names | the task touches that topic |
| never | `JOURNEY.md` | nothing loads it |

One home per rule: two copies drift, and the copy nobody loads is the one that gets edited. The six values
behind that, with the cost each one names, are in [`CONCEPT.md`](CONCEPT.md).

## 3. What a topic holds

Four artefacts, kept apart because each has a different **mutability**. The table below is the summary; the
rules, the drain and the leaf identity are [`skeleton/context/README.md`](skeleton/context/README.md) - the
contract, and the only copy of them:

| File | Job |
| --- | --- |
| `README.md` | entry point, reading order, leaf index, `Verified:` date |
| `HANDOFF.md` | the snapshot a new session reads instead of the chat |
| `MUST-KNOW.md` | constraints for this area only |
| `JOURNEY.md` | one entry per turn, ending at the leaf `id` or `D-####` it produced |

Beyond those, three kinds of leaf: **`L-####-<slug>.md`** (a conclusion with its evidence), **`decisions.md`**
(`D-####` rows of decision, why, and what it ruled out) and the two families **`research/`** and **`plan/`**,
each a sub-index that names its own leaves. What separates them, and when each is written, is the contract's
subject, not this file's.

## 4. What this repo does not carry yet

The tree, the entry file, one folder per harness and the gate runner are here. What is still absent:

- **`briefing.md` and `contextctl brief`** - the generated digest; until a renderer exists the register is
  the copy;
- **`contextctl resolve` and `.context-root`** - the marker earns its place only when a workspace nests two
  trees, and with it a `.gitignore` for a `state/` nothing writes yet;
- **`inbox.md`** - a capture buffer, not designed and routed to by nothing: a thought that cannot be filed
  yet has no home, and is not durable;
- **the hooks** - [`port/hooks/`](port/hooks) holds shapes that say so, and nothing blocks a turn until a
  host copies one.

`scripts/contextctl.py` runs the gates in [`GATES.md`](GATES.md) and moves no file: `check` runs the four
default gates, `check --all` adds the four opt-in ones, and `context.config.json` names the paths and budgets
they read. Gates run at a milestone or when the owner asks, never as a turn-end ritual. `VERSION` and
`LOCKED.md` record the release this was taken from.

## 5. Adopting this tree

Copy `skeleton/AGENTS.md`, `skeleton/context/`, `skeleton/scripts/` and `skeleton/context.config.json` to your
repo root, then the dot-folders for the harnesses you run (`.github/`, `.claude/`, `.cursor/`, `.windsurf/`) and
`port/skill/` if that harness reads `SKILL.md`. Fill the rule shells (MANIFEST step 4) and the copy is a host
tree; then delete `context/topics/widget/` and its row in `context/topics/INDEX.md`. **Nothing in that copy is
a workflow or a required check**: your CI is untouched, and wiring `port/hooks/ci.yml` - or requiring it - is
your decision afterwards.
[`MANIFEST.md`](MANIFEST.md) is the map - which folder belongs to which harness, what is always and what is
ported - plus the two rules that are easy to get wrong: **a repo that keeps `CLAUDE.md` deletes
`AGENTS.md`**, because Claude reads one in place of the other; and **Codex needs no folder at all**, because
its only scoping mechanism would put a thirteenth file inside the frozen `context/`, so the root `AGENTS.md`
carries the routing clause instead. The step-by-step is
[`ADOPT.md`](ADOPT.md); three rules travel with the copy and are worth keeping exactly:

- **`MEMORY.md` stays a line per fact**, and never an aggregate of the topics - that is what the topics
  themselves are for.
- **`HANDOFF.md` is rewritten, never appended.** A snapshot that has to be appended to is a journal, and a
  journal is what a snapshot replaces.
- **A leaf is named in its topic's index in the same turn it is created**, with its `id` and `brief`;
  nothing is a leaf until the index says so.

Gates run at a milestone or when the owner asks - never as a turn-end ritual.

Licence: [MIT](LICENSE).
