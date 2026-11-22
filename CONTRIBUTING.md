# CONTRIBUTING - changing a repo whose product is its prose

> Read this before your first change. It is short on purpose: seven rules, each one bought by a defect this
> repo actually shipped. `AGENTS.md` carries the same rules compressed, because an agent reads that file
> whether or not it reads this one.

**Why this repo is unusual.** There is no library here. The product is **nine documents, a skeleton a host
copies, and one stdlib-only Python file**. So a wrong sentence is not a doc bug, it is incorrect behaviour -
which is why this file is about claims rather than about code style.

## The seven rules, ranked by what they prevent

### 1. A claim about behaviour is observed, not inferred

> Any sentence describing what a command, gate or tool *does* must come from **running it on the commit you are
> changing**, and the command plus its real output goes in the pull request body. "I read the source" is not
> evidence.

**Bought by:** 1.0.2 said a depth-1 clone made `verified` report the history unavailable. It never did - git
presented the boundary commit as the root that added every file, so the gate dated every leaf with a confident
wrong date. Two releases carried the false claim before it was executed. See `LOCKED.md` 1.0.6.

Three corollaries, each also bought:

- **Never describe behaviour under a condition you did not create.** If the claim is about a shallow clone, run
  it in a shallow clone. If you cannot, state the *requirement* instead of the behaviour: "requires full
  history" survives; "reports history unavailable" was false.
- **Quote output verbatim, including the wrong parts.** A paraphrase is the author's belief about the output.
- **If you did not run it, write `UNVERIFIED:` in front of the sentence or delete it.** There is no third
  option, and a reader greps for that word.

### 2. Nothing points outside this repository

> Every path, SHA, tag, issue number and URL in prose, code fences, YAML and comments must resolve **inside this
> repo at HEAD**. Forbidden: absolute paths (`C:\`, `/Users/`, `/home/`), `~/`, `..` that escapes the repo, a
> sibling checkout, "see my other repo".

- A SHA must satisfy `git cat-file -e <sha>`, and the commit subject is quoted beside it.
- Cite by **path plus heading**, never by line number: line numbers rot, paths can be checked.
- **A measurement transfers; a pointer does not.** You may state a number you measured elsewhere. You may not
  say where the work lives, because that resolves for nobody reading this repo.

**Bought twice:** 1.0.3 shipped a citation to `agent/WIRING.md` and a commit this repo never held; 1.0.8 shipped
a sentence pointing at another checkout's topic and leaf number, corrected in 1.0.9. **The second occurrence of
a class converts a reminder into a gate** - that is the escalation rule below.

### 3. A number is derived, never typed

> Any count in prose that also exists in a table, list, enum or code constant must be generated from that source,
> or asserted equal to it by a test.

- A gate's summary string is **part of its contract**. Quoting it in a doc means the doc sentence and the format
  string change in the same commit.
- Use the code's own vocabulary. If the gate counts *filled* entries, the prose says "filled", not "N".
- If the number needs a method to be meaningful, state the method in the same paragraph. A count without its
  bases and their order is not reproducible, and an unreproducible measurement is a claim.

**Bought by:** 1.0.2's intro said *three defects* beside a table of six; the table was right. And a summary
line printed `4 shells filled` beside four `named in shells, absent` findings - 1.0.7 fixed the line, and the
reason it survived is that no test compared the string to the doc.

### 4. The runbook is executed by a stranger

> Every command in `ADOPT.md` is copy-pasteable from an empty directory on a machine that has only the
> prerequisites listed at the top. No step assumes an existing checkout, a preset variable, or a sibling folder.

Each step is numbered, has one command, and states its observable result. A release is not cut until someone
has cloned the tag and pasted the runbook verbatim.

**Bought by:** the `git mv` step that failed on an uncommitted copy, and the install proof that only worked once
the shells had been trimmed - both found by a stranger's run, neither by reading.

### 5. Version and changelog discipline

> The documentation is the public API, so **a false sentence is a bug and fixing it is a PATCH**. New guidance
> is a MINOR. Changing what a document promises is a MAJOR.

- A tagged version is **immutable**: corrections are a new tag, never an amended one. `v1.0.0` through `v1.0.9`
  are all still resolvable, and each is the commit CI proved.
- Release notes are a **file in the tree** (`LOCKED.md`), not text typed into the release UI. The body of a
  release is that file's section at the tag's commit, so "the notes claim X" reduces to `git show <tag>:LOCKED.md`.
- No count of "fixed N things" unless N is computed from a file.

### 6. Scope: what this repo refuses

- **Stdlib only.** The runner is one file. No new runtime dependency, no network call from a check, no check
  that writes outside a temp directory.
- **No drive-by rewording.** A prose document is a versioned artefact; a pull request touching it names which
  claim changed and why.
- **One claim per pull request.** A reviewer cannot verify three unrelated claims from one diff.

### 7. Definition of done

A change is done when all six hold, and the pull request body shows them:

- [ ] the output of the command I ran, pasted
- [ ] every path and SHA I wrote resolves (`git grep` for the ones I added)
- [ ] every number I wrote is derived, or the sentence says where it came from
- [ ] `python skeleton/scripts/contextctl.py check --all` prints `0 blocking findings`
- [ ] `python -m unittest discover -s tests` passes
- [ ] `LOCKED.md` has a section under the reason the change was made, and `VERSION` has moved

## The escalation rule

**The second time a class of defect ships, it becomes a gate - not a stronger reminder.** A rule is a
hypothesis that people will remember; a gate is the observation that they did not. Both of this repo's
external-pointer defects would have been caught by a check that every backticked path resolves.

Until that check exists, the release procedure in `.github/skills/release-verify/SKILL.md` includes a per-term
grep for the names a pointer would have used.

## What does **not** belong here

A code-of-conduct essay, a "ways to contribute" taxonomy, a governance section, an architecture tour. In a repo
this size they cost maintenance and prevent none of the seven. If a proposed section cannot name the defect it
prevents, it is a preference.

## Where the procedure lives

| You want to | Read |
| --- | --- |
| make a change safely, end to end | `.github/skills/contribute/SKILL.md` |
| cut or verify a release | `.github/skills/release-verify/SKILL.md` |
| know why a rule exists | `LOCKED.md`, under the version that bought it |
| know what a gate asserts | `GATES.md` |
| install the tree on a host | `ADOPT.md` |
