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

## 1.0.4 - the gates that measured their own parser

**1.0.4, 2026-11-08.** Seven defects, each measured by adopting v1.0.3 onto a real 11-topic host: every one
is a gate that reported a fact about its own parsing rather than about the tree it was given.

| Was | Is |
| --- | --- |
| `table_rows()` harvested a `Leaf` header as a data row, and `leaf-index`, `shape` and `briefs` read leaf names from **`cells[1]`** whatever the header said. On the host that is **76 of 109** findings - one prose table counted twice, with no true positive available | a header row is the row line a **separator** follows and is never a body row; the leaf column is the header that names a file (`Leaf`, `Leaves`, `File`), with `id` used only when none does, and `id \| Leaf \| Brief` as the fallback when no header is recognised. A **family** README is an index only if its first table names a file column; with no such table it has no index and contributes nothing |
| `pointers` reported `repos/...` and `state/...` (real directories, `/`-anchored in `.gitignore`, absent from every clone) and `~/...` citations as dead, with no way to accept them: **22 permanent false findings** | `accepted_absent` takes paths, prefixes and globs; a matching citation is accepted and the summary prints how many (`..., 22 accepted absent`); an entry that matches no citation is itself a finding; `~/` and `$HOME/` are always accepted with no config |
| leaf naming was the hardcoded `^L-\d{4}`, so on a host whose notes are `NN-name.md` **two gates measured nothing** and `verified` printed `ok 11 dated topics, 0 leaves without history` | `leaf_pattern` (default `"^L-\\d{4}"`) builds the matcher in one place; a `topics_dir` holding files and no leaf reports `leaf_pattern "^L-\d{4}" matches none of 115 files under context/topics; the leaf gates checked nothing` |
| config names were validated **before** gate selection, so `check --only installed` exited 2 with seven errors - the install proof `ADOPT.md` step 6 tells an adopter to run | `--only installed`, run alone, prints each ignored name with `note:` and runs; every other invocation keeps today's strictness |
| `extra_checks` was checked as a list of gate names, so a host's three own rules were refused and the coverage its retired checker was retired into became unreachable | `extra_checks` takes `"module:function"`, resolved from the host's `scripts/`, and runs under `--all`; a missing module, a missing function and a raising function are findings, never tracebacks |
| a config written by Windows PowerShell 5.1 carried a BOM and exited 2 with a Python-internal message | read with `utf-8-sig` |
| the shipped skill said `.context-root` "and `resolve --where` to read it, arrive with `scripts/contextctl.py`" | it says they are **not shipped**, which `MECHANISM.md` already said |
| `ADOPT.md` answered "the host already has a `context/`" with *stop and report* - the state of every long-lived host | a merge procedure: the dirty-tree problem, keep versus replace, a config translation table, the entry-file merge, the order of operations, the verification |

**Two schema decisions, and the reason for each.**

- **`leaf_pattern` defaults to `^L-\d{4}`** - the value the code already hardcoded - so every existing tree
  is read exactly as before and the key is a way *out* of the assumption rather than a migration. The
  alternative, auto-detecting a tree's numbering, guesses at the one thing a gate must not guess: which
  files it is measuring. Its liveness finding is **advisory**, not blocking, deliberately: a tree drained
  to its last leaf is legitimately leaf-free, so a blocking finding would fail a correct drain and teach an
  operator to switch the gate off - the failure the rule exists to prevent. What it replaces was worse:
  `ok` over an empty set.
- **`extra_checks` run only under `--all`.** They are a host's own rules, so they are opt-in exactly like
  the four opt-in gates, and a host that never asked for them is not handed a blocking finding at install.
  The summary's denominator becomes `9 + the extras that ran`, so a tree with none still prints `N of 9
  gates ran` and the CI assertion is unchanged - the count of what ran says what ran.

**One attribution corrected.** The experiment's headline cause was "`table_rows()` harvests every table in a
topic README, not the `## Leaves` table". That is **falsified**: a topic `README.md` was already scoped to
`## Leaves` by `section_rows`. Only **family** READMEs were read with `table_rows()` over every table. The
real cause of the 64 `leaf-index` findings is the **column order** (`cells[1]` assumed, header harvested)
plus, at family level, no rule for which table is the index. Both are fixed above; the family rule is now
stated in `GATES.md` rather than inherited from an accident of which reader a file went through.

