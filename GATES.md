# GATES - what keeps this tree correct, and what is deliberately unchecked

> One question: **what may a check assert, and what is left to a reader?** Authority above this file is
> `CONCEPT.md` (the six values), then `skeleton/context/README.md` (the contract); the operation is
> `MECHANISM.md`, the map `FOLDER.md`, the connection `AGENTIC-SYSTEM.md`. None is restated here. This was
> written **before** the tool, and the tool is built to it: `scripts/contextctl.py` and `context.config.json` implement the set below, so a change here is a change to them.

## The gate set

**Nothing here runs on its own.** No hook, no CI job and no turn-end check is installed by any step of this
repo; `port/hooks/` holds shapes and says so, and gates run at a milestone or when the owner asks. An install
copies files and one script: it adds **no workflow**, changes **no CI config** and requires **no status
check**, and a host that already runs CI never has this tree's example workflow added alongside or merged into
it. So
"posture: gate" below means **blocking when the owner runs `check`**, not blocking something nobody asked
for. Every gate guards an **`act`**; none guards an `ask` or `owner` trigger, since those are questions put
to a human when they matter. *Cadence* says where a gate *belongs*, so a host wiring
`port/hooks/pre-commit.sh` or `ci.yml` knows which subset to call; until then every row means the owner's invocation. *Where*: **both** is this template over `skeleton/context/` and a host over its own `context/`; **host only** means the shape exists only after install.

| Set | Gate | Where | Assertion (one sentence) | Failure it catches (a shape, not a risk) | Finding it prints | Cadence | Posture | Rated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| default | `register` | both | Every **live** folder under `topics_dir` has exactly one row in `index_of_topics`, and every row is one of two forms: **live** - its first cell names a folder under `topics_dir` that exists, and its date equals that topic `README.md`'s `Verified:` - or **drained** - its first cell names a folder under `archive_dir` that exists, with the date the receipt was checked, and no folder of the same name under `topics_dir`. A `Verified:` the gate cannot read (no line starting with it) is a finding, never a skip. | A topic on disk the register does not name; a row still pointing at a folder deleted at drain, or at an archive folder that is not there; a receipt whose date is missing, or that shares a name with a live topic; a topic re-read while its register row keeps the old date; a shim whose date sits at the end of a line, which used to make the row's date go unchecked in silence. | `FAIL register context/topics/INDEX.md:9: row names "pricing/", no such folder`; `FAIL register context/topics/INDEX.md:9: row names "context/archive/pricing/", an archive folder that does not exist`; `FAIL register context/topics/INDEX.md:9: widget/README.md has no "Verified:" line at the start of a line, so this row's date was not checked` | commit | gate | must |
| default | `leaf-index` | both | Every `L-####-*.md` names a row in its nearest index (the topic `## Leaves`, or its family `README.md`), and every row names a file that exists. | A leaf written and never indexed, so no later session knows it exists; a row whose leaf was deleted instead of rewritten. | `FAIL leaf-index context/topics/widget/L-0003-x.md: no row in context/topics/widget/README.md` | commit | gate | must |
| default | `shape` | both | Fixed shapes hold: a leaf's frontmatter (or its first two lines) carries `id:` and `brief:`; every `HANDOFF.md` carries `## Now`; every register and `## Leaves` row carries a date and a brief; every `decisions.md` row carries a `D-####` id; each `MEMORY.md` entry is one line. A missing `id` is reported **in the terms of the `leaf_pattern` in force** - `id: L-####` for the default, the configured pattern for a host that overrides it - and the message always names the two legal forms: the pattern's match, or the file stem. | A leaf that cannot be cited by id; a handoff whose next session has no first action; a decision row nothing can cite; a fact that grew a body under its bullet; and a host told to add an id shape its own config says it does not use. | `FAIL shape context/topics/widget/HANDOFF.md: no "## Now" heading; the next session has no first action` | commit | gate | should |
| default | `caps` | both | Every count is inside its configured cap: `HANDOFF.md` lines, `MUST-KNOW.md` rules and rule characters, `MEMORY.md` lines, leaf lines, topic `README.md` lines, and fan-out (more than 10 rows needs a family index). | A handoff grown to a thousand lines with the real next step at its end; a topic README listing thirty leaves flat. | `FAIL caps context/topics/widget/HANDOFF.md: 214 lines, max 90; move the history to JOURNEY.md and rewrite the snapshot` | milestone | gate | should |
| opt-in | `briefs` | both | No two leaves in **one topic** have `brief` lines above **0.82** similarity - calibrated 2026-11-08: 29 hard negatives (same topic, different conclusions) max at 0.649, so 0.82 leaves a 0.17 margin and fires on 0 of them. | Two leaves holding one conclusion, the second written instead of the first rewritten - **near-verbatim only**: a copy with a word changed scores above 0.9, a rephrasing scores 0.4-0.6 and is deliberately missed. | `FAIL briefs context/topics/widget/README.md:11: brief of L-0003 is 0.86 similar to L-0001` | CI | gate | could |
| opt-in | `verified` | both | A topic `README.md`'s `Verified:` date is not older than the newest **git commit date** among the leaves it indexes (`git log -1 --format=%cs`), never a filesystem mtime - and a **shallow** clone is refused before any date is compared: `git rev-parse --is-shallow-repository` is asked first, and one blocking finding says no date was checked, because a depth-1 boundary commit has no parent and git reports it as the root commit that added every file. A topic `README.md` with no line starting `Verified:` is a finding, not a silent omission from the set. | A topic re-read and one leaf rewritten, while the entry still shows last month's date; a clone that would answer every leaf with the boundary commit's date and print no complaint; a topic dropped from the count because its date is unreadable. | `FAIL verified context/topics/widget/README.md:3: Verified: 2026-09-01, 41 days behind L-0002`; `FAIL verified context: the clone is shallow, so ... no date was checked`; `FAIL verified context/topics/widget/README.md: no "Verified:" line at the start of a line, so this topic was not dated` | CI (2.7 s at 80 leaves, 17.5 s at 500 - one git spawn each, measured 2026-11-08) | gate | could |
| opt-in | `pointers` | both | Every backticked path in `MEMORY.md`, the root rules, the entry block and a topic `README.md` resolves from the tree root, unless it matches an `accepted_absent` entry or begins `~/` or `$HOME/`. | A citation to a file that moved, so a reader follows a dead pointer and trusts nothing after it. | `FAIL pointers context/MEMORY.md:12: "docs/runbook.md" does not resolve` | milestone | gate | should | <!-- leaks:ok -->
| opt-in | `leaks` | both | No backticked citation in the scanned files leaves the tree - an absolute path, a home-relative one, or a `..` that resolves outside the root - and no term from the host's own untracked deny file appears on a line; a line carrying the `leaks:ok` marker is skipped and **counted in the OK line**. The **existence** of an in-tree citation in arbitrary prose is not checked: a document about another tree names paths that are absent here. | A pointer a reader cannot follow because it is on the writer's machine; a sentence naming a host whose identity was meant to stay out of the tree; a rule quoting a forbidden form and looking exactly like a violation of it. | `FAIL leaks context/MEMORY.md:12: "C:\docs\runbook.md" is an absolute or home-relative path; a citation must resolve inside this repo` | milestone | gate | should |
| opt-in | `ported` | host only | Every path listed in `shells` carries a `ported: <YYYY-MM-DD>` line. | A filled rule shell with nothing dating it, so a human cannot rank it against the contract. | `FAIL ported .claude/rules/context.md:3: no "ported:" line` | milestone | gate | once |

