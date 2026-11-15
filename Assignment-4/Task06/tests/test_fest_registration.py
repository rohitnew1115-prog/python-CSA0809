"""Focused tests for the fest package's invalid and missing-file cases."""
import sys
import tempfile
import unittest
from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TASK_ROOT))
from fest_registration import collect, write_outputs


class FestRegistrationTests(unittest.TestCase):
    def test_continues_after_invalid_duplicate_and_missing_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            (folder / "department_cse.csv").write_text(
                "1925260050,P ROHIT,CSE,rohit@example.com,Music;Coding\n"
                "1925260051,Muruga Dharshini,CSE,invalid-email,Dance\n"
                "damaged,row\n",
                encoding="utf-8",
            )
            (folder / "department_ece.csv").write_text(
                "1925260050,P ROHIT,ECE,rohit@example.com,Music\n",
                encoding="utf-8",
            )
            accepted, errors = collect(folder)
            self.assertEqual(len(accepted), 1)
            self.assertTrue(any("invalid email" in error for error in errors))
            self.assertTrue(any("expected 5 fields" in error for error in errors))
            self.assertTrue(any("duplicate registration" in error for error in errors))
            self.assertEqual(sum("missing department file" in error for error in errors), 3)
            output = folder / "output"
            write_outputs(output, accepted, errors)
            for filename in ("clean_master_list.csv", "event_music.csv", "summary_report.txt", "error_log.txt"):
                self.assertTrue((output / filename).is_file())


if __name__ == "__main__":
    unittest.main()
