# herdr Add-on

![Unterstützt amd64](https://img.shields.io/badge/amd64-ja-green.svg)
![Unterstützt aarch64](https://img.shields.io/badge/aarch64-ja-green.svg)

Ein dauerhaft laufender [herdr](https://herdr.dev)-Server in Home Assistant.
herdr ist ein Terminal-Multiplexer für Coding-Agents wie Claude Code: Sitzungen
laufen im Add-on weiter, auch wenn der Client die Verbindung trennt, der Laptop
zugeklappt wird oder die SSH-Verbindung abreißt.

## Funktionen

- herdr-Server startet automatisch mit Home Assistant (mit Watchdog)
- **Web-Terminal** in der Seitenleiste (Ingress)
- **SSH auf Port 2222** (nur mit öffentlichem Schlüssel) für `herdr --remote`
  vom eigenen Rechner
- **Eigener SSH-Schlüssel**, bleibt erhalten, öffentlicher Teil steht im Log:
  zum Verbinden mit anderen herdrs
- **Claude Code** wird beim ersten Start installiert und aktualisiert sich selbst
- **Umgebungsvariablen** für API-Schlüssel und Tokens aus `secrets.yaml`, dazu
  eine Env-Datei und die Konfigurationsoberfläche für Werte, die nicht geheim sind
- `/config`, `/share` und `/addons` beschreibbar, `SUPERVISOR_TOKEN` in allen Panes
- **Home-Assistant-Werkzeuge** für Agents: `ha-state`, `ha-api`, `ha-ws`,
  `ha-check`, `ha-notify`, die Supervisor-CLI `ha` und `yq`
- **ESPHome**: `esphome-build` baut und flasht über den Device Builder,
  `esphome-mcp` verbindet Claude Code mit dessen MCP-Server
- **Anweisungen und Berechtigungen für Agents**: verwalteter Block in
  `CLAUDE.md`/`AGENTS.md`, eigene Anweisungen und Berechtigungsregeln über die
  Konfiguration
- **Claude-Code-Skills** `home-assistant` und `esphome`, vom Add-on aktuell
  gehalten
- Home-Verzeichnis in `/data`: herdr-Layout, Claude-Anmeldung, git-Konfiguration
  und Verlauf überstehen Neustarts und Updates

## Installation

1. Dieses Repository zum Add-on-Store hinzufügen:

   [![Repository hinzufügen](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FOttes42%2Fha-addons)

2. „herdr“ installieren. Das Image wird lokal gebaut, das dauert ein paar Minuten.
3. In der Konfiguration unter `authorized_keys` die öffentlichen SSH-Schlüssel
   eintragen.
4. Add-on starten und „herdr“ in der Seitenleiste öffnen.

## Vom eigenen Rechner verbinden

`~/.ssh/config`:

```
Host ha-herdr
  HostName homeassistant.local
  Port 2222
  User root
```

```sh
herdr --remote ha-herdr   # herdr lokal installiert, schlanker Client
ssh ha-herdr              # oder einfach SSH, dann: herdr
```

## Neustarts

Nach einem Neustart stellt herdr Workspaces, Tabs und Panes mit ihren
Arbeitsverzeichnissen wieder her. Laufende Prozesse überstehen einen Neustart
nicht; unterstützte Agents können ihre Sitzungen fortsetzen.

Mehr Details zu Umgebungsvariablen, Werkzeugen, Einfügen im Web-Terminal und
der ESPHome-Einrichtung: [DOCS.md](DOCS.md)
