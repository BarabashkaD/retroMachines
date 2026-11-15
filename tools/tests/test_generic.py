# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD
"""The repo names no fork or other project as the origin of its files, no project that uses it,
no planning document, and uses the vendor part names in its own text.

GENERIC_WORDS: the fork, its commits and its old paths, the projects that use this repo, planning
wording, and the Soviet part names. Before a line is matched, the bracket source IDs listed in
docs/sources.md (such as the reference sheet IDs) are taken out of it. The exceptions
(GENERIC_EXEMPT, keyed by file, word and a fragment of the line, so a new mention on another line
still fails), each with its reason: an equivalent (an equivalents file or table), the provenance of
a stored copy (where the ROM images were copied from, the licence claim made for them), board
evidence citing a source ID, a quoted source or record title, a file or module name or a language
keyword spelt like a word of the list, and the credit of an original author or base. CHANGELOG.md
(history) and this file are not read; binary files and LICENSES/*.txt are skipped; the fault
patches are read.
"""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wording_lib import ROOT, wording_files  # noqa: E402

GENERIC_WORDS = [r"karabas", r"\bfork\b", r"pocket", r"radio86-rk-pocket", r"analogue",
                 r"rk86_16/", r"run_machine16_sim", r"35e86e7|d995355|dbb92cb",
                 r"\bTasks? \d+\b", r"\bspec \d", r"spec D\d+", r"Global Constraints",
                 r"final review \d{4}-",
                 r"К580|КР580|К155|ИЕ4|ИР13|ТМ2|ГФ24|ВВ55|ВТ57|ВГ75|ВМ80|ИК80|ИК55|ИК57"]
WORDS = [re.compile(w, re.I) for w in GENERIC_WORDS]
NOT_READ = {"CHANGELOG.md", "tools/tests/test_generic.py"}
SOURCES = "docs/sources.md"
SOURCE_ROW = re.compile(r"^\| (\[[^\]]+\]) \|")

EQUIVALENT = "an equivalent: an equivalents file or table"
PROVENANCE = "provenance of a stored copy: where it was copied from, its licence claim"
EVIDENCE = "board evidence citing a source ID"
TITLE = "a quoted source or record title"
FILENAME = "a file or module name, or a language keyword spelt like a word of the list"
CREDIT = "credit of an original author or base"
REASONS = (EQUIVALENT, PROVENANCE, EVIDENCE, TITLE, FILENAME, CREDIT)


def _entries(rel, frag, words, reason):
    return {(rel, w, frag): reason for w in words}


SOVIET_8224 = ("кр580", "гф24")
SOVIET_7492 = ("к155", "ие4")
ROM_FORK = ("karabas", "35e86e7")
GENERIC_EXEMPT = {
    # the equivalents of the clock chips: their equivalents files and the equivalents tables
    **_entries("machines/rk86/ics/intel-8224/equivalents.md", "| КР580ГФ24 | `kr580gf24` | Soviet",
               SOVIET_8224, EQUIVALENT),
    **_entries("machines/rk86/ics/intel-8224/README.md", "| КР580ГФ24 | `kr580gf24` | unverified |",
               SOVIET_8224, EQUIVALENT),
    **_entries("machines/rk86/ics/ti-sn7492/equivalents.md", "| К155ИЕ4 | `k155ie4` | Soviet",
               SOVIET_7492, EQUIVALENT),
    **_entries("machines/rk86/ics/ti-sn7492/README.md", "| К155ИЕ4 | `k155ie4` | unverified |",
               SOVIET_7492, EQUIVALENT),
    # the titles of the Soviet reference sheets in the source list
    **_entries("docs/sources.md", "| КР580ГФ24 reference sheet (the Soviet equivalent of the 8224) |",
               SOVIET_8224, TITLE),
    **_entries("docs/sources.md", "| К155ИЕ4 reference sheet (the Soviet equivalent of the SN7492) |",
               SOVIET_7492, TITLE),
    # where the stored ROM images were copied from (the repository and commit, the download links)
    **_entries("machines/rk86/roms/PROVENANCE.md",
               "- **Copied from:** `karabas-go-core-rk86` (fork `BarabashkaD/karabas-go-core-rk86`",
               ("karabas", "fork"), PROVENANCE),
    **_entries("machines/rk86/roms/PROVENANCE.md",
               "`andykarpov/karabas-go-core-rk86`) at commit `35e86e7", ROM_FORK, PROVENANCE),
    **_entries("machines/rk86/roms/PROVENANCE.md",
               "https://github.com/BarabashkaD/karabas-go-core-rk86/raw/35e86e7dfdeae112873a5d727bdd5f5bd67e0e97/src/roms/BIOS.BIN",
               ROM_FORK, PROVENANCE),
    **_entries("machines/rk86/roms/PROVENANCE.md",
               "and https://github.com/BarabashkaD/karabas-go-core-rk86/raw/35e86e7dfdeae112873a5d727bdd5f5bd67e0e97/src/roms/FONT.BIN",
               ROM_FORK, PROVENANCE),
}


