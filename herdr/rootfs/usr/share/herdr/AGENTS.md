## Umgebung: herdr-Add-on in Home Assistant

Du läufst im herdr-Add-on auf Home Assistant OS, als root in einem
Debian-Container. Neue Panes starten in `/config`, der Home-Assistant-Konfiguration.

- Beschreibbar sind `/config` (Home-Assistant-Konfiguration), `/share`, `/addons`
  und `/addon_config`. `/config/.storage` gehört Home Assistant: nie bearbeiten,
  solange Home Assistant läuft, stattdessen die WebSocket-API (`ha-ws`) nutzen.
- Gibt es `/config/CLAUDE.md` oder `/config/AGENTS.md`, beschreibt sie diese
  Installation und hat Vorrang vor diesen Hinweisen.
- `$SUPERVISOR_TOKEN` authentifiziert am Supervisor (`http://supervisor`) und
  über dessen Proxy an Home Assistant Core. Das Add-on hat die Supervisor-Rolle
  `manager`.

### Werkzeuge

| Werkzeug | Zweck |
|---|---|
| `ha-state [entity\|domain.\|muster] [-a]` | Zustände von Entitäten |
| `ha-api [-s] [METHODE] PFAD [JSON]` | REST-API von Core, `-s` für die Supervisor-API |
| `ha-ws TYP [JSON]` | Ein Befehl der WebSocket-API (Registries, Storage-Dashboards) |
| `ha-check` | Konfiguration prüfen |
| `ha-notify "Text" ["Titel"]` | Benachrichtigung in Home Assistant |
| `ha` | Supervisor-CLI (`ha addons logs <slug>`, `ha backups new`) |
| `yq` | YAML bearbeiten |
| `esphome-build compile\|upload\|install DATEI` | ESPHome-Firmware bauen und flashen |
| `esphome-mcp` | MCP-Server `esphome` für den ESPHome Device Builder (ab 2026.10) |

Details stehen in den Claude-Code-Skills `home-assistant` und `esphome`.

### Regeln

- Nach YAML-Änderungen `ha-check` ausführen, dann die betroffene Domain neu
  laden statt Home Assistant neu zu starten.
- Vor einem Neustart von Home Assistant Core oder eines anderen Add-ons, vor
  dem Flashen eines Geräts und vor schwer umkehrbaren Änderungen nachfragen,
  soweit der Berechtigungsmodus unten nichts anderes sagt.
- Das herdr-Add-on selbst nie neu starten, stoppen oder umkonfigurieren: Das
  beendet alle Sitzungen, auch deine.
- Geheimnisse (`secrets.yaml`, Tokens, Passwörter) nicht ausgeben, außer auf
  ausdrücklichen Wunsch. `/data/options.json` enthält die Add-on-Optionen samt
  `env_vars` im Klartext: nur Schlüsselnamen auslesen, nie die ganze Datei.
- Wenn eine lange oder unbeaufsichtigte Aufgabe fertig ist, `ha-notify` ausführen.
