"""Run the archived checks and compare all non-timing results with the baseline.

From repository root: python code/reproduce.py [--with-milp]
Generated outputs are kept apart from the archived results.
"""
import argparse
import json
import platform
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
def normalized(value):
    if isinstance(value, dict):
        return {k: normalized(v) for k,v in value.items() if k != 'seconds'}
    if isinstance(value, list):
        return [normalized(v) for v in value]
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-milp', action='store_true')
    args = parser.parse_args()
    out = ROOT/'results'/'rerun'
    out.mkdir(exist_ok=True)
    pairs = [('verify107.py','verification107.json'),
             ('exhaustive107.py','exhaustive107_results.json')]
    if args.with_milp:
        pairs.append(('independent_milp_check.py','independent_milp_results.json'))
    report = {'started_at':datetime.now(timezone.utc).isoformat(),
              'python':sys.version, 'platform':platform.platform(),
              'random_seeds':{'verify107':107,'independent_milp_check':20261012},
              'comparisons':[]}
    if args.with_milp:
        import numpy, scipy
        report['dependencies']={'numpy':numpy.__version__,'scipy':scipy.__version__}
    for script, name in pairs:
        run = subprocess.run([sys.executable,str(ROOT/'code'/script)],cwd=out,
                             capture_output=True,text=True)
        (out/(script+'.log')).write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError(f'{script} failed; see results/rerun/{script}.log')
        actual=json.loads((out/name).read_text())
        expected=json.loads((ROOT/'results'/name).read_text())
        if normalized(actual)!=normalized(expected):
            raise AssertionError(f'{name}: non-timing results differ from baseline')
        report['comparisons'].append({'script':script,'output':name,
                                     'all_non_timing_fields_match':True})
        print(script+': all non-timing results match',flush=True)
    report['ended_at']=datetime.now(timezone.utc).isoformat()
    (out/'release_verification.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    main()
