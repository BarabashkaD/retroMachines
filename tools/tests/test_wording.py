# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD
"""No wording that points at private planning documents, in every file of the working tree.

The patterns, the optional private word list (RETRO_PRIVATE_WORDS) and the file scope are in
wording_lib.py (this repo's copy of retroICs' wording helpers). KEPT lists the generic-pattern hits
that are kept as they are, each by file, hit and a fragment of its line (so the same words on
another line still fail) with its reason: a clock step of the machine's own text, and the fault
expect texts that match it. WORD_EXEMPT exempts a word of the private list for one file only. A
stale entry of either fails.
"""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wording_lib import (OWN_FILE, stale_word_exemptions, wording_files,  # noqa: E402
                         wording_hits, words_for, words_for_scan)

# (path, word) -> reason: a private-list word kept in one file only (stale entries fail)
WORD_EXEMPT = {}
CLOCK_STEP = "a clock step (the 8224's period count), not a planning step"
EXPECT_STEP = "a fault's expect text: the clock-step message of the TB, as it prints it"
REASONS = (CLOCK_STEP, EXPECT_STEP)
# (path, hit, line fragment) -> reason; each hit written in two parts, so this file holds none
KEPT = {
    ("machines/rk86/rtl/rk86_clocks16.v", "st" "ep 0", "Φ1 rises: st" "ep 0 of 9;"): CLOCK_STEP,
    ("machines/rk86/component.toml", "st" "ep 4", 'expect = "ERROR: clocks16: f2 at st'):
        EXPECT_STEP,
    ("machines/rk86/component.toml", "st" "ep 6", 'expect = "ERROR: clocks16: f2_fall at st'):
        EXPECT_STEP,
}


def line_hits(text, words, rel, kept, skip_marked=False):
    """The private wordings of text (wording_hits line by line), without the generic-pattern hits
    that an entry of kept covers for rel on a line holding its fragment (the words always count)."""
    found = set()
    for line in text.splitlines():
        generic = set(wording_hits(line, skip_marked=skip_marked))
        generic -= {h for (p, h, frag) in kept if p == rel and frag in line}
        found |= generic | set(wording_hits(line, words, generic=False))
    return sorted(found)


def scan_repo(repo, words, word_exempt=None, kept=None):
    """{name: hits} of every file of the working tree (retroICs' scope) with a hit; the entries of
    KEPT (default) exempt their hits on their lines from the generic patterns, the words of
    WORD_EXEMPT (default) are exempt only for their own path."""
    out = {}
    word_exempt = WORD_EXEMPT if word_exempt is None else word_exempt
    kept = KEPT if kept is None else kept
    for rel, data in wording_files(repo):
        text = data.decode("utf-8", errors="replace")
        hits = line_hits(text, words_for(rel, words, word_exempt), rel, kept,
                         skip_marked=(rel == OWN_FILE))
        if hits:
            out[rel] = hits
    return out


class Wording(unittest.TestCase):
    def test_no_private_wording(self):
        self.assertEqual(scan_repo(ROOT, words_for_scan()), {})

    def test_word_exemptions_current(self):
        self.assertTrue(all(w == w.lower() and r for (_, w), r in WORD_EXEMPT.items()))
        self.assertEqual(stale_word_exemptions(ROOT, WORD_EXEMPT), [])

    def test_word_exemption_only_for_its_path(self):
        rel, word = "machines/x/README.md", "secret" "word"
        data = ("the %s here\n" % word).encode("utf-8")
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d) / "repo"
            (repo / rel).parent.mkdir(parents=True)
            subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
            (repo / rel).write_bytes(data)
            (repo / "other.txt").write_bytes(data)
            subprocess.run(["git", "-C", str(repo), "-c", "core.autocrlf=false", "add", "-A"],
                           check=True)
            self.assertEqual(scan_repo(repo, [word], {(rel, word): "test"}),
                             {"other.txt": [word]})
            self.assertEqual(scan_repo(repo, [word], {}), {rel: [word], "other.txt": [word]})

    def test_kept_entries_current(self):
        # each entry's file has a line with its fragment, and that line still hits with that hit
        for (rel, hit, frag), reason in sorted(KEPT.items()):
            self.assertIn(reason, REASONS)
            p = ROOT / rel
            lines = p.read_text(encoding="utf-8").splitlines() if p.is_file() else []
            self.assertTrue(any(frag in l and hit in wording_hits(l) for l in lines),
                            (rel, hit, frag))

    def test_kept_only_on_its_line(self):
        hit = "st" "ep 4"  # split: keeps this file free of the pattern
        kept = {("a.toml", hit, "f2 at st"): EXPECT_STEP}
        ok = 'expect = "ERROR: clocks16: f2 at %s"\n' % hit
        self.assertEqual(line_hits(ok, [], "a.toml", kept), [])
        # the same hit on another line, in another file, or another hit on the line still count
        self.assertEqual(line_hits("# the %s\n" % hit, [], "a.toml", kept), [hit])
        self.assertEqual(line_hits(ok, [], "b.toml", kept), [hit])
        extra = "Ta" "sk 9"
        self.assertEqual(line_hits(ok.replace('"\n', ' %s"\n' % extra), [], "a.toml", kept),
                         [extra])

    def test_own_file_exempt_only_on_marked_lines(self):
        # the pattern lines of wording_lib.py hit when the file is not exempt; nothing else does
        data = (ROOT / OWN_FILE).read_text(encoding="utf-8")
        self.assertTrue(wording_hits(data))
        self.assertEqual(wording_hits(data, skip_marked=True), [])

    def test_no_old_cpu_paths(self):
        # every path into the 8080 model's own signals goes through core; the pins (pin_*) are
        # also the wrapper's ports
        bad = re.compile(r"\.cpu\.(?!core\b|pin_)[A-Za-z_]|CPU16_ZERO\((?!M\))(?![^)]*\.core\))")
        for p in sorted((ROOT / "machines").rglob("*.v*")):
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                self.assertIsNone(bad.search(line), "%s:%d" % (p.name, n))


if __name__ == "__main__":
    unittest.main()
