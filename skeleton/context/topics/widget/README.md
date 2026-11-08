# widget - one subject, one folder

Verified: 2026-01-01

> An example topic: delete it, and its row, on adoption. The README is the one file a later session
> opens whenever the topic is touched - what this is, the reading order, and where each leaf is named.
> A leaf is named in its **nearest** index: here, until its family (`research/`, `plan/`) has its own
> `README.md`, and then there, with this file naming the folder.

## What this is

One or two sentences: the question this topic answers, or the work it holds.

## Reading order

1. [`MUST-KNOW.md`](./MUST-KNOW.md) - the constraints for this area, if any were earned.
2. [`L-0001-widget-throughput.md`](./L-0001-widget-throughput.md) - what the rig measured, and the verdict.
3. [`decisions.md`](./decisions.md) - only if a choice in this topic is in question.

## Leaves

| id | Leaf | Brief - what it answers |
| --- | --- | --- |
| `L-0001` | `L-0001-widget-throughput.md` | what the rig measured, and the verdict |

Every leaf carries the same `id` and `brief` in its first two lines. A leaf is created and named here in
the same turn, and nothing is a leaf until this table says so.

## Families

- `research/` - background and prior art, written before commitment; [sub-index](./research/README.md).
- `plan/` - plan, phases, tasks, written during and rewritten freely; [sub-index](./plan/README.md).

Both families ship here so the shape is legible; they are **empty on purpose**, and in a real topic a
family is added to this list only when it holds its first leaf - a sub-index that names nothing is a
folder pretending to be structure. Delete these two folders when you adopt.
