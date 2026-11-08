# MEMORY - what is true before any topic is opened

> **Cross-cutting facts only.** Three kinds earn a line here, and nothing else does: what this repo is
> and how to run it when the code does not say; a convention that spans topics; where an external
> system lives.
>
> **A fact that a topic owns goes in that topic's leaf, and nowhere else.** An aggregate of the topics
> is the failure mode of this file: two copies drift, and the copy nobody loads is the one that gets
> edited.
> **Refs point at code, `docs/`, or an external path - never at a topic.** A fact with no such home
> stays self-contained on one line.
> **Test:** it must still be true if every topic folder were deleted, and it must fit on one line.
> A bullet that needs a second sentence is a leaf somewhere else.

## Identity

- Role: <one line>.
- How to run the thing when the code does not say: <one line>.

## Conventions

- Conventions that span topics and are not derivable from the code: <one line each>.

## External

- Where an external system, the host, or a shared reference lives: <one line each>.
