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
  herdr machine add ha-herdr   # als Maschine speichern, erscheint in der Seitenleiste
  herdr --remote ha-herdr      # oder direkt anhängen (schlanker lokaler Client)
  ssh ha-herdr                 # oder einfach SSH, dann: herdr
  ```

### Mit anderen herdrs verbinden

Das Add-on hat einen eigenen SSH-Schlüssel (`~/.ssh/id_ed25519`). Er entsteht
beim ersten Start und übersteht Neustarts und Updates. Den öffentlichen
Schlüssel zeigt das Add-on bei jedem Start im **Log** an (Zeile „Public SSH key
of this herdr“), im Terminal auch mit `cat ~/.ssh/id_ed25519.pub`.

Trag ihn beim anderen herdr (oder beim Zielrechner) unter `authorized_keys`
ein und leg hier einen Host-Eintrag an:

```
# ~/.ssh/config (liegt in /data/home und bleibt erhalten)
Host anderer-herdr
  HostName anderer-host.local
  Port 2222
  User root
```

Am bequemsten ist eine **gespeicherte Maschine**. Sie erscheint in der
Seitenleiste von herdr, ihre Workspaces lassen sich dort öffnen wie die eigenen:

```sh
herdr machine add anderer-herdr --label server   # einrichten und speichern
herdr machine list                                # gespeicherte Maschinen
herdr machine status                              # Verbindung prüfen
herdr --machine server workspace list             # einzelner API-Befehl
```

`herdr machine` kennt außerdem `reconnect`, `rename`, `remove`, `enable` und
`disable`.

Alternativ hängt `herdr --remote` den anderen herdr direkt an. In einem Pane
dieses Add-ons verweigert herdr das als „nested herdr“, weil jedes Pane
`HERDR_ENV=1` gesetzt hat. Für den einen Aufruf die Variable weglassen:

```sh
env -u HERDR_ENV herdr --remote anderer-herdr
```

Der äußere herdr fängt dabei seine eigenen Tastenkürzel zuerst ab, welche gelten,
steuert `--remote-keybindings local|server`.

Für einen neuen Schlüssel `~/.ssh/id_ed25519*` löschen und das Add-on neu starten.

### Kopieren und Einfügen im Web-Terminal

- **Einfügen:** `Strg+V` oder `Strg+Umschalt+V` (macOS: `Cmd+V`). Der Browser
  fragt beim ersten Mal eventuell nach der Berechtigung. Alternativ mit
  gedrückter `Umschalt`-Taste (macOS: `Option`) rechtsklicken und „Einfügen“
  wählen.
- **Kopieren:** Was herdr, Claude Code oder vim in die Zwischenablage kopieren
  (OSC 52), landet in der Zwischenablage deines Rechners. Lässt der Browser das
  ohne Klick nicht zu, erscheint oben rechts ein Knopf „In die Zwischenablage
  kopieren“.
- Text mit gedrückter `Umschalt`-Taste markieren kopiert ihn ebenfalls.
- **Strg+Enter und Umschalt+Enter** kommen als eigene Tasten an (Kitty-Protokoll).
  In Claude Code heißt Strg+Enter „jetzt senden“, Umschalt+Enter „neue Zeile“.
  In einer normalen Shell sind beide keine Enter-Taste mehr.

## Konfiguration

```yaml
authorized_keys:
  - ssh-ed25519 AAAA... name
ha_secrets:
  - grocy_api_key               # wird zu GROCY_API_KEY
  - OPENAI_API_KEY=openai_token # eigener Variablenname
env_vars:
  - name: LOG_LEVEL             # nur für Werte, die nicht geheim sind
    value: debug
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

API-Schlüssel und Tokens (z. B. für GitHub, Grocy oder andere Onlinedienste)
lassen sich allen herdr-Panes und Login-Shells mitgeben. Es gibt drei optionale
Quellen; kommt ein Name mehrfach vor, gewinnt die spätere:

1. **`ha_secrets`** (empfohlen für Geheimnisse): Schlüssel aus
   `/config/secrets.yaml` von Home Assistant. Nur die hier aufgeführten
   Schlüssel werden exportiert, nie die ganze Datei. `grocy_api_key` wird zu
   `GROCY_API_KEY`, `NAME=secret_key` setzt einen eigenen Namen.
