# Workstation Setup

How to set up a local environment and run the hardware-independent part of
this project. There is no hardware bring-up procedure here — see
[`pikvm-setup.md`](pikvm-setup.md) and [`../ROADMAP.md`](../ROADMAP.md) for
that once you're at Phase 0/1 with real hardware in hand.

## Prerequisites

- Python 3.11+
- `git` (with submodule support — this repo carries the constitution as a
  submodule, see `../constitution/`)

No `.nvmrc`/`.tool-versions`/`.python-version` pin exists yet;
`services/pyproject.toml`'s `requires-python = ">=3.11"` is the source of
truth.

## Verify Prerequisites

```bash
python3 --version   # must be 3.11 or newer
git --version
git submodule status # should list constitution, not "-<hash>" (uninitialized)
```

## Installation

```bash
git clone --recurse-submodules git@github.com:esanacore/murderbot-service-core.git
cd murderbot-service-core

# If you cloned without --recurse-submodules:
git submodule update --init

bash scripts/bootstrap-dev-env.sh
```

`scripts/bootstrap-dev-env.sh` creates `services/.venv`, installs
`murderbot-core` in editable mode with dev dependencies, and installs the
pre-commit hooks. See [`../scripts/README.md`](../scripts/README.md).

## First Run

There is no runnable service yet (`docs/software.md` "What's implemented
today vs. planned") — only the library and its test suite:

```bash
source services/.venv/bin/activate
cd services && pytest
```

## Environment Variables

None are used today. Real, machine-specific configuration (PiKVM secrets,
Wi-Fi credentials) is never stored in this repository or in a `.env` file
here — see [`security.md`](security.md) and [`../.gitignore`](../.gitignore).
