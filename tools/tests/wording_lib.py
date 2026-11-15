# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD
"""Helpers of this repo's wording and header tests: the private-wording scan (generic patterns
that point at private planning documents, and the words of an untracked list RETRO_PRIVATE_WORDS),
and the licence header rule of the source files.

Taken from retroICs' tools/tests (its wording and header tests); this repo's own copy,
not an interface for other repos. Changed in the copy: no exception for a task number followed by
"record" in the generic pattern (no file here needs it), the exemption tables passed by the caller,
and the lines that define the patterns exempt only in this file. It uses the retroICs tools
check_comment_only.py and check_privacy.py (lib/retroICs/tools).
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ICS_TOOLS = ROOT / "lib" / "retroICs" / "tools"
SUBMODULE_HINT = "lib/retroICs is missing: run git submodule update --init --recursive"
if not (ICS_TOOLS / "check_privacy.py").is_file():
    raise ImportError(SUBMODULE_HINT)
sys.path.insert(0, str(ICS_TOOLS))
import check_comment_only as cco  # noqa: E402
import check_privacy as cp  # noqa: E402

# Wording that points at private planning documents, generic patterns only. The lines that define
# the patterns end with the marker below; in OWN_FILE only, those lines are exempt from the generic
# patterns (never from the private word list).
PATTERN_MARK = "# wording-pattern"
PLAN_WORDING = re.compile(r"\bthe plan\b|\bplan's\b|\bTasks? \d+|\bStep \d|\bspec \d"  # wording-pattern
                          r"|§|Assumptions of the plan|\bthe spec\b|\bthe brief\b|superpowers"  # wording-pattern
                          r"|\d+\.\d+ a-d of the 0\.8\.0 design", re.I)  # wording-pattern
# a controller as the one who decides; the chips' own controller words (the CRT controller and
# the Buffer Output Controller) are not matched
CONTROLLER_ACTOR = re.compile(r"\bcontroller(?:,| ruling| decision|\))|\bby the controller\b")  # wording-pattern
# more private words, one per line ('#' starts a comment), from an untracked file on the
# maintainer's PC named by this variable; without it only the generic patterns apply, and the
# test says so with this NOTE line
PRIVATE_WORDS_VAR = "RETRO_PRIVATE_WORDS"
GENERIC_ONLY_NOTE = "NOTE: private word list not set: generic patterns only"
# the one file whose marked lines are exempt from the generic patterns (never from the words)
OWN_FILE = "tools/tests/wording_lib.py"

# the licence header rule
SUFFIXES = (".v", ".vh", ".py", ".toml")
OWNER = ("SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), "
         "https://github.com/BarabashkaD")
SPDX_ID = re.compile(r"SPDX-License-Identifier: (\S+)\s*$")
POINTER = re.compile(r"[\w./-]*LICENSE[\w./-]*")
TSELIKOV = "LicenseRef-Tselikov-BSD"


def private_words():
    """The extra words of RETRO_PRIVATE_WORDS, lower case; [] when the variable is not set."""
    path = os.environ.get(PRIVATE_WORDS_VAR)
    if not path:
        return []
    p = Path(path)
    if not p.is_file():
        raise AssertionError("%s does not name a file" % PRIVATE_WORDS_VAR)
    words = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            words.append(line.lower())
    return words


def words_for_scan():
    """private_words(), printing GENERIC_ONLY_NOTE to stderr when the variable is not set."""
    if not os.environ.get(PRIVATE_WORDS_VAR):
        print(GENERIC_ONLY_NOTE, file=sys.stderr)
    return private_words()


def wording_hits(text, words=(), skip_marked=False, generic=True):
    """Every private wording in text: the generic patterns and the given words. With skip_marked,
    a line ending with PATTERN_MARK is exempt from the generic patterns only; generic=False skips
    them on every line. The words are checked on every line."""
    found = set()
    for line in text.splitlines():
        if generic and not (skip_marked and line.rstrip().endswith(PATTERN_MARK)):
            found |= {m.group(0) for m in PLAN_WORDING.finditer(line)}
            found |= {m.group(0) for m in CONTROLLER_ACTOR.finditer(line)}
        low = line.lower()
        found |= {w for w in words if w in low}
    return sorted(found)


def wording_files(repo=ROOT):
    """The files of the working tree as check_privacy sees them (tracked, and untracked but not
    ignored), as (repo-relative name, bytes). Skipped: binary files (a NUL byte in the first 8 KiB,
    or a PDF, which may have none there; no wording to read: check_privacy scans the PDFs) and
    LICENSES/*.txt (the official licence texts, kept byte for byte)."""
    repo = Path(repo)
    out = []
    for f in cp.working_tree_files(repo):
        if not f.is_file():
            continue
        rel = f.relative_to(repo).as_posix()
        if rel.startswith("LICENSES/") and rel.endswith(".txt"):
            continue
        data = f.read_bytes()
        if b"\0" in data[:8192] or data.startswith(b"%PDF-"):
            continue
        out.append((rel, data))
    return sorted(out)


def words_for(rel, words, exempt):
    """The words to check in the file rel: words without those exempt for rel."""
    return [w for w in words if (rel, w) not in exempt]


def stale_word_exemptions(repo, exempt):
    """The entries of exempt whose word is in no line of their file."""
    out = []
    for rel, word in sorted(exempt):
        p = Path(repo) / rel
        lines = p.read_text(encoding="utf-8").lower().splitlines() if p.is_file() else []
        if not any(word in line for line in lines):
            out.append((rel, word))
    return out


def header(text, prefix):
    """The lines of the leading comment block of text."""
    lines = text.split("\n")
    return lines[:cco.leading_block(lines, prefix)]


def header_problems(rel, data, root):
    """Why the file rel (bytes data) of the repo at root has no valid licence header; []."""
    prefix = cco.comment_prefix(rel)
    head = header(data.decode("utf-8"), prefix)
    ids = [m.group(1) for m in (SPDX_ID.search(l) for l in head) if m]
    out = []
    if len(ids) != 1:
        return ["%d SPDX-License-Identifier lines in the header" % len(ids)]
    lic = ids[0]
    if not (Path(root) / "LICENSES" / (lic + ".txt")).is_file():
        out.append("no LICENSES/%s.txt" % lic)
    if not any("SPDX-FileCopyrightText: " in l for l in head):
        out.append("no SPDX-FileCopyrightText line")
    if lic == "BSD-3-Clause" and not any(l.endswith(OWNER) for l in head):
        out.append("BSD-3-Clause without the owner's copyright line")
    tselikov_text = "LICENSES/%s.txt" % TSELIKOV
    for n, line in enumerate(head, 1):
        for token in POINTER.findall(line):
            token = token.rstrip(".,;:")
            if token.startswith("LICENSES/"):
                if not (Path(root) / token).is_file():
                    out.append("line %d: %s is not a file" % (n, token))
            elif not (token == "LICENSE.TXT" and lic == TSELIKOV
                      and any(tselikov_text in l for l in head)):
                out.append("line %d: the licence pointer %s names no file under LICENSES/"
                           % (n, token))
    return out


def source_files(root):
    """(repo-relative name, bytes) of every tracked or untracked-not-ignored source file."""
    root = Path(root)
    out = []
    for f in cp.working_tree_files(root):
        rel = f.relative_to(root).as_posix()
        if f.is_file() and rel.endswith(SUFFIXES):
            out.append((rel, f.read_bytes()))
    return sorted(out)
