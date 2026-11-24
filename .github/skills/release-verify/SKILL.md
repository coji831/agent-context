---
name: release-verify
description: "Prove a tagged release of agent-context matches what its notes claim: run the gates and tests on the tag, install the tree from the tag into an empty directory, run the runbook verbatim, and grep the published tree for pointers it must not contain. Use when tagging a release or auditing an existing tag."
---

# release-verify

Cutting a release and **proving** one are different jobs. This is the second. Every step here exists because a
release of this repo claimed something it had not shown.

## 1. The tag points at a commit CI proved

```bash
git rev-parse v<X.Y.Z>^{commit}          # the commit the tag peels to
gh run list --branch main --limit 1      # the run whose headSha must equal it
```

A tag on a commit that never passed is a claim with no observation. Put the run id in the **release body**, which
is written after the run exists. It cannot go in `LOCKED.md`: the tag is cut before the run finishes, and a tag is
immutable, so a release section that quoted its own run id could only be true by being wrong about when it was
written. `LOCKED.md` records the version and the decision, neither of which depends on a run id.

## 2. The gate and the tests pass **at the tag**, from a clean clone

```bash
git clone --depth 1 --branch v<X.Y.Z> <url> /tmp/verify && cd /tmp/verify
python skeleton/scripts/contextctl.py check --all
python -m unittest discover -s tests
```

Clone by tag, not from the working tree: the working tree can pass while the tag is missing a file. Use
`--depth 1` deliberately, because it also tells you whether the gates survive a shallow clone - `verified` refuses
one loudly, and that refusal is a passing result here, not a failure.

## 3. No pointer leaves the repo

The class of defect this repo has shipped twice. **`leaks` gates most of it** (opt-in, so run `--all`):

```bash
python skeleton/scripts/contextctl.py check --all --only leaks
```

It reports an absolute or home-relative citation, a parent-relative one that resolves outside the root from the
citing file's directory, and any term from `.leaks-deny.txt`. A line that names an outside thing **on purpose** -
a rule quoting the forbidden forms, a harness fact, a historical record - carries the `leaks:ok` marker, and the OK
line prints how many lines carry it, so the exempt surface is a number rather than an assumption.

**What the gate does not check, and you do:** whether an in-tree citation in arbitrary prose *exists*. A document
about another tree legitimately names paths that are absent here - measured at 299 of 641 in this repo - so this
grep is the release's job:

```bash
git grep -n -E '`[^`]*/[^`]*`' -- '*.md'
```

Every hit must resolve inside this repo. A path that does not is a finding.

**The deny-list is yours, and it must not be committed.** Pointers name the author's other work - a checkout they
had open, a private repo, a desk. `leaks` reads `.leaks-deny.txt` at the root, one term per line, and
`skeleton/.gitignore` keeps it out of every diff:

```bash
printf '%s\n' <the names of the repos you have open> > .leaks-deny.txt
python skeleton/scripts/contextctl.py check --all --only leaks
```

**Empty is the only passing result.** Put those terms anywhere in the tree and the leak becomes permanent: a
deny-list containing somebody's repo name is itself the defect it is meant to catch. That is not hypothetical -
the first draft of this file did exactly that, and it was caught by running the grep against the file.

If a hit is legitimate - the licence holder's name, a documented command shape - write the exception and the
reason into the release section.

## 4. A stranger can install it

Follow `ADOPT.md` from step 1 in an empty directory on a machine that has only what the document lists at the top.
Paste nothing from memory, skip nothing, and **do not** `cd` anywhere the document does not tell you to.

What you are looking for is not a crash. It is a **step that only its author can run**: a path that assumes a
sibling checkout, a shell that assumes a filled config, a `git mv` on an untracked copy.

Record, per step, one of: ran and printed what the step says / ran and printed something else / could not run, and
why. The third column is the finding.

## 5. The notes are a file at that commit

```bash
git show v<X.Y.Z>:LOCKED.md | head -40
```

The release body is that section, not a paragraph typed into the release UI. "The notes claim X" then reduces to
"the file at this commit says X", which the command above settles.

Check the section against §1's tag: **does every number in it come from a run in this session, or from a file?**
A number that came from a previous release's text is the 1.0.2 defect.

## 6. Say what was not verified

End the release section with the things you did not do, in the repo's own style - 1.0.7 and 1.0.8 both do. A
release whose notes claim completeness invites the next reader to trust the gaps.

## Anti-patterns

| Do not | Because |
| --- | --- |
| tag before CI is green | the tag is the pin; a red pin is worse than no release |
| verify the working tree instead of the tag | they diverge, which is the whole reason to clone |
| treat a red gate at the tag as the host's problem | the shipped tree is this repo's product |
| publish notes that claim more than §1-§5 showed | this repo has done it, and corrected it in the next patch |