**A host that changes nothing gets the four default gates**, blocking, when it runs `contextctl check` at a
milestone or on request, and **nothing else**: the opt-in five run only under `check --all` or
`check --only <name>`. *Rated* is value against cost: **must** = the memory does not work without it,
**should** = keeps the tree in shape, **could** = a gain smaller than the trust it costs, **once** = belongs
at install or update, not on a loop. The smallest set that keeps the tree working is `register` +
`leaf-index`; `shape` and `caps` earn their place by costing milliseconds; `pointers` is rated **should**
and stays opt-in because it measured 16 false findings on a real consumer repo; `leaks` is opt-in because its
scope is a policy a host sets, not a shape every tree shares; nothing else earns a default run.

### How a leaf index is read

The leaf column is read from the **header row**, never assumed to be the second column. `Leaf`, `Leaves`,
`File`, `Files`, `Filename`, or any header containing `leaf` or `file`, names the file column; `id` is chosen
only when no column names a file, because an `id` cell is an identity and the file name is what the gate
resolves. A table whose **only** identifier is `id` therefore **cannot index leaves**, and it reports that
once: `no column names a file, so this table cannot index leaves; its header is "id | Brief"`. The finding
names the header it read, so a reader knows what to change, and one finding is right because the defect is
the table's shape, not its contents: no row is resolved and no unlisted-leaf sweep runs for that README.
`id` beside a file column - `id | Leaf | Brief` - is the documented shape and is read exactly as before.
A cell written as a **markdown link** names the link's **target**, with any `./` prefix stripped:
`` [`01-clusters.md`](./01-clusters.md) `` resolves to `01-clusters.md`. Writing a table cell as a link is
the ordinary habit, and reading the whole cell as a file name reported 10 false findings on a real host -
`row names "[`01-clusters.md`](./01-clusters.md)", no such file`. A cell with no link keeps the old
reading exactly, and a link whose target does not exist is still one finding, naming the target.
A row line that a separator line follows is a **header**, so it is never a body row. A table with
no separator anywhere is read in the contract's own order, `id | Leaf | Brief` - the leaf column is the
second - so a hand-written table without a header is still read and no column is ever invented.

