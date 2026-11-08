# GATES - what keeps this tree correct, and what is deliberately unchecked

> One question: **what may a check assert, and what is left to a reader?** Authority above this file is
> `CONCEPT.md` (the six values), then `skeleton/context/README.md` (the contract); the operation is
> `MECHANISM.md`, the map `FOLDER.md`, the connection `AGENTIC-SYSTEM.md`. None is restated here. This was
> written **before** the tool, and the tool is built to it: `scripts/contextctl.py` and `context.config.json` implement the set below, so a change here is a change to them.

## The gate set

**Nothing here runs on its own.** No hook, no CI job and no turn-end check is installed by any step of this
repo; `port/hooks/` holds shapes and says so, and gates run at a milestone or when the owner asks. So
"posture: gate" below means **blocking when the owner runs `check`**, not blocking something nobody asked
for. Every gate guards an **`act`**; none guards an `ask` or `owner` trigger, since those are questions put
to a human when they matter. *Cadence* says where a gate *belongs*, so a host wiring
`port/hooks/pre-commit.sh` or `ci.yml` knows which subset to call; until then every row means the owner's invocation. *Where*: **both** is this template over `skeleton/context/` and a host over its own `context/`; **host only** means the shape exists only after install.

| Set | Gate | Where | Assertion (one sentence) | Failure it catches (a shape, not a risk) | Finding it prints | Cadence | Posture | Rated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| default | `register` | both | Every folder under `topics_dir` has exactly one row in `index_of_topics`, every row names a folder that exists, and each row's date equals that topic `README.md`'s `Verified:` date. | A topic on disk the register does not name; a row still pointing at a folder deleted at drain; a topic re-read while its register row keeps the old date. | `FAIL register context/topics/INDEX.md:9: row names "pricing/", no such folder` | commit | gate | must |
| default | `leaf-index` | both | Every `L-####-*.md` names a row in its nearest index (the topic `## Leaves`, or its family `README.md`), and every row names a file that exists. | A leaf written and never indexed, so no later session knows it exists; a row whose leaf was deleted instead of rewritten. | `FAIL leaf-index context/topics/widget/L-0003-x.md: no row in context/topics/widget/README.md` | commit | gate | must |
| default | `shape` | both | Fixed shapes hold: a leaf's frontmatter (or its first two lines) carries `id:` and `brief:`; every `HANDOFF.md` carries `## Now`; every register and `## Leaves` row carries a date and a brief; every `decisions.md` row carries a `D-####` id; each `MEMORY.md` entry is one line. | A leaf that cannot be cited by id; a handoff whose next session has no first action; a decision row nothing can cite; a fact that grew a body under its bullet. | `FAIL shape context/topics/widget/HANDOFF.md: no "## Now" heading; the next session has no first action` | commit | gate | should |
| default | `caps` | both | Every count is inside its configured cap: `HANDOFF.md` lines, `MUST-KNOW.md` rules and rule characters, `MEMORY.md` lines, leaf lines, topic `README.md` lines, and fan-out (more than 10 rows needs a family index). | A handoff grown to a thousand lines with the real next step at its end; a topic README listing thirty leaves flat. | `FAIL caps context/topics/widget/HANDOFF.md: 214 lines, max 90; move the history to JOURNEY.md and rewrite the snapshot` | milestone | gate | should |
| opt-in | `briefs` | both | No two leaves in **one topic** have `brief` lines above **0.82** similarity - calibrated 2026-11-08: 29 hard negatives (same topic, different conclusions) max at 0.649, so 0.82 leaves a 0.17 margin and fires on 0 of them. | Two leaves holding one conclusion, the second written instead of the first rewritten - **near-verbatim only**: a copy with a word changed scores above 0.9, a rephrasing scores 0.4-0.6 and is deliberately missed. | `FAIL briefs context/topics/widget/README.md:11: brief of L-0003 is 0.86 similar to L-0001` | CI | gate | could |
| opt-in | `verified` | both | A topic `README.md`'s `Verified:` date is not older than the newest **git commit date** among the leaves it indexes (`git log -1 --format=%cs`), never a filesystem mtime. | A topic re-read and one leaf rewritten, while the entry still shows last month's date. | `FAIL verified context/topics/widget/README.md:3: Verified: 2026-09-01, 41 days behind L-0002` | CI (2.7 s at 80 leaves, 17.5 s at 500 - one git spawn each, measured 2026-11-08) | gate | could |
| opt-in | `pointers` | both | Every backticked path in `MEMORY.md`, the root rules, the entry block and a topic `README.md` resolves from the tree root. | A citation to a file that moved, so a reader follows a dead pointer and trusts nothing after it. | `FAIL pointers context/MEMORY.md:12: "docs/runbook.md" does not resolve` | milestone | gate | should |
| opt-in | `ported` | host only | Every path listed in `shells` carries a `ported: <YYYY-MM-DD>` line. | A filled rule shell with nothing dating it, so a human cannot rank it against the contract. | `FAIL ported .claude/rules/context.md:3: no "ported:" line` | milestone | gate | once |

