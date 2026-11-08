# Locked

> The decisions behind this shape, and what each release changed. Read when a choice looks arbitrary, or
> before proposing a change to the pattern. A session never loads this file.

## Decisions

Four sets, each taken before the code that depends on it. A ruling outranks a release note: where a release
contradicts one, the release is wrong.

### The shape

| Question | Ruling |
| --- | --- |
| Does a topic with fewer than four artefacts still hold the argument? | **One `README.md` is enough.** The test is one home and one mutability per artefact that exists, never the count. `skeleton/context/README.md` already says a one-leaf topic needs only `README.md`. |
| May a `JOURNEY` entry hold reasoning? | **Yes.** An entry records what happened during the turn, reasoning included. It is never corrected, so it records what was thought, not what is true - and nothing loads it. |
| Is a capture buffer part of the mechanism? | **No, not yet.** The case is not needed, and the home a routing row would name exists in no file. A thought that cannot be filed yet has no home and is not durable. `inbox.md` stays undesigned, with nothing routing to it. |
| Where does a drained topic's archive live? | **`context/archive/`, at the tree root**, flat, files prefixed with the topic name. **Never under `topics/`**: every gate scopes to `topics_dir`, so an archive there reads as a live topic and fails `register` and `leaf-index` on a *correct* drain. |
| Which harness holds the canonical copy of the rules? | **The highest-ranked harness present is the port target** - Claude on a Claude+Copilot repo, Copilot on a Copilot-only repo. A declared primary overrides this only on an explicit owner decision. |

**One consequence worth stating.** The archive ruling is correct because of a property worth making deliberate:
`context/archive/` is invisible to every gate *because* they scope to `topics_dir`. That was true by
construction and is now tested in both directions, so a later refactor cannot quietly move the scan root.

### The operation

| Question | Ruling |
| --- | --- |
| How much of this is enforced? | **Nothing by default.** Each mechanism is a shape a host may enable per trigger as **off** / **surface** / **gate**. The agent writes where a change is reversible and local (`act`), asks where it is irreversible or raises always-loaded cost (`ask`), and needs the owner where the trigger is a judgement (`owner`). |
| When does wrap-up happen? | **By the user, by default.** A detection that suggests one may be enabled later and stays off; never a schedule. |
| When does a leaf become a second leaf? | **When the subject changes** - a different question, measurement or verdict. The count capped is fan-out, never conclusions. |
| Does a host that fills its rule shell have to re-port it? | **A `ported: <date>` line in every filled shell, and no comparison against the block.** A hash gate would need the source block beside the host, and a pointer-only fill is a legal, byte-different body. |
| Where does the runner live, given it must be copied? | **Inside `skeleton/`, with its config.** Copying `skeleton/` then produces the host's tree and the tool has one copy. Not in `port/`, which holds files that would be harmful if they landed unasked: a runner that does nothing until invoked is not one. |
| Is the wrapper's cost ever a reason not to check? | **No.** Measured: 6.4 ms of work against 127 ms as a subprocess on an empty tree, but 36.7 ms of work at one leaf, and at 80 leaves the work is 90% of the wall clock. The cost was never the clock; it was the habit. |

### The gates

| Question | Ruling |
| --- | --- |
| What is the gate set? | **Eight gates plus `installed`, four of them default.** Each guards an `act`; none guards an `ask` or an `owner` trigger, because those are questions put to a human, not findings. |
| What is the one exception to off-by-default? | **`installed`**, host only, rated once, disabled in this repo with the reason recorded. It judges whether the tree arrived, not what it says, and it refuses `--skip` because it is the precondition of every other denominator. |
| What counts as zero subjects? | **A count, not a verdict, unless the location is absent.** `FAIL` when the config points where the tree has nothing; `ok` with the count printed when the location exists and is legitimately empty. Failing both made an install report four blocking findings before its first topic. |
| What is the `briefs` similarity threshold? | **0.82.** Measured on 49 pairs: 26 hard negatives (one topic, different conclusions) max at **0.649**; rephrased duplicates score **0.4-0.6**. So 0.82 fires on zero negatives and catches near-verbatim copies only. Losing a duplicate is preferred to firing on a true tree. |
| Does `verified` block on an uncommitted leaf? | **Yes, and that is accepted.** The only fix left is guessing a date from the working tree, and an uncommitted leaf has no history. A commit clears it. |
| Is there a document length budget? | **No.** Per-document budgets were tried and retired with their arithmetic, and the aggregate with them. The documents answer one question each and are longer than a guess made before they existed; merging to hit a number puts two subjects in one file. What stays budgeted is the **always-loaded surface**: `664 B` entry file, of which the injected block is `625 B`. |
| Which harness behaviours are still unverified? | **A verification plan exists for the two most common harnesses**, Claude Code and Copilot in VS Code. Windsurf and Codex stay queued; no path is guessed into a host. |

