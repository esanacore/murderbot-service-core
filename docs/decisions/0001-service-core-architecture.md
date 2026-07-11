# ADR 0001: Single Raspberry Pi 4 for PiKVM and personality services

Status: Accepted

## Context

MSC needs to run both the critical PiKVM service (video capture, HID,
virtual media, ATX-adjacent control) and a set of non-critical
"personality" services (startup audio, addressable RGB, future
telemetry). These have very different reliability requirements: PiKVM
must stay up whenever the PSU is connected; personality services may
restart, degrade, or be disabled without consequence to the core mission.

The question: run everything on one Raspberry Pi 4, or split PiKVM and
personality features across two separate boards (e.g. a second Pi Zero 2
W or microcontroller dedicated to audio/RGB)?

## Decision

Use a single Raspberry Pi 4 (2GB or 4GB) for both PiKVM and the
personality services, enforcing isolation in software (separate systemd
units, separate failure domains, event-bus-only communication — see
`docs/architecture.md`) rather than in separate hardware.

Also decided as part of this same architectural pass:

- Use a PiKVM-supported **HDMI-to-CSI bridge** rather than a generic USB
  capture dongle, for a cleaner embedded installation. The KVM path is a
  management display, not a high-resolution gaming capture path (see
  `docs/requirements.md` non-goals).
- Use **optocouplers or isolated solid-state outputs** for ATX PWR/RESET,
  never a direct GPIO-to-front-panel-header connection, with a fail-open
  default.
- Split power into a **standby branch** (Pi, capture, network, ATX logic)
  and a **host-on branch** (LEDs, audio, future accessories), never
  backfed into each other (see `docs/power-design.md`).

## Alternatives considered

- **Two boards (Pi 4 for PiKVM + Pi Zero 2 W or MCU for
  personality):** Would give true hardware-level isolation — a kernel
  panic on the personality board literally cannot affect PiKVM. Rejected
  for v1.0 because it roughly doubles the bill of materials and adds a
  second network/power/mounting footprint for a failure mode
  (personality-service crash affecting PiKVM) that can be adequately
  prevented in software given disciplined systemd unit boundaries and the
  power-branch split. Revisit if software isolation proves insufficient
  in practice (Phase 3/4 fault-injection testing, `docs/testing.md`).
- **Pi Zero 2 W instead of Pi 4 for the single-board option:** Rejected —
  PiKVM capture, USB emulation, networking, and the personality services
  all benefit from the Pi 4's CPU, memory, Ethernet, USB, and mature DIY
  PiKVM support; a Zero 2 W's headroom is too tight once personality
  services and future telemetry/API layers (`ROADMAP.md`) are considered.
- **Generic USB capture dongle instead of HDMI-to-CSI bridge:** Simpler
  cabling in some cases but a bulkier, less clean internal installation
  and generally worse PiKVM-ecosystem support than the CSI path.
- **Direct GPIO-to-front-panel wiring (no optocoupler):** Rejected
  outright — a GPIO fault or bad software state could assert an
  unintended, non-fail-open signal onto the motherboard's front-panel
  header, risking the motherboard itself. Isolation is a hard
  requirement, not a nice-to-have (FR-03, FR-07).

## Consequences

- Software must enforce discipline that hardware isolation would have
  given for free — this is why `AGENTS.md` rule 4 and rule 8
  (Protocol-based hardware interfaces) exist as explicit, checked rules
  rather than informal guidance.
- Bill of materials stays smaller and the physical build stays simpler
  (one board to mount, power, and network), which matches the budget
  guidance in the original engineering report (~$95–$155 for a complete
  integrated build).
- If fault-injection testing (`docs/testing.md`) ever demonstrates that a
  personality-service failure *can* affect PiKVM despite the software
  isolation, that is a P0 bug against this ADR's core assumption, not a
  routine defect — it should trigger revisiting the two-board
  alternative above.
