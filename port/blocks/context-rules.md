<!-- block: context-rules -->
<!-- authority: context/README.md § Where a thing goes - if this summary and the contract disagree, the
     contract wins and this block is the stale copy. -->

**You are in `context/`, this repo's memory tree - not a scratch folder.** Before you write anything
durable, decide where it goes:

- a fact that must load before you know which topic to open (what this repo is and how to run it, a
  convention that spans topics, where an external system lives) → one line in `context/MEMORY.md`
- a constraint that applies to every topic → one rule in `context/MUST-KNOW.md`
- a constraint about one area → that topic's `MUST-KNOW.md`
- a conclusion with its evidence → a new leaf in the topic that owns it
- a decision, its reason, and what it ruled out → that topic's `decisions.md`; if no topic owns it, create
  the topic in that same turn, with its register row
- a procedure → a skill, never a longer note
- nothing durable → nowhere; do not write it

Two timing rules, which cannot be deferred to a later turn:

- **a leaf you create is named in its topic `README.md` `## Leaves` table in that same turn**, with its `id`
  and `brief` - nothing is a leaf until the index says so;
- **a `HANDOFF.md` is rewritten whole, never appended.** A snapshot that has to be appended to is a journal,
  and a journal is what a snapshot replaces.

Nothing durable goes in the chat or the commit message. The read order and the stop point are in the entry
file; the full rules are `context/README.md`.
