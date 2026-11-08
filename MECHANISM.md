# MECHANISM - how the tree is used, end to end

> One question: **how is this tree used, and how does it work?** The five stages, the operations at each
> turn, and who may perform each one without asking.

Authority is `CONCEPT.md` (the six values), then `skeleton/context/README.md` (the contract); the file map
is `FOLDER.md`; the write contract and one worked arrival are `AGENTIC-SYSTEM.md` sections 3 and 5; read
order and which tree applies is `port/skill/context-tree/SKILL.md`; the routing table is the contract and
its summary `port/blocks/context-rules.md`; the per-harness table is `AGENTIC-SYSTEM.md` section 2;
adoption is `ADOPT.md`; the install contract is `MANIFEST.md`. None is restated here.

## The question every response answers

Four questions in a fixed order, and the answer always names a file:

| # | Question | If the answer is no |
| --- | --- | --- |
| 1 | Does a topic own this? | the routing table decides: a fact spanning topics is a `MEMORY.md` line; a decision with no topic creates it in that turn, with its register row |
| 2 | Is it durable at all? | write nowhere, and never restate it as recorded |
| 3 | Which kind is it: fact, area rule, leaf, decision, procedure? | then it is not durable yet; write nowhere |
| 4 | Is it mine to write? | a requirement is never edited; the code beats prose |

Nothing durable in the chat, nothing outside the tree, and every write reported as file plus section.

## Three classes of authority

| Class | The agent | Applies when the write is |
| --- | --- | --- |
| **act** | writes it, names file and section in the reply | reversible, one topic, no new always-loaded cost |
| **ask** | proposes the exact write and waits | irreversible, raises always-loaded cost, or spans trees |
| **owner** | cannot start it; your word starts it, then it writes | the trigger is a judgement on your context or subject |

Derived, not chosen: value 2 prices attention, so anything loadable every session needs your consent; value
1 prices a wrong pointer, so removing a file needs it; value 4 makes the rest cheap enough to just do. Class
governs the **trigger** only - once you say "wrap up", the write itself is `act`.

## Topic level

These are the stages of a topic: start (T1), wrap-up (T2), pick-up (T3), drain (T5). Capture - the writes a
turn makes - is the table at each turn, the only stage that happens inside a turn rather than between them.

| # | Operation | Trigger | Writes (mutability) | Class |
| --- | --- | --- | --- | --- |
| T0 | **route** | owning tree or topic not yet known | nothing; reads entry, `MEMORY.md`, `MUST-KNOW.md`, `INDEX.md` | act; **ask** over two repos |
| T1 | **start** | work has no owning topic and either outlives the request or leaves a decision no topic owns | topic `README.md` **created** + `INDEX.md` row **appended**, same turn and date | act |
| T2 | **wrap-up** | you judge the context will not carry the next step | `HANDOFF.md` **created** or **rewritten whole**; `JOURNEY.md` **appended** | **owner** |
| T3 | **pick-up** | reached a topic whose `HANDOFF.md` exists | nothing; `## Now` first, `## Failed` not retried | act |
| T4 | **trim leaves** | a leaf is superseded, duplicated, or decayed to a fact | survivor **rewritten**, other **deleted**, its `## Leaves` row same turn | act; **ask** for another leaf |
| T4a | **retire a family** | last leaf of a family trimmed or promoted away | family `README.md` **deleted**, its line removed | act if it follows its own trim |
| T5 | **drain** | work finished or abandoned | every artefact, per the list below | **owner**; **ask** for the plan |

The state line: `no topic -> started -> live (HANDOFF absent or present, alternating with each wrap-up) ->
drained -> shim`. Only start and drain change the register.

**Prevents.** route: writing one repo's model into another's memory. start: a topic on disk that no register
names. wrap-up: the next session re-deriving from the chat, and a handoff grown to a thousand lines. pick-up:
retrying what already failed, and starting from a next step that stopped being true. trim: a topic growing a
second copy of one conclusion. retire: a sub-index that names nothing. drain: a topic outliving its task as
an unbounded diary.

