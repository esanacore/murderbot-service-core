# AGENTS.md — Rules for coding/repository agents

This file governs any AI coding agent (and is a useful checklist for human
contributors too) working in this repository. It supersedes generic
helpfulness with project-specific safety rules, because this project
controls real electrical hardware attached to a live desktop PC.

## Governance: Eric's Engineering Constitution

This repository also follows
[Eric's Engineering Constitution](constitution/CONSTITUTION.md) (installed
as the read-only `constitution/` submodule — never edit files inside it
directly). Where the constitution's universal defaults and this file's
project-specific rules conflict, **this file wins**
(`constitution/INTEGRATION.md`). Before making changes, also read:

- `constitution/CONSTITUTION.md` — universal principles
- `constitution/AI_WORKFLOW.md` — required step-by-step workflow
- `constitution/TESTING.md`, `constitution/DOCUMENTATION.md`, `constitution/SECURITY.md`
- `TODO.md`, `CHANGELOG.md` — for project context, alongside the docs below

**Project-specific override**: this repository's Architecture Decision
Records live in [`docs/decisions/`](docs/decisions/), not the
constitution's default `docs/adr/` — see
[`docs/adr/0001-record-architecture-decisions.md`](docs/adr/0001-record-architecture-decisions.md)
for why. `docs/adr/` exists only as a pointer.

**gstack skill note**: `CLAUDE.md` (installed by the constitution
bootstrap) references gstack skills (`/browse`, `/setup-gbrain`, etc.).
These require gstack to be installed in the agent's environment
separately — if they aren't available, fall back to this repository's own
tools/skills rather than blocking on them.

## Project purpose (short form)

Murderbot Service Core (MSC) is an internal Raspberry Pi 4–based management
controller for a desktop PC (MSI Z490-A PRO, RTX 4080). It combines DIY
PiKVM, optoisolated ATX power/reset control, startup audio, addressable
RGB, and optional host telemetry, and — over time — grows toward
iDRAC/iLO-style enterprise management features (REST API, web dashboard,
plugin architecture, OTA updates). **PiKVM is the critical service.**
Custom personality features must remain isolated so they cannot disable
KVM, remote ATX control, or recovery. See `docs/architecture.md`.

## Working rules

1. **Do not invent verified hardware pinouts, PSU capacities, GPIO
   assignments, or measured values.** Mark unknowns as `TBD` in the
   relevant doc and create/update a backlog entry in `docs/backlog.md`.
2. **Do not commit copyrighted soundtrack files, credentials, keys,
   passwords, tokens, or machine-specific secrets.** See `assets/README.md`
   and `.gitignore`.
3. **Do not make live PiKVM system changes** (system packages, boot
   configuration, firewall rules, authentication) **unless the task
   explicitly authorizes deployment**, and always with a documented
   rollback procedure. Default to repository scaffolding and testable code.
4. **Keep the physical power, ATX, RGB, audio, and capture domains
   separate** in both documentation and software — see the failure-domain
   table in `docs/architecture.md`. A crash in `murderbot-rgb` or
   `murderbot-audio` must never be able to affect PiKVM or ATX control.
5. **Use safe defaults**: ATX outputs open (no asserted switch state after
   a crash), RGB off, audio muted, brightness limited, and any optional
   hardware disabled unless explicitly configured.
6. **Update documentation, tests, the BOM, and backlog with every
   meaningful change.** A hardware change without an updated
   `hardware/bom.csv` row, wiring note, and (if architectural) ADR is
   incomplete.
7. **Make small, reviewable commits** and preserve a clear rollback path.
   Prefer several small PRs to one large one.
8. **Hardware-facing code must sit behind an interface** (`Protocol` /
   ABC) with a mock implementation, so `pytest` runs with no Raspberry Pi
   attached. See `services/src/murderbot_core/hardware/`.
9. **Phased scope discipline**: do not implement Phase 2+ features (RGB,
   OLED, telemetry, REST API, dashboard, OTA, AI personality) as anything
   more than interface stubs until the prerequisite phase's acceptance
   criteria (`docs/requirements.md`) are met. See `ROADMAP.md`.

## Definition of done (per change)

A change is done when:

- [ ] Code has type hints and passes `ruff` + `mypy` (`services/`).
- [ ] New/changed behavior has a `pytest` test, and the full suite passes.
- [ ] Hardware-facing changes reference real interfaces (Protocol/ABC) with
      a mock used in tests — no untested hardware branches.
- [ ] Relevant `docs/*.md` is updated (architecture, requirements, power,
      wiring, software, testing, security, as applicable).
- [ ] `hardware/bom.csv` is updated if a physical part was added/changed.
- [ ] `CHANGELOG.md` has an `[Unreleased]` entry.
- [ ] No secrets, credentials, or copyrighted media were added (spot-check
      diff, not just filenames).
- [ ] If an architectural decision changed, a new/updated ADR exists in
      `docs/decisions/`.
- [ ] `TODO.md` reflects discovered work and completed roadmap items
      (`constitution/CONSTITUTION.md` Principle 3).

## Non-goals reminder (first release, i.e. through end of Phase 4/5)

- Capturing/streaming the RTX 4080 gaming output at native 4K.
- Replacing motherboard fan control, PSU protection, or any safety-critical
  PC function.
- Exposing PiKVM directly to the public internet without VPN or equivalent.
- A custom production PCB before the bench prototype and pin allocation are
  proven (`electronics/` stays placeholder/KiCad-schematic-only until then).
- Sharing a failure domain between lighting/personality code and the core
  KVM service.

See also the original engineering report's own agent bootstrap section
(preserved for reference/history) and `ROADMAP.md` for how the broader,
multi-year vision in `agent_instructions.md` was reconciled with these
narrower first-release rules.