**A host that changes nothing gets the four default gates**, blocking, when it runs `contextctl check` at a
milestone or on request, and **nothing else**: the opt-in four run only under `check --all` or
`check --only <name>`. *Rated* is value against cost: **must** = the memory does not work without it,
**should** = keeps the tree in shape, **could** = a gain smaller than the trust it costs, **once** = belongs
at install or update, not on a loop. The smallest set that keeps the tree working is `register` +
`leaf-index`; `shape` and `caps` earn their place by costing milliseconds; `pointers` is rated **should**
and stays opt-in because it measured 16 false findings on a real consumer repo; nothing else earns a default run.

### The one exception to "off for everything"

**`installed`**, not in the table because it never judges the tree - it judges whether the tree arrived, and
it is **host only**, **rated once**, and here **disabled** with the reason recorded. It asserts that every
path in `shells` exists, holds no `<!-- PORT:` marker, and is one of the two legal fills - the block body, or
a pointer whose first backticked path resolves - and that `entry_file` carries its marked block. It runs on
**every** invocation, `--only` included, and refuses `--skip`: it is the precondition of every other
denominator, since a tree whose shells were never filled gives the agent a comment where its rules should be.
It prints `FAIL installed .claude/rules/context.md:4: still contains "<!-- PORT: context-rules -->"; the routing table never reached the agent`. It is
the only mechanism here that fires without being selected, and every disable is echoed in the summary line.

## The three owed decisions

**Block drift: a `ported: <date>` line in every filled shell, and no comparison against the block.** Written
by install (MANIFEST step 4), guarded by the opt-in `ported` gate for presence only. A hash gate needs
`port/blocks/context-rules.md` beside the host, and a host installs the skeleton, not the source blocks, so
the gate would be pinned for a shape most repos do not carry. Equality is also the wrong test: the shells
allow a host with another port target to replace the body with one line pointing at that harness's rule
file, so two legal fills are byte-different. And the disagreement is already adjudicated - `AGENTIC-SYSTEM.md`
section 4 rule 4 says the shell yields to the contract - so a human lacks not a verdict but a date to rank
the copy by. The alternative's failure: a hash gate that fires on a legal pointer-only fill, gets switched
off, and takes the true divergences with it. What this leaves is below: whether a filled shell still matches
the block is unchecked.

**Leaf split: a size cap, the contract's fan-out count, and no count on leaves.** A leaf's cap is
`leaves.max_lines` (120), in `caps`; it catches the leaf that became a diary, the only growth failure with a
name in the record. The count capped is **fan-out**, not conclusions: more than ten rows in a `## Leaves`
table or a family `README.md` means add a family index and group inside it, the contract's own remedy. No
maximum number of leaves per topic exists: splitting is decided by *a change of subject*, and a count would
force unrelated conclusions apart to satisfy arithmetic. The near-duplicate `brief` check is a different
question, whether the second leaf was needed at all, so it is `briefs`, opt-in and scoped **per topic**: value 6 lets two trees hold almost the same conclusion, so a comparison across topics would fire on a correct tree.

**The exception is `installed`, above.** `MECHANISM.md` left the slot open because a rule set that is off
everywhere is checked by nobody. It is chosen over the four default gates because those fail only when
someone asks; `installed` is the one whose subject is the installation itself, and an unfilled shell is
invisible by construction - a placeholder is a legal comment whose absence of rules reads like a rule set.

## What is deliberately unchecked

| Considered and refused | Why |
| --- | --- |
| Whether a leaf's content is still true, or a `MEMORY.md` line has quietly become an aggregate of topics | No reader of truth; the code wins over any document about it, and an aggregate in one line has no shape. |
| Whether a leaf is superseded, no longer worth keeping, or whether two leaves say one conclusion differently | Both need the meaning of the body; `briefs` at 0.82 catches a near-verbatim caption only - measured 2026-11-08, it caught 2 of 20 rephrased duplicates at 0.80 and none above that. A rephrasing is missed on purpose: the owner's rule is to lose a duplicate rather than fire on a true tree |
| Whether a topic is finished, so drain is due | `MECHANISM.md`: no check tells a finished topic from a quiet one. |
| Whether a wrap-up was needed, or happened | Nothing schedules it; a missing `HANDOFF.md` is a state, not a defect, and a suggestion detector stays off. |
| Whether a turn's `JOURNEY` entry was written | Nothing loads it, and the number of turns is unknowable from the tree; a missing entry looks exactly like a turn that did no work. |
| Whether a rule belongs at the root or in one topic (the root-rule admission test) | A judgement on blast radius, raised as an `ask` at the moment the rule is written. |
| Whether a host-supplied requirement record (a spec, a locked brief) was edited | It is not an artefact of this tree, so no file here can be compared against it; `ask` holds that rule. |
| Whether two copies of one rule agree (root and topic `MUST-KNOW`, block and contract) | An equality a reader resolves by the stated dispute order; a gate would have to know which copy is authority, which is the judgement it would be making. |
| Whether a filled shell's body still matches the block | The `ported:` decision above; the marker dates the copy and a human compares it when a disagreement surfaces. |
| Whether a drained topic's shim names the path and the date checked | The contract asks for both, and a shim is prose a human writes once at drain; a missing date is caught by the next reader, not by a shape. |
| Whether a row names the *right* folder, or a pointer the *right* file | Resolution is not correctness: the shape check answers only whether the path exists. |
| Whether a `## Now` is a good next step | `shape` checks that the heading is present and says so; quality has no shape. |
| Whether a topic belongs to this tree rather than another | Value 6: `resolve --where` answers it as a question, and the honest answer is sometimes two entries. |
| Whether a stray file in a topic folder has a home | A filename allowlist would fire on the files a host legitimately keeps beside its memory. |
| Whether the read order was actually followed, or whether the entry block and the skill still list it the same way | The order is checkable by a reader at a dispute, which is all section 4 claims; nothing observes what a session read. |
| The size of the always-loaded surface (a `tier` budget, 32 KiB) | It never fired on a real tree; six files and a `du` answer the same question. |
| A generated `briefing.md` | This tree ships no renderer, and the register is the copy; the gate would scan zero files. |
| `inbox.md` (a capture buffer and its 40-line cap) | Not designed and nothing routes to it; no gate may require it and no command may create it. |

