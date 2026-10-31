"""Execute each notebook in a fresh kernel and save only successful results."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of', required=True, help='Observation cutoff YYYY-MM-DD (not a historical source vintage)')
    parser.add_argument('--offline', action='store_true', help='Require the matching cached snapshot')
    parser.add_argument('--notebooks', nargs='*', help='Optional notebook filenames; default all six')
    args = parser.parse_args()
    os.environ['ANALYSIS_AS_OF'] = args.as_of
    os.environ['ANALYSIS_OFFLINE'] = '1' if args.offline else '0'
    os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
    os.environ.setdefault('MPLCONFIGDIR', '/tmp/famafrench-matplotlib')
    paths = [ROOT / p for p in args.notebooks] if args.notebooks else sorted(ROOT.glob('[0-9][0-9]_*.ipynb'))
    report = {'as_of': args.as_of, 'python': sys.version, 'offline': args.offline,
              'packages': {p: importlib.metadata.version(p) for p in ['numpy','pandas','scipy','statsmodels','yfinance','matplotlib','nbclient','nbformat']}, 'notebooks': []}
    report_dir = ROOT / '.local' / 'reports'
    report_dir.mkdir(parents=True, exist_ok=True)
    destination = report_dir / f'execution_{args.as_of}.json'
    started = time.monotonic()
    for path in paths:
        print(f'Executing {path.name} ...', flush=True)
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        before = time.monotonic()
        km = KernelManager(kernel_name='python3')
        km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
        try:
            NotebookClient(nb, km=km, timeout=600, resources={'metadata': {'path': str(ROOT)}}, allow_errors=False).execute()
            nbformat.validate(nb)
            nbformat.write(nb, path)
        except Exception as exc:
            report['notebooks'].append({'file': path.name, 'status': 'failed', 'error': str(exc), 'seconds': round(time.monotonic()-before,2)})
            destination.write_text(json.dumps(report, indent=2)+'\n')
            raise
        finally:
            if km.has_kernel:
                km.shutdown_kernel(now=True)
        record = {'file': path.name, 'status': 'passed', 'code_cells': sum(c.cell_type=='code' for c in nb.cells),
                  'seconds': round(time.monotonic()-before,2), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        report['notebooks'].append(record)
        destination.write_text(json.dumps(report, indent=2)+'\n')
        print(f'  Passed in {record["seconds"]}s', flush=True)
    report['total_seconds'] = round(time.monotonic()-started,2)
    destination.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Execution report: {destination}', flush=True)

if __name__ == '__main__':
    main()
