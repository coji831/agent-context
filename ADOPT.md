# ADOPT - putting this tree on a host repo

> For the agent asked *"set up this memory tree in repo X"*. **Fresh** and **add-on** differ in **two**
> respects, both named below: whether the entry file is created or upserted (§5), and whether `MEMORY.md` is
> written from scratch or migrated from what the repo already has (§4A vs §4B). Everything else is the same
> job.
>
> Three folders, and only the right parts land: [`skeleton/`](skeleton) holds the per-harness **shells**,
> [`port/blocks/`](port/blocks) the **shared text** that fills them, and [`port/`](port) everything that
> cannot be a shell. [`MANIFEST.md`](MANIFEST.md) maps one to the other.
> The pattern is [`CONCEPT.md`](CONCEPT.md); the files are [`FOLDER.md`](FOLDER.md); why a harness needs
> any of it is [`AGENTIC-SYSTEM.md`](AGENTIC-SYSTEM.md).

## Step 1 - ask three things, then say which mode you are in

| Question | Why it changes the job |
| --- | --- |
| Where does this repo's knowledge live today? | the migration points at it; nothing is deleted |
| Which harnesses run here, and which is primary? | that decides every path below, and the highest-ranked one owns the rule body |
| Should this block, or only report? | a repo in month one wants reports; a settled repo can block |

Rank order is Claude, then Copilot, then Cursor, then Windsurf (Codex needs no shell) - [`MANIFEST.md`](MANIFEST.md) § *The rank*.

If you cannot ask, adopt in the **softest** shape, say so in one line, and leave the decision written
down for the human to harden.

## Step 2 - copy the memory, the gate runner, and its config

```bash
cp -r <scaffold>/skeleton/context <repo>/
cp -r <scaffold>/skeleton/scripts <repo>/
cp <scaffold>/skeleton/context.config.json <repo>/
```

`context/` is the one entry that is **always** copied and never merged: it is the memory, and a host that
already has one does the merge in the last section instead of this copy. Do **not** copy the entry file here - that is
step 5, because an add-on host already has one and a blind copy would overwrite it.

`scripts/contextctl.py` and `context.config.json` are what make the copy checkable, and they are inert until
invoked. The config already points at the host's own `context/` and names the four rule files in `shells`,
so `check --only installed` fails until step 6 fills them - that failure is the install check, not a fault.
Copy neither, and the tree is memory with no gates; say so once rather than leaving it to be discovered.

The harness dot-folders are **not** in this copy: which of `.github/`, `.claude/`, `.cursor/`, `.windsurf/`
exists is decided in step 6, because copying four folders into a repo that runs one is a named failure.

## Step 3 - the example topic, both halves at once

Delete `context/topics/widget/` **and** its row in `context/topics/INDEX.md` in the same edit. The
register is checked in both directions, so a folder without a row and a row without a folder are the same
defect seen from two sides. Leaving the row behind is the check working, not the copy failing.

## Step 4A - fresh repo

Write `context/MEMORY.md`: one line per fact, pointing at the file that owns it. `MUST-KNOW.md` stays
short - a rule that has never prevented anything is a reader's tax. Then create your first real topic
from [`FOLDER.md`](FOLDER.md)'s worked example.

## Step 4B - add-on: migrate by pointing, delete nothing

1. **`MEMORY.md` gets pointers, not prose.** A 40 KB legacy doc becomes ~45 lines of one-line facts, each
   pointing at the file that owns it. The compression is the work, not a side effect.
2. **One topic `README.md` per subject that already exists**, carrying a `Verified:` date taken from the
   file's own history, not from today: `git log -1 --format=%cs -- <path>`.
3. **A register row for every topic, and no row without a folder.**
4. **Leave the old documents where they are.** A moved file breaks every other reader's links; a pointer
   keeps both audiences working and the old location can be archived later, calmly.

## Step 5 - place the entry file

This is where the two modes actually part company. **Never copy the entry block over a file the host already
has.**

**Fresh host, one harness** - copy it:

```bash
cp <scaffold>/skeleton/AGENTS.md <repo>/
```

**Fresh host, Claude Code** - **rename, do not copy**: `git mv AGENTS.md CLAUDE.md` after copying it. The
copy must be tracked before it can be renamed, so commit it first - an untracked copy fails with
`fatal: not under version control`. On a host with no commit yet, rename it with a plain
`mv AGENTS.md CLAUDE.md` (or `Move-Item` in PowerShell) and let the first commit record the new name. Claude
reads one *in place of* the other, so a host with both has one loaded and one never read. Then set
`entry_file` to `CLAUDE.md` in `context.config.json`: it ships as `AGENTS.md`, and every gate that reads the
entry file fails with `entry file not found` until you change it.

