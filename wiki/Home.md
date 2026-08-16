# Home

Welcome to the **Murderbot Service Core (MSC)** wiki. Wiki pages are authored
under `wiki/` in this repository and reviewed through normal pull requests.

## What this project does

An embedded, Raspberry Pi–based service processor that lives inside the
"Murderbot" desktop PC (MSI Z490-A PRO / i7-10700 / RTX 4080) and provides
enterprise-style out-of-band management in the spirit of Dell iDRAC / HP iLO
/ Lenovo XClarity — plus custom personality features: startup audio,
addressable RGB, and eventually host telemetry, a plugin architecture, and a
web dashboard.

## Current status

Pre-hardware: documentation and software-scaffolding phase. No board has been
wired into the host PC yet; nothing here is a validated schematic, pinout, or
power budget until the `TBD` markers in `docs/` are resolved. **Read the
safety warning in the README and `docs/power-design.md` before energizing
anything** — PiKVM must always remain reliable and isolated from failures in
every other subsystem (see `docs/architecture.md` for the failure-domain
rules).

## Where things live

- `docs/` — power design, wiring, architecture, and `docs/decisions/` ADRs
- `constitution/` — Eric's Engineering Constitution submodule (read-only)

## See also

- `docs/HELP.md` — common questions and troubleshooting
- `TODO.md` — the living roadmap
