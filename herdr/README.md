# herdr Add-on

![Supports amd64](https://img.shields.io/badge/amd64-yes-green.svg)
![Supports aarch64](https://img.shields.io/badge/aarch64-yes-green.svg)

Persistenter [herdr](https://herdr.dev)-Server in Home Assistant. herdr ist ein
Terminal-Multiplexer für Coding-Agents wie Claude Code: Die Sitzungen laufen im
Add-on weiter, egal ob der Client getrennt wird, der Laptop zugeklappt ist oder
die SSH-Verbindung abreißt.

## Funktionen

- herdr-Server startet automatisch mit Home Assistant (mit Watchdog)
- **Web-Terminal** in der Seitenleiste (Ingress)
- **SSH auf Port 2222** (nur Public Key) für `herdr --remote` vom eigenen Rechner
- **Claude Code** wird beim ersten Start installiert und aktualisiert sich selbst
- `/config`, `/share` und `/addons` beschreibbar, `SUPERVISOR_TOKEN` in allen Panes
- Home-Verzeichnis in `/data`: herdr-Layout, Claude-Anmeldung, Git-Konfiguration
  und Verlauf überstehen Neustarts und Updates

## Installation

1. Dieses Repository im Add-on-Store hinzufügen:

   [![Add repository](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FOttes42%2Fha-addons)

2. „herdr“ installieren. Das Image wird lokal gebaut, das dauert ein paar Minuten.
3. In der Konfiguration die eigenen SSH-Public-Keys unter `authorized_keys` eintragen.
4. Starten und „herdr“ in der Seitenleiste öffnen.

## Verbinden vom eigenen Rechner

`~/.ssh/config`:

```
Host ha-herdr
  HostName homeassistant.local
  Port 2222
  User root
```

```sh
herdr --remote ha-herdr   # herdr lokal installiert, dünner Client
ssh ha-herdr              # oder per SSH, dann: herdr
```

## Neustarts

herdr stellt nach einem Neustart Workspaces, Tabs und Panes samt Verzeichnissen
wieder her. Die laufenden Prozesse selbst überleben einen Neustart nicht;
unterstützte Agents können ihre Sitzung fortsetzen.

Weitere Details: [DOCS.md](DOCS.md)
