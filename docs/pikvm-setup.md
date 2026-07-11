# PiKVM Setup

MSC builds on [PiKVM](https://pikvm.github.io/pikvm/) rather than
reimplementing BIOS-level remote access. This document records the
project's specific configuration choices; for general PiKVM usage, defer
to the upstream docs linked below.

## Authoritative upstream references

| Source | URL | Use |
|---|---|---|
| PiKVM DIY V2 Quickstart Guide | https://pikvm.github.io/pikvm/v2/ | DIY Raspberry Pi 4 capture and cabling baseline |
| PiKVM Handbook | https://pikvm.github.io/pikvm/ | Authoritative configuration, GPIO, security, and operations documentation |
| PiKVM ATX Board Documentation | https://pikvm.github.io/pikvm/atx_board/ | Remote motherboard power-control architecture reference |

Do not duplicate PiKVM's own documentation here beyond what's needed for
MSC-specific context — link to it instead, so this document doesn't drift
out of sync with upstream.

## Project-specific choices

| Item | Value | Status |
|---|---|---|
| PiKVM image variant/version | `TBD` | Select in Phase 0 (`ROADMAP.md`); record exact image name + checksum here once flashed |
| Raspberry Pi model | Pi 4 Model B, 2GB or 4GB | Decided — see `docs/decisions/0001-service-core-architecture.md` |
| Capture method | HDMI-to-CSI bridge (not USB capture dongle) | Decided — see ADR 0001; specific bridge model `TBD`, see `hardware/bom.csv` |
| Network access model | VPN-first; no direct port-forward to PiKVM web UI | Decided — see `docs/security.md` |
| ATX control | PiKVM's own ATX GPIO/board integration, wired through MSC's optoisolated interface | See `docs/wiring.md`, `docs/power-design.md` |

## Bring-up checklist (Phase 0/1)

1. Flash the selected PiKVM image to the microSD card.
2. Record the image version and SHA-256 checksum below.
3. Boot on bench power (not yet installed in the host PC) and confirm
   local Ethernet access to the web UI.
4. Connect the HDMI-to-CSI bridge and confirm capture from a test source
   before connecting to the RTX 4080.
5. Confirm keyboard/mouse HID emulation and virtual media against the
   test source.
6. Only after the above: connect to the RTX 4080 and verify POST/BIOS
   visibility (`docs/testing.md` Phase 1 matrix).
7. Apply the project's security baseline (`docs/security.md`) —
   credentials, VPN access, no raw port-forwarding — before leaving the
   Pi on any persistent network.

## Image / configuration record

| Field | Value |
|---|---|
| Image name | `TBD` |
| Image version | `TBD` |
| SHA-256 checksum | `TBD` |
| Date flashed | `TBD` |
| Configuration export location | Not committed to this repo — see `SECURITY.md` and `.gitignore`; store an encrypted backup outside version control |

## Recovery

Recovery procedure (reflash steps, configuration restore) is `TBD` pending
Phase 0 completion. It will document how to recreate the PiKVM
configuration from a fresh image using only files stored in this
repository plus the (out-of-repo) encrypted config export, per v1.0
acceptance criterion #8 (`docs/requirements.md`).
