# MVP Backlog

This backlog translates `PRODUCT_REQUIREMENTS.md` into buildable delivery
slices. It mirrors `../ROADMAP.md`'s phases; `../ROADMAP.md` is canonical
for sequencing rationale, this file is the constitution-mandated
milestone view. "MVP" here means `v1.0.0` as defined in
`requirements.md`'s acceptance criteria — see `../docs/versioning-and-releases.md`.

`../TODO.md` remains the living project roadmap for day-to-day discovered
work; this file is milestone-based delivery planning.

## Milestone 0: Foundation (current)

- [x] Repository structure, governance docs, CI.
- [x] Hardware-independent `murderbot_core` package (event bus, state
      machine, config parsing, mock hardware/audio/RGB/telemetry).
- [ ] Inventory/acquire Pi, microSD, capture bridge; flash PiKVM image
      (`../docs/backlog.md` P0 items).

## Milestone 1: PiKVM Core Proof (FR-01, FR-02)

- [ ] Validate BIOS/POST visibility across RTX 4080 outputs.
- [ ] Verify HID emulation, virtual media, reboot recovery.
- [ ] Extended stability + undervoltage/thermal check.

## Milestone 2: ATX Integration (FR-03, FR-04, FR-07, NFR-02)

- [ ] Characterize standby-branch power budget (`../docs/power-design.md`).
- [ ] Build and validate optoisolated PWR/RESET interface, fail-open
      confirmed under fault injection.
- [ ] Host-state sensing wired into the state machine.

## Milestone 3: Personality — Audio (FR-08 partial)

- [ ] I2S amplifier + speaker, printed enclosure.
- [ ] Audio triggers only on genuine host power-up, with cooldown.

## Milestone 4: Personality — RGB (FR-06, FR-08 partial, FR-09)

- [ ] Level-shifted NeoPixel output, brightness-capped.
- [ ] Boot/idle/load/fault/shutdown lighting profiles.

## Milestone 5: v1.0 Validation (FR-05, FR-10, all NFRs)

- [ ] Full fault-injection matrix (`../docs/testing.md`) executed with
      evidence recorded.
- [ ] 24-hour stability test + recovery drill.
- [ ] All `MUST` rows in `REQUIREMENTS_TRACEABILITY.md` marked `Verified`.
- [ ] Tag `v1.0.0` per `../docs/versioning-and-releases.md`.
