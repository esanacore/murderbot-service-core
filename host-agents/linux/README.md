# host-agents/linux/

Empty. Planned: a small Linux daemon reporting host OS identity, CPU/GPU
temperature, utilization, memory, and shutdown intent to
`murderbot-telemetry.service` over an authenticated transport (see
`../../docs/architecture.md` "Host agent" row and
`../../docs/security.md`).

Not started - this is a P3 backlog item (`../../docs/backlog.md`,
`../../ROADMAP.md` post-1.0 item 3). The service core must remain fully
useful without this agent; do not add a hard dependency from
`murderbot-core` on this agent's presence.
