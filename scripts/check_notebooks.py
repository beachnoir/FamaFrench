"""Check committed notebook structure, executable syntax and successful outputs."""
import ast
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
for path in sorted(ROOT.glob('[0-9][0-9]_*.ipynb')):
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)
    expected = 0
    for cell in nb.cells:
        if cell.cell_type != 'code' or not cell.source.strip():
            continue
        ast.parse(cell.source, filename=path.name)
        expected += 1
        if cell.execution_count != expected:
            raise ValueError(f'{path.name}: missing or out-of-order execution count at cell {expected}')
        if any(o.output_type == 'error' for o in cell.outputs):
            raise ValueError(f'{path.name}: saved execution error')
    print(f'{path.name}: valid, {expected} executed code cells, no saved errors')