2. **Env-Datei**: `/addon_configs/<slug>_herdr/env` (erreichbar über Samba oder
   das Studio-Code-Server-Add-on), eine Zeile `KEY=value` pro Variable, `#` für
   Kommentare. Die Datei wird beim ersten Start mit Beispielen angelegt.
3. **`env_vars`**: Name/Wert-Paare aus der Konfigurationsoberfläche des Add-ons.
   Gedacht für Einstellungen, die nicht geheim sind.

`HOME`, `PATH`, `SHELL`, `TERM` und `SUPERVISOR_TOKEN` verwaltet das Add-on, sie
lassen sich nicht überschreiben. Das Add-on-Log nennt nur die Namen der
geladenen Variablen, nie ihre Werte.

#### Geheimnisse gehören in `secrets.yaml`

Tokens und Passwörter bitte nicht in `env_vars` eintragen. Die Oberfläche zeigt
die Werte zwar verdeckt an, gespeichert werden sie aber im Klartext in
`/data/options.json` des Add-ons. Diese Datei liegt im selben Container, in dem
die Agents als root arbeiten, und wird beim Untersuchen der Umgebung leicht
mitgelesen. Dann steht das Token im Chatverlauf. Außerdem landet sie in jeder
Add-on-Sicherung.

Besser:

1. Das Geheimnis in `/config/secrets.yaml` eintragen:

   ```yaml
   github_pat: ghp_...
   ```

2. In der Add-on-Konfiguration unter `ha_secrets` darauf verweisen:

   ```yaml
   ha_secrets:
     - GITHUB_PAT=github_pat
   ```

3. Das Add-on neu starten. In den Panes steht dann `$GITHUB_PAT` bereit.

So liegen alle Geheimnisse an einer Stelle, Agents behandeln `secrets.yaml` als
vertraulich, und ein Token lässt sich an einer Stelle austauschen. Eine harte
Grenze ist das nicht: Was als Umgebungsvariable exportiert wird, kann jeder
Prozess im Add-on lesen, auch ein Agent. Gib dem Add-on deshalb nur Tokens mit
den Rechten, die die Agents wirklich brauchen.

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

Nicht ins Backup gehen Caches (`~/.cache`), Erweiterungen (siehe unten) und
ältere Claude-Code-Versionen. Fehlt Claude Code nach einer Wiederherstellung,
installiert das Add-on es beim Start neu.

Nach einem Neustart stellt herdr Workspaces, Tabs und Panes mit ihren
Arbeitsverzeichnissen wieder her. Laufende Prozesse überstehen einen Neustart
nicht; unterstützte Agents können ihre Sitzungen fortsetzen.

### Arbeitsverzeichnis für Claude Code

herdr startet neue Panes in `/config`. Dort sollte auch Claude Code laufen:

- **Vertrauensabfrage:** Claude Code fragt pro Verzeichnis einmal, ob du dem
  Ordner vertraust, und merkt sich die Antwort. Für das Home-Verzeichnis
  (`/data/home`) speichert es sie nie, dort kommt die Frage bei jedem Start.
- **Memory:** Claude Code legt seine automatischen Notizen pro Startverzeichnis
  ab (`~/.claude/projects/-config/memory/` für `/config`). Wer mal hier, mal dort
  startet, hat getrennte Notizen.

Workspaces aus älteren Versionen werden mit ihrem alten Verzeichnis
wiederhergestellt, oft `/data/home`. Dann einen neuen Workspace in `/config`
öffnen und den alten schließen.

Allgemeine Regeln und Wissen über Home Assistant bringt das Add-on selbst mit
(verwalteter Block in `~/.claude/CLAUDE.md`, Skills). Was nur deine Installation
betrifft (Räume, Namen, eigene Pakete), gehört in `/config/CLAUDE.md`; laufende
Projekte und persönliche Vorlieben in die Memory.

## Umgebung

