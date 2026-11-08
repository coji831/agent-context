---
name: context-tree
description: "Read order and stop point for this repo's context/ memory tree, and which tree applies in a multi-root workspace. Use when starting a task in this repo, or when a task may touch context/."
---

# context-tree

The rules are `context/README.md`. This file is only the order, and it is the only copy of that order.

## Read, then stop

1. **`context/MEMORY.md`** - the facts that are true before any topic is opened. One line each; a bullet
   with a body is a defect to report, not to work around.
2. **`context/MUST-KNOW.md`** - the constraints that apply to every topic. Read before acting on one: a
   rule here has already cost somebody real time.
3. **The one topic the task touches** - its `README.md`, then its `MUST-KNOW.md`, then its `HANDOFF.md`.
   `## Now` is the first action; `## Failed` is what not to retry.
4. **Stop at step 3.** If the task touches no topic, open none. Opening topics "for context" is how a
   one-screen start becomes an expensive one.

Only when a fact is missing: the leaf the topic `README.md` names, or the topic `decisions.md` when a
choice is being relitigated. `context/README.md` is not a step before step 1 - it opens when a rule is
unclear. `JOURNEY.md` is never read by an agent.

If the handoff contradicts the code, **the code wins**, and the contradiction is a finding worth
recording.

## Which tree

A repo's memory root is the directory holding `context/topics/INDEX.md`. Resolve by **proximity to the
file you are editing**, and stop at the repo boundary. A workspace holding more than one tree is
**N independent trees**.

- Never merge two `MEMORY.md` files, never promote one repo's note into another repo's topic.
- Durable knowledge shared across trees belongs to a reference the host owns, not to whichever tree you
  happened to have open.
- If the task needs the other tree, say so and ask. Expanding scope silently writes one repo's model
  into another's memory.

> If a workspace ever nests two trees, a `.context-root` marker settles which one owns a path; it, and
> `resolve --where` to read it, are **not shipped yet** - `contextctl.py` runs `check` and a `brief` stub,
> and `resolve` is not written, so the marker is a design this tree names and no copy carries.
