# herdr für Home Assistant

![amd64](https://img.shields.io/badge/amd64-ja-green.svg)
![aarch64](https://img.shields.io/badge/aarch64-ja-green.svg)

![herdr mit mehreren Tabs und Panes](https://raw.githubusercontent.com/Ottes42/ha-addons/main/herdr/images/screenshot-raumklima.png)

[herdr](https://herdr.dev) ist ein Terminal-Multiplexer für Coding-Agents. Dieses
Add-on lässt ihn dauerhaft in Home Assistant laufen: Claude Code arbeitet weiter,
auch wenn du die Verbindung trennst, und hat dabei alles, was es für deine
Installation braucht.

## Was drin ist

**Zugriff**
- Web-Terminal in der Seitenleiste, mit Zwischenablage und Strg+Enter
- SSH auf Port 2222 für `herdr` vom eigenen Rechner
- Eigener SSH-Schlüssel, um andere herdrs zu verbinden

**Für Agents**
- Claude Code, installiert und selbst aktualisierend
- Werkzeuge für Home Assistant: `ha-state`, `ha-api`, `ha-ws`, `ha-check`, `ha-notify`, `ha`
- ESPHome bauen und flashen: `esphome-build`, MCP-Server `esphome-mcp`
- ESPHome-Logs ohne Kabel und dekodierte Absturzberichte: `esphome-logs`, `esphome-crash`
- Skills für Home Assistant, ESPHome und herdr, eigene Anweisungen und Berechtigungen

**Werkzeuge und Erweiterungen**
- Node.js 24, `uv`, `gh`, `git`, `vim`, `jq`, `yq`, `ripgrep`
- Weitere Pakete aus Debian, npm und Python per Konfiguration, eigene Startskripte
- Geheimnisse aus `secrets.yaml` als Umgebungsvariablen

**Dauerhaft**
- Workspaces, Anmeldung und Verlauf überstehen Neustarts und Updates
- Backups ohne Caches und neu installierbare Erweiterungen

| | |
|---|---|
| ![Zweiter Tab: Add-ons mit Status und anstehenden Updates](https://raw.githubusercontent.com/Ottes42/ha-addons/main/herdr/images/screenshot-addons.png) | ![Workspace „ha-addons“: git-Verlauf und config.yaml nebeneinander](https://raw.githubusercontent.com/Ottes42/ha-addons/main/herdr/images/screenshot-repo.png) |
| Tabs: Add-ons und Updates im Blick | Workspaces: am Add-on-Repo arbeiten |

## Loslegen

1. Repository zum Add-on-Store hinzufügen:

   [![Repository hinzufügen](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FOttes42%2Fha-addons)

2. „herdr“ installieren und starten, dann „herdr“ in der Seitenleiste öffnen.
3. Für SSH die eigenen öffentlichen Schlüssel unter `authorized_keys` eintragen.

## Vom eigenen Rechner

```
# ~/.ssh/config
Host ha-herdr
  HostName homeassistant.local
  Port 2222
  User root
```

```sh
herdr machine add ha-herdr   # erscheint in der Seitenleiste von herdr
herdr --remote ha-herdr      # oder direkt anhängen
```

Alles Weitere, von Erweiterungen bis ESPHome, steht in der
[Dokumentation](DOCS.md).
