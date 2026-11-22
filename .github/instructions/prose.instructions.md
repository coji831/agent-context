---
description: "Rules for changing this repo's prose, which is its product: claims are observed, nothing points outside the repo, numbers are derived. Read before editing any .md here."
applyTo: "**/*.md"
---

<!-- The long form, with the evidence behind each rule, is `CONTRIBUTING.md`. This file is the same three rules
     compressed, because a rule a contributor has to go and find is a rule that fires after the mistake. -->

**In this repo the prose is the product.** A false sentence is incorrect behaviour, not a typo. Three rules apply
to every markdown file here, including `LOCKED.md`.

1. **Claims are observed, not inferred.** Any sentence about what a command, gate or tool *does* comes from
   running it on this commit, with the output pasted into the pull request. If you did not run it, prefix the
   sentence `UNVERIFIED:` or delete it. Do not describe behaviour under a condition you did not create - state
   the requirement: "requires full history" survives, "reports history unavailable" was false here for two
   releases.

2. **Nothing points outside this repo.** Every path, SHA, tag and URL resolves at HEAD. No `C:\`, no `/Users/`,
   no `/home/`, no `~/`, no `../` escaping the tree, no sibling checkout, no "see my other repo". A SHA needs
   `git cat-file -e`. Cite path plus heading; line numbers rot. **A measurement transfers; a pointer does not** -
   you may state a number you measured elsewhere, never where the work lives.

3. **A number is derived, never typed.** If the count also exists in a table, a list or a constant, generate it
   or assert it equal in a test. A gate's summary string is part of its contract: quoting it means the sentence
   and the format string move in the same commit. Put the method beside the number, or the number is not
   reproducible.

**Before you save the file**, grep what you added for the shapes rule 2 forbids:

```bash
git grep -n -E '(/Users/|/home/|\.\./|~/)' -- '*.md'
```

A hit is a finding, unless it sits inside a fence that documents the rule itself.