- `/config`, `/share` und `/addons` sind beschreibbar eingebunden, der eigene
  Konfigurationsordner des Add-ons liegt unter `/addon_config`.
- `SUPERVISOR_TOKEN` steht in allen Panes und Login-Shells bereit
  (`http://supervisor/core/api/...`).
- Claude Code wird beim ersten Start installiert und aktualisiert sich selbst.
- Dabei sind Node.js 24 (`node`, `npm`, `npx`), `uv`/`uvx` für Python, die
  GitHub-CLI `gh`, `git`, `vim`, `nano`, `jq`, `yq` und `ripgrep`.
- **GitHub:** Steht `GH_TOKEN` oder `GITHUB_TOKEN` in der Umgebung (am besten
  über `ha_secrets`, z. B. `GH_TOKEN=github_token`), nutzen `gh` und `git push`
  über HTTPS diesen Token.

## Erweiterungen

Weitere Werkzeuge kommen über die Konfiguration dazu. Ein Hintergrunddienst
installiert sie nach dem Start, herdr ist währenddessen schon nutzbar.
Fortschritt und Fehler stehen im Add-on-Log. Eine Erweiterung, die nicht
installiert werden kann, hält das Add-on nicht an.

```yaml
apt_packages:
  - htop
npm_packages:
  - ruflo                 # ohne Version: beim Start aktualisiert, wenn es eine neue gibt
  - "@scope/tool@1.2.3"   # mit Version: bleibt fest
uv_tools:
  - ruff
```

| Option | Wohin | Beim Start |
|---|---|---|
| `apt_packages` | in den Container | jedes Mal installiert, Downloads aus dem Cache |
| `npm_packages` | `~/.local` (Befehle in `~/.local/bin`) | nur neu geladen, wenn sich die Version ändert |
| `uv_tools` | `~/.local/share/uv` | ohne Versionsangabe aktualisiert |

Wer ein Paket aus der Liste nimmt, dem entfernt herdr es beim nächsten Start.
Installierte Erweiterungen und Caches überstehen Neustarts, gehen aber **nicht**
ins Backup. Nach einer Wiederherstellung installiert herdr sie neu. Von Hand
aufrufen: `herdr-extensions`.

### Eigene Startschritte

Skripte unter `/addon_config/init.d/*.sh` laufen nach den Erweiterungen bei jedem
Start, alphabetisch, im Verzeichnis `/config` und mit deinen Umgebungsvariablen.
Gut für Konfiguration, die Erweiterungen brauchen, etwa MCP-Server für Claude Code:

```sh
# /addon_config/init.d/20-ruflo.sh
claude mcp get ruflo >/dev/null 2>&1 || claude mcp add --scope user ruflo -- ruflo mcp start
```

ruflo schickt standardmäßig Nutzungsereignisse an seine Server („Funnel“).
Abschalten mit `RUFLO_FUNNEL=0` in `/addon_config/env`.

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
Werkzeuge, der Skill `herdr` (aus `herdr --skill`) die Steuerung von Panes,
Tabs und Workspaces. Sie werden bei jedem Start nach `~/.claude/skills`
geschrieben, eigene Änderungen an diesen drei Skills gehen dabei verloren. Der MCP-Server `esphome`
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

Läuft `esphome-build` in herdr (auch aus Claude Code heraus), öffnet es unter
dem aufrufenden Pane ein Fortschritts-Pane: Phase, Balken für Kompilieren und
Hochladen, Laufzeit und das Ende des Logs. Der nächste Build nutzt dasselbe
Pane wieder, schließen kannst du es jederzeit. `ESPHOME_BUILD_PANE=0` schaltet
das ab. Das ganze Log liegt unter `/tmp/esphome-build/<gerät>.log`. Builds über
den MCP-Server `esphome` zeigen kein Pane.

## Sicherheit

Das Add-on bietet vollen Shell-Zugriff mit Schreibrechten auf deine
Home-Assistant-Konfiguration und auf die Supervisor-API mit der Rolle `manager`
(Add-ons verwalten und umkonfigurieren, Backups). Trag nur Schlüssel ein, denen
du vertraust, und gib Port 2222 nicht ins Internet frei.
