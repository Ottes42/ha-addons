---
name: esphome
description: Edit, validate, compile and install ESPHome device firmware through the ESPHome Device Builder add-on. Use for anything about ESPHome devices, their YAML in /config/esphome, OTA updates, failed installs or firmware versions.
---

Device YAML lives in `/config/esphome` and can be read and edited directly.
Builds and installs go through the ESPHome Device Builder add-on, so they use
its toolchain and stored credentials. Both tools reach it on port 6052; if they
report that the port is not mapped, ask the user to enable
`leave_front_door_open` and map port 6052 in the ESPHome add-on.

## esphome-build (any ESPHome version)

```sh
esphome-build compile esp32c3-btproxy-buro.yaml
esphome-build install esp32c3-btproxy-buro.yaml        # compile, then OTA upload
esphome-build upload  esp32c3-btproxy-buro.yaml OTA    # upload the last build
```

Filter the output, the upload progress bar is long:
`esphome-build install x.yaml 2>&1 | grep -vE 'Uploading: \[' | tail -30`.
Exit code 1 means failure; the log tail says why.

## MCP server `esphome` (ESPHome 2026.10 and newer)

`esphome-mcp` bridges Claude Code to the builder's MCP endpoint. Check it with
`esphome-mcp --check`; on older builders it says the endpoint is missing, then
use `esphome-build`.

Flow: `list_devices` → `get_config` → `update_config` (needs the text
`get_config` returned as `expected`) → `validate_config` → `install` → poll
`get_job` until it finishes. Long work is start-then-poll.

## Rules

- A flash has no undo. Never install a config that drops `wifi:`, `api:` or
  `ota:` or changes the board; only a serial cable recovers that.
- Install one device, confirm it comes back online in Home Assistant
  (`ha-ws config/device_registry/list`, `sw_version`), then the next.
- Do not print `secrets.yaml` or passwords unless the user asks.

## OTA encryption (ESPHome 2026.9+)

OTA updates move from `ota: password:` to `ota: encryption:` (reuses the API
key). Migrate in two installs: first update with the password still in the
config, then replace `password:` with `encryption:` and install again. Removing
the password first fails with `ESP requests password, but no password given!`.
Unencrypted updates stop working with 2027.3.0.