### The history

| Question | Ruling |
| --- | --- |
| When may the published history be rewritten? | **Force-pushing the history is permitted only until the first fork.** After that, the repository is append-only and every fix is a patch release. The window exists because a pre-publication rewrite costs nobody anything; it closes the moment someone can build on a commit, and nothing about the pattern makes an exception for its own repository. |

## 1.0.1 - the first patch

**1.0.1, 2026-11-08.** Three defects, none of them found by a gate: a session with no knowledge of this
design adopted a host repo and reported where the written rules left it to guess.

| Was | Is |
| --- | --- |
| the rule block's `MEMORY.md` row routed one kind of fact, while `MEMORY.md` accepts three - what the repo is and how to run it, a convention that spans topics, and where an external system lives - so an external host and its log path had no route in the block | the row names all three; the block's other rows were checked against the contract and needed no change |
| `MANIFEST.md` § *Install* step 2 still said `git mv AGENTS.md CLAUDE.md` with no note that the copy must be tracked, the defect `ADOPT.md` step 5 had already fixed | it points at `ADOPT.md` step 5 instead of restating it, so the instruction has one copy |
| the contract's leaf-identity section explained that `decisions.md` is absent from `## Leaves` by reference to the tool's own patterns, so the rule was unreadable without the source | the rule is stated whole: the rows carry `D-####` ids, so the leaf table indexes conclusions and not choices |

### The first observation of the adoption check

The two behavioural checks `ADOPT.md` step 8 asks for - the read order, and whether the scoped rule fires -
were **observed** for the first time on 2026-11-08, by a session with no knowledge of this design. It read
`MEMORY.md`, then `MUST-KNOW.md`, then the topic register, and stopped; and it routed a decision to a new
topic's `decisions.md` while quoting the filled rule shell. Only a live session can produce this evidence,
which is why it was quoted rather than observed until now.

## The first release

**1.0.0, 2026-11-08.** Four iterations preceded it and none of them left this machine, so the record below is
the whole of this repo's history: what each pass changed and the measurement that forced it. The shape and the
gates came first, then an installation that found seven defects, then a calibration, then the pass that made
the repo publishable.

### The shape, and the gate set

Twelve files under `skeleton/context/`, one entry file, one dot-folder per harness, the shared rule text in
`port/blocks/`, and a gate runner built to `GATES.md`.

| Piece | Detail |
| --- | --- |
| the runner | stdlib only, one file, **moves no file**: draining a topic, trimming a leaf and retiring a family are judgements |
| the shells | each harness's real path holds frontmatter plus a `<!-- PORT: ... -->` marker; filling it from the shared block *is* the install, and a host still containing a marker was never installed |
| the two configs | the repo's own points at `skeleton/context/`; the one inside `skeleton/` points at a host's `context/` |
| the tests | one defect fixture per gate, plus a clean tree, zero-denominator and CLI cases |
| the cadence | nothing runs on its own; `check` and `check --all` when the owner or a hook calls them |

**Two claims were false when measured**, and are recorded because a spec that is right on paper and wrong in
the runner is the drift this structure exists to prevent. The summary's denominator was the numerator
(`f"{len(ran)} of {len(ran)}"` printed `1 of 1` for a single gate), and `installed` could be silenced with
`--skip`. Both now have tests.

