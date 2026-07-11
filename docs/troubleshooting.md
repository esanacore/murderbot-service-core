# Troubleshooting

This document accumulates known-tricky failure modes as they're
discovered. It is intentionally sparse today — entries should be added
only once actually encountered and diagnosed (per `AGENTS.md` rule 1, no
speculative "fixes" for problems not yet observed), with the exception of
the structural guidance below.

## How to add an entry

```
### Symptom
What was observed.

### Cause
Root cause once diagnosed (not a guess).

### Fix / workaround
What resolved it, or the current workaround if unresolved.

### Related
Links to the relevant docs/backlog/ADR entries.
```

## Where to look first

| Symptom area | Check |
|---|---|
| PiKVM unreachable | `docs/pikvm-setup.md` bring-up checklist; confirm standby branch is actually powered (`docs/power-design.md`) |
| No video in PiKVM | Confirm which RTX 4080 output carries POST/BIOS (§5.2 discussion in `docs/architecture.md` / original report); check capture bridge cabling |
| ATX pulse not registering / stuck | `docs/testing.md` Phase 2 fault-injection tests; verify fail-open behavior, check optocoupler wiring against `docs/wiring.md` |
| Undervoltage warnings | `vcgencmd get_throttled`; revisit `docs/power-design.md` standby-branch budget — likely an unmeasured or underestimated load |
| Audio not playing / looping | Check `murderbot-audio.service` logs; verify cooldown logic in `services/src/murderbot_core/audio/`; confirm clip exists locally per `assets/README.md` (not committed) |
| RGB not lighting / wrong colors | Check level shifter wiring (FR-06) and brightness cap config; verify host-on branch is actually powered |
| A service crash affected PiKVM | This should be impossible per the failure-domain design (`docs/architecture.md`) — treat as a P0 bug, not a config issue, and open an issue immediately |

## Known issues

*(none recorded yet — this project is pre-hardware-bringup as of this
writing)*