def source_ids(repo=ROOT):
    """The bracket source IDs that docs/sources.md lists (the first cell of its table rows)."""
    p = Path(repo) / SOURCES
    if not p.is_file():
        return []
    return [m.group(1) for m in (SOURCE_ROW.match(l)
                                 for l in p.read_text(encoding="utf-8").splitlines()) if m]


def hits(text, rel, exempt, ids=()):
    """[(line number, word)] of the words in text that no exemption of rel covers; the bracket
    source IDs ids are taken out of each line first (the exemption fragments match the whole
    line)."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        bare = line
        for sid in ids:
            bare = bare.replace(sid, "")
        for w in WORDS:
            for m in w.finditer(bare):
                key = m.group(0).lower()
                if any(p == rel and kw == key and frag in line for (p, kw, frag) in exempt):
                    continue
                out.append((n, m.group(0)))
    return out


def scan(repo=ROOT, exempt=None):
    exempt = GENERIC_EXEMPT if exempt is None else exempt
    ids = source_ids(repo)
    out = {}
    for rel, data in wording_files(repo):
        if rel in NOT_READ:
            continue
        found = hits(data.decode("utf-8", errors="replace"), rel, exempt, ids)
        if found:
            out[rel] = found
    return out


class Generic(unittest.TestCase):
    def test_no_project_words(self):
        self.assertEqual(scan(), {})

    def test_exempt_entries_not_stale(self):
        stale = []
        for (rel, word, frag), reason in sorted(GENERIC_EXEMPT.items()):
            self.assertIn(reason, REASONS, (rel, word))
            p = ROOT / rel
            lines = p.read_text(encoding="utf-8").splitlines() if p.is_file() else []
            if not any(frag in l and word in l.lower() for l in lines):
                stale.append((rel, word, frag))
        self.assertEqual(stale, [])

    def test_exemption_is_per_line(self):
        text = "credit: the Karabas core\nthe Karabas machine\n"
        exempt = {("a.md", "karabas", "credit:"): CREDIT}
        self.assertEqual(hits(text, "a.md", exempt), [(2, "Karabas")])

    def test_source_ids_taken_out(self):
        ids = source_ids()
        self.assertIn("[ГФ24]", ids)
        self.assertIn("[ИЕ4]", ids)
        self.assertEqual(hits("see [ГФ24] and [ИЕ4]\n", "a.md", {}, ids), [])
        self.assertEqual(hits("the К155ИЕ4 counter [ИЕ4]\n", "a.md", {}, ids),
                         [(1, "К155"), (1, "ИЕ4")])

    def test_words(self):
        # the planning words written in two parts, so this file holds none of them for the
        # wording test (test_wording.py)
        for text in ("the Karabas core", "a fork of it", "radio86-rk-pocket", "Pocket", "Analogue",
                     "src/rtl/rk86_16/x.v", "run_machine16_sim.py", "at 35e86e7",
                     "Ta" "sk 4", "sp" "ec 4.1", "spec D12", "Global Constraints",
                     "final review 2026-11-14", "КР580ВМ80А", "К155ИЕ4", "КР580ВГ75"):
            self.assertTrue(hits(text + "\n", "a.md", {}), text)
        for text in ("forked", "fork_n", "D79", "SN7492", "8224"):
            self.assertEqual(hits(text + "\n", "a.md", {}), [], text)


if __name__ == "__main__":
    unittest.main()
