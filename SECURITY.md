# Security Policy

This project also follows
[Eric's Engineering Constitution Security Standards](constitution/SECURITY.md)
(Principle 5) — including its threat-modeling triggers for new egress
paths, new auth/authz surfaces, and new trust-sensitive dependencies. This
document is the project-specific policy required by that framework; where
the two differ, this document governs (`constitution/INTEGRATION.md`).

## Scope

Murderbot Service Core (MSC) is a management controller with remote,
BIOS-level access to a physical desktop PC (video, keyboard/mouse
emulation, power/reset control) via PiKVM, plus custom services running
alongside it. A vulnerability here can translate directly into unauthorized
physical-machine control. Treat this project's security posture at least as
seriously as a data-center BMC/iDRAC/iLO deployment, scaled to a home lab.

## Supported versions

Pre-1.0: only the `main` branch is supported. There is no LTS branch yet.
This will be revisited at the first tagged `v1.0.0` release — see
`docs/versioning-and-releases.md`.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, use GitHub's private vulnerability reporting (Security tab →
"Report a vulnerability") on this repository, or contact the maintainer
directly through the contact information on their GitHub profile. Include:

- A description of the vulnerability and its impact
- Steps to reproduce (or a proof of concept)
- Affected component(s) (PiKVM config, `murderbot-core`, host agents, CI,
  etc.)

Expect an acknowledgment within 7 days. This is a hobbyist project without
a formal SLA, but security reports will be prioritized over feature work.

## Threat model (summary)

See `docs/security.md` for the full write-up. In short:

- **PiKVM must never be exposed directly to the public internet.**
  VPN-first (or equivalent) remote access is required; see `docs/security.md`.
- Secrets, SSH keys, Wi-Fi credentials, and any machine-specific identifiers
  must never be committed. `.gitignore` and `configs/examples/` (sanitized
  examples only) enforce this at the repo level; real configuration lives
  outside version control on the deployed Pi.
- Custom services (`murderbot-audio`, `murderbot-rgb`, `murderbot-telemetry`)
  run with the least privilege required and must not be able to modify
  PiKVM system packages, boot configuration, or firewall rules — see
  `AGENTS.md` rule 3 and `docs/architecture.md`.
- Host telemetry agents (`host-agents/`) are optional, authenticated, and
  the system must remain fully functional (KVM + ATX) without them.

## Disclosure

Once a report is confirmed, a fix will be developed on a private branch
where feasible, and a coordinated disclosure with a `CHANGELOG.md` entry and
a new patch release will follow. Given the small scale of this project,
disclosure timelines will be handled case-by-case with the reporter.
