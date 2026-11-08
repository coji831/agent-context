#!/usr/bin/env python3
"""Tests for contextctl: every gate fails on its own defect and passes on a clean tree.

Run with:  python -m unittest discover -s tests -v
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skeleton" / "scripts"))

import contextctl  # noqa: E402

TODAY = date.today().isoformat()

ENTRY = """# AGENTS.md

<!-- context:begin -->
**This repo's memory is `context/`, not your session.** Load `context/MEMORY.md` at the start, then
`context/topics/INDEX.md` when the task names no topic, then stop.
<!-- context:end -->
"""

MEMORY = """# MEMORY

- this repo is a test fixture
"""

ROOT_RULES = """# MUST-KNOW

1. **A rule that applies everywhere.**
"""

INDEX = """# Topic register

| Topic | What it covers | Verified |
| --- | --- | --- |
| `context/topics/widget/` | the widget | {today} |
"""

TOPIC_README = """# widget

Verified: {today}

## Leaves

| id | Leaf | Brief - what it answers |
| --- | --- | --- |
| `L-0001` | `L-0001-widget.md` | what the rig measured |
"""

HANDOFF = """# HANDOFF

## Now

read the scheduler's batch size
"""

DECISIONS = """# decisions

| id | Date | Decision | Why | Ruled out |
| --- | --- | --- | --- | --- |
| `D-0001` | {today} | measure before tuning | the rig disagreed with the spec | trusting the spec |
"""

TOPIC_RULES = """# MUST-KNOW

1. **A rule for this area only.**
"""

LEAF = """---
id: L-0001
brief: what the rig measured
---

# L-0001 - widget throughput

42/s.
"""

SHELL = """---
description: rules for the tree
---

The routing table lives here.

