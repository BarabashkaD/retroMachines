# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD
"""Licence headers of the source files (.v, .vh, .py, .toml) of this repo, by the family's header
rule (wording_lib.header_problems, this repo's copy of retroICs' rule): the SPDX lines in each
header, the licence text under LICENSES/, every licence pointer of a header naming a file under
LICENSES/. No file here is exempt.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wording_lib import header_problems, source_files  # noqa: E402


class Headers(unittest.TestCase):
    def test_every_source_file_has_a_licence_header(self):
        files = source_files(ROOT)
        # a floor against an empty scan, not a count (the import tools and their tests are gone)
        self.assertGreater(len(files), 10)
        self.assertFalse(any(rel.startswith("lib/") for rel, _ in files))
        bad = {rel: header_problems(rel, data, ROOT) for rel, data in files}
        self.assertEqual({k: v for k, v in bad.items() if v}, {})

    def test_header_problems(self):
        # the rule itself (the copy in wording_lib.py), as retroICs tests it
        owner = ("SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), "
                 "https://github.com/BarabashkaD")
        ok = ("// SPDX-License-Identifier: BSD-3-Clause\n// %s\nmodule m;\n" % owner).encode()
        self.assertEqual(header_problems("a.v", ok, ROOT), [])
        cases = {
            b"module m;\n": "0 SPDX",
            ok.replace(b"BSD-3-Clause", b"MIT"): "no LICENSES/MIT.txt",
            ok.replace(b"Dmitry", b"Someone"): "without the owner's",
            ok.replace(b"module m;", b"// see ../../LICENSE.TXT\nmodule m;"): "names no file",
            ok.replace(b"module m;", b"// see LICENSES/X.txt\nmodule m;"): "is not a file",
            # an SPDX line below the header is not in the header
            b"module m;\n// SPDX-License-Identifier: BSD-3-Clause\n": "0 SPDX",
        }
        for data, want in cases.items():
            self.assertIn(want, " ".join(header_problems("a.v", data, ROOT)), data)


if __name__ == "__main__":
    unittest.main()