## The liveness rule

A gate must have a non-zero denominator: a gate that measures nothing reports success, and one that scans
zero files has silently passed. Three obligations, and they bind the tool:

1. **Every gate counts its subjects and prints the count in its OK line**: `ok leaf-index 12 topics, 27
   leaves`; `ok pointers 88 cited paths in 9 files`. The summary's denominator is **all nine known names**, never
   the number that ran, so `check` says `5 of 9` and only `--all` says `9 of 9`: a ratio of one is no reading.
2. **Zero subjects is reported, and it blocks only where the location is absent**: `FAIL caps 0 artefacts;
   that location does not exist, and a gate that scanned nothing has not passed` is a misconfiguration, while
   `ok register 0 rows and folders - nothing here yet` is a fresh install or a drained topic and prints its
   count. Failing both, measured 2026-11-08, made an install report four blocking findings before its first topic.
3. **A gate pinned for a shape the repo does not carry fails on the absent path**, never on silence:
   `FAIL installed .windsurf/rules/context.md: named in shells, absent`. A host without that harness removes
   the path from `shells`, or lists the gate in `checks_disabled`, and the summary echoes `disabled: ported`
   so a silenced gate is never invisible. `--warn` prints the same findings and exits 0; it does not turn a
   zero into a pass.

## The config surface

Keys the gate set requires, and nothing else. Paths: `memory`, `root_rules`, `index_of_topics`,
`topics_dir`, `entry_file`, `shells`, and `port_target` (the one shell holding the body; the rest are
pointers). Budgets: `artefacts` and `root_artefacts` entries carrying `max_lines`, `max_rules`,
`max_rule_chars` and `requires`; plus `leaves.max_lines` and `briefs.threshold`. Fan-out is **not** a key:
it is the contract's constant (10). Gates: `checks_disabled` (default `[]`), `checks_advisory` (default `[]`;
a name here prints, never blocks), `extra_checks` (default `[]`; a host's assertion, same output shape).

**A config that names a gate which does not exist fails loudly.** Any unknown name, in `checks_disabled`,
`checks_advisory`, `extra_checks`, `--only` or `--skip`, exits **2** and lists every known name, the eight
gates and `installed`, so a typo never reads as a pass and a hook naming a removed gate learns on run one.
No key creates a file: `inbox`, `briefing` and `state/` are not config, none being an artefact here.

## One worked failure, end to end

A topic drained last week and its register row was never touched; or a folder was renamed and the row kept
the old path. Either way `context/topics/INDEX.md` line 9 says `pricing/` and nothing is there.

```
$ contextctl check
installed    ok    4 shells filled, entry block present
register     FAIL  13 folders, 13 rows
  context/topics/INDEX.md:9: row names "pricing/", no such folder
leaf-index   ok    12 topics, 27 leaves
shape        ok    41 files
caps         ok    41 files
1 blocking finding; 5 of 9 gates ran; 0 advisory; disabled: none
```

Exit 1. **Two legitimate responses.** *Fix the cause:* decide which copy is stale. If the row is right, the
folder was renamed, and the row is repointed and re-dated - one `act`, the turn the rename happened. If the
folder is right, the drain finished, and the row becomes the drained row naming the shim's path and the date
checked - an `owner` write, T5. *Make it advisory on purpose:* `"checks_advisory": ["register"]` in
`context.config.json`, with a `decisions.md` row saying why - a register written by another tool and lagging
one commit, say. The gate keeps printing; it stops blocking. There is no inline ignore, so silencing is
always a config entry plus a recorded reason, the shape `LOCKED.md` records for every other decision here.