A **topic** `README.md` is read only inside its `## Leaves` heading, and every table under that heading is
read. A **family** `README.md` (`<topic>/<subdir>/README.md`) carries its index in the **first table whose
header names a column it can resolve** - a file column, or `id` alone, which reports the finding above and
resolves no row; a family README with neither has **no index and contributes nothing** - no row, and no
expectation that a leaf beside it is named - so a family README that holds a prose table is not read as a
leaf index.

### The one exception to "off for everything"

**`installed`**, not in the table because it never judges the tree - it judges whether the tree arrived, and
it is **host only**, **rated once**, and here **disabled** with the reason recorded. It asserts that every
path in `shells` exists, holds no `<!-- PORT:` marker, and is one of the two legal fills - the block body, or
a pointer whose first backticked path resolves - and that `entry_file` carries **exactly one** marked block,
holding something. The markers are counted, not merely found: a second block is an upsert that ran twice, an
empty block is a host whose routing table was replaced with nothing, and a `begin` after its `end` is no block
at all - three states review cannot see and, until 1.0.7, only step 5's hand `git diff` caught. It runs on
**every** invocation, `--only` included, and refuses `--skip`: it is the precondition of every other
denominator, since a tree whose shells were never filled gives the agent a comment where its rules should be.
It prints `FAIL installed .claude/rules/context.md:4: still contains "<!-- PORT: context-rules -->"; the routing table never reached the agent`. Its summary line counts the shells that arrived, so `0 of 4 shells filled`
is a failed install and not a tidy one. It is
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
| Whether a drained topic's archive holds what it should | The row checks that the folder exists and carries a date; which leaves went into it is a judgement made at drain, and no shape separates a complete archive from a partial one. |
| Whether an in-tree citation in arbitrary prose exists | Measured 2026-11-24: 299 backticked file paths in this repo do not resolve from the root, and almost all are correct - `ADOPT.md` describes *another* tree, so `MEMORY.md` and `scripts/contextctl.py` are host paths, not this repo's. `pointers` keeps the existence check for the four files where a citation is tree-root-relative by convention; `leaks` checks what is wrong in every tree. |
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
   leaves`; `ok pointers 88 cited paths in 9 files`. The summary's denominator is **all ten known names**
   plus the `extra_checks` that ran, never the number that ran, so `check` says `5 of 10` and only `--all`
   says `10 of 10` (or `11 of 11` with one host check): a ratio of one is no reading.
2. **Zero subjects is reported, and it blocks only where the location is absent**: `FAIL caps 0 artefacts;
   that location does not exist, and a gate that scanned nothing has not passed` is a misconfiguration, while
   `ok register 0 rows and folders - nothing here yet` is a fresh install or a drained topic and prints its
   count. Failing both, measured 2026-11-08, made an install report four blocking findings before its first topic.
3. **A gate pinned for a shape the repo does not carry fails on the absent path**, never on silence:
   `FAIL installed .windsurf/rules/context.md: named in shells, absent`. A host without that harness removes
   the path from `shells`, or lists the gate in `checks_disabled`, and the summary echoes `disabled: ported`
   so a silenced gate is never invisible. `--warn` prints the same findings and exits 0; it does not turn a
   zero into a pass.
4. **A leaf pattern that matches no file is reported, not green.** `leaf_pattern` is the one place leaf
   naming lives, `^L-\d{4}` by default. A `topics_dir` that holds files and none of them a leaf prints
   `leaf_pattern "^L-\d{4}" matches none of 115 files under context/topics; the leaf gates checked nothing`,
   once per run, from the first leaf gate the run selected - the count is in the message, and the message
   says what it measured. It is **advisory**: a tree drained to its last leaf is legitimately leaf-free, so
   a blocking finding would fail a correct drain and teach an operator to switch the gate off. A pattern
   that does not compile exits **2** before any gate runs, like any other config error.
5. **A clone that cannot answer truthfully is refused, not believed.** `verified` asks
   `git rev-parse --is-shallow-repository` **before** it compares any date, because in a depth-1 clone the
   boundary commit has no parent and git reports it as the root commit that added every file: `git log -1
   --format=%cs -- <leaf>` then returns that one commit's date for every leaf, so the
   `undated == len(leaves)` guard cannot fire and `ok ... 0 leaves without history` is a confident wrong
   answer. Measured on a real host, 2026-11-08: a depth-1 clone of 97 commits dated every sampled leaf
   `2026-11-08`, the clone boundary, where the true date was `2026-10-23`. So a shallow clone prints
   **one** finding for the whole run - `the clone is shallow, so the last-commit date git reports for a
   leaf is the clone boundary's, not the leaf's; no date was checked` - prints no per-leaf comparison,
   names the remedy (`fetch-depth: 0` on checkout, or `git fetch --unshallow`), and **blocks**: a silent
   wrong answer is worse than a loud failure. A host that cannot provide history lists `verified` in
   `checks_advisory`, which is the opt-out that already exists.

## An advisory gate is a backlog, and a backlog needs a payer

`checks_advisory` prints a finding and exits 0 on it, which is the right setting for a host in its first month.
It is not a neutral choice: the count becomes a promise, and only two things keep a promise - a scheduled
migration, or a rule attached to work the host already does. **The second is the one that has been measured.**

| Shape | Measured on a real host, 2026-11-08 to 2026-11-23 | Verdict |
| --- | --- | --- |
| advisory, no per-turn rule | 305 findings, unchanged, while the tree grew from 12 topics to 13 | a number nobody acts on |
| advisory + *a leaf you touch earns its `id:`, `brief:` and index row* | **305 → 175 (-43%)** in fifteen days with no migration and no operator: `shape` -82, `leaf-index` -51, and 49 leaves carrying a real `brief` where 2 did | **the recommended shape** |
| advisory, then `checks_disabled` | the count disappears with the block, so the backlog stops being visible | never - it erases the reading |

Two obligations follow. **Say what pays it down**, in the host's root rules, attached to an act rather than a
date. And **give the advisory decision an end condition** - which gate turns blocking, and when - because an
advisory gate nobody has agreed to promote is a permanently quiet one.

**A count that grows is not automatically a regression.** A host adding leaves adds findings; what matters is
the debt against the material, not the absolute number. `caps` rose by 6 in the reading above while the total
fell by 130, and that was new leaves over the cap, which is what a growing tree looks like.

## The config surface

Keys the gate set requires, and nothing else. Paths: `memory`, `root_rules`, `index_of_topics`,
`topics_dir`, `archive_dir`, `entry_file`, `shells`, and `port_target` (the one shell holding the body; the rest
are pointers). **`archive_dir`** (default `context/archive`) is where a drained topic's folder lives: a register
row whose first cell names a folder there is a **receipt**, checked for existence and a date, and a value inside
`topics_dir` exits **2** because every gate scopes there. **`leaks`** takes an object: `roots` (default
`["context"]` - the scope is a policy, and a host with code beside its memory points it there), `suffixes`
(default the same nine text forms `pointers` understands), `deny_file` (default `.leaks-deny.txt`, **gitignored
and never committed**: the names a host must not leak are themselves a leak), and `marker` (default `leaks:ok`).
Budgets: `artefacts` and `root_artefacts` entries
carrying `max_lines`, `max_rules`, `max_rule_chars` and `requires`; plus `leaves.max_lines` and
`briefs.threshold`. **Leaf naming:**
`leaf_pattern` (default `"^L-\\d{4}"`), the regular expression, matched against a file name under
`topics_dir`, that decides what a leaf is - a host whose notes are `01-scheduler.md` sets `"^\\d{2}-"` and
its leaves stop being invisible. It must match leaf files only: whatever it matches is read for an `id` and
a `brief`. Fan-out is **not** a key:
it is the contract's constant (10). Gates: `checks_disabled` (default `[]`), `checks_advisory` (default `[]`;
a name here prints, never blocks), `extra_checks` (default `[]`; a host's own check - the point below).
**`extra_checks` is where a host attaches a rule this tool does not ship.** Each entry is
`"module:function"`; the module is resolved from `<root>/scripts/` (that path is put on `sys.path`, so a
module may import its siblings) and the function is called as `function(root, cfg)`. Its return value is a
list of findings: a **dict** with `message` plus optional `rel` and `line`, or a **plain string**. Each
check prints as one line named `extra:<module>.<function>`. They run **only under `check --all`**, exactly
like the five opt-in gates, and the summary's denominator becomes `10 + the extras that ran` - so a tree
with no extras still prints `N of 10 gates ran`. An entry that is not `module:function` exits **2**; a
module that will not import, a function that is absent and a function that raises are each a **finding**,
never a traceback that ends the run.

**Two things a host rule gets wrong, and both have been measured.** A host rule is written once, against the
material in front of its author, and then meets material the author never saw. This tree ships **no** rule that
resolves citations inside a leaf - `pointers` deliberately covers the four routing files in `MEMORY.md`, the
root rules, the entry block and a topic `README.md`, because a leaf cites the world - so leaf-level citation
checking is the seam where that judgement lands, and where it has failed twice:

- **Scope.** A rule that resolves a path must say what the path resolves *against*. The failure is a per-file
  exception map - one entry per document that cites something unusual - because it cannot grow. Measured
  2026-11-23: a host with a **two-entry** map and 66 documents citing client code produced **296 findings, and
  227 of them were paths that exist, resolved from the wrong base**. Declare bases as a **list tried in
  order** - the tree root, the citing file's own folder, each checkout the host reads - and keep a per-file
  entry only as an override; the same corpus then reports 69.
- **Granularity.** A blocking host rule coarser or finer than the material becomes the dominant failure mode of
  the whole surface: in that same reading **all 296 blocking findings came from one host rule, and all nine
  shipped gates were green**. A host rule earns `block` after it has been watched over real material; before
  that it belongs in `checks_advisory`, which is the host's own dated decision.
`accepted_absent` (default `[]`) is `pointers`'s list of citations a clone cannot resolve: an entry is a
path, a path prefix or a glob, a citation matching one is **accepted, not reported**, and the gate's own
line prints how many it accepted - `ok pointers 108 cited paths in 14 files, 22 accepted absent` - so a
check that covers less than it claims says so out loud. An entry that matches no citation is itself a
finding (`FAIL pointers context.config.json: accepted_absent entry "repos/" matched no citation`), so the
list cannot rot into a list nobody read. **A citation beginning `~/` or `$HOME/` is always accepted, and <!-- leaks:ok -->
counted in the same number, with no config**: a memory tree may legitimately cite a user-level file, and
no tree root can resolve one.

**A config that names a gate which does not exist fails loudly.** Any unknown name, in `checks_disabled`,
`checks_advisory`, `--only` or `--skip`, exits **2** and lists every known name, the nine gates and
`installed`, so a typo never reads as a pass and a hook naming a removed gate learns on run one.
**The one exception is `--only installed`, run alone**: it is the install proof `ADOPT.md` step 6 tells an
adopter to run, and it never consults those lists, so a host carrying its own legacy gate names still gets
its install checked - each ignored name is printed to stderr with `note:` and never silently dropped. Any
other invocation is strict. A config carrying a UTF-8 BOM is read (`utf-8-sig`): Windows PowerShell 5.1's
`Set-Content -Encoding utf8` writes one, and a config that cannot be read is an install that cannot be proven.
No key creates a file: `inbox`, `briefing` and `state/` are not config, none being an artefact here.

## One worked failure, end to end

A topic drained last week and its register row was never touched; or a folder was renamed and the row kept
the old path. Either way `context/topics/INDEX.md` line 9 says `pricing/` and nothing is there.

```
$ contextctl check
installed    ok    4 of 4 shells filled, entry block present
register     FAIL  13 rows, 13 folders, 0 drained
  context/topics/INDEX.md:9: row names "pricing/", no such folder
leaf-index   ok    12 topics, 27 leaves
shape        ok    41 files
caps         ok    41 files
1 blocking finding; 5 of 10 gates ran; 0 advisory; disabled: none
```

Exit 1. **Two legitimate responses.** *Fix the cause:* decide which copy is stale. If the row is right, the
folder was renamed, and the row is repointed and re-dated - one `act`, the turn the rename happened. If the
folder is right, the drain finished, and the row becomes an **address** - its first cell the archive folder, its
date the day the receipt was checked - an `owner` write, T5. *Make it advisory on purpose:* `"checks_advisory": ["register"]` in
`context.config.json`, with a `decisions.md` row saying why - a register written by another tool and lagging
one commit, say. The gate keeps printing; it stops blocking. There is no inline ignore, so silencing is
always a config entry plus a recorded reason, the shape `LOCKED.md` records for every other decision here.
