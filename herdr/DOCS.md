# herdr

Ein dauerhaft laufender [herdr](https://herdr.dev)-Server in Home Assistant.
Coding-Agents wie Claude Code laufen hier weiter, auch wenn der Client die
Verbindung trennt.

## Zugriff

- **Web-Terminal:** „herdr“ in der Seitenleiste. Verbindet sich mit dem
  laufenden Server.
- **SSH / herdr remote:** Port 2222, Anmeldung nur als `root` mit öffentlichem
  Schlüssel.

  Beispiel für `~/.ssh/config`:

  ```
  Host ha-herdr
    HostName homeassistant.local
    Port 2222
    User root
  ```

  ```sh
  herdr --remote ha-herdr   # schlanker lokaler Client, herdr lokal installiert
  ssh ha-herdr              # oder einfach SSH, dann: herdr
  ```

### Kopieren und Einfügen im Web-Terminal

Das Web-Terminal (ttyd mit xterm.js) schickt `Strg+V` als Steuerzeichen an das
Terminal, statt einzufügen. Diese Wege sollten funktionieren:

- **Windows/Linux:** `Strg+Umschalt+V` oder `Umschalt+Einfg`
- **macOS:** `Cmd+V`
- **Maus:** herdr fängt die Maus ab. Mit gedrückter `Umschalt`-Taste
  (macOS: `Option`) erscheint beim Rechtsklick das Kontextmenü des Browsers mit
  „Einfügen“; so lässt sich auch Text markieren und kopieren.

## Konfiguration

```yaml
authorized_keys:
  - ssh-ed25519 AAAA... name
ha_secrets:
  - grocy_api_key               # wird zu GROCY_API_KEY
  - OPENAI_API_KEY=openai_token # eigener Variablenname
env_vars:
  - name: SOME_TOKEN
    value: "..."
agent_instructions: "Antworte auf Deutsch."
claude_allow:
  - Bash(git status)
claude_deny:
  - Bash(rm -rf *)
```

### `authorized_keys`

Öffentliche Schlüssel, die sich per SSH anmelden dürfen. Ohne Schlüssel ist keine
SSH-Anmeldung möglich (das Web-Terminal funktioniert trotzdem).

### Umgebungsvariablen

API-Schlüssel und Tokens (z. B. für Grocy oder andere Onlinedienste) lassen sich
allen herdr-Panes und Login-Shells mitgeben. Es gibt drei optionale Quellen;
kommt ein Name mehrfach vor, gewinnt die spätere:

1. **`ha_secrets`**: Schlüssel aus `/config/secrets.yaml` von Home Assistant. Nur
   die hier aufgeführten Schlüssel werden exportiert, nie die ganze Datei.
   `grocy_api_key` wird zu `GROCY_API_KEY`, `NAME=secret_key` setzt einen eigenen
   Namen.
2. **Env-Datei**: `/addon_configs/<slug>_herdr/env` (erreichbar über Samba oder
   das Studio-Code-Server-Add-on), eine Zeile `KEY=value` pro Variable, `#` für
   Kommentare. Die Datei wird beim ersten Start mit Beispielen angelegt.
3. **`env_vars`**: Name/Wert-Paare aus der Konfigurationsoberfläche des Add-ons.
   Die Werte werden dort verdeckt angezeigt.

`HOME`, `PATH`, `SHELL`, `TERM` und `SUPERVISOR_TOKEN` verwaltet das Add-on, sie
lassen sich nicht überschreiben. Das Add-on-Log nennt nur die Namen der
geladenen Variablen, nie ihre Werte.

### Anweisungen und Berechtigungen für Agents

Beim Start schreibt das Add-on einen verwalteten Block in `~/.claude/CLAUDE.md`
(Claude Code) und `~/.codex/AGENTS.md` (Codex). Er beschreibt die Umgebung, die
Werkzeuge und Grundregeln. Mit `agent_instructions` hängst du eigene Anweisungen
an. Text außerhalb des Blocks bleibt unverändert, Änderungen im Block werden beim
nächsten Start überschrieben.

In `~/.claude/settings.json` ergänzt das Add-on Berechtigungsregeln:

- Lesende Befehle wie `ha-state`, `ha-check`, `ha addons logs` und
  `esphome-build compile` sind ohne Rückfrage erlaubt.
- `claude_allow` und `claude_deny` nehmen weitere Regeln im Format von
  Claude Code auf, z. B. `Bash(git status)` oder `Edit(/config/packages/**)`.
- Regeln, die du selbst in `settings.json` einträgst, bleiben erhalten. Regeln,
  die das Add-on gesetzt hat und die nicht mehr konfiguriert sind, entfernt es
  wieder.

Änderungen wirken nach einem Neustart des Add-ons. Laufende Panes gehen dabei
verloren, siehe unten.

## Was erhalten bleibt

Das Home-Verzeichnis liegt in `/data/home` und übersteht Neustarts und Updates:
herdr-Zustand (`~/.config/herdr`), Claude Code samt Anmeldung (`~/.local`,
`~/.claude`), git-Konfiguration und Shell-Verlauf.

Nach einem Neustart stellt herdr Workspaces, Tabs und Panes mit ihren
Arbeitsverzeichnissen wieder her. Laufende Prozesse überstehen einen Neustart
nicht; unterstützte Agents können ihre Sitzungen fortsetzen.

## Umgebung

- `/config`, `/share` und `/addons` sind beschreibbar eingebunden, der eigene
  Konfigurationsordner des Add-ons liegt unter `/addon_config`.
- `SUPERVISOR_TOKEN` steht in allen Panes und Login-Shells bereit
  (`http://supervisor/core/api/...`).
- Claude Code wird beim ersten Start installiert und aktualisiert sich selbst.

## Home-Assistant-Werkzeuge

| Werkzeug | Zweck |
|---|---|
| `ha-state [entity\|domain.\|muster] [-a]` | Zustände von Entitäten, z. B. `ha-state light.` |
| `ha-api [-s] [METHODE] PFAD [JSON]` | REST-API von Core, `-s` für die Supervisor-API |
| `ha-ws TYP [JSON]` | Ein Befehl der WebSocket-API (Registries, Storage-Dashboards) |
| `ha-check` | Konfiguration prüfen |
| `ha-notify "Text" ["Titel"]` | Benachrichtigung in Home Assistant oder über `HA_NOTIFY_SERVICE` |
| `ha`, `yq` | Supervisor-CLI und YAML-Editor |
| `esphome-build compile\|upload\|install DATEI` | ESPHome-Firmware über den Device Builder bauen und flashen |
| `esphome-mcp [--check]` | MCP-Brücke zum Device Builder (ab ESPHome 2026.10) |

Die Claude-Code-Skills `home-assistant` und `esphome` beschreiben diese
Werkzeuge. Sie werden bei jedem Start nach `~/.claude/skills` kopiert, eigene
Änderungen an diesen beiden Skills gehen dabei verloren. Der MCP-Server `esphome`
wird beim Start für Claude Code eingetragen, sofern es noch keinen mit diesem
Namen gibt.

### ESPHome

`esphome-build` und `esphome-mcp` steuern das Add-on ESPHome Device Builder.
Builds und Installationen nutzen also dessen Toolchain und gespeicherte
Zugangsdaten. Add-ons können keine Ingress-Sitzungen öffnen, deshalb verwenden
beide den eigenen Port des Device Builders:

1. ESPHome-Add-on → Konfiguration: `leave_front_door_open` einschalten.
2. Unter Netzwerk den Port `6052/tcp` auf `6052` setzen und das Add-on neu
   starten.

Die Werkzeuge finden den Port selbst, `ESPHOME_URL` überschreibt die Adresse.
**Der Device Builder hat auf Port 6052 dann keine Anmeldung**: Jeder in deinem
Netzwerk kann deine Geräte ändern und flashen. Mach das nur in einem
vertrauenswürdigen Netzwerk.

`esphome-mcp` braucht den MCP-Endpunkt des Device Builders (ab ESPHome 2026.10).
Bis dahin meldet es das, und `esphome-build` übernimmt.

## Sicherheit

Das Add-on bietet vollen Shell-Zugriff mit Schreibrechten auf deine
Home-Assistant-Konfiguration und auf die Supervisor-API mit der Rolle `manager`
(Add-ons verwalten und umkonfigurieren, Backups). Trag nur Schlüssel ein, denen
du vertraust, und gib Port 2222 nicht ins Internet frei.
