# Changelog

## Unveröffentlicht

- Neue Option `permission_mode` (`read`, `build`, `admin`): Stufen, was Claude Code
  ohne Rückfrage darf, bis hin zum Neustart von Home Assistant Core und anderen
  Add-ons (`admin`). Die Agent-Hinweise bekommen einen passenden Abschnitt.
  Das herdr-Add-on selbst neu zu starten, zu stoppen oder zu aktualisieren ist
  jetzt immer per Regel verboten

## 1.4.3

- `esphome-build`: Die Einblendungen zeigen auch den Fortschritt beim Kompilieren
  und Hochladen, mit Balken in Schritten von 20 % (höchstens alle 5 Sekunden)

## 1.4.2

- `esphome-build` meldet sich in herdr mit Einblendungen oben rechts (Start,
  kompiliert, Ergebnis mit Laufzeit) statt mit einem Pane. Das Pane mit dem Log
  öffnet sich nur noch, wenn der Build fehlschlägt. `ESPHOME_BUILD_PANE=1`
  bringt das Fortschritts-Pane für jeden Build zurück
- herdr-Einblendungen sind ab Werk an (oben rechts), solange die herdr-Konfiguration
  keinen eigenen Abschnitt `[ui.toast]` hat

## 1.4.1

- `esphome-build` zeigt in herdr den Fortschritt in einem eigenen Pane unter
  dem aufrufenden: Phase, Balken für Kompilieren (ESP-IDF-Schritte) und
  Hochladen, Laufzeit, Ende des Logs. Wird beim nächsten Build wiederverwendet,
  `ESPHOME_BUILD_PANE=0` schaltet es ab
- `xclip`, `xsel`, `wl-copy` und `wl-paste` gibt es als Ersatz, der per OSC 52
  in die Zwischenablage des Browsers kopiert. Keine Meldung „No clipboard
  utilities available“ mehr, z. B. bei `gh auth login`

## 1.4.0

- **Fertiges Image** von GitHub (ghcr.io) statt Bau auf dem Home-Assistant-Rechner:
  Updates gehen schneller und brauchen dort keinen Speicher mehr
- **Erweiterungen** über die Konfiguration: `apt_packages`, `npm_packages`
  (z. B. ruflo, ohne Version beim Start aktualisiert) und `uv_tools`. Ein
  Hintergrunddienst installiert sie nach dem Start, Fehler halten das Add-on
  nicht an. Eigene Startschritte unter `/addon_config/init.d/*.sh`
- Node.js 24, `uv`/`uvx` und die GitHub-CLI `gh` sind dabei. Mit `GH_TOKEN`
  funktionieren `gh` und `git push` über HTTPS
- Backups ohne Caches, Erweiterungen und ältere Claude-Code-Versionen; nach
  einer Wiederherstellung werden sie neu installiert
- Web-Terminal: Strg+Enter und Umschalt+Enter kommen als eigene Tasten an,
  in Claude Code „jetzt senden“ und „neue Zeile“
- Claude-Code-Skill `herdr` (aus `herdr --skill`, passend zur installierten Version)
- `build.yaml` entfällt, das Dockerfile ist die einzige Bauanleitung

## 1.3.1

- `vim` ist installiert
- Doku: andere herdrs als gespeicherte Maschine verbinden (`herdr machine add`),
  `herdr --remote` aus einem Pane heraus mit `env -u HERDR_ENV`

## 1.3.0

- Eigener SSH-Schlüssel für ausgehende Verbindungen (`~/.ssh/id_ed25519`),
  wird beim ersten Start erzeugt und bleibt erhalten. Der öffentliche Schlüssel
  steht bei jedem Start im Add-on-Log, so lässt sich herdr mit anderen herdrs
  verbinden (`herdr --remote`)

## 1.2.1

- Doku und Konfigurationsoberfläche raten davon ab, Tokens in `env_vars` zu
  speichern; Geheimnisse gehören in `secrets.yaml` und werden über `ha_secrets`
  eingebunden (mit Beispiel)
- Agent-Regel: `/data/options.json` nie ganz ausgeben (enthält `env_vars` im
  Klartext)
- Skill `home-assistant`: Stolperfallen zu YAML- und Storage-Dashboards,
  Umbenennen von Entities und dauerhaft abgeschalteten Automationen
- Doku: Claude Code in `/config` starten (Vertrauensabfrage, Memory pro
  Verzeichnis) und was ins Add-on, in `/config/CLAUDE.md` oder in die Memory gehört
- Web-Terminal: Kopieren aus herdr und Claude Code (OSC 52) landet in der
  Zwischenablage des Rechners, `Strg+V` fügt ein
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
