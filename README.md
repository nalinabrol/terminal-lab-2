# Lab 2 — Terminal tools

[Open your Lab 2 Codespace](https://codespaces.new/nalinabrol/terminal-lab-2?quickstart=1)

This repository is private. Students need repository access before this link will
work. Sign in with your own GitHub account and create a Codespace on `main`, or
resume your existing Lab 2 Codespace. Lab 1 uses a separate repository.

## Start the lab

1. Wait for setup. Accept **Trust Folder & Continue** if asked.
2. A maximized Bash terminal opens after startup. If needed, use the Command
   Palette command **Lab 2: Focus Bash Terminal**.
3. At the repository root, run `bash terminal-lab-2/start.sh`.
4. Enter your instructor-assigned ID, run the exact `cd` command printed by setup,
   then run `pwd` and `cat identity.txt`.
5. Follow the [student booklet](Lab_2_Terminal_Tools_Student_Booklet.pdf).

Setup preserves existing attempts. Generated work stays in the ignored `lab-work/`
folder. Keep your Codespace and attempts for instructor review.

## Materials

- [Student booklet PDF](Lab_2_Terminal_Tools_Student_Booklet.pdf): 13 A4 pages,
  seven experiments, independent challenge, answer spaces, hints and reference.
- [Booklet text](Lab_2_Terminal_Tools_Student_Booklet.md): searchable text counterpart.
- [Practice kit ZIP](Lab_2_Terminal_Tools_Practice_Kit.zip): the same three runtime
  files already included in `terminal-lab-2/`; no download is needed in Codespaces.
- [Instructor guide](INSTRUCTOR_GUIDE.md): timing, setup, facilitation and answer checks.
- [Page plan](LAB_PLAN.md): the implemented structure and scope.

Topics: history and history search, nano, less, sort, uniq, cut, and diff.
Permissions and environment-variable lessons are reserved for class.

## Check saved work

From your `lab-work/lab2-ID` folder:

```bash
python3 ../../terminal-lab-2/check.py
```

The checker reads 15 result files and checks preservation of original evidence
(16 checks). It does not repair, upload or submit work. Written explanations and
interactive demonstrations remain part of the lab.

## Environment and validation

Ubuntu 24.04, Bash, Python 3, nano, less, GNU coreutils, diffutils, grep and manual
pages. The runtime uses Python's standard library and normal shell commands.

```bash
bash scripts/verify_environment.sh
python3 -B scripts/interactive_smoke.py
```

The first command validates tools and all four student variants in temporary
folders. The second checks Bash history, nano and less in isolated terminals.
Neither modifies student attempts. Both run in GitHub Actions.

Workspace defaults hide sidebars and disable AI chat and suggestions; students can
change them. The startup extension does not type commands or erase history.

## Authoring

`build_booklet.py` builds the PDF and Markdown using ReportLab. It uses Arial on
macOS or DejaVu fonts on Linux (install `fonts-dejavu-core` when needed). Render and
inspect all 13 pages after layout/content edits. `verify_lab.py` independently checks
file workflows. Generator, checker and verification source are visible practice
materials, not exam security mechanisms. See [validation evidence](VALIDATION.md).
