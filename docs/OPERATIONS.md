# Operations

This project has no traditional software deployment (no server, no cloud
environments) — "operations" here means installing and operating a
physical management controller inside a PC. This document is `TBD`-heavy
by design until Phase 2+ hardware exists; see `../AGENTS.md` rule 1.

## Deployment

- **Environments**: "bench" (Pi powered on a lab supply, not yet installed
  in Murderbot) and "installed" (mounted inside the case, wired to the
  ATX/standby branches). See `../ROADMAP.md` Phase 0-5.
- **Deployment procedure**: flash the PiKVM image (`pikvm-setup.md`
  bring-up checklist), deploy `services/` via `git clone` + the systemd
  units in `../services/systemd/` (not auto-installed — `../AGENTS.md`
  rule 3), then physically install per `wiring.md` only after bench
  proof.
- **Approvals/gates**: none automated (solo project) — each `../ROADMAP.md`
  phase has its own exit criteria that must be met before starting the
  next.
- **Rollback**: reflash from the recorded PiKVM image checksum
  (`pikvm-setup.md`); `services/` rollback is a normal `git revert` +
  systemd restart. Physical/electrical changes are reverted by
  disconnecting the branch in question (`power-design.md`) — see Incident
  Response below for the fast path.

## Monitoring & Observability

- **Logs**: `journalctl -u murderbot-*` once real services exist
  (`services/src/murderbot_core/logging_setup.py` configures stdout
  logging captured by journald).
- **Metrics**: none yet — `vcgencmd get_throttled` is checked manually
  during bench/integration tests (`testing.md`); no persistent metrics
  store exists (post-1.0 telemetry, `../ROADMAP.md`).
- **Alerts**: none — this is a home-lab project with a single operator.

## Safe Operations

- **Backup/Restore**: PiKVM image + config export, stored encrypted
  outside version control (`security.md`); no other persistent state
  exists today.
- **Maintenance mode**: N/A — services are independent
  (`architecture.md` failure-domain table); disabling `murderbot-audio`
  or `murderbot-rgb` for maintenance never affects PiKVM/ATX.
- **Stateful changes**: none — the state machine (`software.md`) holds
  only in-memory state, re-derived from real hardware signals on
  restart, by design (no persisted state to migrate).

## Incident Response

For a project controlling physical power/reset lines, "incident" mostly
means "something is electrically or thermally wrong," not "a deployment
broke":

1. **Identify the impact** — is PiKVM/ATX control affected (critical,
   `architecture.md`), or only a personality service (non-critical)?
2. **Check `vcgencmd get_throttled`** for undervoltage/thermal flags and
   `journalctl` for the affected service.
3. **If genuinely unsafe** (suspected overcurrent, overheating,
   unexpected ATX assertion): physically disconnect the standby or
   host-on power branch (`power-design.md`) rather than trying to
   software-fix it live.
4. **If a personality service is misbehaving**: `systemctl stop
   murderbot-audio` / `murderbot-rgb` (independent restart, no PiKVM
   impact per design) and file an issue with the `bug_report.yml`
   template, checking the "Safety impact" box if relevant.
5. Record the incident in `troubleshooting.md` once diagnosed, per that
   file's "How to add an entry" section.