ported: {today}
"""


class Tree:
    """A throwaway tree that is a legal agent-context, so a test can break one thing."""

    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.files = {
            "AGENTS.md": ENTRY,
            "context/MEMORY.md": MEMORY,
            "context/MUST-KNOW.md": ROOT_RULES,
            "context/topics/INDEX.md": INDEX,
            "context/topics/widget/README.md": TOPIC_README,
            "context/topics/widget/HANDOFF.md": HANDOFF,
            "context/topics/widget/decisions.md": DECISIONS,
            "context/topics/widget/MUST-KNOW.md": TOPIC_RULES,
            "context/topics/widget/L-0001-widget.md": LEAF,
            ".claude/rules/context.md": SHELL,
        }
        for name, text in self.files.items():
            self.write(name, text)
        self.config({"shells": [".claude/rules/context.md"]})
        self.git()

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.format(today=TODAY), encoding="utf-8")

    def read(self, name: str) -> str:
        return (self.root / name).read_text(encoding="utf-8")

    def append(self, name: str, text: str) -> None:
        self.write(name, self.read(name) + text.format(today=TODAY))

    def config(self, extra: dict) -> None:
        (self.root / "context.config.json").write_text(json.dumps(extra), encoding="utf-8")

    def git(self) -> None:
        for command in (["init", "-q"], ["add", "-A"],
                        ["-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qm", "tree"]):
            subprocess.run(["git", "-C", str(self.root)] + command, capture_output=True, text=True)

    def run(self, *args: str) -> tuple[int, str]:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            code = contextctl.main(["--root", str(self.root)] + list(args))
        return code, buffer.getvalue()

    def digest(self) -> str:
        hasher = hashlib.sha256()
        for path in sorted(self.root.rglob("*")):
            if path.is_file() and ".git" not in path.parts:
                hasher.update(path.as_posix().encode())
                hasher.update(path.read_bytes())
        return hasher.hexdigest()

    def close(self) -> None:
        self.tmp.cleanup()

    def clear(self) -> None:
        """Leave a root with a config and nothing else: the zero-denominator tree."""
        for path in sorted(self.root.rglob("*"), reverse=True):
            if path.is_file() and ".git" not in path.parts and path.name != "context.config.json":
                path.unlink()
            elif path.is_dir() and ".git" not in path.parts and path != self.root:
                try:
                    path.rmdir()
                except OSError:
                    pass


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = Tree()
        self.addCleanup(self.tree.close)

    def assert_passes(self, *args: str) -> None:
        code, out = self.tree.run(*args)
        self.assertEqual(code, 0, out)

    def assert_fails_with(self, needle: str, *args: str) -> str:
        code, out = self.tree.run(*args)
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)
        return out


class CleanTree(Base):
    def test_all_gates_pass(self) -> None:
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 0, out)
        self.assertIn("0 blocking findings", out)
        self.assertIn("9 of 9 gates ran", out)

    def test_default_run_is_the_four(self) -> None:
        code, out = self.tree.run("check")
        self.assertEqual(code, 0, out)
        self.assertIn("5 of 9 gates ran", out)
        self.assertNotIn("briefs", out)

    def test_run_writes_nothing(self) -> None:
        before = self.tree.digest()
        self.tree.run("check", "--all")
        self.assertEqual(before, self.tree.digest())


class Register(Base):
    def test_row_without_folder(self) -> None:
        self.tree.append("context/topics/INDEX.md",
                         "| `context/topics/pricing/` | pricing | {today} |\n")
        self.assert_fails_with('row names "context/topics/pricing/", no such folder', "check")

    def test_folder_without_row(self) -> None:
        self.tree.write("context/topics/pricing/README.md", "# pricing\n\nVerified: " + TODAY + "\n")
        self.assert_fails_with("folder has no row", "check")

    def test_date_differs_from_the_topic_readme(self) -> None:
        readme = self.tree.read("context/topics/widget/README.md").replace(TODAY, "2020-01-01")
        self.tree.write("context/topics/widget/README.md", readme)
        self.assert_fails_with("differs from widget/README.md Verified", "check")


class LeafIndex(Base):
    def test_leaf_with_no_row(self) -> None:
        self.tree.write("context/topics/widget/L-0002-more.md",
                        "---\nid: L-0002\nbrief: another conclusion\n---\n")
        self.assert_fails_with("no row in context/topics/widget/README.md", "check")

    def test_row_with_no_file(self) -> None:
        self.tree.append("context/topics/widget/README.md",
                         "| `L-0009` | `L-0009-gone.md` | a leaf that is not there |\n")
        self.assert_fails_with('row names "L-0009-gone.md", no such file', "check")


class LeafColumns(Base):
    """The leaf column is read from the header, never assumed to be the second one.

    A host writes `| Leaf | What it answers |`, and a gate that took `cells[1]` read the *brief* as a
    file name and the header row itself as a row - two findings per table, neither true.
    """

    def leaves_section(self, table: str) -> None:
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\n" + table)

    def test_host_column_order(self) -> None:
        self.leaves_section("| Leaf | What it answers |\n| --- | --- |\n"
                            "| `L-0001-widget.md` | what the rig measured |\n")
        self.assert_passes("check", "--only", "leaf-index", "--only", "shape")

    def test_published_column_order(self) -> None:
        self.assert_passes("check", "--only", "leaf-index", "--only", "shape")

    def test_two_columns(self) -> None:
        self.leaves_section("| id | Leaf |\n| --- | --- |\n"
                            "| `L-0001` | `L-0001-widget.md` |\n")
        self.assert_passes("check", "--only", "leaf-index", "--only", "shape")

    def test_no_header_falls_back_to_the_documented_order(self) -> None:
        self.leaves_section("| `L-0001` | `L-0001-widget.md` | what the rig measured |\n")
        self.assert_passes("check", "--only", "leaf-index")

    def test_missing_file_is_still_found_in_the_leaf_column(self) -> None:
        self.leaves_section("| Leaf | What it answers |\n| --- | --- |\n"
                            "| `L-0009-gone.md` | a leaf that is not there |\n")
        self.assert_fails_with('row names "L-0009-gone.md", no such file', "check", "--only", "leaf-index")

    def test_a_prose_table_outside_the_leaves_section_is_ignored(self) -> None:
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## What this is\n\n"
                        "| Project | Note |\n| --- | --- |\n| pvl-rentals | ask the client first |\n\n"
                        "## Leaves\n\n| Leaf | What it answers |\n| --- | --- |\n"
                        "| `L-0001-widget.md` | what the rig measured |\n")
        self.assert_passes("check", "--only", "leaf-index", "--only", "shape")

    def test_a_family_index_is_the_first_table_naming_a_file(self) -> None:
        self.tree.write("context/topics/widget/plan/README.md",
                        "# plan/\n\n> written during the work.\n\n"
                        "| Phase | State |\n| --- | --- |\n| one | done |\n\n"
                        "| id | Leaf | Brief - what it answers |\n| --- | --- | --- |\n"
                        "| `L-0002` | `L-0002-plan.md` | the order of the phases |\n")
        self.tree.write("context/topics/widget/plan/L-0002-plan.md",
                        "---\nid: L-0002\nbrief: the order of the phases\n---\n")
        self.assert_passes("check", "--only", "leaf-index")

    def test_a_family_without_a_leaf_table_contributes_nothing(self) -> None:
        self.tree.write("context/topics/widget/plan/README.md",
                        "# plan/\n\n| Phase | State |\n| --- | --- |\n| one | done |\n")
        self.tree.write("context/topics/widget/plan/L-0002-plan.md",
                        "---\nid: L-0002\nbrief: the order of the phases\n---\n")
        self.assert_passes("check", "--only", "leaf-index")


ID_ONLY_README = ("# widget\n\nVerified: {today}\n\n## Leaves\n\n"
                  "| id | Brief |\n| --- | --- |\n| `NN-01` |  |\n")


class IdOnlyTable(Base):
    """A table whose only identifier is `id` cannot index leaves, and says so once.

    An `id` cell is an identity, not a file name: resolving it as one reports the row's leaf as missing
    and the leaf as unindexed - two false findings replacing one true fact. The gate reports that the
    table cannot index leaves, naming the header it saw, and resolves no row from it.
    """

    def id_only(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "leaf_pattern": "^NN-\\d{2}"})
        self.tree.write("context/topics/widget/README.md", ID_ONLY_README)
        self.tree.write("context/topics/widget/NN-01-a.md", "---\nid: NN-01\nbrief: b\n---\n")

    def test_one_finding_and_neither_row_nor_leaf_is_reported(self) -> None:
        self.id_only()
        code, out = self.tree.run("check", "--only", "leaf-index")
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count("cannot index leaves"), 1, out)
        self.assertEqual(out.count("no such file"), 0, out)
        self.assertEqual(out.count("no row in"), 0, out)

    def test_the_finding_names_the_header_it_saw(self) -> None:
        self.id_only()
        code, out = self.tree.run("check", "--only", "leaf-index")
        self.assertEqual(code, 1, out)
        self.assertIn("id | Brief", out)

    def test_the_documented_column_order_still_indexes(self) -> None:
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\n"
                        "| id | Leaf | Brief |\n| --- | --- | --- |\n"
                        "| `L-0001` | `L-0001-widget.md` | what the rig measured |\n")
        self.assert_passes("check", "--only", "leaf-index")

    def test_a_header_with_no_id_still_passes(self) -> None:
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\n"
                        "| Leaf | What |\n| --- | --- |\n"
                        "| `L-0001-widget.md` | what the rig measured |\n")
        self.assert_passes("check", "--only", "leaf-index")

    def test_a_family_readme_of_id_only_reports_once(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "leaf_pattern": "^NN-\\d{2}"})
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\n"
                        "| id | Leaf | Brief |\n| --- | --- | --- |\n")
        self.tree.write("context/topics/widget/plan/README.md",
                        "# plan/\n\n| id | Brief |\n| --- | --- |\n| `NN-02` | the order |\n")
        self.tree.write("context/topics/widget/plan/NN-02-a.md", "---\nid: NN-02\nbrief: the order\n---\n")
        code, out = self.tree.run("check", "--only", "leaf-index")
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count("cannot index leaves"), 1, out)
        self.assertEqual(out.count("no such file"), 0, out)
        self.assertEqual(out.count("no row in"), 0, out)

    def test_shape_does_not_report_the_same_false_fact(self) -> None:
        self.id_only()
        code, out = self.tree.run("check", "--only", "shape")
        self.assertEqual(code, 0, out)
        self.assertNotIn("leaf row has no brief", out)

    def test_a_leaves_section_with_no_table_is_unchanged(self) -> None:
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\nprose, and no table.\n")
        self.assert_fails_with("no row in context/topics/widget/README.md", "check", "--only", "leaf-index")

    def test_briefs_reads_no_line_from_a_table_it_cannot_resolve(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "leaf_pattern": "^NN-\\d{2}",
                          "briefs": {"threshold": 0.6}})
        self.tree.write("context/topics/widget/README.md", ID_ONLY_README)
        self.tree.write("context/topics/widget/NN-01-a.md",
                        "---\nid: NN-01\nbrief: the rig measured 42 per second at batch sixteen\n---\n")
        self.tree.write("context/topics/widget/NN-02-b.md",
                        "---\nid: NN-02\nbrief: the rig measured 42 per second at batch twenty\n---\n")
        code, out = self.tree.run("check", "--only", "briefs")
        self.assertEqual(code, 1, out)
        self.assertIn("context/topics/widget/NN-02-b.md", out)
        self.assertNotIn("README.md:", out)


class Shape(Base):
    def test_leaf_without_brief(self) -> None:
        self.tree.write("context/topics/widget/L-0001-widget.md", "---\nid: L-0001\n---\nbody\n")
        self.assert_fails_with("no `brief:`", "check")

    def test_handoff_without_now(self) -> None:
        self.tree.write("context/topics/widget/HANDOFF.md", "# HANDOFF\n\n## State\n\nthe state\n")
        self.assert_fails_with('no "## Now" heading', "check")

    def test_memory_entry_on_two_lines(self) -> None:
        self.tree.write("context/MEMORY.md", "# MEMORY\n\n- a fact that keeps\n  going on\n")
        self.assert_fails_with("entry continues onto a second line", "check")

    def test_decision_row_without_id(self) -> None:
        self.tree.write("context/topics/widget/decisions.md",
                        "# decisions\n\n| id | Date | Decision | Why | Ruled out |\n"
                        "| --- | --- | --- | --- | --- |\n| 1 | today | x | y | z |\n")
        self.assert_fails_with("not a `D-####` id", "check")


class Caps(Base):
    def test_handoff_over_budget(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"],
                          "artefacts": {"HANDOFF.md": {"max_lines": 3}}})
        self.assert_fails_with("lines, max 3", "check")

    def test_fan_out_past_ten(self) -> None:
        rows = "".join("| `L-00%02d` | `L-00%02d-x.md` | brief %d |\n" % (i, i, i) for i in range(2, 13))
        self.tree.append("context/topics/widget/README.md", rows)
        for i in range(2, 13):
            self.tree.write("context/topics/widget/L-00%02d-x.md" % i,
                            "---\nid: L-00%02d\nbrief: brief %d\n---\n" % (i, i))
        self.assert_fails_with("fan-out is 10", "check")

    def test_leaf_over_budget(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "leaves": {"max_lines": 5}})
        self.assert_fails_with("lines, max 5", "check")


class Briefs(Base):
    def test_two_leaves_one_conclusion(self) -> None:
        self.tree.append("context/topics/widget/README.md",
                         "| `L-0002` | `L-0002-again.md` | what the rig measured |\n")
        self.tree.write("context/topics/widget/L-0002-again.md",
                        "---\nid: L-0002\nbrief: what the rig measured\n---\n")
        self.assert_fails_with("similar to L-0001", "check", "--all")

    def test_short_briefs_are_not_similar(self) -> None:
        self.tree.append("context/topics/widget/README.md",
                         "| `L-0002` | `L-0002-other.md` | why the floor moved |\n")
        self.tree.write("context/topics/widget/L-0002-other.md",
                        "---\nid: L-0002\nbrief: why the floor moved\n---\n")
        self.assert_passes("check", "--all")


class Pointers(Base):
    def test_dead_citation(self) -> None:
        self.tree.append("context/MEMORY.md", "\n- see `docs/runbook.md` for the rig\n")
        self.assert_fails_with('"docs/runbook.md" does not resolve', "check", "--all")

    def test_bare_names_are_prose(self) -> None:
        self.tree.append("context/MEMORY.md", "\n- see `HANDOFF.md` and `docs/` when in doubt\n")
        self.assert_passes("check", "--all")


class AcceptedAbsent(Base):
    """A gitignored directory and a home-relative path are permanent false findings without a list.

    The host this was measured on carries `repos/` and `state/` for real, `/`-anchored in `.gitignore`
    and so absent from every clone, plus two `~/` citations; the retired checker it replaced accepted
    32 entries and its summary printed how many it had accepted.
    """

    def cite(self, token: str) -> None:
        self.tree.append("context/MEMORY.md", "\n- see `" + token + "` for it\n")

    def configured(self, entries: list[str]) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "accepted_absent": entries})

    def test_a_prefix_entry_accepts_and_is_counted(self) -> None:
        self.configured(["repos/"])
        self.cite("repos/pvl-rentals/README.md")
        code, out = self.tree.run("check", "--only", "pointers")
        self.assertEqual(code, 0, out)
        self.assertIn("1 accepted absent", out)

    def test_a_glob_entry_accepts(self) -> None:
        self.configured(["reports/qa-*.md"])
        self.cite("reports/qa-2026-11.md")
        self.assert_passes("check", "--only", "pointers")

    def test_a_home_relative_path_needs_no_config(self) -> None:
        self.cite("~/.copilot/instructions/terminal-command-safety.instructions.md")
        self.cite("$HOME/.copilot/agents/reviewer.md")
        code, out = self.tree.run("check", "--only", "pointers")
        self.assertEqual(code, 0, out)
        self.assertIn("2 accepted absent", out)

    def test_a_citation_outside_the_list_still_fails(self) -> None:
        self.configured(["repos/"])
        self.cite("docs/runbook.md")
        self.assert_fails_with('"docs/runbook.md" does not resolve', "check", "--only", "pointers")

    def test_an_entry_that_matches_nothing_is_a_finding(self) -> None:
        self.configured(["repos/"])
        self.assert_fails_with('accepted_absent entry "repos/" matched no citation',
                               "check", "--only", "pointers")


class Installed(Base):
    def test_port_marker_survives(self) -> None:
        self.tree.append(".claude/rules/context.md", "\n<!-- PORT: context-rules -->\n")
        self.assert_fails_with("still contains", "check")

    def test_pointer_shell_to_a_missing_file(self) -> None:
        self.tree.write(".claude/rules/context.md",
                        "The rules for this tree are in `.github/nowhere.md`; read it before you write.\n")
        self.assert_fails_with("which does not resolve", "check")

    def test_missing_entry_block(self) -> None:
        self.tree.write("AGENTS.md", "# AGENTS.md\n\nno block here\n")
        self.assert_fails_with("no <!-- context:begin -->", "check")

    def test_nothing_to_check(self) -> None:
        self.tree.config({})
        (self.tree.root / "AGENTS.md").unlink()
        self.assert_fails_with("has not passed", "check", "--only", "installed")


class Ported(Base):
    def test_no_ported_line(self) -> None:
        self.tree.write(".claude/rules/context.md", "The routing table lives here.\n")
        self.assert_fails_with('no "ported:" line', "check", "--only", "ported")

    def test_zero_shells_passes_with_a_count(self) -> None:
        self.tree.config({})
        code, out = self.tree.run("check", "--only", "ported")
        self.assertEqual(code, 0, out)
        self.assertIn("0 shells configured", out)


class ShippedWorkflows(unittest.TestCase):
    """The workflows a host copies must be able to gate the merge they are copied to guard.

    Two lines are load-bearing and neither is visible in a review of a green run. A check-run is named by
    the job, so a job whose `name:` differs from the workflow's reports a check no branch protection
    requires - the pull request stays blocked forever. And the date gate reads each leaf's last commit,
    which a depth-1 clone cannot answer, so it reports the history as unavailable on every push. Both were
    missing from the adopter template shipped in 1.0.1, which is why they are measured rather than prose.
    """

    ROOT = Path(__file__).resolve().parents[1]
    WORKFLOWS = (".github/workflows/context.yml", "port/hooks/ci.yml")

    def read(self, name: str) -> str:
        path = self.ROOT / name
        self.assertTrue(path.is_file(), f"{name} is missing from the release")
        return path.read_text(encoding="utf-8")

    def job(self, name: str, text: str) -> tuple[str | None, str | None]:
        """(job id, its display name) for the single job under the top-level `jobs:` key."""
        lines = text.splitlines()
        starts = [i for i, line in enumerate(lines) if line.rstrip() == "jobs:"]
        self.assertEqual(len(starts), 1, f"{name}: expected exactly one top-level jobs: key")
        job_id = job_name = None
        for line in lines[starts[0] + 1:]:
            if not line.strip():
                continue
            if not line.startswith(" "):
                break
            indent = len(line) - len(line.lstrip())
            key, _, value = line.strip().partition(":")
            if indent == 2:
                job_id, job_name = key, None
            elif indent == 4 and key == "name":
                job_name = value.strip()
        return job_id, job_name

    def test_the_job_name_is_the_check_run_name(self) -> None:
        checked = 0
        for name in self.WORKFLOWS:
            text = self.read(name)
            workflow = re.search(r"(?m)^name:\s*(\S.*?)\s*$", text)
            self.assertIsNotNone(workflow, f"{name} has no top-level name:")
            job_id, job_name = self.job(name, text)
            self.assertIsNotNone(job_id, f"{name} has no job under jobs:")
            self.assertIsNotNone(job_name, f"{name}: job {job_id!r} has no name:, so the check-run is "
                                           f"named after the job id and never satisfies a required "
                                           f"status check named {workflow.group(1)!r}")
            self.assertEqual(job_name.strip("'\""), workflow.group(1).strip("'\""),
                             f"{name}: job {job_id!r} is named {job_name!r}, not the workflow's "
                             f"{workflow.group(1)!r}, so the required check never reports")
            checked += 1
        self.assertEqual(checked, len(self.WORKFLOWS),
                         f"only {checked} of {len(self.WORKFLOWS)} shipped workflows were read")

    def test_checkout_fetches_the_full_history(self) -> None:
        checked = 0
        for name in self.WORKFLOWS:
            text = self.read(name)
            self.assertIn("actions/checkout", text, f"{name} checks nothing out")
            self.assertRegex(text, r"(?m)^\s+fetch-depth:\s*['\"]?0\s*$",
                             f"{name}: checkout omits fetch-depth: 0, so a depth-1 clone dates no leaf "
                             f"and the date gate reports unavailable history on every push")
            checked += 1
        self.assertEqual(checked, len(self.WORKFLOWS),
                         f"only {checked} of {len(self.WORKFLOWS)} shipped workflows were read")


class LeafPattern(Base):
    """Leaf naming is a config value: a host that numbers its notes `01-name.md` had no leaves at all.

    Measured on the real host: `L-####-*.md` = 0, `NN-*.md` = 87, and `verified` printed
    `ok 11 dated topics, 0 leaves without history` - a green gate over an empty set.
    """

    def numbered(self) -> None:
        (self.tree.root / "context/topics/widget/L-0001-widget.md").unlink()
        self.tree.write("context/topics/widget/01-scheduler.md",
                        "---\nid: 01-scheduler\nbrief: what the batch size measured\n---\n")
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\n| Leaf | What it answers |\n"
                        "| --- | --- |\n| `01-scheduler.md` | what the batch size measured |\n")
        self.tree.git()

    def test_the_default_pattern_is_unchanged(self) -> None:
        self.assert_passes("check", "--all")

    def test_a_configured_pattern_finds_the_hosts_leaves(self) -> None:
        self.numbered()
        self.tree.config({"shells": [".claude/rules/context.md"], "leaf_pattern": "^\\d{2}-"})
        code, out = self.tree.run("check", "--only", "leaf-index", "--only", "verified")
        self.assertEqual(code, 0, out)
        self.assertIn("1 topics, 1 leaves", out)

    def test_nothing_matching_the_pattern_is_reported(self) -> None:
        self.numbered()
        code, out = self.tree.run("check", "--only", "verified")
        self.assertEqual(code, 0, out)
        self.assertIn('leaf_pattern "^L-\\d{4}" matches none of', out)
        self.assertIn("the leaf gates checked nothing", out)

    def test_a_broken_pattern_is_a_config_error(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "leaf_pattern": "("})
        code, out = self.tree.run("check", "--only", "verified")
        self.assertEqual(code, 2, out)
        self.assertIn("not a valid regular expression", out)


class Verified(Base):
    def test_stale_date(self) -> None:
        readme = self.tree.read("context/topics/widget/README.md").replace(TODAY, "2020-01-01")
        self.tree.write("context/topics/widget/README.md", readme)
        index = self.tree.read("context/topics/INDEX.md").replace(TODAY, "2020-01-01")
        self.tree.write("context/topics/INDEX.md", index)
        self.tree.git()
        self.assert_fails_with("days behind L-0001", "check", "--only", "verified")


class Liveness(Base):
    def test_empty_tree_fails_every_gate(self) -> None:
        self.tree.config({})
        self.tree.clear()
        for gate in ("register", "leaf-index", "shape", "caps"):
            code, out = self.tree.run("check", "--only", gate)
            self.assertEqual(code, 1, f"{gate} passed on an empty tree: {out}")
            self.assertIn("has not passed", out)

    def test_empty_but_present_tree_passes(self) -> None:
        """A location that exists and holds nothing yet is a count, not a defect.

        This is a fresh install before its first topic, and it is the state that made four
        blocking findings teach an operator to switch correct gates off.
        """
        self.tree.clear()
        topics = self.tree.root / "context" / "topics"
        topics.mkdir(parents=True)
        (topics / "INDEX.md").write_text("# Topic register\n", encoding="utf-8")
        self.tree.write("AGENTS.md", ENTRY)
        self.tree.config({})
        for gate in ("register", "leaf-index", "briefs", "verified"):
            code, out = self.tree.run("check", "--only", gate)
            self.assertEqual(code, 0, f"{gate} failed on an empty but present tree: {out}")
            self.assertIn("nothing here yet", out)

    def test_drained_topic_still_passes_briefs(self) -> None:
        """Drain archives the leaves; the gate counts topics, so finished work can go green."""
        (self.tree.root / "context/topics/widget/L-0001-widget.md").unlink()
        (self.tree.root / "context/topics/widget/HANDOFF.md").unlink()
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n## Leaves\n\n| id | Leaf | Brief - what it answers |\n"
                        "| --- | --- | --- |\n")
        self.tree.git()
        code, out = self.tree.run("check", "--only", "briefs")
        self.assertEqual(code, 0, out)
        self.assertIn("0 briefs in 1 topics", out)


class Archive(Base):
    """A drained topic's files live at context/archive/, outside every gate's scan."""

    def drain(self) -> None:
        root = self.tree.root
        archive = root / "context" / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        for name in ("L-0001-widget.md", "decisions.md", "JOURNEY.md"):
            source = root / "context" / "topics" / "widget" / name
            if source.exists():
                (archive / f"widget-{name}").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
                source.unlink()
        (root / "context/topics/widget/HANDOFF.md").unlink()
        self.tree.write("context/topics/widget/README.md",
                        "# widget\n\nVerified: {today}\n\n> shim: the work moved to `context/MEMORY.md`.\n\n"
                        "## Leaves\n\n| id | Leaf | Brief - what it answers |\n| --- | --- | --- |\n")
        self.tree.git()

    def test_archive_at_the_root_passes_every_gate(self) -> None:
        self.drain()
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 0, out)
        self.assertIn("0 blocking findings", out)

    def test_archive_inside_topics_is_a_finding(self) -> None:
        """The failure the default location exists to prevent: an archive under topics/ reads as a topic."""
        self.drain()
        misplaced = self.tree.root / "context" / "topics" / "archive"
        misplaced.mkdir()
        (misplaced / "widget-L-0001-widget.md").write_text(LEAF, encoding="utf-8")
        self.tree.git()
        code, out = self.tree.run("check")
        self.assertEqual(code, 1, out)
        self.assertIn("context/topics/archive: folder has no row", out)
        self.assertIn("context/topics/archive: topic has no README.md", out)


class ExtraChecks(Base):
    """A host attaches its own rules through `extra_checks`; the published tool rejected the key outright.

    Measured on the real host: three unique rules (`shell_checks:refs`, `:one_home`, `:briefing_current`)
    were refused as gate names, so the coverage its retired checker was retired *into* became unreachable.
    """

    def module(self, source: str) -> None:
        path = self.tree.root / "scripts" / "host_checks.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")

    def configured(self, *specs: str) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "extra_checks": list(specs)})

    def test_a_host_check_reports_under_its_own_name(self) -> None:
        self.module('def policy(root, cfg):\n'
                    '    return [{"message": "policy.md is missing", "rel": "docs/policy.md", "line": 3}]\n')
        self.configured("host_checks:policy")
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 1, out)
        self.assertIn("extra:host_checks.policy", out)
        self.assertIn("docs/policy.md:3: policy.md is missing", out)

    def test_plain_strings_are_accepted(self) -> None:
        self.module('def shallow(root, cfg):\n    return ["a plain sentence"]\n')
        self.configured("host_checks:shallow")
        self.assert_fails_with("a plain sentence", "check", "--all")

    def test_a_clean_check_raises_the_denominator(self) -> None:
        self.module('def clean(root, cfg):\n    return []\n')
        self.configured("host_checks:clean")
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 0, out)
        self.assertIn("extra:host_checks.clean", out)
        self.assertIn("10 of 10 gates ran", out)

    def test_it_runs_only_with_all(self) -> None:
        self.module('def clean(root, cfg):\n    return ["should not run"]\n')
        self.configured("host_checks:clean")
        code, out = self.tree.run("check")
        self.assertEqual(code, 0, out)
        self.assertNotIn("extra:", out)
        self.assertIn("5 of 9 gates ran", out)

    def test_zero_extras_keeps_the_denominator(self) -> None:
        self.configured()
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 0, out)
        self.assertIn("9 of 9 gates ran", out)

    def test_a_missing_module_is_a_finding_not_a_traceback(self) -> None:
        self.configured("nowhere:policy")
        self.assert_fails_with('no "nowhere" module under scripts/', "check", "--all")

    def test_a_missing_function_is_a_finding(self) -> None:
        self.module('def other(root, cfg):\n    return []\n')
        self.configured("host_checks:policy")
        self.assert_fails_with('has no callable "policy"', "check", "--all")

    def test_a_raising_function_is_a_finding(self) -> None:
        self.module('def boom(root, cfg):\n    raise ValueError("spec broke")\n')
        self.configured("host_checks:boom")
        self.assert_fails_with("raised ValueError: spec broke", "check", "--all")

    def test_a_spec_without_a_function_is_a_config_error(self) -> None:
        self.configured("host_checks")
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 2, out)
        self.assertIn('is not "module:function"', out)


class InstallProof(Base):
    """`check --only installed` is the runbook's install proof, so a legacy config may not preempt it.

    Measured on the real host: seven `is not a gate this tool has` errors and exit 2 for `--all` **and**
    for `--only installed` - the command ADOPT step 6 tells an adopter to run.
    """

    def legacy(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"],
                          "checks_advisory": ["budget", "journey"],
                          "checks_disabled": ["leaves"],
                          "extra_checks": ["shell_checks:refs"]})

    def test_only_installed_runs_despite_unknown_names(self) -> None:
        self.legacy()
        code, out = self.tree.run("check", "--only", "installed")
        self.assertEqual(code, 0, out)
        self.assertIn("installed    ok", out)

    def test_the_ignored_names_are_printed_not_swallowed(self) -> None:
        self.legacy()
        code, out = self.tree.run("check", "--only", "installed")
        self.assertEqual(code, 0, out)
        self.assertIn("note:", out)
        self.assertIn('"budget" is not a gate this tool has', out)

    def test_any_other_invocation_keeps_todays_strictness(self) -> None:
        self.legacy()
        code, out = self.tree.run("check")
        self.assertEqual(code, 2, out)
        self.assertIn("error:", out)

    def test_a_bom_encoded_config_is_read(self) -> None:
        path = self.tree.root / "context.config.json"
        payload = {"shells": [".claude/rules/context.md"]}
        path.write_bytes(b"\xef\xbb\xbf" + json.dumps(payload).encode("utf-8"))
        self.assert_passes("check")


class Cli(Base):
    def test_unknown_gate_exits_two(self) -> None:
        code, out = self.tree.run("check", "--only", "registr")
        self.assertEqual(code, 2, out)
        self.assertIn("unknown gate", out)
        self.assertIn("known gates", out)

    def test_disabled_gate_cannot_be_asked_for(self) -> None:
        self.tree.config({"checks_disabled": ["installed"]})
        code, out = self.tree.run("check", "--only", "installed")
        self.assertEqual(code, 2, out)
        self.assertIn("disabled", out)

    def test_unknown_name_in_config_exits_two(self) -> None:
        self.tree.config({"checks_advisory": ["shappe"]})
        code, out = self.tree.run("check")
        self.assertEqual(code, 2, out)
        self.assertIn("not a gate this tool has", out)

    def test_warn_exits_zero_with_the_same_finding(self) -> None:
        self.tree.append("context/topics/INDEX.md",
                         "| `context/topics/pricing/` | pricing | {today} |\n")
        code, out = self.tree.run("check", "--all", "--warn")
        self.assertEqual(code, 0, out)
        self.assertIn("no such folder", out)

    def test_advisory_prints_and_does_not_block(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "checks_advisory": ["register"]})
        self.tree.append("context/topics/INDEX.md",
                         "| `context/topics/pricing/` | pricing | {today} |\n")
        code, out = self.tree.run("check")
        self.assertEqual(code, 0, out)
        self.assertIn("1 advisory", out)

    def test_json_is_parseable(self) -> None:
        code, out = self.tree.run("check", "--all", "--json")
        self.assertEqual(code, 0, out)
        payload = json.loads(out)
        self.assertEqual(payload["exit"], 0)
        self.assertEqual(len(payload["gates"]), 9)
        self.assertEqual(payload["gates"][0]["gate"], "installed")

    def test_disabled_names_are_echoed(self) -> None:
        self.tree.config({"shells": [".claude/rules/context.md"], "checks_disabled": ["ported"]})
        code, out = self.tree.run("check", "--all")
        self.assertEqual(code, 0, out)
        self.assertIn("disabled: ported", out)

    def test_installed_cannot_be_skipped(self) -> None:
        code, out = self.tree.run("check", "--skip", "installed")
        self.assertEqual(code, 2, out)
        self.assertIn("cannot be skipped", out)

    def test_partial_run_declares_the_full_denominator(self) -> None:
        code, out = self.tree.run("check", "--only", "register")
        self.assertEqual(code, 0, out)
        self.assertIn("2 of 9 gates ran", out)


class BriefStub(Base):
    """`brief` is the command a session-start hook calls, so it must not fail the session.

    It has no renderer behind it. A missing subcommand exits 2 with an argparse error, which a hook
    reports as a broken session; a stub that says what it is does not.
    """

    def files(self) -> list[str]:
        return sorted(path.relative_to(self.tree.root).as_posix()
                      for path in self.tree.root.rglob("*") if path.is_file())

    def test_brief_exits_zero_and_says_it_is_not_implemented(self) -> None:
        code, out = self.tree.run("brief")
        self.assertEqual(code, 0, out)
        self.assertIn("not implemented yet", out)
        self.assertIn("no digest was written", out)

    def test_brief_writes_nothing(self) -> None:
        before = self.files()
        self.tree.run("brief")
        self.assertEqual(before, self.files(), "brief changed the tree")

    def test_brief_accepts_check_without_writing(self) -> None:
        before = self.files()
        code, out = self.tree.run("brief", "--check")
        self.assertEqual(code, 0, out)
        self.assertIn("not implemented yet", out)
        self.assertEqual(before, self.files(), "brief --check changed the tree")

    def test_an_unknown_command_still_exits_two(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            self.tree.run("briefing")
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
