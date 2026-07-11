# examples/

Empty pending a runnable end-to-end service (`../docs/software.md` "What's
implemented today vs. planned" — only the library layer exists so far,
not a running `murderbot-core` process).

Planned first example, once `murderbot_core.core_service` exists: a
minimal script wiring `HostStateMachine` + `EventBus` + the mock
hardware/audio/RGB backends together, runnable with no Raspberry Pi, to
demonstrate the event flow end-to-end before real backends exist.
