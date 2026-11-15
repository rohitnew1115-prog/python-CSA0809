"""Create persistent evidence showing that an absent department is logged."""
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fest_registration import collect, write_outputs


if __name__ == "__main__":
    task_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as temporary:
        input_folder = Path(temporary)
        (input_folder / "department_cse.csv").write_text(
            "1925260050,P ROHIT,CSE,rohit@example.com,Music;Coding\n", encoding="utf-8"
        )
        accepted, errors = collect(input_folder)
        output = task_root / "output" / "missing_department_case"
        write_outputs(output, accepted, errors)
    print((task_root / "output" / "missing_department_case" / "error_log.txt").read_text(encoding="utf-8"))
