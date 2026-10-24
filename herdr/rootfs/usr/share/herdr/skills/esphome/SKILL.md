---
name: esphome
description: ESPHome-Firmware über das Add-on ESPHome Device Builder bearbeiten, prüfen, kompilieren und installieren. Nutzen für alles rund um ESPHome-Geräte, ihr YAML in /config/esphome, OTA-Updates, fehlgeschlagene Installationen oder Firmware-Versionen, Geräte-Logs, Abstürze, Bootschleifen, Safe Mode und OTA-Rollback.
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

## Logs und Abstürze

```sh
esphome-logs kiana-nachtuhr.yaml                 # 60 s Logs über die API, ohne Kabel
esphome-logs kiana-nachtuhr.yaml 120 --until 'Boot seems successful'
esphome-logs kiana-nachtuhr.yaml 30 --no-states  # ohne Zustandsänderungen
esphome-crash kiana-nachtuhr.yaml                # Absturz des letzten Boots, dekodiert
esphome-crash kiana-nachtuhr.yaml - < log.txt    # gespeicherten Auszug dekodieren
```

Immer mit Zeitlimit aufrufen (`0` läuft endlos): Ist das Gerät offline,
versucht der Device Builder es still weiter. `--until` endet mit Exit-Code 1,
wenn die Zeit vorher abläuft. Die Warnung `EncryptionHelloAPIError` direkt nach
dem Start ist harmlos, der Builder verbindet danach verschlüsselt.

Beim Verbinden eines Log-Clients gibt das Gerät seine Konfigurationsübersicht
aus, darunter Safe-Mode- und Rollback-Hinweise und den Absturzbericht. Was
darin steht:

- `*** CRASH DETECTED ON PREVIOUS BOOT ***` mit `Reason` (z. B. `Task wdt`,
  `LoadProhibited`), `PC` und `BT0…`: Absturz vor dem letzten Neustart.
  Großgeschrieben (`PC:`, `BT0:`) stammt er von der laufenden Firmware;
  ESPHome dekodiert dann selbst, in den Logs stehen `Decoded 0x…`-Zeilen.
- `Captured by a different firmware build` mit kleingeschriebenem `pc:`/`bt0:`:
  Der Absturz kam von einer anderen Firmware, meist der gerade geflashten, die
  per Rollback verworfen wurde. ESPHome dekodiert das absichtlich nicht.
  `esphome-crash` dekodiert gegen den letzten lokalen Build und sagt am Ende,
  ob das passt: „likely the crashed build“ heißt verwertbar, „most likely
  WRONG“ heißt, der lokale Build ist die laufende Firmware, die Symbole sind
  Unsinn. Deshalb **`esphome-crash` vor dem nächsten Kompilieren** ausführen,
  danach ist die ELF des abgestürzten Builds überschrieben.
- `OTA rollback detected! Rolled back from partition 'app1'` und `The device
  reset before the boot was marked successful`: Die neue Firmware ist beim
  Booten abgestürzt, das Gerät läuft wieder mit der alten. Das Flashen gilt
  also nicht als gelungen, auch wenn der Upload „Successfully uploaded“ meldete.
  Nach einem Flash daher mit `esphome-logs … --until 'Boot seems successful'`
  oder per `sw_version` in der Geräte-Registry prüfen.
- `SAFE MODE IS ACTIVE`, `Boot loop detected`, `Last reset too quick; invoke in
  N restarts`: Bootschleife; im Safe Mode läuft nur WLAN und OTA. Ursache in
  der Konfiguration beheben und neu flashen.
- `brownout`: Stromversorgung, keine Firmware-Ursache.

Den Backtrace von oben nach unten lesen: `pc`/`bt0` ist die Stelle des
Absturzes, darunter die Aufrufer. Zeilen mit `gerät.yaml:NN` zeigen auf
Lambdas im YAML, `src/…` auf eigene Header und ESPHome-Code. Ein Task-WDT heißt:
`loop()` oder `setup()` hing (lange Schleifen, `delay()`, Zugriffe auf Objekte,
die noch nicht eingerichtet sind, z. B. LVGL aus einem `on_value`, das beim
Setup durch `restore_value`/`initial_option` feuert).

Fallen:

- Der Absturzbericht bleibt nur bis zum nächsten Neustart, sobald ein
  API-Client ihn abgeholt hat (Dashboard-Logs, `esphome-logs`). Ein Flash oder
  Neustart nach dem Abholen löscht ihn.
- `esphome-crash` braucht einen lokalen Build im Device Builder
  (`not decoded: no_build` → einmal `esphome-build compile`).
- Logs zeigen nur, was `logger: level:` durchlässt; Geräte ohne `api:` liefern
  keine Logs über das Netz.

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
