#!/usr/bin/env python3
"""contextctl - the gate runner for an agent-context tree.

Built to GATES.md. It reads and reports; it never writes, moves or deletes a file,
because draining a topic, trimming a leaf and retiring a family are judgements no
script makes. A run leaves the repository byte-identical.

    python scripts/contextctl.py check            # the four default gates
    python scripts/contextctl.py check --all      # plus the four opt-in gates
    python scripts/contextctl.py check --all --warn
    python scripts/contextctl.py check --only register --only leaf-index

Exit codes: 0 no blocking finding, 1 blocking findings, 2 usage or config error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

FAN_OUT = 10
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERIFIED_RE = re.compile(r"(?m)^\s*Verified:\s*(\d{4}-\d{2}-\d{2})")
LEAF_FILE = re.compile(r"^(L-\d{4})-")
DECISION_RE = re.compile(r"^D-\d{4}$")
RULE_START = re.compile(r"^(?:[-*+]|\d+\.)\s+\S")
BACKTICK = re.compile(r"`([^`\n]+)`")
PORT_MARKER = re.compile(r"<!--\s*PORT:[^>]*-->")
PORTED = re.compile(r"(?m)^\s*(?:<!--\s*)?ported:\s*(\d{4}-\d{2}-\d{2})")
POINTER = re.compile(r"The rules for this tree are in\s+`([^`]+)`")
HEADING = re.compile(r"^##\s+(.*?)\s*$")
PATH_SUFFIXES = (".md", ".py", ".json", ".yml", ".yaml", ".sh", ".ps1", ".toml", ".txt")

DEFAULTS = {
    "memory": "context/MEMORY.md",
    "root_rules": "context/MUST-KNOW.md",
    "index_of_topics": "context/topics/INDEX.md",
    "topics_dir": "context/topics",
    "entry_file": "AGENTS.md",
    "shells": [],
    "port_target": None,
    "checks_disabled": [],
    "checks_advisory": [],
    "extra_checks": [],
    "leaves": {"max_lines": 120},
    "briefs": {"threshold": 0.82},
    "artefacts": {
        "README.md": {"max_lines": 80,
                      "over": "move the detail to a leaf and let the entry name it"},
        "HANDOFF.md": {"max_lines": 90, "requires": ["## Now"],
                       "over": "move the history to JOURNEY.md and rewrite the snapshot"},
        "MUST-KNOW.md": {"max_rules": 25, "max_rule_chars": 640,
                         "over": "distil the weakest rule away; a rule that never prevented a mistake is not one"},
        "JOURNEY.md": {},
        "decisions.md": {},
    },
    "root_artefacts": {
        "MEMORY.md": {"max_lines": 150,
                      "over": "demote the prose to a leaf and leave its pointer here"},
        "MUST-KNOW.md": {"max_rules": 10, "max_rule_chars": 640,
                         "over": "prune; the cap is ten because the first rule is the one that costs most"},
    },
}


# --------------------------------------------------------------------------- config


def merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for key, value in (over or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge(out[key], value)
        else:
            out[key] = value
    return out


def known_names() -> list[str]:
    """Registry order, with the install precondition first: the order a run prints."""
    return ["installed"] + [name for name, _, _ in CHECKS]


def load_config(root: Path, explicit: str | None) -> tuple[dict, list[str]]:
    """Return the merged config and any complaint about a name it mentions."""
    path = Path(explicit) if explicit else root / "context.config.json"
    raw = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    cfg = merge(DEFAULTS, raw)
    for key in ("artefacts", "root_artefacts"):
        cfg[key] = {name: spec for name, spec in cfg[key].items() if spec is not None}
    problems = []
    known = set(known_names())
    for key in ("checks_disabled", "checks_advisory", "extra_checks"):
        for name in cfg.get(key) or []:
            if name not in known:
                problems.append(f'{key}: "{name}" is not a gate this tool has')
    return cfg, problems


# --------------------------------------------------------------------------- model


@dataclass(frozen=True)
class Finding:
    gate: str
    path: str
    line: int | None
    message: str

    def render(self) -> str:
        where = self.path if self.line is None else f"{self.path}:{self.line}"
        return f"  {where}: {self.message}"


@dataclass
class Result:
    gate: str
    findings: list[Finding]
    count: int
    detail: str
    advisory: bool = False


@dataclass
class Leaf:
    path: Path
    rel: str
    id: str
    brief: str
    lines: list[str]


@dataclass
class Topic:
    name: str
    dir: Path
    readme: Path
    families: list[Path] = field(default_factory=list)


def table_rows(lines: list[str]) -> list[tuple[int, list[str]]]:
    """Body rows of every markdown table; header and separator lines dropped."""
    rows = []
    for number, raw in enumerate(lines, 1):
        text = raw.strip()
        if not text.startswith("|"):
            continue
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells if cell):
            continue
        if cells and cells[0].strip("`").lower() in ("id", "topic", "what"):
            continue
        rows.append((number, cells))
    return rows


def section_rows(lines: list[str], heading: str) -> list[tuple[int, list[str]]]:
    """Body rows of the table inside one `## heading`, with real line numbers."""
    start = None
    for index, raw in enumerate(lines):
        match = HEADING.match(raw)
        if match and f"## {match.group(1)}" == heading:
            start = index + 1
            break
    if start is None:
        return []
    end = len(lines)
    for index in range(start, len(lines)):
        if HEADING.match(lines[index]):
            end = index
            break
    offset = start
    return [(number + offset, cells) for number, cells in table_rows(lines[start:end])]


def rule_blocks(lines: list[str]) -> list[tuple[int, list[str]]]:
    """Top-level list items with their indented continuation lines."""
    blocks: list[tuple[int, list[str]]] = []
    current = None
    for number, raw in enumerate(lines, 1):
        if RULE_START.match(raw) and not raw[:1].isspace():
            current = [raw]
            blocks.append((number, current))
        elif current is not None and raw.strip() and raw[:1].isspace():
            current.append(raw)
        elif not raw.strip():
            current = None
    return blocks


def parse_leaf(text: str) -> tuple[str, str]:
    """`id` and `brief` from a leaf: frontmatter first, then the first lines."""
    lines = text.splitlines()
    body = lines
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                body = lines[1:index]
                break
    found: dict[str, str] = {}
    for raw in body:
        match = re.match(r"^(id|brief):\s*(.*?)\s*$", raw)
        if match and match.group(1) not in found:
            found[match.group(1)] = match.group(2)
    return found.get("id", ""), found.get("brief", "")


class Ctx:
    def __init__(self, root: Path, cfg: dict):
        self.root = root
        self.cfg = cfg
        self.tree_root = (root / cfg["memory"]).parent
        self.topics_dir = root / cfg["topics_dir"]
        self.topics = self._topics()
        self.leaves = self._leaves()

    def _topics(self) -> list[Topic]:
        if not self.topics_dir.is_dir():
            return []
        topics = []
        for entry in sorted(self.topics_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            families = sorted(p for p in entry.iterdir() if p.is_dir() and (p / "README.md").exists())
            topics.append(Topic(entry.name, entry, entry / "README.md", families))
        return topics

    def _leaves(self) -> list[Leaf]:
        leaves = []
        for path in sorted(self.topics_dir.rglob("L-*.md")):
            if not LEAF_FILE.match(path.name):
                continue
            text = self.read(path) or ""
            ident, brief = parse_leaf(text)
            leaves.append(Leaf(path, self.rel(path), ident, brief, text.splitlines()))
        return leaves

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def read(self, path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None

    def topics_of(self, topic: Topic) -> list[Leaf]:
        return [leaf for leaf in self.leaves if topic.dir in leaf.path.parents]


def topic_verified(readme: Path) -> str:
    try:
        text = readme.read_text(encoding="utf-8")
    except OSError:
        return ""
    match = VERIFIED_RE.search(text)
    return match.group(1) if match else ""


def zero(gate: str, where: str, what: str, exists: bool = True) -> Result:
    """Zero subjects, reported rather than silently passed.

    The liveness rule exists because a gate that scanned nothing used to print OK. Reporting the
    count is that rule; failing the run is right only when the reason is a misconfiguration. So an
    absent location blocks - the config points where the tree has nothing - while a location that
    exists and is legitimately empty passes with its count printed: a fresh install before its first
    topic, a drained topic whose leaves have been archived. Neither case is silent, and neither
    teaches an operator to switch a correct gate off.
    """
    if exists:
        return Result(gate, [], 0, f"0 {what} - nothing here yet")
    return Result(gate, [Finding(gate, where, None,
                                 f"0 {what}; that location does not exist, and a gate that scanned "
                                 f"nothing has not passed")], 0, f"0 {what}")


# ---------------------------------------------------------------------- the gates


def gate_register(ctx: Ctx) -> Result:
    gate = "register"
    index = ctx.root / ctx.cfg["index_of_topics"]
    folders = {topic.name: topic for topic in ctx.topics}
    text = ctx.read(index)
    rows = []
    findings = []
    if text is None:
        findings.append(Finding(gate, ctx.rel(index), None, "register file not found"))
    else:
        for number, cells in table_rows(text.splitlines()):
            raw = cells[0].strip("`").strip()
            name = raw.rstrip("/").split("/")[-1]
            when = cells[-1].strip("`") if len(cells) > 1 else ""
            rows.append((number, name, raw, when))
    for number, name, raw, when in rows:
        if name not in folders:
            findings.append(Finding(gate, ctx.rel(index), number, f'row names "{raw}", no such folder'))
            continue
        verified = topic_verified(folders[name].readme)
        if when and verified and when != verified:
            findings.append(Finding(gate, ctx.rel(index), number,
                                    f"row date {when} differs from {name}/README.md Verified: {verified}"))
    seen: dict[str, list[int]] = {}
    for number, name, _, _ in rows:
        seen.setdefault(name, []).append(number)
    for name, numbers in seen.items():
        if len(numbers) > 1:
            findings.append(Finding(gate, ctx.rel(index), numbers[1], f'duplicate rows for "{name}"'))
    for name, topic in sorted(folders.items()):
        if name not in seen:
            findings.append(Finding(gate, ctx.rel(topic.dir), None, "folder has no row; add one dated row"))
    count = len(rows) + len(folders)
    if count == 0:
        return zero(gate, ctx.rel(index), "rows and folders", ctx.topics_dir.is_dir())
    return Result(gate, findings, count, f"{len(folders)} folders, {len(rows)} rows")


def gate_leaf_index(ctx: Ctx) -> Result:
    gate = "leaf-index"
    findings = []
    scanned = 0
    for topic in ctx.topics:
        if not topic.readme.exists():
            findings.append(Finding(gate, ctx.rel(topic.dir), None,
                                    "topic has no README.md, so nothing indexes it"))
            continue
        indexes = [topic.readme] + [family / "README.md" for family in topic.families]
        for index in indexes:
            scanned += 1
            lines = (ctx.read(index) or "").splitlines()
            rows = section_rows(lines, "## Leaves") if index == topic.readme else table_rows(lines)
            listed = []
            for number, cells in rows:
                if len(cells) < 2:
                    continue
                leaf_name = cells[1].strip("`").strip()
                listed.append(leaf_name)
                if not (index.parent / leaf_name).exists():
                    findings.append(Finding(gate, ctx.rel(index), number,
                                            f'row names "{leaf_name}", no such file'))
            for leaf in ctx.leaves:
                if leaf.path.parent == index.parent and leaf.path.name not in listed:
                    findings.append(Finding(gate, leaf.rel, None, f"no row in {ctx.rel(index)}"))
        for family in sorted(p for p in topic.dir.iterdir() if p.is_dir()):
            owned = [p for p in family.glob("L-*.md") if LEAF_FILE.match(p.name)]
            if owned and not (family / "README.md").exists():
                for leaf in owned:
                    findings.append(Finding(gate, ctx.rel(leaf), None,
                                            f"leaf sits in {ctx.rel(family)}/, which has no README.md"))
    if scanned == 0:
        return zero(gate, ctx.rel(ctx.topics_dir), "topic READMEs", ctx.topics_dir.is_dir())
    return Result(gate, findings, scanned, f"{len(ctx.topics)} topics, {len(ctx.leaves)} leaves")


def gate_shape(ctx: Ctx) -> Result:
    gate = "shape"
    findings = []
    examined = 0
    for leaf in ctx.leaves:
        examined += 1
        match = LEAF_FILE.match(leaf.path.name)
        if not leaf.id:
            findings.append(Finding(gate, leaf.rel, 1,
                                    "no `id: L-####` in the frontmatter or the first two lines"))
        elif match and leaf.id != match.group(1):
            findings.append(Finding(gate, leaf.rel, 1,
                                    f"id {leaf.id} does not match the file name ({match.group(1)})"))
        if not leaf.brief:
            findings.append(Finding(gate, leaf.rel, 2,
                                    "no `brief:`; the index cannot say what this leaf answers"))
    for topic in ctx.topics:
        handoff = topic.dir / "HANDOFF.md"
        if handoff.exists():
            examined += 1
            if not re.search(r"(?m)^##\s+Now\s*$", ctx.read(handoff) or ""):
                findings.append(Finding(gate, ctx.rel(handoff), None,
                                        'no "## Now" heading; the next session has no first action'))
        readme = ctx.read(topic.readme)
        if readme is not None:
            examined += 1
            for number, cells in section_rows(readme.splitlines(), "## Leaves"):
                if len(cells) < 3 or not cells[2].strip("`").strip():
                    findings.append(Finding(gate, ctx.rel(topic.readme), number,
                                            "leaf row has no brief; the table exists so the leaf stays shut"))
        decisions = topic.dir / "decisions.md"
        if decisions.exists():
            examined += 1
            for number, cells in table_rows((ctx.read(decisions) or "").splitlines()):
                ident = cells[0].strip("`").strip()
                if not DECISION_RE.match(ident):
                    findings.append(Finding(gate, ctx.rel(decisions), number,
                                            f'row starts with "{ident}", not a `D-####` id'))
    memory = ctx.tree_root / "MEMORY.md"
    if memory.exists():
        examined += 1
        lines = (ctx.read(memory) or "").splitlines()
        for index, raw in enumerate(lines):
            if not RULE_START.match(raw) or raw[:1].isspace():
                continue
            after = index + 1
            if (after < len(lines) and lines[after].strip() and lines[after][:1].isspace()
                    and not RULE_START.match(lines[after])):
                findings.append(Finding(gate, ctx.rel(memory), index + 1,
                                        "entry continues onto a second line; a fact is one line, its body is a leaf"))
    index_file = ctx.root / ctx.cfg["index_of_topics"]
    if index_file.exists():
        examined += 1
        for number, cells in table_rows((ctx.read(index_file) or "").splitlines()):
            when = cells[-1].strip("`") if len(cells) > 1 else ""
            if not DATE_RE.match(when):
                findings.append(Finding(gate, ctx.rel(index_file), number,
                                        f'row has no date ({when or "empty"}); expected YYYY-MM-DD'))
    if examined == 0:
        return zero(gate, ctx.rel(ctx.tree_root), "files", ctx.tree_root.is_dir())
    return Result(gate, findings, examined, f"{examined} files")


def gate_caps(ctx: Ctx) -> Result:
    gate = "caps"
    findings = []
    examined = 0

    def check(path: Path, spec: dict) -> None:
        nonlocal examined
        if not spec or not path.exists():
            return
        examined += 1
        lines = (ctx.read(path) or "").splitlines()
        budget = spec.get("max_lines")
        if budget and len(lines) > budget:
            findings.append(Finding(gate, ctx.rel(path), None,
                                    f"{len(lines)} lines, max {budget}; {spec.get('over', 'trim it')}"))
        budget = spec.get("max_rules")
        if budget:
            blocks = rule_blocks(lines)
            if len(blocks) > budget:
                findings.append(Finding(gate, ctx.rel(path), None,
                                        f"{len(blocks)} rules, max {budget}; {spec.get('over', 'prune')}"))
            longest = spec.get("max_rule_chars")
            if longest:
                for number, block in blocks:
                    size = sum(len(part) for part in block)
                    if size > longest:
                        findings.append(Finding(gate, ctx.rel(path), number,
                                                f"rule is {size} characters, max {longest}"))
    for topic in ctx.topics:
        for name, spec in ctx.cfg["artefacts"].items():
            check(topic.dir / name, spec)
        readme = ctx.read(topic.readme)
        if readme is not None:
            rows = section_rows(readme.splitlines(), "## Leaves")
            if len(rows) > FAN_OUT:
                findings.append(Finding(gate, ctx.rel(topic.readme), None,
                                        f"{len(rows)} leaves, fan-out is {FAN_OUT}; add a family index and group within it"))
    budget = int(ctx.cfg["leaves"]["max_lines"])
    for leaf in ctx.leaves:
        examined += 1
        if len(leaf.lines) > budget:
            findings.append(Finding(gate, leaf.rel, None,
                                    f"{len(leaf.lines)} lines, max {budget}; a leaf is a conclusion, not a diary"))
    for name, spec in ctx.cfg["root_artefacts"].items():
        check(ctx.tree_root / name, spec)
    if examined == 0:
        return zero(gate, ctx.rel(ctx.tree_root), "artefacts", ctx.tree_root.is_dir())
    return Result(gate, findings, examined, f"{examined} artefacts")


def gate_briefs(ctx: Ctx) -> Result:
    gate = "briefs"
    threshold = float(ctx.cfg["briefs"]["threshold"])
    findings = []
    briefs = 0
    for topic in ctx.topics:
        lines = (ctx.read(topic.readme) or "").splitlines()
        row_line = {}
        for number, cells in section_rows(lines, "## Leaves"):
            if len(cells) >= 2:
                row_line[cells[1].strip("`").strip()] = number
        own = [leaf for leaf in ctx.topics_of(topic) if leaf.brief]
        briefs += len(own)
        for index, first in enumerate(own):
            for second in own[index + 1:]:
                ratio = SequenceMatcher(None, first.brief.lower(), second.brief.lower()).ratio()
                if ratio < threshold:
                    continue
                number = row_line.get(second.path.name)
                where = ctx.rel(topic.readme) if number else second.rel
                findings.append(Finding(gate, where, number,
                                        f"brief of {second.id or second.path.stem} is {ratio:.2f} similar to "
                                        f"{first.id or first.path.stem}; one conclusion, two leaves?"))
    if not ctx.topics:
        return zero(gate, ctx.rel(ctx.topics_dir), "topics", ctx.topics_dir.is_dir())
    return Result(gate, findings, len(ctx.topics), f"{briefs} briefs in {len(ctx.topics)} topics")


def git_date(root: Path, rel: str) -> str | None:
    try:
        done = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cs", "--", rel],
                              capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    out = done.stdout.strip()
    return out if DATE_RE.match(out) else None


def gate_verified(ctx: Ctx) -> Result:
    gate = "verified"
    findings = []
    scanned = 0
    undated = 0
    for topic in ctx.topics:
        verified = topic_verified(topic.readme)
        if not verified:
            continue
        scanned += 1
        newest = None
        newest_leaf = None
        for leaf in ctx.topics_of(topic):
            when = git_date(ctx.root, leaf.rel)
            if when is None:
                undated += 1
                continue
            if newest is None or when > newest:
                newest, newest_leaf = when, leaf
        if newest and newest > verified:
            days = (date.fromisoformat(newest) - date.fromisoformat(verified)).days
            findings.append(Finding(gate, ctx.rel(topic.readme), None,
                                    f"Verified: {verified}, {days} days behind "
                                    f"{newest_leaf.id or newest_leaf.path.stem} ({newest})"))
    if scanned == 0:
        return zero(gate, ctx.rel(ctx.topics_dir), "dated topics")
    if findings == [] and undated and undated == len(ctx.leaves):
        findings.append(Finding(gate, ctx.rel(ctx.tree_root), None,
                                f"git history unavailable for all {undated} leaves, so no date was checked"))
    return Result(gate, findings, scanned, f"{scanned} dated topics, {undated} leaves without history")


def path_like(token: str) -> bool:
    """A citation is a relative path with a file suffix; a bare name is prose."""
    if any(ch in token for ch in "*{}<> :|") or "://" in token:
        return False
    if token.startswith("#") or token.startswith("-") or "/" not in token:
        return False
    last = token.rstrip("/").split("/")[-1]
    return last.lower().endswith(PATH_SUFFIXES)


def resolves(ctx: Ctx, source: Path, token: str) -> bool:
    token = token.strip().strip("`").split("#")[0]
    if not token:
        return True
    bases = [ctx.tree_root, ctx.tree_root.parent, source.parent, ctx.root]
    return any((base / token).exists() for base in bases)


def gate_pointers(ctx: Ctx) -> Result:
    gate = "pointers"
    findings = []
    tokens = 0
    files = [ctx.root / ctx.cfg["memory"], ctx.root / ctx.cfg["root_rules"],
             ctx.root / ctx.cfg["entry_file"]] + [topic.readme for topic in ctx.topics]
    for path in files:
        text = ctx.read(path)
        if text is None:
            continue
        for number, raw in enumerate(text.splitlines(), 1):
            for token in BACKTICK.findall(raw):
                if not path_like(token):
                    continue
                tokens += 1
                if not resolves(ctx, path, token):
                    findings.append(Finding(gate, ctx.rel(path), number, f'"{token}" does not resolve'))
    if tokens == 0:
        return zero(gate, ctx.rel(ctx.tree_root), "cited paths", ctx.tree_root.is_dir())
    return Result(gate, findings, tokens, f"{tokens} cited paths in {len(files)} files")


def gate_ported(ctx: Ctx) -> Result:
    gate = "ported"
    findings = []
    shells = [ctx.root / name for name in ctx.cfg["shells"]]
    for shell in shells:
        text = ctx.read(shell)
        if text is None:
            findings.append(Finding(gate, ctx.rel(shell), None, "named in shells, absent"))
        elif not PORTED.search(text):
            findings.append(Finding(gate, ctx.rel(shell), None,
                                    'no "ported:" line; nothing dates this copy against the block'))
    if not shells:
        return Result(gate, [], 0, "0 shells configured")
    return Result(gate, findings, len(shells), f"{len(shells)} shells")


def gate_installed(ctx: Ctx) -> Result:
    gate = "installed"
    findings = []
    shells = [ctx.root / name for name in ctx.cfg["shells"]]
    for shell in shells:
        text = ctx.read(shell)
        if text is None:
            findings.append(Finding(gate, ctx.rel(shell), None, "named in shells, absent"))
            continue
        marker = PORT_MARKER.search(text)
        if marker:
            number = text[:marker.start()].count("\n") + 1
            findings.append(Finding(gate, ctx.rel(shell), number,
                                    f'still contains "{marker.group(0)}"; the routing table never reached the agent'))
        pointer = POINTER.search(text)
        if pointer and not resolves(ctx, shell, pointer.group(1)):
            findings.append(Finding(gate, ctx.rel(shell), None,
                                    f'pointer names "{pointer.group(1)}", which does not resolve'))
    entry = ctx.root / ctx.cfg["entry_file"]
    text = ctx.read(entry)
    if text is None:
        findings.append(Finding(gate, ctx.rel(entry), None, "entry file not found"))
    elif "<!-- context:begin -->" not in text or "<!-- context:end -->" not in text:
        findings.append(Finding(gate, ctx.rel(entry), None,
                                "no <!-- context:begin --> ... <!-- context:end --> block"))
    if not shells and text is None:
        return zero(gate, ctx.rel(ctx.root), "shells and entry file", entry.exists())
    present = bool(text) and "<!-- context:begin -->" in text
    return Result(gate, findings, len(shells) + 1,
                  f"{len(shells)} shells filled, entry block {'present' if present else 'missing'}")


CHECKS = [
    ("register", gate_register, "default"),
    ("leaf-index", gate_leaf_index, "default"),
    ("shape", gate_shape, "default"),
    ("caps", gate_caps, "default"),
    ("briefs", gate_briefs, "opt-in"),
    ("verified", gate_verified, "opt-in"),
    ("pointers", gate_pointers, "opt-in"),
    ("ported", gate_ported, "opt-in"),
]
GATES = {name: fn for name, fn, _ in CHECKS}


# ---------------------------------------------------------------------------- cli


def select(cfg: dict, args) -> tuple[list[str], list[str]]:
    disabled = list(cfg["checks_disabled"])
    if args.only:
        refused = [name for name in args.only if name in disabled]
        if refused:
            raise SystemExit(f'error: {", ".join(refused)} is disabled in context.config.json')
        chosen = ["installed"] + [name for name in args.only if name != "installed"]
    elif args.all:
        chosen = known_names()
    else:
        chosen = ["installed"] + [name for name, _, kind in CHECKS if kind == "default"]
    if args.skip:
        if "installed" in args.skip:
            raise SystemExit("error: installed runs on every invocation and cannot be skipped; "
                             "disable it in checks_disabled with the reason recorded")
        chosen = [name for name in chosen if name not in args.skip]
    return [name for name in chosen if name not in disabled], disabled


def command_brief() -> int:
    """`brief` is a stub: the shape a hook needs, with no renderer behind it."""
    print("brief: not implemented yet - this release ships the gates only, so no digest was written "
          "and none was compared.", file=sys.stderr)
    print("The command exists so a session-start hook has something real to call; until a renderer "
          "exists the register is the copy.", file=sys.stderr)
    print("Exit 0 is deliberate: a hook that failed here would block the session it is starting. "
          "`--check` is accepted and changes nothing.", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="contextctl",
                                     description="Run the gates in GATES.md over an agent-context tree.")
    parser.add_argument("command", nargs="?", default="check", choices=["check", "brief"],
                        help="check (default) runs the gates; brief is a stub that writes nothing")
    parser.add_argument("--all", action="store_true", help="run the opt-in gates too")
    parser.add_argument("--only", action="append", metavar="GATE", help="run only this gate (repeatable)")
    parser.add_argument("--skip", action="append", metavar="GATE", help="leave this gate out (repeatable)")
    parser.add_argument("--warn", action="store_true", help="print every finding and exit 0")
    parser.add_argument("--root", default=None, help="tree root (default: current directory)")
    parser.add_argument("--config", default=None, help="path to context.config.json")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--check", action="store_true",
                        help="with brief: compare instead of writing (accepted; brief is a stub)")
    args = parser.parse_args(argv)

    if args.command == "brief":
        return command_brief()

    root = Path(args.root).resolve() if args.root else Path.cwd().resolve()
    try:
        cfg, problems = load_config(root, args.config)
    except json.JSONDecodeError as error:
        print(f"error: context.config.json is not valid JSON: {error}", file=sys.stderr)
        return 2

    requested = list(args.only or []) + list(args.skip or [])
    unknown = sorted(set(requested) - set(known_names()))
    if unknown:
        print(f'error: unknown gate(s): {", ".join(unknown)}', file=sys.stderr)
        print(f"known gates: {', '.join(known_names())}", file=sys.stderr)
        return 2
    if problems:
        for line in problems:
            print(f"error: {line}", file=sys.stderr)
        print(f"known gates: {', '.join(known_names())}", file=sys.stderr)
        return 2

    try:
        chosen, disabled = select(cfg, args)
    except SystemExit as error:
        print(error, file=sys.stderr)
        return 2

    ctx = Ctx(root, cfg)
    advisory = set(cfg["checks_advisory"])
    results: list[Result] = []
    blocking = 0
    advisory_findings = 0
    for name in chosen:
        result = GATES[name](ctx) if name in GATES else gate_installed(ctx)
        result.advisory = bool(args.warn) or name in advisory
        if result.findings:
            if result.advisory:
                advisory_findings += len(result.findings)
            else:
                blocking += len(result.findings)
        results.append(result)

    if args.json:
        payload = {
            "root": root.as_posix(),
            "gates": [{"gate": result.gate,
                       "status": "ok" if not result.findings else "fail",
                       "advisory": result.advisory,
                       "subjects": result.count,
                       "detail": result.detail,
                       "findings": [{"path": f.path, "line": f.line, "message": f.message}
                                    for f in result.findings]}
                      for result in results],
            "blocking": blocking,
            "advisory_findings": advisory_findings,
            "disabled": disabled,
            "exit": 1 if blocking else 0,
        }
        print(json.dumps(payload, indent=2))
        return 1 if blocking else 0

    for result in results:
        status = "ok" if not result.findings else ("FAIL" if not result.advisory else "warn")
        print(f"{result.gate:<12} {status:<5} {result.detail}")
        for finding in result.findings:
            print(finding.render())
    noun = "finding" if blocking == 1 else "findings"
    ran_text = f"{len(results)} of {len(known_names())} gates ran"
    print(f"{blocking} blocking {noun}; {ran_text}; "
          f"{advisory_findings} advisory; disabled: {', '.join(disabled) if disabled else 'none'}")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
