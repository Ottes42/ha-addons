---
name: esphome
description: Edit, validate, compile and install ESPHome device firmware through the ESPHome Device Builder add-on. Use for anything about ESPHome devices, their YAML in /config/esphome, OTA updates, failed installs or firmware versions.
---

The ESPHome Device Builder add-on exposes an MCP server. herdr connects to it
through `esphome-mcp` (MCP server `esphome`, registered for Claude Code on add-on
start). It reaches the builder's ingress site via the Supervisor, so compiles and
installs use the builder's own toolchain and stored credentials.

- Check the connection: `esphome-mcp --check` (lists the available tools).
- Typical flow: `list_devices` → `get_config` → `update_config` (needs the text
  `get_config` returned as `expected`) → `validate_config` → `install` → poll
  `get_job` until it finishes, then read its output tail.
- Long work is start-then-poll; `install` returns a job id immediately.
- A flash has no undo. Never install a config that drops `wifi:`, `api:` or
  `ota:` or changes the board; only a serial cable recovers that.
- Do not read `secrets.yaml` through the tools unless the user asks; it puts
  secrets into the conversation.
- YAML files live in `/config/esphome` and can also be read directly; edits
  made through `update_config` land in the builder's version history.

## OTA encryption (ESPHome 2026.9+)

OTA updates move from `ota: password:` to `ota: encryption:` (reuses the API
key). Migrate in two installs: first update with the password still in the
config, then replace `password:` with `encryption:` and install again. Removing
the password first fails with `ESP requests password, but no password given!`.
Unencrypted updates stop working with 2027.3.0.
