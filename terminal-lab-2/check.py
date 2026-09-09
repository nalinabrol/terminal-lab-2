#!/usr/bin/env python3
"""Read-only feedback on saved results; does not prove authorship or tool use."""
from collections import Counter
import difflib
from pathlib import Path
import sys
from setup import make_data, valid_id


def expected_results(student_id):
    source = make_data(student_id)
    identity = dict(line.split('=', 1) for line in source['identity.txt'].splitlines())
    notice = f'Event: {identity["EVENT"]}\nRoom: {identity["ROOM"]}\nDoors open: {identity["TIME"]}\nBring your student card.\n'
    handbook = source['practice/handbook.txt'].splitlines()
    collection = handbook[handbook.index('COLLECTION - ACTIVE ' + identity['EVENT']) + 1] + '\n'
    lines = lambda key: source[key].splitlines()
    text = lambda values: '\n'.join(values) + '\n'
    results = {
        'work/notice.txt': notice,
        'work/collection.txt': collection,
        'work/names-sorted.txt': text(sorted(lines('practice/names.txt'))),
        'work/scores-desc.txt': text(sorted(lines('practice/scores.txt'), key=int, reverse=True)),
        'work/unique-names.txt': text(sorted(set(lines('practice/repeated-names.txt')))),
        'work/name-counts.txt': Counter(lines('practice/repeated-names.txt')),
        'work/registration-names.txt': text(row.split('|')[1] for row in lines('practice/registrations.txt')),
        'work/id-workshop.txt': text('|'.join([row.split('|')[0], row.split('|')[2]]) for row in lines('practice/registrations.txt')),
        'work/workshop-counts.txt': Counter(row.split('|')[2] for row in lines('practice/registrations.txt')),
        'work/timetable.txt': source['practice/timetable-approved.txt'],
        'work/challenge/announcement.txt': notice,
        'work/challenge/participants.txt': text(sorted({row.split('|')[1] for row in lines('challenge/registrations.txt')})),
        'work/challenge/workshop-counts.txt': Counter(row.split('|')[2] for row in lines('challenge/registrations.txt')),
        'work/challenge/timetable.txt': source['challenge/schedule-approved.txt'],
    }
    return source, results


def counts_match(actual, expected):
    parsed = {}
    try:
        for line in actual.splitlines():
            count, value = line.split(maxsplit=1)
            if value in parsed or int(count) < 1:
                return False
            parsed[value] = int(count)
    except (ValueError, TypeError):
        return False
    return parsed == dict(expected)


def normal_diff(before, after):
    """GNU/BSD normal diff format for these simple, uniquely anchored schedules."""
    a, b = before.splitlines(), after.splitlines()
    output = []
    span = lambda start, stop: str(start + 1) if stop - start == 1 else f'{start + 1},{stop}'
    for kind, i, j, k, l in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if kind == 'equal':
            continue
        if kind == 'replace':
            output += [span(i, j) + 'c' + span(k, l)] + ['< ' + v for v in a[i:j]] + ['---'] + ['> ' + v for v in b[k:l]]
        elif kind == 'delete':
            output += [span(i, j) + 'd' + str(k)] + ['< ' + v for v in a[i:j]]
        else:
            output += [str(i) + 'a' + span(k, l)] + ['> ' + v for v in b[k:l]]
    return '\n'.join(output) + '\n'


def check(root, student_id):
    root = Path(root)
    source, expected = expected_results(student_id)
    expected['work/challenge/schedule-diff.txt'] = normal_diff(source['challenge/schedule-before.txt'], source['challenge/schedule-approved.txt'])
    results = []
    for relative, wanted in expected.items():
        path = root / relative
        try:
            actual = path.read_text(encoding='utf-8') if not path.is_symlink() else None
            ok = counts_match(actual, wanted) if isinstance(wanted, Counter) and actual is not None else actual == wanted
        except (OSError, UnicodeError):
            ok = False
        results.append((relative, bool(ok)))
    preserved = True
    for relative, content in source.items():
        if relative.startswith('work/'):
            continue
        path = root / relative
        try:
            preserved &= not path.is_symlink() and path.read_bytes() == content.encode()
        except OSError:
            preserved = False
    results.append(('Original evidence files preserved', bool(preserved)))
    return results


def main():
    root = Path.cwd()
    if not root.name.startswith('lab2-') or not valid_id(root.name[5:]):
        sys.exit('Run this checker from your lab-work/lab2-ID folder, as shown by setup.')
    results = check(root, root.name[5:])
    for label, passed in results:
        print(('PASS  ' if passed else 'CHECK ') + label)
    score = sum(passed for _, passed in results)
    print(f'\n{score}/{len(results)} file checks passed. No files were changed or submitted.')
    print('Also complete your written answers and demonstrate history, nano, and less to your instructor.')
    return 0 if score == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
