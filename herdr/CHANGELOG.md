# Changelog

## Unveröffentlicht

- Doku und Konfigurationsoberfläche raten davon ab, Tokens in `env_vars` zu
  speichern; Geheimnisse gehören in `secrets.yaml` und werden über `ha_secrets`
  eingebunden (mit Beispiel)
- `ha-state` und die anderen Werkzeuge brechen in einer Pipe (`| head`) ohne
  Traceback ab
- `ha-check --help` und `herdr-agents --help` zeigen die Hilfe, statt loszulaufen

## 1.2.0

- Dokumentation, Konfigurationsoberfläche (neu `de.yaml`), Skills und
  Agent-Hinweise auf Deutsch
- Anweisungen für Agents: verwalteter Block in `~/.claude/CLAUDE.md` und
  `~/.codex/AGENTS.md`, eigene Anweisungen über `agent_instructions`
- Berechtigungen für Claude Code: lesende Werkzeuge ohne Rückfrage erlaubt,
  eigene Regeln über `claude_allow` und `claude_deny` in `~/.claude/settings.json`
- `esphome-build`: ESPHome-Firmware über den Device Builder kompilieren,
  hochladen oder installieren (funktioniert mit ESPHome 2026.9)
- `esphome-mcp` und `esphome-build` nutzen Port 6052 des Device Builders.
  Add-ons können keine Ingress-Sitzungen öffnen, die Rolle ist deshalb wieder
  `manager`
- Der Supervisor-Token geht nicht mehr an den Device Builder
- Hinweise zum Einfügen im Web-Terminal

## 1.1.0

- Home-Assistant-Werkzeuge: `ha-state`, `ha-api`, `ha-ws`, `ha-check`,
  `ha-notify`, dazu die Supervisor-CLI `ha` und `yq`
- `esphome-mcp`: MCP-Brücke zum ESPHome Device Builder, für Claude Code als
  `esphome` eingetragen
- Claude-Code-Skills `home-assistant` und `esphome`
- Supervisor-Rolle `admin` für die ESPHome-Ingress-Sitzung (hat nicht
  funktioniert, siehe 1.2.0)

## 1.0.0

- herdr 0.9.3
- Umgebungsvariablen für Panes und Shells aus `secrets.yaml` (`ha_secrets`),
  einer Env-Datei im Add-on-Konfigurationsordner und der
  Konfigurationsoberfläche (`env_vars`)
- Englische Dokumentation und Konfigurationsbezeichnungen
- Add-on-Version unabhängig von der herdr-Version

## 0.9.3

- Erste Version mit herdr 0.9.3, SSH auf Port 2222 und Web-Terminal über Ingress
