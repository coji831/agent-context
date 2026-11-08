# CONCEPT - what `agent-context` is for

`agent-context` is a repo-shaped pattern for an agent's durable memory: a small tree of markdown files a
session reads at the start and writes to before it stops. It exists because an agent's memory does not
survive the session and a file does. Its unit is not a document but a placement rule: every kind of
knowledge has one home, and the home is chosen by when that knowledge has to load.

## The ranking

**1. The tree is the memory; the chat is not.** A session ends, a window is compacted, a transcript is
rewritten - none of that is a record. So the tree is what a session loads from at the start and writes to
before it stops, and a claim nobody can open in this session is not a fact. The failure it prevents is not
an agent that forgot but one that remembered a superseded version and acted on it - an index pointing at
four deleted folders, a handoff grown to a thousand lines with the real one near its end. A confident wrong
pointer is worse than no memory. Cost: every session pays a read before it does any work, and the
productive moment has to stop for a write.

**2. Attention is the budget.** A file's job is decided by what makes it load, not by how important it is:
the entry file carries pointers, the procedure loads only when the task matches it, scoped rules load when
a file they govern is touched, and bodies wait in leaves. One home per rule, because two copies drift and
the copy nobody loads is the one that gets edited. Cost: what an agent was never triggered to load, it does
not know - a procedure nobody matched is a procedure missing; every pointer is one more thing that can go
stale; and the always-loaded file is paid for at every start even when it is not read.

**3. A topic is memory, not a task.** A request is work that closes; a topic is a container that outlives
it and later drains. Authority - a spec, a locked brief - is host-supplied, and a topic never becomes it:
if a decision exists only in a topic, it is not yet a requirement. Cost: the distinction has to be held
every time someone reaches for a folder, the drain is a judgement no script performs, and a topic that
outlives its task leaves a shim whose path and date someone must verify.

**4. Mutability decides the file.** A snapshot rewritten at wrap-up and a history appended forever cannot
share a document; neither can constraints that are pruned and an index that is consulted. What is rewritten
is one use, what is appended is never corrected, what is pruned is only current. Cost: four files where one
would hold more prose, and a wrap-up that is four edits rather than one - and one file too few turns the
history into the snapshot, which is how a handoff reaches a thousand lines.

**5. Nothing durable is invisible.** The register names every topic, each topic's entry names every leaf,
and each name says in one line what the leaf answers; what is not named is not in the tree, whatever is on
disk. Cost: a second edit at the moment a leaf is created, in that same turn, and a name that has to be
kept true when the leaf is rewritten - or the tree quietly stops describing itself.

**6. One tree per root, and it does not merge.** A workspace of several repos is several trees, each
anchored on its own marker, with its own memory and its own topics; knowledge shared across them belongs to
a reference the host owns. Cost: scope has to be decided and stated rather than assumed, a task that truly
spans two repos needs a question instead of a guess, and the honest answer is sometimes two entries that
say almost the same thing.

## What this is not

- **Not a memory service.** Files, and at most a text index - no embeddings, no daemon, no network.
- **Not a task tracker or a requirement record.** Those are the host's; this tree is working state that drains.
- **Not a framework to comply with.** The pattern is prose you copy, and can change.
- **Not a transcript.** A leaf is a conclusion with its evidence, not a conversation pasted.

> **Decided 2026-11-07 - one `README.md` is enough.** A topic carrying only its entry file still holds the
> argument. The four artefacts are separated because they have different mutability, not because all four
> are compulsory: `context/README.md` already says a one-leaf, one-session topic needs only `README.md`, and
> what was never stated is that this is *the pattern* rather than a departure from it. It is the pattern.
>
> The test is therefore not the file count but whether every artefact that *does* exist has one home and one
> mutability. A topic that appends to its handoff, or snapshots inside its journey, has left the pattern
> whatever it carries - and that is a defect a count would never have caught either.