**Drain, artefact by artefact.** `MUST-KNOW.md` distilled then **deleted**; leaves and `decisions.md`
distilled to a `MEMORY.md` line or a root rule, then the files **archived** - not deleted, because they hold
the evidence the distilled line rests on; `research/` **moved** if still true, else archived; `JOURNEY.md`
**archived wholesale**, never deleted - it is the dataset; `plan/` and `HANDOFF.md` **deleted**, a stale
"next" is a trap; `README.md` **rewritten** into a shim naming the path, what moved, the date checked; the
register row **rewritten** to say drained. A shim with no date deletes the right copy and points at the wrong
one.

**Where "archived" means.** `context/archive/`, at the tree root, flat, each file prefixed with its topic name
(`billing-export-L-0001-export-rate.md`). **Never inside `topics/`**: every gate scopes to `topics_dir`, so an
archive folder there is read as a live topic and its leaves as live leaves, which fails `register` and
`leaf-index` on a correct drain. The folder is outside every scan, which is the point of putting it there. The
default is `[policy]`; a repo that wants another location says so in the shim, which names the path it used.

## At each turn

| # | Operation | Fires when | Writes (mutability) | Class |
| --- | --- | --- | --- | --- |
| U1 | **new leaf** | a conclusion has evidence the `brief` cannot carry | `L-####-<slug>.md` **created**, `id` and `brief` first two lines; row **appended** same turn | act |
| U1b | **rewrite it** | a later turn sharpens the same conclusion | same file **rewritten**; never a second leaf | act |
| U2 | **a leaf family** | before commitment (`research/`), or during work (`plan/`) | family `README.md` **created** naming its leaves; topic README names the folder | act |
| U3 | **area rule** | a rule already cost somebody real time, in this area | topic `MUST-KNOW.md` **created** with the first, then **pruned** | act |
| U3b | **root rule** | the rule holds for every topic | root `MUST-KNOW.md`, admission-tested, ordered by blast radius | **ask** |
| U4 | **journey entry** | the turn ends | `J-####` **appended**: the route taken, the reasoning, and the id it produced | act |
| U5 | **memory line** | a fact is true before any topic opens | one line **appended**; never an aggregate; a bullet with a body is a defect | **ask** |
| U5b | **correct one** | an existing line stopped being true | that line **rewritten** in place | act |
| U6 | **decision row** | a choice's reason outlives the turn | `decisions.md`, `D-####` **appended**: decision, why, what it ruled out | act |
| U7 | **bump the date** | a re-read found the material still true | topic `README.md` `Verified:` **rewritten** | act |

**The three boundaries.** A fact with no evidence is a `MEMORY.md` line. A choice with its reason is a
`decisions.md` row. Anything that needs both is a leaf. `MUST-KNOW.md` carries neither a fact nor evidence,
only a rule a reader must not violate.

**Families split by mutability, not subject.** `research/` grows and is rarely edited; `plan/` is rewritten
freely. A family exists only once it holds a leaf; until then the leaf is named in the topic README.

**What a journey entry records.** What happened in the turn, reasoning included: the route taken, what was
considered and set aside, and the `L-####` or `D-####` it ended at. "Write the process, not only the
result." An entry is never edited, so its reasoning is a record of what was thought at that moment, not a
claim that is still true - which is exactly why nothing loads the file. Append freely; do not go back.

