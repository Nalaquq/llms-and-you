"""Tests that every shell command on the site is given for both platforms.

Students bring whatever laptop they own. A command written only for bash is not
a small inconvenience to the third of the room on Windows -- it is a wall on the
night before, in a course with no prerequisites, and the failure is silent
because a Windows student has no way to know what the command should have been.

So this is checked rather than remembered. A code block containing anything that
differs between a Unix shell and PowerShell has to live inside a tab set that
covers both. Commands identical on both platforms -- most of `git`, all of
`claude` -- need no tabs, and forcing them into tabs would only add noise.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from course_site.loaders import load_schedule

ROOT = Path(__file__).resolve().parents[1]

UNIX_TAB = "macOS / Linux"
WINDOWS_TAB = "Windows (PowerShell)"

SHELL_LANGS = {"bash", "sh", "zsh", "shell", "console", "powershell", "pwsh"}

# Things that do not survive being pasted into the other shell. Each is a real
# failure students have hit, not a stylistic difference.
DIVERGENT = {
    "python3": re.compile(r"\bpython3\b"),
    "pip3": re.compile(r"\bpip3\b"),
    "source": re.compile(r"(?m)^\s*source\s"),
    "export": re.compile(r"(?m)^\s*export\s+\w+="),
    "a Unix venv path": re.compile(r"\.venv/bin"),
    "a Windows venv path": re.compile(r"\.venv\\+Scripts"),
    "a PowerShell env var": re.compile(r"\$env:"),
    "a bash env var": re.compile(r"(?<!\$env:)\$[A-Z_]{3,}"),
    "a home-directory path": re.compile(r"~/\."),
    "a PowerShell cmdlet": re.compile(r"(?m)^\s*(Set|Get|New)-\w+"),
}

# One example per pattern, so a typo in a regex fails here rather than quietly
# switching off part of this file.
EXAMPLES = {
    "python3": "python3 -m venv .venv",
    "pip3": "pip3 install anthropic",
    "source": "source .venv/bin/activate",
    "export": "export ANTHROPIC_API_KEY='sk-ant-...'",
    "a Unix venv path": ".venv/bin/pytest",
    "a Windows venv path": ".venv\\Scripts\\activate",
    "a PowerShell env var": "$env:ANTHROPIC_API_KEY = 'sk-ant-...'",
    "a bash env var": "echo $ANTHROPIC_API_KEY",
    "a home-directory path": "cat ~/.zshrc",
    "a PowerShell cmdlet": "Set-ExecutionPolicy -Scope CurrentUser",
}

FENCE = re.compile(r"(?m)^(?P<indent>[ \t]*)```(?P<lang>\w*)\n(?P<body>.*?)^(?P=indent)```", re.S)
TAB = re.compile(r'(?m)^(?P<indent>[ \t]*)=== "(?P<label>[^"]+)"')

# README.md is read on GitHub, which does not render content tabs. There the
# same job is done by a bold label directly above the block.
BOLD_LABEL = re.compile(r"(?m)^\*\*(?P<label>[^*]+)\*\*\s*\n\s*$")


def _sources() -> list[tuple[str, str]]:
    """Every place a command can reach a student: hand-written pages, and prose
    inside ``schedule.yml`` that becomes a generated session page."""
    out = [
        (str(p.relative_to(ROOT)), p.read_text(encoding="utf-8"))
        for p in sorted(ROOT.glob("docs/**/*.md"))
        # docs/sessions/ is generated from schedule.yml, which is checked below.
        if "sessions" not in p.parts
    ]
    out.append(("README.md", (ROOT / "README.md").read_text(encoding="utf-8")))
    for d in load_schedule():
        prose = "\n".join(x for x in (d.session.activity, d.session.summary) if x)
        out.append((f"data/schedule.yml ({d.slug})", prose))
    return out


def _platform_label_at(text: str, pos: int, indent: int) -> str | None:
    """The platform this block is labelled with, by either convention.

    On the site that is the nearest ``=== "..."`` above it, indented less than
    the block. In README.md, where tabs do not render, it is a bold label on the
    line above.
    """
    above = list(TAB.finditer(text, 0, pos))
    if above and len(above[-1].group("indent").expandtabs(4)) < indent:
        return above[-1].group("label")
    bold = BOLD_LABEL.search(text, max(0, pos - 200), pos)
    return bold.group("label") if bold else None


def _blocks():
    for name, text in _sources():
        for m in FENCE.finditer(text):
            yield name, text, m


@pytest.mark.parametrize("marker", sorted(DIVERGENT))
def test_every_divergence_pattern_still_matches_its_example(marker: str):
    """Guard the guard. A typo here would switch off part of this file silently."""
    assert DIVERGENT[marker].search(EXAMPLES[marker]), (
        f"the {marker!r} pattern no longer matches {EXAMPLES[marker]!r}"
    )


def test_every_divergence_pattern_has_an_example():
    assert set(DIVERGENT) == set(EXAMPLES)


def test_platform_specific_commands_live_in_tabs():
    """A command that differs between shells must be shown for both shells."""
    offenders: list[str] = []
    for name, text, m in _blocks():
        if m.group("lang") not in SHELL_LANGS:
            continue
        found = [k for k, pat in DIVERGENT.items() if pat.search(m.group("body"))]
        if not found:
            continue
        indent = len(m.group("indent").expandtabs(4))
        if _platform_label_at(text, m.start(), indent) is None:
            line = text[: m.start()].count("\n") + 1
            offenders.append(f"{name}:{line} uses {', '.join(found)} outside a platform tab set")
    assert not offenders, "\n".join(["shell commands that only work on one platform:", *offenders])


def test_every_tab_set_covers_both_platforms():
    """Half a tab set is worse than none -- it looks complete and is not."""
    problems: list[str] = []
    for name, text in _sources():
        groups: list[list[str]] = []
        last_indent, last_end = None, 0
        for m in TAB.finditer(text):
            indent = len(m.group("indent").expandtabs(4))
            # A run of `===` at the same indent, with only their own content
            # between them, is one tab set.
            gap = text[last_end : m.start()]
            if groups and indent == last_indent and not re.search(r"(?m)^\S", gap):
                groups[-1].append(m.group("label"))
            else:
                groups.append([m.group("label")])
            last_indent, last_end = indent, m.end()

        for labels in groups:
            unknown = [x for x in labels if x not in (UNIX_TAB, WINDOWS_TAB)]
            if unknown:
                problems.append(f"{name}: unexpected tab label(s) {unknown}")
            elif set(labels) != {UNIX_TAB, WINDOWS_TAB}:
                problems.append(f"{name}: tab set {labels} does not cover both platforms")
    assert not problems, "\n".join(problems)


def test_the_setup_guide_says_commands_come_in_two_flavours():
    """The convention only works if students are told it exists."""
    text = (ROOT / "docs" / "guides" / "setup.md").read_text(encoding="utf-8")
    assert UNIX_TAB in text and WINDOWS_TAB in text
    assert "pick your platform once" in text.lower(), (
        "the setup guide must explain the tabs before using them"
    )