**Claude plus a harness that reads `AGENTS.md`** (Cursor, Codex) - rename as above, then copy
`port/AGENTS-stub.md` to `AGENTS.md`. The stub points at `CLAUDE.md`; it carries no second copy of the block.

**Add-on - the host already has whichever file its harness reads** - **upsert, never overwrite**:

- both `<!-- context:begin -->` and `<!-- context:end -->` present -> replace **only** what is between them;
- neither present -> append the whole block;
- **exactly one present -> stop and report.** A lone marker is an interrupted merge, and guessing
  duplicates the block.

Then run the upsert twice and `git diff`: the second run must be a no-op. A second block is the failure the
markers exist to prevent - and `installed` counts them, so a duplicate or an empty block fails the gate in
1.0.7 and later rather than waiting for the diff to be read.

## Step 6 - copy the shells, then fill every marker

**Copy the shells** for the harnesses you actually run: `.github/` (Copilot), `.claude/` (Claude), `.cursor/`
(Cursor), `.windsurf/` (Windsurf - **verify first**, its path is unconfirmed). Never copy one for a harness
that is absent: a rule for an absent harness is cost with no reader.

**Then trim `shells` in `context.config.json` to what you copied - this is not optional.** The shipped config
names all four paths, and `installed` fails on a path that is named but absent, so a literal install reports
`.cursor/rules/context.mdc: named in shells, absent` on a correct tree. Delete those entries, keep
`port_target` pointing at the file you filled, and the install check passes.

**Codex needs no folder.** Its only scoping mechanism is directory placement, which would mean adding a
thirteenth file to the frozen `context/`; the root `AGENTS.md` already tells it to read the contract before
writing.

**Name the port target** - **the highest-ranked harness present**; a declared primary is recorded and overrides that only on an explicit owner decision.
Every shell you fill - the port target's and each pointing one - also carries its own `ported: <YYYY-MM-DD>`
line: the date of the copy, which is how a human ranks it against the block, and the `ported` gate fails
without it.
Then, in this order:

1. **Fill the port target's rule shell.** Replace its `<!-- PORT: context-rules -->` marker block with the body of
   [`port/blocks/context-rules.md`](port/blocks/context-rules.md) - the frontmatter stays, the marker and its
   note go.
2. **Point every other present harness at it.** Replace that harness's marker block with one line, directly
   under its frontmatter: *"The rules for this tree are in `<port target path>`; read it before you write."*
   One body per repo, never two.
3. **Copy the skill** to the **highest-ranked present harness that has a verified skill path** - usually the
   port target itself, unless the port target is Cursor, which documents no skill mechanism. `port/skill-stub/`
   goes to every other present harness with a verified path. No verified path means **no skill**, not a
   guessed one. **No gate checks the skill:** the copy is its only proof, so a green `check --all` does not
   mean it landed.
4. **Hooks** only if step 7 says yes - a shape from `port/hooks/`, its `command` strings from
   [`port/blocks/hook-commands.md`](port/blocks/hook-commands.md).

### A harness not in the table

`AGENTIC-SYSTEM.md` §2 has the four-step procedure; in short - find the file it reads (its docs, not a
guess), upsert the entry block there, add a shell in its own frontmatter dialect if it has one, and if it
has no scoping at all put the filled block in the always-loaded file and accept the always-on cost. Then add
its row to [`MANIFEST.md`](MANIFEST.md) so the next adoption does not rediscover it.

**Then prove the install:**

```
python scripts/contextctl.py check --only installed
```

That is the proof: it passes only when every path in `shells` exists and holds no marker. **Do not use
`grep -rn "PORT:" .`** - step 2 copies `scripts/contextctl.py`, whose own source contains the string, so that
grep can never come back empty on a correct install. If you want a text search instead of the gate, search for
the marker and not the word:

```
grep -rn "<!-- PORT:" . --exclude-dir=.git --exclude-dir=node_modules
```

Run either in the **host** repo, never in this pattern repo - here every doc that describes the marker contains
one. A `PORT:` marker is not a comment: it is the fact that the install is incomplete, and `skeleton/` is the
only place one is legal.

## Step 7 - one enforcement level, only if asked

Recommend the **git pre-commit hook** from [`port/hooks/`](port/hooks) and nothing else: one file,
harness-independent, survives every editor change. Tell the human `--no-verify` exists.

