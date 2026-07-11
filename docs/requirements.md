# Requirements

## Functional requirements

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| FR-01 | The service core shall remain reachable while the PC is off but the PSU is connected. | Must | Power host down; verify network and web UI remain available. |
| FR-02 | The system shall provide remote keyboard, mouse, and video suitable for BIOS/UEFI use. | Must | Enter firmware setup remotely and navigate menus. |
| FR-03 | The system shall activate host power and reset through isolated parallel connections. | Must | Verify local and remote controls independently. |
| FR-04 | The startup sequence shall trigger from host main-rail state, not merely Pi boot. | Must | Cold boot and soft restart tests. |
| FR-05 | Audio and RGB faults shall not disable PiKVM or ATX control. | Must | Disable each service and verify KVM remains functional. |
| FR-06 | NeoPixel data shall be translated from 3.3 V to 5 V logic. | Must | Inspect schematic and verify signal at first pixel. |
| FR-07 | High-current accessories shall not be powered from Raspberry Pi GPIO power pins. | Must | Power-path inspection and current measurement. |
| FR-08 | Configuration shall support separate profiles for Windows, Linux, booting, idle, and fault states. | Should | Profile-switching functional test. |
| FR-09 | The design shall use keyed or clearly labeled connectors and include test points. | Should | Physical design review. |
| FR-10 | The repository shall support automated linting, unit tests, and documentation checks. | Should | CI pipeline passes on pull request. |

Priority follows MoSCoW: "Must" requirements gate the v1.0 release
(`ROADMAP.md` Phase 5); "Should" requirements are strongly expected but
can slip a point release with an explicit ADR/backlog note explaining why.

## Non-functional / project goals

### Primary goals

- Browser-based, BIOS-level console access independent of the host OS.
- Safe remote power-button/reset-button activation while preserving the
  physical case controls.
- A short licensed or user-supplied startup clip when the main host power
  rails become active.
- Deterministic boot/idle/load/fault/shutdown RGB behaviors.
- A design modular enough to add displays, sensors, telemetry, MQTT, or
  Home Assistant later without revisiting the core (see `ROADMAP.md`).
- A reproducible repository: schematics, software, test procedures,
  decisions, BOM data, and build documentation.

### Non-goals for the first release (through v1.0, `ROADMAP.md` Phase 5)

- Capturing or streaming the RTX 4080 gaming output at native 4K
  resolution.
- Replacing motherboard fan control, PSU protection, or any
  safety-critical PC function.
- Exposing PiKVM directly to the public internet without a secured VPN or
  equivalent access layer.
- Building a custom production PCB before the bench prototype and pin
  allocation are proven.
- Allowing lighting or personality code to share a failure domain with the
  core KVM service.

## v1.0 acceptance criteria

Release 1.0 is complete when **all** of the following hold:

1. PiKVM is available from a trusted network while Murderbot is shut down
   but connected to AC.
2. POST and firmware setup can be viewed and controlled remotely.
3. Power and reset work remotely and locally, with no stuck or repeated
   button state.
4. Loss or restart of RGB/audio services does not interrupt the KVM
   session.
5. The startup clip plays once per genuine host power-up and does not
   loop after a service restart.
6. RGB output uses level shifting, current limiting, fusing, and a
   documented brightness cap.
7. The Pi shows no undervoltage or thermal warnings during the
   integration stability test.
8. The repository can recreate the configuration from a fresh PiKVM image
   using documented steps.
9. All schematics and wiring diagrams match the as-built system.
10. No copyrighted audio file, secret, password, private key, or
    machine-specific credential is committed.

Each criterion above should be traceable to a test in
`docs/testing.md`'s matrix before it is checked off in a release PR.
