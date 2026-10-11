# Changelog

## 1.2.0

- `esphome-build`: compile, upload or install ESPHome firmware through the
  Device Builder (works with ESPHome 2026.9)
- `esphome-mcp` and `esphome-build` use the Device Builder's port 6052; add-ons
  cannot open ingress sessions, so the role is back to `manager`
- Tools find their library relative to their own path

## 1.1.0

- Home Assistant tools: `ha-state`, `ha-api`, `ha-ws`, `ha-check`, `ha-notify`,
  plus the Supervisor CLI `ha` and `yq`
- `esphome-mcp`: MCP bridge to the ESPHome Device Builder, registered for
  Claude Code as `esphome` (compile, install and edit devices)
- Bundled Claude Code skills `home-assistant` and `esphome`
- Supervisor role `admin`, needed for the ESPHome ingress session and add-on
  management

## 1.0.0

- herdr 0.9.3
- Environment variables for panes and shells from `secrets.yaml` (`ha_secrets`),
  an env file in the add-on config folder and the configuration UI (`env_vars`)
- English documentation and configuration labels
- Add-on version is now independent of the herdr version

## 0.9.3

- Initial release with herdr 0.9.3, SSH on port 2222 and ingress web terminal