### The first installation: seven defects

**Installed on a repo that is not this one for the first time**: an add-on host with Claude and Copilot shells.
It worked - `installed` failed before the fill, passed after, failed again on a restored marker, and a full
session from start to drain stayed green. The run also retracted **three false positives a correct tree
produced**, and found seven defects:

| # | Was | Is |
| --- | --- | --- |
| 1 | the install proof `grep -rn "PORT:" .` could never pass, because the install copies `scripts/contextctl.py`, whose line 35 contains the word | `check --only installed` is the proof; a text search, where wanted, is `grep -rn "<!-- PORT:"` |
| 2 | `cp -r skeleton/scripts` carried `__pycache__/` into the host, and no install step copied a `.gitignore` | `skeleton/.gitignore` ships and is in the install steps, with "merge, do not overwrite" |
| 3 | the shipped config named four `shells` while the runbook forbids copying a shell for an absent harness, so a literal install could not pass `installed` | trimming `shells` is an explicit install step |
| 4 | `briefs` failed forever on a correctly drained topic, because its denominator was leaf briefs and drain archives the leaves | `briefs` counts **topics** |
| 5 | zero subjects was always a `FAIL`, so an install before its first topic reported four blocking findings | `zero()` takes the location's existence: absent blocks, present-and-empty prints its count |
| 6 | `verified` was cadenced at *milestone*: **2 681.8 ms at 80 leaves, 17 479.8 ms at 500**, one git spawn each | cadence is **CI**, with the measurement in the cell |
| 7 | three finding strings omitted a trailing clause the tool prints, and one byte figure described the whole entry file rather than the block | all four made true |

**The cost was measured, and it is not the clock.** On an empty tree the gates were 6.4 ms of work against
127 ms as a subprocess; at one leaf the work is 36.7 ms, and at 80 leaves it is 90% of the wall clock. What the
measurement rules out is a cadence argument built on startup time.

### The archive, and a measured threshold

| Change | Detail |
| --- | --- |
| drain names its destination | `context/archive/` at the tree root, flat, prefixed with the topic name; tested in both directions - outside every gate's scan when it is there, two blocking findings when it is put under `topics/` |
| `briefs` calibrated | 0.82, from 49 measured pairs. 26 hard negatives max at **0.649**; rephrased duplicates score **0.4-0.6**. The gate therefore catches near-verbatim copies only, which is the deliberate trade: lose a duplicate rather than fire on a true tree |

### Publication: five defects

**The last pass before release, and the one that made the repo describe only itself.** Every reference to
another checkout or an earlier version was removed, and `README.md` section 3 went back to pointing at the
contract instead of paraphrasing it.

| Change | Detail |
| --- | --- |
| five defects from the stability protocol | a clone URL left as a placeholder in `README.md`; two files with no final newline; one spelling pair split six-to-forty-two and another three-to-one; `README.md` restating the contract's mutability paragraph |
| the release | **`v1.0.0`, 2026-11-08** - published to `https://github.com/coji831/agent-context`, licence MIT, and `main` requires the `context` check and a pull request |

## Changing the pattern

1. Propose the change where the decision lives, with the measurement or the failing case that motivates it.
2. Apply it, then bump `VERSION`.
3. Run both, from the repo root:

   ```bash
   python skeleton/scripts/contextctl.py check --all
   python -m unittest discover -s tests
   ```

4. Record the release here, under the reason it was made.

**A change with no failing case behind it is a preference, not a fix.** Every defect below the first release was
reproduced before it was changed, and the two false claims were each measured before they were corrected.

## Verifying a release

There is no hash manifest, deliberately: a checksum tells you that a file has not changed, not that it still
says something true. What verifies a release is:

| Check | Command |
| --- | --- |
| the gates hold | `python skeleton/scripts/contextctl.py check --all` |
| the gates' own tests hold | `python -m unittest discover -s tests` |
| the shipped tree still installs | copy `skeleton/` into an empty repo, fill the rules, run `check --only installed` |
| the badge is honest | the CI run on the tagged commit |