**When a leaf becomes a new leaf.** By default the moment the subject changes - a different question, a
different measurement, a different verdict. A rewrite stays a rewrite while the subject holds, however many
turns that takes. **Settled in `GATES.md`:** a leaf's growth is capped at `leaves.max_lines` (a gate), the
count capped is fan-out rather than conclusions (the contract's constant), and **no maximum number of leaves
per topic exists** - a count would force unrelated conclusions apart to satisfy arithmetic.

## What is detectable, and what is not

A hook or check can compare: a file no index names, a row whose file is gone, a count over a cap, a date
older than the commit that last touched the file, a format broken, two `brief` lines that are
near-duplicates.

It cannot judge: stale, superseded, finished, worth keeping, belongs at the root, no longer the same
conclusion. Every `act` above has a detectable shape; almost every `ask` and every `owner` does not. That is
not a gap, it is why the ladder exists - and `ask` is the cheap substitute, since a mechanism too
judgemental to gate can still be raised as a question at the moment it matters.

## Nothing is enforced by default

Each trigger above is a shape this repo ships; a host may enable any of them, per trigger, at one of three
postures: **off** (prose the agent follows), **surface** (printed, nothing blocks), **gate** (blocks a
commit, a merge or a turn). **Settled in `GATES.md`:** nothing is on by default, the four default gates run
only when the owner or a hook calls `check`, and the single exception to "off for everything" is `installed`,
which judges whether the tree arrived rather than what it says. A mechanism that blocks on day one is
disabled on day two, and the tree is workable by hand today.

## The commands

| Intent | Shape | Blocks? |
| --- | --- | --- |
| keep the digest current | `contextctl brief` | no |
| remind | `contextctl check --all --warn` | no - prints every finding, exit 0 |
| gate the commit | `contextctl check` | yes |
| gate the merge | `contextctl check --all` | yes |
| settle which tree owns a path | `contextctl resolve --where` | no |

**Only the `check` rows exist so far**, with `--warn`, `--all`, `--only` and `--skip`; `brief` and `resolve`
are not written, and a hook that names them fails loudly on its first run, which is correct. `GATES.md` is the
set `check` runs. **The tool moves no file** - draining a topic, trimming a leaf and retiring a family are
judgements it will not make.

## Two things nothing schedules

`wrap-up` is yours: a schedule would fire when the context is fine and stay silent when it is not. A
detection that suggests one may be enabled, and stays off by default. `drain` is a judgement: only someone
reading the topic can say its work is finished, and no check tells a finished topic from a quiet one. When
neither happens, a topic with no `HANDOFF.md` has not been wrapped up - a state, not a defect - and a topic
that never drains stays live, its register row and date intact. What is missing is the transfer.

## One worked session

The task: "the widget rig reads 40 percent below target - why?". Session A is the first ever on this topic.

1. `AGENTS.md` loads; its marked block says memory is `context/`, the order, the stop point and the skill.
2. `context/MEMORY.md` then `context/MUST-KNOW.md`: "the rig is `benches/rig.py` on `data/`"; "payload sizes
   are fixed; never tune the fixture."
3. `context/topics/widget/README.md`: purpose, order, `## Leaves` naming `L-0001` and its brief; the brief
   does not answer the question, so its leaf opens.
4. `context/topics/widget/MUST-KNOW.md`: "the 5 ms floor is per batch, not per call."
5. No `HANDOFF.md` exists, so the read stops there: that absence is the state "never wrapped up".
6. The first edit under `context/` fires the scoped rule, filled at install: the routing table is loaded.
7. The subject is new, so `L-0002-floor-is-per-call.md` is **created** and its row **appended** to
   `## Leaves`, same turn.
8. `JOURNEY.md` gains `J-0001`, appended: read `L-0001`, measured the floor per call, created `L-0002`.
9. You call wrap-up, so `HANDOFF.md` is **created** whole: `## Now` = "read the scheduler's batch size and
   settle L-0002"; `## Failed` = "retuning the fixture: it changed the input, not the floor."
10. Session B starts, steps 1 to 5 identical, and step 6 now exists: `HANDOFF.md` whole, `## Now` as its
    first action, `## Failed` as what not to retry.
11. What B reads that A wrote: `HANDOFF.md` in every section, and the `L-0002` row in `## Leaves`, which may
    answer B's question without the leaf ever being opened.
12. The topic stays live; nothing has drained it, and nothing will until someone judges the work finished.
