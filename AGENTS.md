# AGENTS.md - the rules for changing this repo

This repo's product is **prose plus one stdlib Python file**. A wrong sentence is incorrect behaviour, so the
rules are about claims. `CONTRIBUTING.md` has the long form and the evidence; this is the compressed copy,
because you read this file whether or not you read that one.

## Seven rules

1. **A claim about behaviour is observed.** Run it on the commit you are changing and paste the command and its
   output into the pull request. "I read the source" is not evidence. If you did not run it, write `UNVERIFIED:`
   in front of the sentence or delete it. Never describe behaviour under a condition you did not create - state
   the requirement instead.
2. **Nothing points outside this repo.** Every path, SHA, tag and URL resolves at HEAD. No absolute paths, no
   `~/`, no `../` escaping the tree, no sibling checkout, no "see my other repo". A SHA needs
   `git cat-file -e <sha>`. Cite path plus heading, never line numbers. **A measurement transfers; a pointer
   does not.**
3. **A number is derived, never typed.** A count that also exists in a table or a constant is generated from it
   or asserted equal by a test. A gate's summary string is part of its contract. State the method beside the
   number, or the number is not reproducible.
4. **The runbook is executed by a stranger.** Every command in `ADOPT.md` runs from an empty directory with
   nothing preset. Each step has one command and a stated observable result.
5. **Docs are the API.** A false sentence is a bug, so fixing it is a PATCH; new guidance is MINOR; changing what
   a document promises is MAJOR. A tag is immutable - corrections are a new tag. Release notes are a section of
   `LOCKED.md`, never text typed into the release UI.
6. **Scope.** Stdlib only, one runner file, no network in a check. No drive-by rewording of prose. One claim per
   pull request.
7. **The second time a class of defect ships, it becomes a gate - not a stronger reminder.**

## Before you push

```bash
python skeleton/scripts/contextctl.py check --all      # must print 0 blocking findings
python -m unittest discover -s tests                   # must pass
```

Then: `VERSION` has moved, `LOCKED.md` has a section under the reason for the change, and the pull request body
carries the output you ran.

## Where things are

| | |
| --- | --- |
| the change procedure | `.github/skills/contribute/SKILL.md` |
| the release procedure | `.github/skills/release-verify/SKILL.md` |
| what a gate asserts | `GATES.md` |
| why a rule exists, and when each version claimed what | `LOCKED.md` |
| which file is which | `FOLDER.md` |
| how a host installs this | `ADOPT.md` |
| the prose rules, scoped to markdown | `.github/instructions/prose.instructions.md` |

## Two things not to do

- **Do not patch `skeleton/scripts/contextctl.py` into shape for one host.** It is copied byte-identical, and a
  host's own rules belong in its own `scripts/`, wired through `extra_checks`.
- **Do not add a file "for agents" without saying which failure it prevents.** This repo has one of those
  already: this file says so in its first paragraph.
