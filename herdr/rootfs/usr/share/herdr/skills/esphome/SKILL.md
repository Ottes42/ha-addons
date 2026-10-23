---
name: esphome
description: ESPHome-Firmware über das Add-on ESPHome Device Builder bearbeiten, prüfen, kompilieren und installieren. Nutzen für alles rund um ESPHome-Geräte, ihr YAML in /config/esphome, OTA-Updates, fehlgeschlagene Installationen oder Firmware-Versionen.
---

Die Geräte-YAMLs liegen in `/config/esphome` und lassen sich direkt lesen und
bearbeiten. Builds und Installationen laufen über das Add-on ESPHome Device
Builder, nutzen also dessen Toolchain und gespeicherte Zugangsdaten. Beide
Werkzeuge erreichen ihn über Port 6052; melden sie, dass der Port nicht
freigegeben ist, den Nutzer bitten, im ESPHome-Add-on `leave_front_door_open`
einzuschalten und Port 6052 freizugeben.

## esphome-build (jede ESPHome-Version)

```sh
esphome-build compile esp32c3-btproxy-buro.yaml
esphome-build install esp32c3-btproxy-buro.yaml        # kompilieren, dann per OTA hochladen
esphome-build upload  esp32c3-btproxy-buro.yaml OTA    # letzten Build hochladen
```

Die Ausgabe filtern, der Upload-Fortschrittsbalken ist lang:
`esphome-build install x.yaml 2>&1 | grep -vE 'Uploading: \[' | tail -30`.
In herdr zeigt `esphome-build` den Fortschritt selbst in einem Pane unter dem
aufrufenden an (nichts weiter zu tun), das volle Log liegt in
`/tmp/esphome-build/<gerät>.log`. Für Builds, die der Nutzer mitverfolgen soll,
deshalb `esphome-build` statt MCP-`install` nehmen.
Exit-Code 1 heißt Fehler, das Ende des Logs sagt warum. „No route to host“
heißt: Gerät offline.

## MCP-Server `esphome` (ab ESPHome 2026.10)

`esphome-mcp` verbindet Claude Code mit dem MCP-Endpunkt des Device Builders.
Prüfen mit `esphome-mcp --check`; bei älteren Versionen meldet es, dass der
Endpunkt fehlt, dann `esphome-build` nehmen.

Ablauf: `list_devices` → `get_config` → `update_config` (braucht den Text aus
`get_config` als `expected`) → `validate_config` → `install` → `get_job` abfragen,
bis der Job fertig ist. Lange Aufgaben starten und dann abfragen.

## Regeln

- Ein Flash lässt sich nicht rückgängig machen. Nie eine Konfiguration
  installieren, die `wifi:`, `api:` oder `ota:` entfernt oder das Board ändert;
  das rettet nur noch ein serielles Kabel.
- Vor dem Flashen nachfragen. Ein Gerät installieren, prüfen, dass es in Home
  Assistant wieder online ist (`ha-ws config/device_registry/list`,
  `sw_version`), dann das nächste.
- `secrets.yaml` und Passwörter nicht ausgeben, außer auf Wunsch.

## OTA-Verschlüsselung (ESPHome 2026.9+)

OTA-Updates wechseln von `ota: password:` zu `ota: encryption:` (nutzt den
API-Schlüssel). Umstellung in zwei Installationen: erst mit Passwort in der
Konfiguration aktualisieren, dann `password:` durch `encryption:` ersetzen und
erneut installieren. Wer das Passwort zuerst entfernt, bekommt
`ESP requests password, but no password given!`. Unverschlüsselte Updates
funktionieren nur bis 2027.3.0.
