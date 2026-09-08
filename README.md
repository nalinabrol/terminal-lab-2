# Lab 2 — Terminal tools

[Open your Lab 2 Codespace](https://codespaces.new/nalinabrol/terminal-lab-2?quickstart=1)

Sign in with your own GitHub account and create your own Codespace on `main`.
Resume that same Codespace for later sessions. This repository is separate from Lab 1.

## Current status

The development environment is configured. The exercise plan is in [LAB_PLAN.md](LAB_PLAN.md).
The final exercises, student data generator, checker, and PDF have not been authored yet.

## First launch

1. Follow the Codespace link above and wait for setup to finish.
2. Accept **Trust Folder & Continue** if prompted for this course repository.
3. A maximized Bash terminal should open automatically after extension activation.
4. Check the environment at any time with `bash scripts/verify_environment.sh`.

If necessary, use the Command Palette command **Lab 2: Focus Bash Terminal**.
The startup extension focuses the terminal without typing commands or resetting work.

## Topics

- Command history: `history`, filtering history, Ctrl+R, editing recalled commands, Ctrl+G.
- Editing text: `nano`.
- Navigating long documents: `less`.
- Sorting text and numbers: `sort`.
- Removing and counting duplicates: `uniq`.
- Extracting fields: `cut`.
- Comparing file versions: `diff`.

Permissions and environment variables are reserved for classroom teaching.
Lab 1 commands support the new exercises without repeating their introductory lessons.

## Environment

Ubuntu 24.04 devcontainer, Bash, Python 3, nano, less, GNU coreutils, diffutils,
grep, and manual pages. Required tools and text-processing behaviours are checked
automatically during container creation and through GitHub Actions.

Workspace defaults hide the editor/sidebar and disable AI chat, Copilot completions,
next-edit suggestions, and inline suggestions. Students can change these settings;
they are classroom defaults, not an enforcement mechanism.

Future student attempts will use the ignored `lab-work/` folder. Shell history is
the student's own interactive Bash history; setup does not seed or clear it.
Interactive history search will be verified during the exercise using commands
students type themselves. History persistence across terminal sessions is outside
the current lab scope.
