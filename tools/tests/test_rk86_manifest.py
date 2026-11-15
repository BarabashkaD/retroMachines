# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Dmitry Veremeev (BarabashkaD), https://github.com/BarabashkaD
"""machines/rk86/component.toml: the RTL file list that simrun gives for the machine."""
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ICS = ROOT / "lib" / "retroICs"
SUBMODULE_HINT = "lib/retroICs is missing: run git submodule update --init --recursive"
if not (ICS / "tools" / "simrun").is_dir():
    raise ImportError(SUBMODULE_HINT)

# simrun's order: the dependencies first (rtl.depends order: the 8080A wrapper and its model, the
# 8255A, 8257, 8275), then the machine's own files (rtl.files order)
SIMRUN_ORDER = [
    'verilog work "lib/retroICs/ics/intel/8080a/rtl/intel_8080a.v"',
    'verilog work "lib/retroICs/ics/intel/8080a/rtl/upstream/k580vm80a.v"',
    'verilog work "lib/retroICs/ics/intel/8255a/rtl/intel_8255a.v"',
    'verilog work "lib/retroICs/ics/intel/8257/rtl/intel_8257.v"',
    'verilog work "lib/retroICs/ics/intel/8275/rtl/intel_8275.v"',
    'verilog work "machines/rk86/rtl/rk86_clocks16.v"',
    'verilog work "machines/rk86/rtl/rk86_video16.v"',
    'verilog work "machines/rk86/rtl/rk86_machine16.v"',
]


class FileList(unittest.TestCase):
    def filelist(self):
        env = dict(os.environ, PYTHONPATH=str(ICS / "tools"))
        cmd = [sys.executable, "-B", "-m", "simrun", "filelist", "machines/rk86", "--format", "prj",
               "--relative-to", ".", "--search", ".", "--search", "lib/retroICs"]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout.splitlines()

    def test_order_dependencies_first(self):
        # the chip models first, then the machine's own files; Icarus takes any order, a synthesis
        # tool may not
        self.assertEqual(self.filelist(), SIMRUN_ORDER)

    def test_every_file_exists(self):
        for line in self.filelist():
            path = line.split('"')[1]
            self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
