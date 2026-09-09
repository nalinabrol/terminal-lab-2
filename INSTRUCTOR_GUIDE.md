# Lab 2 instructor guide

## Purpose

Students find earlier commands, edit notices, navigate long documents, sort records,
count duplicates, extract fields and compare versions. Familiar navigation and
redirection support the new tasks. Permissions, environment variables, processes,
archives and substantive scripting remain outside this lab.

The campus-event records are fictional and original. No student personal information
is required. Names identify fictional participants within each small dataset.

## Before class

1. `nalinabrol/terminal-lab-2` is private. Arrange intended students' access before
   distributing the Codespace link. Do not change visibility without the owner's instruction.
2. Have students create or resume their own Lab 2 Codespaces before the timed session.
   First sign-in, access and container-build time are outside the teaching clock.
3. Print the student PDF at actual size: 13 A4 pages, seven sheets when duplex with
   long-edge binding. The final reverse side can remain blank.
4. Run `bash scripts/verify_environment.sh` and `python3 -B scripts/interactive_smoke.py`
   at the Codespace repository root. Tests use temporary files and isolated terminals.
5. Create a review attempt using `bash terminal-lab-2/start.sh` and an unused demo ID.
   Run its printed cd command; confirm pwd, identity.txt and nano work/notice.txt.
6. In the browser terminal, sample Control+R, an older match, Right Arrow to accept
   for editing, and Control+G to cancel. On Mac use Control, not Command.
7. Assign unique short IDs, such as A017: 1–24 ASCII letters/digits, hyphens or
   underscores, beginning with a letter/digit. IDs are case-sensitive; do not use emails.

The student launch link is https://codespaces.new/nalinabrol/terminal-lab-2?quickstart=1.
The instructor review URL is not a substitute for students' own Codespaces.

## Timing: 98 minutes, approximately 100

| Minutes | Pages | Activity |
|---|---|---|
| 0–5 | 1 | Setup and identity |
| 5–13 | 2 | History and history search |
| 13–23 | 3 | nano |
| 23–31 | 4 | less |
| 31–41 | 5 | sort |
| 41–51 | 6 | uniq |
| 51–61 | 7 | cut |
| 61–71 | 8 | diff |
| 71–88 | 9–10 | Independent challenge and evidence |
| 88–98 | 11 | Checker, correction and exit questions |
| As needed | 12–13 | Hints and reference |

These are planning estimates, not student-pilot measurements. Demonstrations are
included. For a strict 90-minute slot, shorten whole-class demonstrations by five
minutes and the exit block by three, sampling live checks during the session.
Do not silently drop a topic or the challenge.

## Facilitation and answer checks

### History

Let students type the starter commands individually. Setup does not seed or clear
history. History numbers may differ; history 10 shows at most ten remembered entries.
The filtering command may match itself because its text contains the search fragment.

Ctrl+R starts reverse incremental search; repeated Ctrl+R selects an older match.
Right Arrow accepts without execution, Enter runs, and Ctrl+G cancels and restores
prior input. Start cancellation from an empty prompt. The independent edit searches
TIME= in identity.txt. Watch the action rather than accepting a pasted command as proof.
If a browser intercepts the shortcut, first check terminal focus and the Control key;
use the history-list method while resolving the browser issue. Omit !! and !number.

### nano

The four expected lines are Event, Room, Doors open, and `Bring your student card.`
Values come from identity.txt. Preserve order, case, punctuation and the final newline.
Keep practice/notice-original.txt unchanged. Explain that ^O means Control+O, then
observe a save and reopen. Correct bytes alone cannot establish nano use.

### less

The first COLLECTION match is archived. The applicable match is COLLECTION - ACTIVE
with the student's event. work/collection.txt contains the sentence immediately below
it, including the generated desk/time and final full stop. The third match belongs to
another event. Ask students to use n and N and explain the surrounding heading.

### sort

Ordinary score order: `10, 100, 2, 25, 8`. Numeric ascending: `2, 8, 10, 25, 100`.
Required descending: `100, 25, 10, 8, 2`, one per line. The six input names are distinct
and consistently capitalized. Preserve original file order. No locale lesson is needed.

### uniq

The dataset has adjacent and separated duplicates. Sort before uniq to produce four
distinct names. Counts vary by ID: the first selected name occurs three times, the
second twice, the third once or twice, and the fourth once. Leading spaces from uniq -c
are normal. The checker accepts count padding and any count-row order, but rejects
duplicate labels and incorrect counts. Counts should sum to the original row count.

### cut

ID is field 1, name field 2, workshop field 3; there is no header. `cut -d "|" -f 2`
selects names, while `-f 1,3` keeps IDs and workshops with their delimiter. Preserve
original order and repetitions in registration-names.txt. Workshop counts count rows,
not distinct people. The simple format does not teach general CSV parsing.
work/workshops.txt is an intermediate file, not an additional graded result.

### diff

The working timetable initially matches the old version. Art changes from 09:30 to
09:45, the 10:00 Break is removed, and 11:00 Closing is added. Normal diff uses `<`
for the first file and `>` for the second; a/c/d indicate add/change/delete. After
repairing the working copy, comparison with the approved file is empty.
Instructor detail: diff exits 0 for identical files, 1 for differences and greater
than 1 for errors. Exit-code theory is not required student content.

### Challenge

All challenge inputs and working copies exist from setup, independent of guided work.

- Announcement: four lines beneath APPROVAL - CURRENT and its instruction line.
- Participants: field 2, sorted and deduplicated; five distinct names.
- Workshop counts: field 3, sorted and counted; include every registration row.
- Comparison: normal diff, before first and approved second; no flags or timestamps.
- Timetable: Design moves from 10:30 to 10:45; 11:00 Break disappears; 12:00 Showcase
  is added. The repaired-versus-approved comparison must be empty.

For exact per-ID outputs, the generator/checker and verify_lab.py reproduce them.
These are visible practice materials, not an exam-security system. Individualised
data reduces unchanged copying but does not establish independent authorship.

## Feedback and submission

From lab-work/lab2-ID, run `python3 ../../terminal-lab-2/check.py`. It verifies 15
results and preservation of original evidence (16 checks). Missing/incorrect results
print CHECK and exit nonzero. It makes no network requests, repairs or submissions.
Exact text outputs include final newlines; frequency reports tolerate padding.

Collect written observations and specify the actual class submission channel. The kit
does not invent a destination or deadline. Sample an interactive demonstration and
ask for a changed input/search term. Grade reasoning and results, not typing speed or
command brevity. Individual live checks for every learner require sufficient staff/time.

## Recovery

Re-running setup with the same ID preserves the attempt. Assign a new ID for a fresh
attempt. Do not recursively delete students' work. To restore damaged original
evidence, preserve current work and restore only the affected file from a separately
generated copy of the same ID. Check pwd and the error before diagnosing missing files.
The checker explains the expected lab root when launched from a different directory.

## Authoring and packaging

Runtime: Bash, Python standard library and listed terminal tools. Only PDF authoring
needs ReportLab and fonts (Arial on macOS, DejaVu on Linux).

```bash
python3 build_booklet.py
python3 -B verify_lab.py
python3 -B scripts/interactive_smoke.py
```

Render and inspect every page after PDF changes. The practice ZIP contains only
start.sh, setup.py and check.py under one terminal-lab-2 folder. Codespaces already
includes the kit, so students need not unpack the ZIP there. Validation evidence is
in VALIDATION.md. For command details, use installed help history, man bash and each
tool's --help output. This lab uses no copied external exercise text or datasets.
