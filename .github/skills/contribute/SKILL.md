---
name: contribute
description: "The procedure for changing this repo safely: gather the failing case first, change one claim, prove it with a command, then record it. Use when making any change to agent-context, whether the change is code, prose, or the skeleton a host copies."
---

# contribute

The rules are `CONTRIBUTING.md`. This is only the order to do them in, and it exists because the two most
expensive defects here were both **prose that nobody executed** - not code that failed.

## 1. Find the failing case before the change

A change with no failing case behind it is a preference. Get one of these, in this order of preference:

- **an observation** - a command whose real output contradicts what a document says, pasted as it printed;
- **a second occurrence** - a class of defect that has already shipped once; this alone justifies a gate;
- **a stranger's failure** - someone followed the runbook and could not, with the step they were on.

Write the failing case in one sentence before touching a file. If you cannot, stop - you are about to add a
preference, and this repo is small enough that preferences are the noise.

## 2. Decide where the change belongs

| The change is | It goes in |
| --- | --- |
| what a gate asserts, or how it reports | `skeleton/scripts/contextctl.py`, and a test in `tests/` |
| what a host must do to install | `ADOPT.md`, and `MANIFEST.md` if the contract moved |
| why the shape is what it is | `CONCEPT.md` or `FOLDER.md` |
| what a gate is and when it runs | `GATES.md` |
| a release, and the decision behind it | `LOCKED.md` |
| a rule for contributors | `CONTRIBUTING.md`, and the compressed copy in `AGENTS.md` |

**One claim per pull request.** If your failing case touches a gate and a document, that is two claims unless the
document quotes the gate's output - in which case rule 3 of `CONTRIBUTING.md` makes it one.

## 3. Make the change, and run the thing you changed

```bash
python skeleton/scripts/contextctl.py check --all
python -m unittest discover -s tests
```

For a gate change, also **break the gate on purpose** in a fixture and watch it fail. A check nobody has seen
fail is a check nobody should trust.

For a prose change that describes behaviour, the output you paste into the pull request is the one you ran at
**this** commit. Not a remembered run, not the previous release's.

## 4. Prove the claims in your own diff

Three greps, and each one has caught a real release:

```bash
# rule 2 - nothing points outside the repo
git grep -n -E '(/Users/|/home/|\.\./|~/)' -- '*.md'

# rule 2 - every backticked path you added resolves
git diff --unified=0 HEAD -- '*.md' | grep '^+' | grep -o '`[^`]*/[^`]*`'

# rule 1 - nothing you wrote is a claim you did not run
git diff HEAD -- '*.md' | grep '^+' | grep -iE 'reports|prints|returns|fails|emits|produces'
```

The third list is short by design. Read every line and ask: *did I run this, or am I describing what it should
do?* Prefix `UNVERIFIED:` for the ones you did not.

## 5. Record it

- Bump `VERSION`: a false sentence fixed is a PATCH, new guidance is a MINOR, a changed promise is a MAJOR.
- Add a section to `LOCKED.md` **under the reason the change was made**, as a `Was | Is` table. The reason is a
  sentence about the defect, not about the release.
- Say in the section what the change does **not** do, when that is the honest answer. Several sections here end
  that way, and they are the reason the next reader does not re-litigate it.

## 6. Cut and verify the release

Use `release-verify`. It is a separate procedure because cutting a release and *proving* the release are two
different jobs, and the second one is where the shallow-clone defect would have been caught.

## Anti-patterns, each with the release that proves it

| Do not | Because |
| --- | --- |
| describe behaviour you did not create | 1.0.2's depth-1 claim was false for two releases |
| point at another checkout | 1.0.3 and 1.0.8 both did, and both had to be corrected |
| type a count that a table already holds | 1.0.2 said three beside a table of six |
| patch the runner to suit one host | it is copied byte-identical; a host's rules belong in its own script |
| add a document "for agents" without naming its failure | that is how this repo got one artefact nobody read |
