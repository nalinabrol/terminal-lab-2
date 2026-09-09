#!/usr/bin/env python3
"""Exercise real shell workflows and failure cases in temporary student attempts."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'terminal-lab-2'))
from setup import create, make_data, valid_id
from check import check


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}


def solve(root):
    identity = dict(line.split('=', 1) for line in (root/'identity.txt').read_text().splitlines())
    notice = (root/'work/notice.txt').read_text().replace('Hall-0', identity['ROOM']).replace('08:00',identity['TIME'])
    (root/'work/notice.txt').write_text(notice + 'Bring your student card.\n')
    handbook = (root/'practice/handbook.txt').read_text().splitlines()
    active = handbook.index('COLLECTION - ACTIVE ' + identity['EVENT'])
    (root/'work/collection.txt').write_text(handbook[active+1]+'\n')
    # Editing is simulated for result validation. interactive_smoke.py separately
    # exercises actual Bash history, nano, and less in a terminal.
    (root/'work/timetable.txt').write_text((root/'work/timetable.txt').read_text().replace('09:30 Art','09:45 Art').replace('10:00 Break\n','')+'11:00 Closing\n')
    brief = (root/'challenge/brief.txt').read_text().splitlines()
    active = brief.index('APPROVAL - CURRENT ' + identity['EVENT'])
    (root/'work/challenge/announcement.txt').write_text('\n'.join(brief[active+2:active+6])+'\n')
    (root/'work/challenge/timetable.txt').write_text((root/'work/challenge/timetable.txt').read_text().replace('10:30 Design','10:45 Design').replace('11:00 Break\n','')+'12:00 Showcase\n')
    subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', '''
sort practice/names.txt > work/names-sorted.txt
sort -nr practice/scores.txt > work/scores-desc.txt
sort practice/repeated-names.txt | uniq > work/unique-names.txt
sort practice/repeated-names.txt | uniq -c > work/name-counts.txt
cut -d '|' -f 2 practice/registrations.txt > work/registration-names.txt
cut -d '|' -f 1,3 practice/registrations.txt > work/id-workshop.txt
cut -d '|' -f 3 practice/registrations.txt > work/workshops.txt
sort work/workshops.txt | uniq -c > work/workshop-counts.txt
cut -d '|' -f 2 challenge/registrations.txt | sort | uniq > work/challenge/participants.txt
cut -d '|' -f 3 challenge/registrations.txt > work/challenge/workshops.txt
sort work/challenge/workshops.txt | uniq -c > work/challenge/workshop-counts.txt
diff challenge/schedule-before.txt challenge/schedule-approved.txt > work/challenge/schedule-diff.txt || test "$?" -eq 1
diff work/timetable.txt practice/timetable-approved.txt
diff work/challenge/timetable.txt challenge/schedule-approved.txt
'''], cwd=root, check=True)


def main():
    with tempfile.TemporaryDirectory(prefix='lab2-verification-') as temp:
        for sid in ['A017', 'B104', 'C233', 'student-42']:
            root = Path(temp)/('lab2-'+sid)
            create(sid, root)
            assert len(check(root,sid)) == 16
            assert not all(passed for _,passed in check(root,sid))
            solve(root)
            before = snapshot(root)
            results = check(root,sid)
            assert all(passed for _,passed in results), results
            assert snapshot(root) == before, 'Checker mutated files'
            subprocess.run([sys.executable, '-B', str(ROOT/'terminal-lab-2/check.py')],cwd=root,check=True,stdout=subprocess.DEVNULL)
            try:
                create(sid,root)
            except FileExistsError:
                pass
            else:
                raise AssertionError('Repeat setup replaced an attempt')
            assert snapshot(root) == before
            wrong = root/'work/challenge/participants.txt'
            wrong.write_text(wrong.read_text() + 'OTHER_PERSON\n')
            assert not dict(check(root,sid))['work/challenge/participants.txt']
            wrong.write_bytes(before['work/challenge/participants.txt'])
            counts = root/'work/workshop-counts.txt'
            counts.write_text('999 Art\n')
            assert not dict(check(root,sid))['work/workshop-counts.txt']
            counts.write_bytes(before['work/workshop-counts.txt'])
            collection = root/'work/collection.txt'
            collection.write_text('Collect badges at Desk-0 at 08:00.\n')
            assert not dict(check(root,sid))['work/collection.txt']
            collection.write_bytes(before['work/collection.txt'])
            original = root/'practice/scores.txt'
            original.write_text('2\n')
            assert not dict(check(root,sid))['Original evidence files preserved']
            original.write_bytes(before['practice/scores.txt'])
            assert all(passed for _,passed in check(root,sid))
            print(f'{sid}: 16/16; wrong participant/count/instruction and changed original rejected; repeat setup and read-only checks passed.')
        for sid in ['', '../escape', 'a/b', 'a b', '-wrong', 'A'*25]:
            assert not valid_id(sid)
            try:
                create(sid,Path(temp)/'invalid')
            except ValueError:
                pass
            else:
                raise AssertionError('Invalid ID accepted')
        assert not (Path(temp)/'invalid').exists()
    print('All four variants and invalid-ID checks passed.')


if __name__ == '__main__':
    main()
