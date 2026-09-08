#!/usr/bin/env python3
"""Check required text-tool behaviour using disposable files, not student work."""
from pathlib import Path
import subprocess
import tempfile


def run(*args, input=None):
    return subprocess.run(args, input=input, text=True, capture_output=True, check=True).stdout


def main():
    # ASCII fixtures give the same ordering across typical classroom locales.
    assert run('sort', '-n', input='100\n2\n10\n') == '2\n10\n100\n'
    names = run('sort', input='Mira\nAsha\nMira\n')
    assert run('uniq', input=names) == 'Asha\nMira\n'
    counts = [line.split() for line in run('uniq', '-c', input=names).splitlines()]
    assert counts == [['1', 'Asha'], ['2', 'Mira']]
    assert run('cut', '-d', '|', '-f', '2', input='A01|Asha|Art\n') == 'Asha\n'
    with tempfile.TemporaryDirectory(prefix='lab2-preflight-') as folder:
        original = Path(folder) / 'original.txt'
        revised = Path(folder) / 'revised.txt'
        original.write_text('Room A\n')
        revised.write_text('Room B\n')
        same = subprocess.run(['diff', str(original), str(original)], capture_output=True)
        different = subprocess.run(['diff', str(original), str(revised)], capture_output=True)
        assert same.returncode == 0 and not same.stdout
        assert different.returncode == 1 and different.stdout
    print('Numeric sorting, duplicate counts, field extraction, and file comparison: passed.')


if __name__ == '__main__':
    main()
