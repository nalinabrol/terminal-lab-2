#!/usr/bin/env python3
"""Deterministic fictional lab data; an existing attempt is never overwritten."""
import hashlib
import re
import shlex
import sys
from pathlib import Path


def valid_id(value):
    return re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,23}', value) is not None


def make_data(student_id):
    if not valid_id(student_id):
        raise ValueError('Use 1-24 letters/digits, hyphens or underscores; begin with a letter/digit.')
    digest = hashlib.sha256(student_id.encode()).hexdigest()
    seed = int(digest[:8], 16)
    event = 'EV' + digest[:6].upper()
    room = 'Hall-' + str(1 + seed % 8)
    time = ['09:15', '09:30', '09:45'][seed % 3]
    desk = 'Desk-' + str(1 + seed % 6)
    collection = 'Collect badges at ' + desk + ' at ' + time + '.'
    names = ['Asha', 'Dev', 'Ira', 'Mira', 'Neel', 'Zoya']
    offset = seed % len(names)
    names = names[offset:] + names[:offset]
    repeated = [names[0], names[0], names[1], names[2], names[1], names[0], names[3]]
    if seed % 2:
        repeated += [names[2]]
    registrations = [f'S{i+1:02d}|{name}|{["Art", "Code", "Music"][i % 3]}' for i, name in enumerate(repeated)]
    challenge_names = [names[4], names[1], names[4], names[5], names[1], names[0], names[5], names[4]]
    if seed % 3:
        challenge_names.append(names[0])
    challenge_rows = [f'R{i+1:02d}|{name}|{["Design", "Robotics", "Writing"][i % 3]}' for i, name in enumerate(challenge_names)]
    approved_notice = f'Event: {event}\nRoom: {room}\nDoors open: {time}\nBring your student card.\n'
    draft_notice = f'Event: {event}\nRoom: Hall-0\nDoors open: 08:00\n'
    old = '09:00 Welcome\n09:30 Art\n10:00 Break\n10:30 Music\n'
    new = '09:00 Welcome\n09:45 Art\n10:30 Music\n11:00 Closing\n'
    c_old = '10:00 Welcome\n10:30 Design\n11:00 Break\n11:30 Robotics\n'
    c_new = '10:00 Welcome\n10:45 Design\n11:30 Robotics\n12:00 Showcase\n'
    handbook = [f'{i:03d} General event preparation note {i}.' for i in range(1, 111)]
    handbook[12:15] = ['COLLECTION - ARCHIVED', 'Collect badges at Desk-0 at 08:00.', 'This instruction is outdated.']
    handbook[57:60] = ['COLLECTION - ACTIVE ' + event, collection, 'This is the approved instruction for your event.']
    handbook[92:95] = ['COLLECTION - OTHER EVENT', 'Collect badges at Desk-9 at 16:00.', 'This instruction is for another event.']
    brief = [f'{i:03d} Challenge preparation note {i}.' for i in range(1, 91)]
    brief[15:20] = ['APPROVAL - OLD', 'Event: OLD', 'Room: Hall-0', 'Doors open: 07:00', 'Do not use this archived notice.']
    brief[62:68] = ['APPROVAL - CURRENT ' + event, 'Use these four lines for the final announcement:', *approved_notice.rstrip().splitlines()]
    files = {
        'identity.txt': f'LAB_ID={student_id}\nEVENT={event}\nROOM={room}\nTIME={time}\n',
        'practice/notice-original.txt': draft_notice,
        'practice/handbook.txt': '\n'.join(handbook) + '\n',
        'practice/names.txt': '\n'.join(reversed(names)) + '\n',
        'practice/scores.txt': '100\n2\n25\n10\n8\n',
        'practice/repeated-names.txt': '\n'.join(repeated) + '\n',
        'practice/registrations.txt': '\n'.join(registrations) + '\n',
        'practice/timetable-before.txt': old,
        'practice/timetable-approved.txt': new,
        'challenge/brief.txt': '\n'.join(brief) + '\n',
        'challenge/announcement-draft.txt': draft_notice,
        'challenge/registrations.txt': '\n'.join(challenge_rows) + '\n',
        'challenge/schedule-before.txt': c_old,
        'challenge/schedule-approved.txt': c_new,
        'work/notice.txt': draft_notice,
        'work/timetable.txt': old,
        'work/challenge/announcement.txt': draft_notice,
        'work/challenge/timetable.txt': c_old,
    }
    return files


def create(student_id, destination):
    files = make_data(student_id)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for relative, content in files.items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    return destination


def main():
    student_id = input('Enter your instructor-assigned lab ID (not your email): ').strip()
    if not valid_id(student_id):
        sys.exit('Invalid ID. Use 1-24 letters/digits, hyphens or underscores; begin with a letter/digit.')
    destination = Path(__file__).resolve().parent.parent / 'lab-work' / ('lab2-' + student_id)
    if destination.is_symlink():
        sys.exit('This attempt path is a symbolic link. Ask your instructor for a new ID.')
    try:
        create(student_id, destination)
    except FileExistsError:
        if not destination.is_dir():
            sys.exit('The attempt path is not a folder. Ask your instructor for a new ID.')
        print('This attempt already exists. Your work has been preserved.')
    print('\nEnter your lab folder with this exact command:')
    print('cd ' + shlex.quote(str(destination)))
    print('\nThen run: pwd')
    print('Then run: cat identity.txt')
    print('Follow the Lab 2 booklet. No commands have been added to your shell history.')


if __name__ == '__main__':
    main()
