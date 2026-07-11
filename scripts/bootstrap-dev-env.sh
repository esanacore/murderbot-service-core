#!/usr/bin/env bash
# Set up a local development environment for murderbot-core.
# Safe to re-run. Does not touch any hardware or PiKVM configuration -
# see AGENTS.md rule 3.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICES_DIR="${REPO_ROOT}/services"

cd "${SERVICES_DIR}"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip >/dev/null
pip install -e ".[dev]"

if command -v pre-commit >/dev/null 2>&1; then
  (cd "${REPO_ROOT}" && pre-commit install)
else
  echo "pre-commit not found on PATH after install; check services/.venv/bin is on PATH" >&2
fi

echo "Dev environment ready. Activate with: source ${SERVICES_DIR}/.venv/bin/activate"
