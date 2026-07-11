# Troubleshooting

This project's troubleshooting guide lives at
[`troubleshooting.md`](troubleshooting.md) (lowercase — written before
this constitution-mandated uppercase path existed; see
`decisions/0002-repository-structure-and-license.md`'s reconciliation
approach for why duplicate content isn't kept in both places). This file
is kept as a pointer so `docs/TROUBLESHOOTING.md`-relative links from
constitution tooling and templates (e.g. `HELP.md`,
`AGENT_PROMPTS.md`) still resolve to something.

See [`troubleshooting.md`](troubleshooting.md) for:

- How to add a new troubleshooting entry
- Where to look first by symptom area (PiKVM unreachable, no video, ATX
  pulse issues, undervoltage, audio/RGB problems)
- The current (empty, pre-hardware-bring-up) known-issues log

For generic dev-environment reset (not project-specific): remove
`services/.venv`, re-run `bash scripts/bootstrap-dev-env.sh`.
