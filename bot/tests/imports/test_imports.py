import os
import sys
import importlib
from pathlib import Path

import pytest

project_root = Path(os.path.abspath(".")).resolve()

python_files = [
    p
    for p in project_root.rglob("*.py")
    if "__pycache__" not in p.parts
       and not any(part.startswith(".") for part in p.parts)
       and "tests" not in p.parts
]

python_files = [str(p) for p in sorted(python_files)]


@pytest.mark.parametrize("filepath", python_files)
def test_can_import_module(filepath):
    file_path = Path(filepath)
    rel_path = file_path.relative_to(project_root).with_suffix("")
    parts = rel_path.parts

    if parts[-1] == "__init__":
        parts = parts[:-1]

    module_name = ".".join(parts)
    assert module_name, f"Empty module name for {filepath}"

    sys.path.insert(0, str(project_root))
    try:
        importlib.import_module(module_name)
    finally:
        sys.path.pop(0)
