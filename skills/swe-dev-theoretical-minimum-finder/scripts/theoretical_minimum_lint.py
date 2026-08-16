#!/usr/bin/env python3
"""Structural linter for swe-dev-theoretical-minimum-finder dossiers.

This tool checks provenance plumbing and artifact shape. It does NOT verify factual
correctness, source quality, or whether a citation truly supports a claim.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Target capability and scope",
    "## Minimum at a glance",
    "## Dependency map",
    "## Theoretical minimum",
    "## Exclusions and deferrals",
    "## Deep structures, invariants, and limits",
    "## Minimum source spine",
    "## Training sequence",
    "## Mastery examination",
    "## Contradictions and disputed points",
    "## Unknowns and search gaps",
    "## Claims and evidence ledger",
    "## Source Registry",
    "## Audit result",
]
REQUIRED_EXAM_HEADINGS = [
    "### Resource conditions",
    "### Blank-page regeneration",
    "### Unseen and transfer problems",
    "### Process rubric",
    "### Oral defenses",
    "### Integrated challenge",
    "### Hint ladder",
]
REQUIRED_FRONTMATTER = (
    "artifact_version",
    "topic",
    "target_capability",
    "intended_learner",
    "entry_assumptions",
    "generated_at",
    "scope",
)
REQUIRED_AUDIT_FIELDS = (
    "Provenance integrity",
    "Target capability clarity",
    "Prerequisite closure",
    "Deletion-test strength",
    "Core Tier 1-2 coverage",
    "Counterevidence search",
    "Mastery-exam validity",
    "Link/content verification",
    "Known hallucination risks removed",
    "Remaining uncertainty",
    "Structural lint",
)
PROCESS_CRITERIA = (
    ("framing and assumptions", re.compile(r"\b(fram|assum)", re.I)),
    ("representation choice", re.compile(r"\brepresent", re.I)),
    ("decomposition or intermediate derivation", re.compile(r"\b(decompos|deriv|intermediate)", re.I)),
    ("decisive checks", re.compile(r"\b(check|counterexample|invariant|evidence)", re.I)),
    ("recovery from dead ends", re.compile(r"\b(recover|recovery|dead end|unproductive)", re.I)),
    ("boundaries and uncertainty", re.compile(r"\b(boundar|uncertain|limitation)", re.I)),
    ("clarity under questioning", re.compile(r"\b(question|clarity|defen)", re.I)),
)

ALLOWED_VERIFICATION = {"content", "existence-only", "blocked", "unverified"}
RISKY_WORDS = re.compile(r"\b(canonical|consensus|definitive|proven|verified|standard text|universally accepted)\b", re.I)
SOURCE_REF = re.compile(r"\[(S\d{2,3})\]")
SOURCE_DEF = re.compile(r"^### \[(S\d{2,3})\]\s+(.+?)\s*$", re.M)
SOURCE_COUNT_DEF = re.compile(r"^\s{2}tier_([0-5]):\s*(\d+)\s*$", re.M)
MINIMUM_REF = re.compile(r"\[(M\d{2,3})\]")
MINIMUM_DEF = re.compile(r"^### \[(M\d{2,3})\]\s+(.+?)\s*$", re.M)
MARKER = re.compile(r"\[(SYNTHESIS|INFERENCE|UNKNOWN|CONTESTED)\]")
REQUIRED_MINIMUM_FIELDS = (
    "Own without notes",
    "Enables",
    "Depends on",
    "Removal failure",
    "Non-redundancy",
    "Regeneration test",
    "Defense obligation",
    "Sources",
)


def frontmatter_body(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    return text[4:end]


def frontmatter(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in frontmatter_body(text).splitlines():
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*\s*:", line):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"\'')
    return data


def declared_source_counts(text: str) -> dict[str, int]:
    body = frontmatter_body(text)
    start = re.search(r"^source_counts:\s*$", body, re.M)
    if not start:
        return {}
    remainder = body[start.end():]
    next_key = re.search(r"^\S[^:]*:\s*", remainder, re.M)
    block = remainder[:next_key.start()] if next_key else remainder
    return {f"tier_{match.group(1)}": int(match.group(2)) for match in SOURCE_COUNT_DEF.finditer(block)}


def source_blocks(text: str) -> dict[str, dict[str, str]]:
    pos = text.find("## Source Registry")
    if pos < 0:
        return {}
    registry = text[pos:]
    matches = list(SOURCE_DEF.finditer(registry))
    out: dict[str, dict[str, str]] = {}
    for i, m in enumerate(matches):
        sid, title = m.group(1), m.group(2)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(registry)
        block = registry[start:end]
        fields: dict[str, str] = {"Title": title}
        for line in block.splitlines():
            mm = re.match(r"^-\s+([^:]+):\s*(.*)$", line.strip())
            if mm:
                fields[mm.group(1).strip()] = mm.group(2).strip()
        if sid in out:
            fields["__duplicate__"] = "true"
        out[sid] = fields
    return out


def minimum_blocks(text: str) -> dict[str, dict[str, str]]:
    minimum = section(text, "## Theoretical minimum")
    matches = list(MINIMUM_DEF.finditer(minimum))
    out: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        minimum_id, title = match.group(1), match.group(2)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(minimum)
        block = minimum[start:end]
        fields: dict[str, str] = {"Title": title}
        for line in block.splitlines():
            field_match = re.match(r"^-\s+([^:]+):\s*(.*)$", line.strip())
            if field_match:
                fields[field_match.group(1).strip()] = field_match.group(2).strip()
        if minimum_id in out:
            fields["__duplicate__"] = "true"
        out[minimum_id] = fields
    return out


def section(text: str, heading: str, next_level: str = "## ") -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    next_heading = re.escape(next_level.strip())
    m = re.search(rf"\n{next_heading}\s+", text[start:])
    end = start + m.start() if m else len(text)
    return text[start:end]


def drop_section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return text
    m = re.search(r"\n##\s+", text[start + len(heading):])
    end = start + len(heading) + m.start() if m else len(text)
    return text[:start] + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: theoretical_minimum_lint.py <dossier.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: dossier not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    fm = frontmatter(text)
    if not fm:
        errors.append("missing or malformed YAML frontmatter")
    if fm.get("generator") != "swe-dev-theoretical-minimum-finder":
        errors.append("frontmatter must contain generator: swe-dev-theoretical-minimum-finder")
    if fm.get("status") not in {"grounded", "mixed", "limited", "exploratory"}:
        errors.append("frontmatter status must be grounded|mixed|limited|exploratory")
    for field in REQUIRED_FRONTMATTER:
        if not fm.get(field):
            errors.append(f"frontmatter missing required field: {field}")
    counts = declared_source_counts(text)
    if "source_counts" not in fm:
        errors.append("frontmatter missing required field: source_counts")
    elif set(counts) != {f"tier_{tier}" for tier in range(6)}:
        errors.append("frontmatter source_counts must declare integer tier_0 through tier_5 values")
    if "limitations" not in fm:
        errors.append("frontmatter missing required field: limitations")
    elif not fm["limitations"] and not re.search(r"^limitations:\s*\n\s+-\s+\S", frontmatter_body(text), re.M):
        errors.append("frontmatter limitations must be [] or a non-empty list")

    for h in REQUIRED_HEADINGS:
        if h not in text:
            errors.append(f"missing required heading: {h}")
    exam = section(text, "## Mastery examination")
    for h in REQUIRED_EXAM_HEADINGS:
        if h not in exam:
            errors.append(f"missing required examination heading: {h}")

    if re.search(r"\b(TODO|TBD|PLACEHOLDER)\b|<[^>]{2,40}>", text, re.I):
        warnings.append("dossier contains TODO/TBD/placeholder-like text")

    sources = source_blocks(text)
    if not sources:
        errors.append("Source Registry contains no parseable source entries")

    for sid, fields in sources.items():
        if fields.get("__duplicate__") == "true":
            errors.append(f"duplicate source ID: {sid}")
        for key in ("Tier", "Type", "URL / identifier", "Accessed", "Verification", "Supports", "Limitations"):
            if key not in fields:
                errors.append(f"{sid} missing Source Registry field: {key}")
        ver = fields.get("Verification", "")
        if ver and ver not in ALLOWED_VERIFICATION:
            errors.append(f"{sid} has invalid Verification value: {ver}")
        tier = fields.get("Tier", "")
        if tier and not re.fullmatch(r"[0-5]", tier):
            errors.append(f"{sid} Tier must be 0..5, got: {tier}")

    actual_counts = {
        f"tier_{tier}": sum(fields.get("Tier") == str(tier) for fields in sources.values())
        for tier in range(6)
    }
    for tier, declared_count in counts.items():
        actual_count = actual_counts[tier]
        if declared_count != actual_count:
            errors.append(
                f"source_counts {tier} declares {declared_count} but Source Registry contains {actual_count}"
            )

    # Analyze citations outside the Source Registry so definitions do not count as use.
    registry_pos = text.find("## Source Registry")
    body = text[:registry_pos] if registry_pos >= 0 else text
    cited = set(SOURCE_REF.findall(body))
    substantive_body = drop_section(drop_section(body, "## Unknowns and search gaps"), "## Audit result")
    substantive_cited = set(SOURCE_REF.findall(substantive_body))
    for sid in sorted(cited):
        if sid not in sources:
            errors.append(f"citation {sid} has no Source Registry entry")
    for sid in sorted(substantive_cited):
        if sid in sources:
            ver = sources[sid].get("Verification")
            if ver in {"existence-only", "blocked", "unverified"}:
                errors.append(f"citation {sid} is used substantively but Verification={ver}; only content-verified sources may carry claims")

    unused = sorted(set(sources) - cited)
    if unused:
        warnings.append("registry entries never cited outside registry: " + ", ".join(unused))

    units = minimum_blocks(text)
    if not units:
        errors.append("Theoretical minimum contains no parseable [Mxx] units")
    for minimum_id, fields in units.items():
        if fields.get("__duplicate__") == "true":
            errors.append(f"duplicate minimum unit ID: {minimum_id}")
        for key in REQUIRED_MINIMUM_FIELDS:
            if not fields.get(key):
                errors.append(f"{minimum_id} missing minimum-unit field: {key}")

        dependencies = set(MINIMUM_REF.findall(fields.get("Depends on", "")))
        for dependency in sorted(dependencies):
            if dependency not in units:
                errors.append(f"{minimum_id} depends on unknown minimum unit {dependency}")
            elif dependency == minimum_id:
                errors.append(f"{minimum_id} depends on itself")

        support = fields.get("Sources", "")
        if support and not SOURCE_REF.search(support) and not MARKER.search(support):
            errors.append(f"{minimum_id} Sources must contain a source ID or synthesis marker")

    blank_page = section(exam, "### Blank-page regeneration", "### ")
    for minimum_id in sorted(units):
        if f"[{minimum_id}]" not in blank_page:
            warnings.append(f"{minimum_id} has no explicit blank-page regeneration task")

    process_rubric = section(exam, "### Process rubric", "### ")
    for label, pattern in PROCESS_CRITERIA:
        if not pattern.search(process_rubric):
            warnings.append(f"Process rubric does not mention {label}")

    audit = section(text, "## Audit result")
    for field in REQUIRED_AUDIT_FIELDS:
        if not re.search(rf"^-\s+{re.escape(field)}:\s*\S", audit, re.M):
            errors.append(f"Audit result missing required field: {field}")

    # Risky epistemic language should normally have an inline citation or explicit marker.
    for lineno, line in enumerate(substantive_body.splitlines(), 1):
        if RISKY_WORDS.search(line) and not SOURCE_REF.search(line) and not MARKER.search(line):
            if not line.startswith("#") and len(line.strip()) > 30:
                warnings.append(f"line {lineno}: strong status word without source/marker: {line.strip()[:120]}")

    # Grounded status should have at least one cited Tier 1/2 source and no fatal provenance error.
    if fm.get("status") == "grounded":
        grounded_citations = [sid for sid in substantive_cited if sources.get(sid, {}).get("Tier") in {"0", "1", "2"}]
        if not grounded_citations:
            errors.append("status=grounded but no cited Tier 0-2 sources were found")

    if errors:
        print(f"FAIL: {len(errors)} structural error(s)")
        for e in errors:
            print(f"ERROR: {e}")
    else:
        print("PASS: no structural errors")

    if warnings:
        print(f"WARN: {len(warnings)} warning(s)")
        for w in warnings:
            print(f"WARN: {w}")
    else:
        print("WARN: none")

    print("NOTE: this linter checks structure, provenance plumbing, and examination coverage only; it does not certify factual correctness or mastery.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
