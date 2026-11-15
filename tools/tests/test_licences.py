# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD
"""The licence texts of LICENSES/ and LICENSE are byte-identical copies of the retroICs
submodule's; NOTICE names this repo only (the family's rule: each repo's NOTICE names that repo,
with its attribution line, and credits the original authors whose work its files contain), ASCII
and LF."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ICS = ROOT / "lib" / "retroICs"
SUBMODULE_HINT = "lib/retroICs is missing: run git submodule update --init --recursive"
ATTRIBUTION = ("Contains retroMachines by Dmitry Veremeev (BarabashkaD), "
               "https://github.com/BarabashkaD, BSD-3-Clause and CC BY 4.0.")
COPYRIGHT = "Copyright (c) 2026, Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD"


class Licences(unittest.TestCase):
    def test_texts_equal_retroics(self):
        self.assertTrue((ICS / "LICENSES").is_dir(), SUBMODULE_HINT)
        ours = sorted(p.name for p in (ROOT / "LICENSES").glob("*.txt"))
        theirs = sorted(p.name for p in (ICS / "LICENSES").glob("*.txt"))
        self.assertEqual(ours, theirs)
        for name in ours:
            self.assertEqual((ROOT / "LICENSES" / name).read_bytes(),
                             (ICS / "LICENSES" / name).read_bytes(), name)

    def test_license_equals_retroics(self):
        self.assertTrue(ICS.is_dir(), SUBMODULE_HINT)
        self.assertEqual((ROOT / "LICENSE").read_bytes(), (ICS / "LICENSE").read_bytes())

    def test_notice_names_this_repo_only(self):
        data = (ROOT / "NOTICE").read_bytes()
        self.assertTrue(data.isascii())
        self.assertNotIn(b"\r", data)
        self.assertTrue(data.endswith(b"\n") and not data.endswith(b"\n\n"))
        text = data.decode("ascii")
        lines = text.split("\n")
        self.assertEqual(lines[:4], ["retroMachines", COPYRIGHT, "", ATTRIBUTION])
        # one attribution line, this repo's; no other repo's attribution or NOTICE text
        self.assertEqual([l for l in lines if l.startswith("Contains ")], [ATTRIBUTION])
        self.assertNotIn("Contains retroICs", text)
        self.assertNotIn("@", text)

    def test_notice_credits(self):
        text = " ".join((ROOT / "NOTICE").read_text(encoding="ascii").split())
        for phrase in ("every Markdown file is under CC BY 4.0 (LICENSES/CC-BY-4.0.txt)",
                       "BSD-3-Clause (LICENSE, LICENSES/BSD-3-Clause.txt)", "faults/*.patch",
                       "machines/rk86/roms/monitor.bin, font.bin",
                       "monitor.bin: the monitor of the Radio-86RK, published in Radio magazine "
                       "(Moscow), 1986",
                       "D. Gorshkov, G. Zelenko, Yu. Ozerov and S. Popov",
                       "font.bin: the character generator of the Radio-86RK; its authorship and "
                       "publication are not established (open)",
                       "machines/rk86/roms/PROVENANCE.md", "LICENSES/LicenseRef-Tselikov-BSD.txt",
                       "lib/retroICs", "the NOTICE of retroICs"):
            self.assertIn(phrase, text, phrase)

    def test_notice_names_no_other_project(self):
        # the owner's files carry no origin; the ROMs' copy source is in roms/PROVENANCE.md only.
        # Each word written in two parts, so this file holds none of them.
        low = (ROOT / "NOTICE").read_text(encoding="ascii").lower()
        for word in ("kara" "bas", "poc" "ket", "analo" "gue", "fo" "rk", "mis" "ter", "apo" "gee"):
            self.assertNotIn(word, low, word)


if __name__ == "__main__":
    unittest.main()
