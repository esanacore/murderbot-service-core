# firmware/

Reserved, currently unused.

MSC runs entirely as Linux/Python services on the Raspberry Pi through
Phase 0-5 (`../ROADMAP.md`) — there is no separate microcontroller today,
so there is no firmware to build. This directory exists so a future
addition that *does* need dedicated MCU firmware (for example, a
standalone OLED/sensor co-processor considered in `../ROADMAP.md`
post-1.0 items 1-2) has an obvious home, rather than forcing a repository
restructure later — see
`../docs/decisions/0002-repository-structure-and-license.md`.

Do not add speculative firmware here ahead of an actual microcontroller
being selected for an actual roadmap item (`AGENTS.md` rule 1).