## 1.0.3 - the stub, the sources, and a record that counts

**1.0.3, 2026-11-08.** The three findings 1.0.2 left to the owner, ruled and applied, plus the count its own
record had got wrong.

| Was | Is |
| --- | --- |
| the hook examples wired `contextctl.py brief`, and no build shipped the command; a comment said so, while the executable line still named a subcommand that dies on an unknown choice | `brief` is a **stub**: it writes no digest, compares none, prints one message to stderr and exits **0** - deliberately, because a failing session-start hook blocks the session it is starting. Four tests hold it, one of them asserting it changes no file |
| `AGENTIC-SYSTEM.md` justified its harness table as "2026-11-07, <vendor> docs" with no document a reader could open, once 1.0.2 removed the provenance pointer | numbered **Sources** under the table, fetched 2026-11-08, each stating only what it settles |
| `skeleton/.claude/rules/context.md` carried `<!-- unverified: … -->` for a key its own frontmatter already used | the marker is deleted: `paths` is documented as **the only rule field Claude reads** |

**Two claims moved with the citations, one in each direction, and that is the point.** Claude's glob key left
its queue - `unverified` -> `paths:`, stated by two vendors and now loaded by the shipped shell. Copilot's
"nearest in the directory tree wins" lost its parenthetical - no fetched source states a precedence between
nested `AGENTS.md` files, so it is marked **unverified** instead of kept from memory. `MANIFEST.md`'s rank
table, capability matrix and V2 row were brought to the same answer, so one fact no longer has two
strengths.

**The count.** 1.0.2's intro said *three defects* while its table and sweep had fixed six. It now says what the
release did, and its table carries all six rows.

## 1.0.2 - the template that gated nothing

**1.0.2, 2026-11-08.** Two of these defects were in the file a *host* copies rather than in this repo's own:
1.0.1 fixed the check-run name here and left the same trap, twice, in `port/hooks/ci.yml`. Four more came
from a sweep for one class - a claim the repo cannot satisfy - and after the fixes came the guard that keeps
the first two from returning, and a re-run of a proof that had been confounded. The table is the whole
act-inventory of the release; the sweep's denominator is below it.

| Was | Is |
| --- | --- |
| `port/hooks/ci.yml` declared its job `check:` with no `name:`, so the job reported a check called `check` and an adopter's required status check named `context` never reported; and it checked out at depth 1, so the date gate found no commit date on any leaf and blocked every push | the job is named for the required check and checkout sets `fetch-depth: 0`, each with one comment saying why it is load-bearing and `GATES.md` named rather than the spec restated |
| `MECHANISM.md` Q1 answered "no" with *do the work, write nothing durable, say so* - contradicting the ruling that a decision with no owning topic creates it in that turn with its register row, and contradicting `T1` two screens below it | the routing table is the authority: a fact spanning topics is a `MEMORY.md` line, and a decision with no topic creates it with its row. The restatement is replaced by the reference, the fix used at `git mv` in 1.0.1 |
| three hook examples wired `contextctl.py brief` with no marker in the file a host copies; only `port/hooks/README.md` and `port/blocks/hook-commands.md` said the command is not shipped | every hook JSON carries the marker, so the shape cannot be mistaken for a working command by a reader who copied it |
| `AGENTIC-SYSTEM.md` cited `agent/WIRING.md`, "still readable from `54ba837`" - neither that file nor that commit exists in this repository | the pointer is gone and its one claim kept |
| `port/hooks/README.md` pointed at `../copilot/hooks/`, a folder this repo does not ship | it points at `copilot-vscode-hooks.json`, which exists |
| `GATES.md` quoted a register line as `1 finding (13 folders, 13 rows)` and a pointers line as `88 tokens in 9 files` | both match what the tool prints: `13 folders, 13 rows`, and `88 cited paths in 9 files` |

### The guard, made mechanical

