# Security

MSC has BIOS-level, physical-power-level control over a real desktop PC.
This document is the detailed threat model behind the summary in
`SECURITY.md`.

## Threat boundaries

| Boundary | Policy |
|---|---|
| PiKVM web UI / API | Never exposed directly to the public internet. VPN-first (e.g. WireGuard/Tailscale) or an equivalent secured access layer is required for any remote (off-LAN) access. No raw port-forwarding on the home router. |
| PiKVM authentication | Strong, unique credentials; PiKVM's own auth mechanisms kept up to date per upstream guidance (`docs/pikvm-setup.md`). |
| Local LAN access | Trusted-network assumption for the initial release — the LAN itself is not treated as a hostile boundary in Phase 0–5, though this should be revisited before any post-1.0 REST API/dashboard work (`ROADMAP.md`) widens the attack surface. |
| Custom services (`murderbot-audio`, `murderbot-rgb`, `murderbot-telemetry`) | Run with least privilege; must not have write access to PiKVM system packages, boot configuration, or firewall rules (`AGENTS.md` rule 3). |
| Host telemetry agents (`host-agents/`) | Optional and authenticated; system remains fully functional (KVM + ATX) without them (`docs/architecture.md`). |
| Secrets, keys, machine-specific config | Never committed — see `.gitignore` and `configs/examples/` (sanitized examples only). |

## Update strategy

- PiKVM itself is updated per upstream guidance
  (https://pikvm.github.io/pikvm/); this repository does not fork or
  vendor PiKVM's own update mechanism.
- MSC's own services (`services/`) are updated via normal git-based
  deployment during Phases 0–5; automated OTA is explicitly deferred to
  post-1.0 (`ROADMAP.md`) until a versioning/rollback story exists
  (`docs/versioning-and-releases.md`).
- Before any update touching PiKVM system packages, boot config, or
  firewall rules, an image backup and rollback procedure must exist
  first (`AGENTS.md` rule 3).

## Secrets handling

- No SSH keys, Wi-Fi credentials, PiKVM admin credentials, or API tokens
  are stored in this repository, in any form (including "example" files
  with real-looking but fake values that could be mistaken for real ones —
  use obviously placeholder values like `CHANGE_ME` in
  `configs/examples/`).
- Real configuration lives on the deployed Pi, outside version control,
  with an encrypted backup stored by the maintainer outside this repo.
- `.gitignore` blocks common secret file patterns as a backstop, not as
  the primary control — the primary control is not creating those files
  in a tracked path to begin with.

## Media licensing (adjacent security/compliance concern)

Startup audio clips are licensing-sensitive, not just a technical
concern — see `assets/README.md`. No copyrighted soundtrack may be
committed (`AGENTS.md` rule 2, v1.0 acceptance criterion #10 in
`docs/requirements.md`).

## Reporting

See `SECURITY.md` for how to report a vulnerability.

## Known gaps / TBD

- LAN-boundary threat model for post-1.0 REST API / web dashboard is not
  yet written — track as a backlog item once Phase 5 nears completion.
- Formal secrets-scanning in CI (beyond `detect-private-key` in
  `.pre-commit-config.yaml`) is not yet configured.
