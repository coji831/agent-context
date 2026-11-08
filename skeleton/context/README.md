# context/ - the memory contract

> Rules only. This file states where a thing goes and what may not happen; it does not list the topics -
> that register is `context/topics/INDEX.md`, because a rule must not change when a topic opens or closes.
>
> **Two kinds of sentence live here, and they are marked.** `[concept]` is why the pattern works:
> changing it means adopting a different pattern. `[policy]` is this repo's choice: change it freely and
> say so here. **No budget and no path is written here** - those belong to `context.config.json`, so a
> rule does not move when a budget does. A structural constant that no config key owns, such as a nesting
> depth, is stated where it is governed.

## Where a thing goes `[concept]`

| The work was | It goes to |
| --- | --- |
| a fact that must load before you know which topic to open | one line in `MEMORY.md` |
| a constraint that applies to every topic | one rule in `MUST-KNOW.md` |
| a constraint about one area | that topic's `MUST-KNOW.md` |
| a conclusion with its evidence | a leaf in the topic that owns it |
| a decision, its reason, what it ruled out | a leaf in the topic that made it - `decisions.md` |
| the same, when no topic owns it | the topic is created in that same turn, with its register row - a folder with no row is a finding |
| a procedure | a skill, not a longer note |
| nothing durable | nowhere - do not write it |

One home per kind: two copies drift, and the copy nobody loads is the one that gets edited.

## What loads, and when `[concept]`

The unit is not a tier number, it is **what makes a file load**. A trigger is something a harness can
honour; a content type is not.

| Slot | Ships | Loads when |
| --- | --- | --- |
| start read | `MEMORY.md` | once, at start |
| root rules | `MUST-KNOW.md` | with the tree |
| on demand | this contract | a rule is unclear |
| on demand | a topic's `README.md`, then the leaf it names | the task touches that topic |
| never | `JOURNEY.md` | nothing loads it |

## A topic is not a task `[concept]`

A **request** is the unit of *work*; a **topic** is the unit of *memory*. They have different lifetimes,
and confusing them is how a topic becomes an unbounded diary.

1. A request arrives.
2. It is written down *as it happens* inside a topic: `plan/` while it runs, `HANDOFF.md` at each
   wrap-up, `JOURNEY.md` append-only, `research/` before commitment.
3. When the topic **drains**, what is still true is distilled to the durable home and the topic becomes a
   shim. Nothing in a topic is authority.

**A requirement record is host-supplied.** A spec, a locked brief - the thing a chat calls "what must be
true" - is not an artefact of this tree. Where a host keeps one, the agent does not edit it, and a change
is a **new revision**. **A topic never becomes that record**: a decision that exists only in a topic is
not yet a requirement.

## What a topic may hold `[policy]`

Four artefacts, kept apart because each has a different **mutability** - what is rewritten and what is
appended cannot share one document.

| File | Job | Written |
| --- | --- | --- |
| `README.md` | entry point: purpose, reading order, leaf index, `Verified:` date | rarely; when a leaf is added |
| `HANDOFF.md` | the snapshot a new session reads instead of the chat | **rewritten at wrap-up; one use, replaced** |
| `MUST-KNOW.md` | present-tense constraints for this area only | pruned; created only when one is earned |
| `JOURNEY.md` | append-only: one entry per turn, saying what happened and where it ended. **It may hold reasoning**; it is never corrected, so it records what was thought, not what is true | appended, never edited |

**Wrap-up is a decision, not a schedule** - the user's call: the remaining context will not carry the
next step, or the next step should begin fresh. `HANDOFF.md` is written then and read once at pick-up, so
a wrap-up that never happens has no backstop.

**Create them on need.** A one-leaf, one-session topic needs only `README.md`. A topic with no `HANDOFF.md`
has not been wrapped up - a state, not a defect, and the drain deletes that file by design. What is
required is that a handoff which *exists* says what to do first: `## Now`.

Two leaf families, split by mutability rather than subject: `research/` (written before commitment, grows,
rarely edited) and `plan/` (written during, rewritten freely). A family with its own `README.md` is a
**sub-index**: it names its leaves, and the topic README names the folder.

`JOURNEY.md` is a **producer with no consumer** - nothing loads it, so a topic whose turns were never noted
looks exactly like a topic with no turns, and absence must not be read as evidence of no work. Because an
entry is never corrected, the reasoning it may carry is a record of the thought of the moment; it is written
freely and never cited as a conclusion.

## A leaf is a conclusion, and it has an identity `[concept]`

A leaf is not a note. It is a conclusion **with its evidence** - what was asked, how it was measured, the
verdict, the option rejected. A fact without evidence is a `MEMORY.md` line; a choice with a reason is that
topic's `decisions.md`; anything that needs both is a leaf.

Every leaf carries an **`id`** and a **`brief`** - one line saying what it answers - in its first two lines,
and the topic README's index repeats both. That is what makes a leaf citable from a `JOURNEY` entry, which
names an id and never a line number, and checkable when the leaf is rewritten.

The index's **header names the column holding the file name** (`Leaf`, or `File`); the gate reads that column
and never assumes the second one, so `| Leaf | What it answers |` and `| id | Leaf | Brief |` both work. A
table with no header at all is read in the order above, `id | Leaf | Brief`. A **family** `README.md` is an
index only when its first table names a file column: prose in a table is not a leaf index, and a family
README without one is not read as one.

`decisions.md` is the one leaf whose **name** is fixed rather than derived from an id; its rows carry the
ids instead, `D-####`, and a `JOURNEY` entry cites the row it produced. That is also why it is not listed in
`## Leaves`: the leaf table indexes conclusions, not choices, and a choice is cited by its `D-####` row
rather than by a leaf id.

## Nesting and naming `[concept]`

Depth ≤3, fan-out ~10. At 11 entries add an index and group within it - do not add a level. **Numbers are
identity, never order**; dated filenames belong only inside append-only logs.

## When a topic closes `[policy]`

| Artefact | Fate |
| --- | --- |
| `MUST-KNOW.md` | **distil** to the durable home, then delete the file |
| `research/` | move to the durable home if still true, else archive |
| `JOURNEY.md` | **archive wholesale** - never delete; it is the dataset |
| `plan/`, `HANDOFF.md` | delete - a stale "next" is a trap |
| leaves, `decisions.md` | what is still true becomes a line in `MEMORY.md` or a rule in `MUST-KNOW.md`; the leaf itself is archived, not deleted, because it holds the evidence the distilled line rests on |
| `README.md` | becomes a **shim**: authoritative path, what moved, the date checked |
| the register row | bump its date and say **drained** |

**Archive means `context/archive/`, at the tree root.** One flat folder, files prefixed with the topic name
(`<topic>-<original name>`) so two topics can never collide, and **never under `topics/`** - every gate scopes
itself to `topics_dir`, so a folder there reads as a topic and its leaves as live ones. The location is a
`[policy]` default, not a concept: a repo that wants its archive elsewhere changes it in one place, the shim,
which names the path it actually used.

Records and journeys are kept because their value is *historical*; must-know lines are deleted because
their value is *current*. A shim to an unverified document deletes the correct copy and points at the wrong
one, so a shim names the path *and* the date.
