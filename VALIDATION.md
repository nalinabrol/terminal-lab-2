# Lab 2 validation

Prepared on 9 September 2026. The repository remains private.

## Local checks

- Four IDs (A017, B104, C233, student-42) complete the real Bash file workflows at
  16/16 checks each. The verification solver reads generated evidence and uses
  sort, uniq, cut and diff to produce the required results.
- Wrong challenge participant lists, incorrect counts, archived collection
  instructions and modified original evidence are rejected for each variant.
- The checker leaves all file bytes unchanged. Existing-attempt creation is refused
  without overwriting files, and invalid IDs are rejected before creating a folder.
- Isolated terminal checks pass for Bash history filtering, Ctrl+R, older matching
  commands, accepting/editing before execution and Ctrl+G cancellation; actual nano
  editing/saving; and less searching, next/previous matches and source preservation.
- The practice ZIP contains exactly start.sh, setup.py and check.py in one
  terminal-lab-2 folder; archive integrity and byte-for-byte agreement were checked.
- Python, Bash, JSON and startup-extension JavaScript syntax checks pass.
- Student booklet: 13 A4 pages. All pages were rendered with Poppler and visually
  inspected; the revised sorting page was rendered and inspected again. Page numbers,
  headings, code blocks and answer spaces fit the intended page plan.

## Scope of this evidence

Interactive terminal automation tests the actual programs. Browser UI verification
and the current GitHub Actions result are recorded after repository publication.
No student classroom pilot has been performed, so the approximately 100-minute
duration remains an estimate. The checker verifies results, not authorship or whether
the student used the requested interactive tool.