**Installing this tree changes no workflow, no CI config and no required check.** The tree is files plus one
script under `scripts/`; every hook, every workflow and every required status check that runs it is the
host's choice, made after the install and owned by the host. [`port/hooks/ci.yml`](port/hooks/ci.yml) is an
**example** to adapt or ignore: it is not part of an install, it must not be added alongside or merged into a
CI the host already has, and requiring it as a status check is a host decision, never something this tool
needs. Nothing here reads the host's CI, and nothing here edits it.

If a host does adapt that workflow, keep its `fetch-depth: 0`: a depth-1 clone makes the clone boundary
commit look like the commit that added every leaf, so `verified` **fails loudly on every push** (the shallow
finding, `GATES.md`) instead of inventing dates. That is why depth is not optional *for this workflow* - and
why the workflow itself is: a host that cannot provide history either fetches it or lists `verified` in
`checks_advisory`.

## Step 8 - prove it, or it is not adopted

`python scripts/contextctl.py check --all --warn` arrives with the copy, so prove it by machine first and by
hand after. Set `port_target` and your `shells` in `context.config.json`; then:

1. **No marker survives.** `check --only installed` passes, and reports each shell it examined. Run it in the
   **host**, never here. Do not substitute `grep -rn "PORT:" .`: step 2 copies the tool, whose source contains
   that string, so the grep is non-empty on a correct install. Use `grep -rn "<!-- PORT:"` if you want a text search.
2. **One rule body, not two.** Exactly one file under the harness folders contains the routing table; the
   others contain one line pointing at it.
3. **The entry block is cited paths.** Open every path it names and confirm it exists.
4. **The upsert idempotent.** Run step 5's upsert a second time; `git diff` is empty.
5. **The read order holds.** Give an agent this repo and confirm it reads `MEMORY.md` first and stops at the
   one topic - not that it opens every topic "for context".
6. **The rule fires.** Ask *"where does a decision go?"* - the answer must name a leaf in the topic that made
   it, not `MEMORY.md`. That proves the scoped rule loaded, not just the entry block.

A machine pass is not an adoption. Run `check --all --warn`, triage every finding into *fix now* / *advisory
with the reason written down* / *this shape does not exist here*, then **break a register row on purpose** and
watch the check fail. A check nobody has seen fail is a check nobody should trust.

## If the host already has a `context/`

This is the state of every long-lived host, and it is a **merge**, not a copy: the published tree supplies
the shape and the gates, the host supplies the content. Nothing the host wrote to its memory is deleted by
any step below.

**0. Commit first, or say that the dates are provisional.** `verified` dates a leaf from its last **git
commit** (`git log -1 --format=%cs -- <leaf>`), never from the working tree, so an uncommitted leaf has no
history and the gate cannot be honest about it. A dirty tree therefore fails or passes on a fact the commit
would change. Commit the memory, then run the gates; if you cannot commit, run them anyway and label every
date finding **provisional** in one line, rather than reporting a clean run you did not earn.

**1. Keep the host's content and the host's own scripts.** Every file under `context/topics/` stays exactly
where it is - the leaves, `decisions.md`, `HANDOFF.md`, `JOURNEY.md`, the family folders. The host's own
`scripts/` stay too: `contextctl.py` arrives beside them under its own name, and a host script the config
no longer names is dormant, not broken.

**2. Let `skeleton/` replace the shape, and only the shape.** `context/README.md` is the **contract** and is
replaced by the published one - two copies of one document drift, and the one nobody loads is the one that
gets edited. `context/topics/INDEX.md` is written fresh (the register, split out of whatever file carried
it). `context/MEMORY.md` and `context/MUST-KNOW.md` are written if absent, by pointing, not by copying the
skeleton's placeholder: a `- Role: <one line>.` file passes every shape check and migrates nothing. The
skeleton's `widget/` example and its row are deleted together, at once (step 3). **`.gitignore` is merged,
never copied**: a blind copy of `skeleton/.gitignore` stops ignoring the directories the host keeps real
data in.

**3. Translate the config.** The published config knows a smaller set of keys. For each key the host already
has:

