#!/usr/bin/env bash
set -euo pipefail
lab_repository="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$lab_repository"
for lab_command in bash python3 nano less sort uniq cut diff grep cat head tail wc find; do
    command -v "$lab_command" >/dev/null || { printf 'Missing: %s\n' "$lab_command" >&2; exit 1; }
done
[[ "$(type -t history)" == builtin ]] || { printf 'Bash history is unavailable.\n' >&2; exit 1; }
python3 -B scripts/verify_tools.py
bash -n terminal-lab-2/start.sh
python3 -B verify_lab.py
printf '\nLab 2 environment is ready.\n'
printf 'Topics: history and search, nano, less, sort, uniq, cut, diff.\n'
printf 'Start: bash terminal-lab-2/start.sh\n'
printf 'Use your assigned lab ID, then follow the printed cd command and the booklet.\n'
