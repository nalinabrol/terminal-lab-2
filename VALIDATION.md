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

## Linux and Codespace checks

- GitHub Actions passed on runtime commit `2d07c8f`:
  https://github.com/nalinabrol/terminal-lab-2/actions/runs/34309481171
- In the existing Ubuntu 24.04 review Codespace, pulled `main` with a fast-forward
  update, then ran the full readiness check and interactive terminal smoke suite.
  All four 16/16 workflows and Bash/nano/less checks passed.
- Browser review confirmed the maximized Bash terminal and hidden sidebars/AI chat.
  The student-facing start.sh prompted for an ID and created DEMO-LAB2 under
  `/workspaces/terminal-lab-2/lab-work/lab2-DEMO-LAB2`. It is an unsolved review attempt.
- Browser key injection did not visibly trigger Ctrl+R. Actual Ctrl+R/Ctrl+G bytes
  passed in isolated Bash terminals inside the Codespace, but this is not a claim
  that every browser/physical-keyboard combination was tested. The instructor guide
  includes a browser shortcut preflight and the history-list fallback.

## Scope of this evidence

Interactive terminal automation tests the actual programs. Browser startup and the
student setup flow were also checked as described above.
No student classroom pilot has been performed, so the approximately 100-minute
duration remains an estimate. The checker verifies results, not authorship or whether
the student used the requested interactive tool.
