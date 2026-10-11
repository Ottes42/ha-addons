---
name: home-assistant
description: Talk to Home Assistant from the herdr add-on. Use when reading entity states, calling services, rendering templates, checking the configuration, editing registries or storage dashboards over the WebSocket API, managing other add-ons, or notifying the user when a long task is done.
---

The herdr add-on ships small CLI tools that authenticate with `$SUPERVISOR_TOKEN`
through the Supervisor proxy. Prefer them over hand-written curl or Python clients.

| Tool | Use |
|---|---|
| `ha-state [entity\|domain.\|pattern] [-a]` | States as `entity<TAB>value unit<TAB>name`; `-a` prints full JSON with attributes. `ha-state light.`, `ha-state 'sensor.buro_*'` |
| `ha-api [-s] [METHOD] PATH [JSON\|-]` | Core REST API (`states/...`, `services/<domain>/<service>`, `template`, `history/period/...`). `-s` targets the Supervisor API (`addons`, `addons/<slug>/logs`, `backups`) |
| `ha-ws TYPE [JSON\|-]` | One WebSocket command, prints its `result`. Registries (`config/entity_registry/list`, `.../update`), `lovelace/config`, `lovelace/config/save`, `recorder/...` |
| `ha-check` | Validate the configuration, exit 1 when invalid. Run before any reload or restart |
| `ha-notify "msg" ["title"]` | Notify the user (persistent notification, or `HA_NOTIFY_SERVICE`) |
| `ha` | Official Supervisor CLI: `ha addons`, `ha addons logs <slug>`, `ha backups new --name X`, `ha core info` |
| `yq` | Edit YAML in place: `yq -i '.key = "value"' file.yaml` |

## Rules

- Read a project's `CLAUDE.md` in `/config` first; it overrides these defaults.
- After YAML changes: `ha-check`, then reload the specific domain
  (`ha-api POST services/automation/reload`) instead of restarting Core.
- Never edit `/config/.storage/` while Home Assistant runs; use `ha-ws` instead.
- Render templates to test them: `ha-api POST template '{"template": "{{ ... }}"}'`.
- The add-on runs with Supervisor role `manager`. Do not restart, stop or
  reconfigure the herdr add-on itself (it ends the session), and ask before
  restarting Core or other add-ons.
- When a long or unattended task finishes, run `ha-notify`.
