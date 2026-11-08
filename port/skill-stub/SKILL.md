---
name: context-tree
description: "Read order and stop point for this repo's context/ memory tree, and which tree applies in a multi-root workspace. Use when starting a task in this repo, or when a task may touch context/."
---

# context-tree

> **Pointer, not a copy.** The procedure lives in exactly one file - the highest-ranked harness's
> `SKILL.md` - and this stub exists only because this harness reads its own skill directory. The
> frontmatter above is byte-identical to the canonical copy's, which is what makes the match work.

Read the canonical `SKILL.md` in the sibling harness's skill directory and follow it exactly:

```
<canonical skill path>
```

If that path no longer exists, **say so and stop** - do not reconstruct the procedure from memory. The
canonical body is the only one, and a second copy written here would drift from it silently.