A comment in this repo's own workflow did not stop the trap surviving 1.0.1, so it is measured now.
`tests/test_gates.py::ShippedWorkflows` reads both shipped workflows - `.github/workflows/context.yml` and
`port/hooks/ci.yml`, **2 files**, both asserted - for (a) the job's `name:` equal to the workflow's `name:`,
and (b) a checkout step that sets `fetch-depth: 0`. Each of the four lines was deleted locally, one at a
time, and the suite failed each time; restored, both tests pass. **The first draft of the depth assertion
passed a workflow whose only `fetch-depth: 0` was inside the comment above the step**, so the assertion is
anchored to a YAML line rather than to a substring - a guard that a comment satisfies is not a guard.

### The merge is blocked by a *failing* check, re-proved

The 1.0.1 proof was confounded: a pull request was refused while the required check `context` did not exist
at all, so nothing observed showed that a failing gate blocks. Re-run on `prove-gate-blocks`, one commit off
`main`, adding a register row for a folder that does not exist:

| Observation | Measured |
| --- | --- |
| the gate fails locally, before CI is asked | `register FAIL 1 folders, 2 rows`; `check --all` exits **1**, `1 blocking finding; 7 of 9 gates ran` |
| the required check reports, and reports failure | check-run **`context`**, conclusion **FAILURE**, run `42476747052`, PR #3 |
| the refusal is not `strict` demanding an up-to-date branch | `mergeable: MERGEABLE`, `mergeStateStatus: BLOCKED`, `ahead=1 behind=0` - the out-of-date state is `BEHIND`, and this is not it |
| the merge refuses | `X Pull request coji831/agent-context#3 is not mergeable: the base branch policy prohibits the merge.` |
| the cause is readable in the log | `skeleton/context/topics/INDEX.md:13: row names "context/topics/pricing/", no such folder` then `1 blocking finding` |

Closed unmerged, branch deleted; `main`'s head check-run was `context: success` again afterwards.

### The sweep, with its denominator

**49 tracked files** read for the same class - a claim the repo cannot satisfy - with every path-like
citation in the 32 Markdown files resolved against the tree each one addresses: **142 resolved, 15 not.**
Fourteen of the fifteen are host destinations or illustrative host trees and are correct as written. The
one defect was a provenance pointer: `AGENTIC-SYSTEM.md` cited `agent/WIRING.md`, "still readable from
`54ba837`", and neither that file nor that commit exists in this repository. The other three rows came from
the same pass - a hook shape whose command was unmarked, a path to a folder that is not shipped, and two
`GATES.md` quotes, `1 finding (13 folders, 13 rows)` and `88 tokens in 9 files`, that the tool does not
print. A quotation written from memory of output is the same defect as a path written from memory of a tree.

## 1.0.1 - the first patch

**1.0.1, 2026-11-08.** Three defects, none of them found by a gate, and one rule that was never stated: a
session with no knowledge of this design adopted a host repo and reported where the written rules left it
to guess.

| Was | Is |
| --- | --- |
| the rule block's `MEMORY.md` row routed one kind of fact, while `MEMORY.md` accepts three - what the repo is and how to run it, a convention that spans topics, and where an external system lives - so an external host and its log path had no route in the block | the row names all three; the block's other rows were checked against the contract and needed no change |
| `MANIFEST.md` § *Install* step 2 still said `git mv AGENTS.md CLAUDE.md` with no note that the copy must be tracked, the defect `ADOPT.md` step 5 had already fixed | it points at `ADOPT.md` step 5 instead of restating it, so the instruction has one copy |
| the contract's leaf-identity section explained that `decisions.md` is absent from `## Leaves` by reference to the tool's own patterns, so the rule was unreadable without the source | the rule is stated whole: the rows carry `D-####` ids, so the leaf table indexes conclusions and not choices |

### The ruling on a decision no topic owns

| Question | Ruling |
| --- | --- |
| Where does a decision go when no topic owns it? | **The topic is created in that same turn, with its register row.** The blind session created one on judgement alone and said so, which proved the rule was unstated; and the alternative put the decision in `MEMORY.md`, whose own header says a fact a topic owns goes in that topic's leaf and nowhere else. The ruling is about a decision needing a home, not a topic for every task - `CONCEPT.md` value 3 stands. |

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
