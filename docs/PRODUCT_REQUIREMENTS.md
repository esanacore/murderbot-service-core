# Product Requirements

This document translates the project's product intent into concrete
requirements, per [Eric's Engineering Constitution](../constitution/CONSTITUTION.md)
Principle 1. It mirrors the fuller narrative in
[`requirements.md`](requirements.md) (goals, non-goals, v1.0 acceptance
criteria) using this constitution's ID/traceability format; when the two
disagree on wording, `requirements.md` is canonical for intent and this
file is canonical for the stable IDs the traceability matrix keys off.

IDs keep the original engineering report's `FR-NN` two-digit scheme
(`FR-01`...`FR-10`) rather than the constitution's suggested `FR-001`
format, since those IDs are already referenced throughout `docs/`,
`AGENTS.md`, and the PR template — introducing a second numbering scheme
for the same requirements would be actively confusing.

## Requirement Levels

- `MUST`: gates the v1.0 release (see `requirements.md` MoSCoW note).
- `SHOULD`: strongly expected; can slip a point release with an explicit
  ADR/backlog note explaining why.

## Product Summary

Murderbot Service Core (MSC) is a Raspberry Pi 4-based management
controller installed inside a desktop PC ("Murderbot"), providing
BIOS-level remote access (PiKVM), remote power/reset, startup audio,
addressable RGB, and — post-1.0 — telemetry and a plugin ecosystem. See
`../README.md` and `../ROADMAP.md`.

## Functional Requirements

### Remote management (PiKVM / ATX)

**FR-01** `MUST` The service core shall remain reachable while the PC is
off but the PSU is connected.
- Acceptance criteria: `FR-01-AC-1`: power host down; network and web UI
  remain available.

**FR-02** `MUST` The system shall provide remote keyboard, mouse, and
video suitable for BIOS/UEFI use.
- Acceptance criteria: `FR-02-AC-1`: enter firmware setup remotely and
  navigate menus.

**FR-03** `MUST` The system shall activate host power and reset through
isolated parallel connections.
- Acceptance criteria: `FR-03-AC-1`: verify local and remote controls
  independently.

**FR-04** `MUST` The startup sequence shall trigger from host main-rail
state, not merely Pi boot.
- Acceptance criteria: `FR-04-AC-1`: cold boot and soft restart tests pass.

### Failure isolation

**FR-05** `MUST` Audio and RGB faults shall not disable PiKVM or ATX
control.
- Acceptance criteria: `FR-05-AC-1`: disable each service and verify KVM
  remains functional.

### RGB / power safety

**FR-06** `MUST` NeoPixel data shall be translated from 3.3V to 5V logic.
- Acceptance criteria: `FR-06-AC-1`: inspect schematic and verify signal
  at first pixel.

**FR-07** `MUST` High-current accessories shall not be powered from
Raspberry Pi GPIO power pins.
- Acceptance criteria: `FR-07-AC-1`: power-path inspection and current
  measurement.

### Configuration / delivery

**FR-08** `SHOULD` Configuration shall support separate profiles for
Windows, Linux, booting, idle, and fault states.
- Acceptance criteria: `FR-08-AC-1`: profile-switching functional test.

**FR-09** `SHOULD` The design shall use keyed or clearly labeled
connectors and include test points.
- Acceptance criteria: `FR-09-AC-1`: physical design review.

**FR-10** `SHOULD` The repository shall support automated linting, unit
tests, and documentation checks.
- Acceptance criteria: `FR-10-AC-1`: CI pipeline passes on pull request.

## Non-Functional Requirements

### Security

**NFR-01** `MUST` PiKVM must never be exposed directly to the public
internet without a VPN or equivalent secured access layer; secrets and
machine-specific credentials must never be committed.
- Acceptance criteria: `NFR-01-AC-1`: `docs/security.md` threat-boundary
  table reviewed; `.gitignore` secret patterns present; no secret in any
  commit (spot-checked in PR review, `AGENTS.md` "Definition of done").

### Reliability

**NFR-02** `MUST` A crash/restart of any personality service
(audio/RGB/telemetry) or of `murderbot-core` itself must never assert an
unintended ATX pulse, and ATX outputs must default open.
- Acceptance criteria: `NFR-02-AC-1`: fault-injection tests in
  `docs/testing.md` (kill each service mid-operation; verify fail-open
  and no PiKVM impact).

### Testability

**NFR-03** `MUST` Hardware-facing code (GPIO, audio, RGB, telemetry) must
sit behind a `Protocol`/mock interface so unit tests run without a
Raspberry Pi attached.
- Acceptance criteria: `NFR-03-AC-1`: `services/src/murderbot_core/{hardware,audio,rgb,telemetry}/`
  each define a Protocol + mock, exercised by `tests/test_hardware_interfaces.py`.

## Explicit Non-Goals

- `WON'T` Native 4K capture/streaming of the RTX 4080 gaming output.
- `WON'T` Replacing motherboard fan control, PSU protection, or any
  safety-critical PC function.
- `WON'T` A custom production PCB before the bench prototype and pin
  allocation are proven.
- `WON'T` Sharing a failure domain between lighting/personality code and
  the core KVM service, at any point.

See `requirements.md`'s "Non-goals for the first release" for the full
narrative.

## Acceptance Criteria Summary

A release is `v1.0.0`-ready when every `MUST` requirement above (and
every `MUST`-level item in `requirements.md`'s "v1.0 acceptance
criteria") is `Verified` in `docs/REQUIREMENTS_TRACEABILITY.md`. See
`docs/versioning-and-releases.md` for the release process itself.

- [ ] All `MUST` requirements above are `Verified` in `docs/REQUIREMENTS_TRACEABILITY.md`.
- [ ] All ten numbered acceptance criteria in `requirements.md`'s "v1.0
      acceptance criteria" section are met.

## Traceability

See [`REQUIREMENTS_TRACEABILITY.md`](REQUIREMENTS_TRACEABILITY.md).