| Host key | What it becomes |
| --- | --- |
| `briefing` | **dropped.** This tree ships no renderer and no key may create a briefing; `brief` is a stub that writes nothing. Keep the host's own generator and its file if it has one, but no gate can require it. |
| `inbox` | **dropped.** Nothing routes to it and no command may create it. |
| `budget` | **dropped.** There is no document-length budget; per-document caps are `artefacts` entries. |
| `journey` | **dropped.** `JOURNEY.md` has no shape gate, and the producer contract lived in a `note` command this tool does not ship. |
| `leaves` | **renamed.** `leaves.max_lines` survives as the leaf line cap. Leaf *naming* is the new **`leaf_pattern`**, and a host that numbers its notes must set it (`"^\\d{2}-"` for `01-scheduler.md`) or every leaf gate measures zero. |
| `limits` | **dropped.** No gate has that name; leaving it in `checks_advisory` exits 2 on any run other than `--only installed`. |
| `extra_checks` | **now covered by `extra_checks`.** The published tool takes `"module:function"` strings resolved from the host's own `scripts/`, run under `check --all`. This is where the host's own rules move to, and it is the reason they are not lost. |
| `artefacts` | **renamed field by field.** The published spec is `{max_lines, max_rules, max_rule_chars, requires, over}` and it **merges over** the defaults; a host shape such as `{role, count, max}` becomes `{"max_lines": 90}`. A glob key (`*-handoff.md`) has no equivalent: declare the exact file names, because a key that matches nothing is silence. |
| `brief_sections` | **dropped.** Nothing renders a digest to section. |
| `kb` | **dropped.** No index, no embeddings and no `search`. |

Three path keys do exist and must be **split**: a host that points `memory` and `index_of_topics` at the
same `context/README.md` gets three separate files instead - `memory`, `root_rules` and `index_of_topics`.
`FOLDER.md` § *Not in this tree yet* is the list of everything this tree does not carry; read it before
translating a key rather than after the run reports that the key is unknown.

**4. Merging the entry file is the step that loses something.** The published `skeleton/AGENTS.md` is 664 B
and the `<!-- context:begin -->` ... `<!-- context:end -->` block inside it is 625 B; the rest is a title.
So the job is **upsert**, per step 5: append the block to the host's file, or replace only what sits between
its markers. A host whose entry file is a long routing table keeps every row of it. A blind copy replaces
the table with 625 B and nothing reports the deleted lines.

**5. Order of operations.** Each step is checkable before the next one starts.

1. Commit the memory, or record that it is dirty (step 0).
2. Copy `skeleton/scripts/` and `skeleton/context.config.json`; merge `skeleton/.gitignore`.
3. Replace `context/README.md` with the contract; delete the copied `widget/` example **and** its register row.
4. Write `context/topics/INDEX.md`: one row per topic folder, dated from each topic's own `Verified:` line.
5. Write `MEMORY.md` and `MUST-KNOW.md` by pointing at what the host already has (step 4B).
6. Translate the config with the table above; set `leaf_pattern` to the host's own leaf naming.
7. Upsert the entry block, then run the upsert a second time and confirm `git diff` is empty.
8. Install the shells for the harnesses actually present and trim `shells` to them (step 6).
9. Set `port_target`, then run the checks below.

**6. Verification, and what a green run does not prove.** `check --only installed` must pass - and it now
survives a config that still names the host's retired gates, printing each one with `note:`, so a stale
`checks_advisory` no longer hides the install. Then `check --all --warn` and triage every finding into *fix
now* / *advisory with the reason written down* / *this shape does not exist here*. Three readings matter
more than the exit code: `leaf-index` must print a **non-zero leaf count** (a zero means `leaf_pattern` is
wrong, not that the tree has no leaves); `pointers` must print `accepted absent` for the directories the
clone cannot carry, instead of one finding per citation; and a register row broken on purpose must fail.
Two trees in one repo root is not a merge - if the host already carries a memory tree from another
scaffold, decide which one owns `context/` before starting, and never promote one tree's note into the
other's topic.

## The failure modes this runbook exists to prevent

| Failure | What it looks like |
| --- | --- |
| copying the tree and never migrating | an empty `MEMORY.md` beside a 40 KB legacy doc; the agent reads neither |
| migrating by moving | every old link breaks, so the old readers stop trusting the surface |
| copying every harness folder | four harnesses' files in a repo that runs one; the loaded rule is not the edited one |
| copying the entry file over the host's | the host's own instructions vanish, silently - nothing reports a deleted line |
| leaving a `PORT:` marker | the rule file states no rules, and nothing says so - the install looks finished and is not |
| filling two harnesses with the same block | two bodies in one repo, and the one nobody loads is the one that gets edited |
| keeping both `AGENTS.md` and `CLAUDE.md` | Claude substitutes rather than merges - the other is text nobody will read |
| turning everything on at once | 60 findings on day one, so all of them get disabled |
| restating the contract in the entry file | two copies that disagree within a month |
| installing a harness hook first | it breaks on the next editor change and is removed, taking the habit with it |
| adopting into a repo that already has a `context/` | two trees answering to one root - the merge nobody asked for |
| reporting the transcript | the human cannot tell whether anything was migrated |
