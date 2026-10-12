---
name: home-assistant
description: Mit Home Assistant aus dem herdr-Add-on sprechen. Nutzen beim Lesen von Entitätszuständen, Aufrufen von Diensten, Rendern von Templates, Prüfen der Konfiguration, Bearbeiten von Registries oder Storage-Dashboards über die WebSocket-API, Verwalten anderer Add-ons oder um den Nutzer nach einer langen Aufgabe zu benachrichtigen.
---

Das herdr-Add-on bringt kleine CLI-Werkzeuge mit, die sich mit `$SUPERVISOR_TOKEN`
über den Supervisor-Proxy anmelden. Nimm sie statt selbst geschriebener curl-
oder Python-Clients.

| Werkzeug | Zweck |
|---|---|
| `ha-state [entity\|domain.\|muster] [-a]` | Zustände als `entity<TAB>wert einheit<TAB>name`; `-a` gibt das volle JSON mit Attributen aus. `ha-state light.`, `ha-state 'sensor.buro_*'` |
| `ha-api [-s] [METHODE] PFAD [JSON\|-]` | REST-API von Core (`states/...`, `services/<domain>/<service>`, `template`, `history/period/...`). `-s` spricht die Supervisor-API an (`addons`, `addons/<slug>/logs`, `backups`) |
| `ha-ws TYP [JSON\|-]` | Ein WebSocket-Befehl, gibt sein `result` aus. Registries (`config/entity_registry/list`, `.../update`), `lovelace/config`, `lovelace/config/save`, `recorder/...` |
| `ha-check` | Konfiguration prüfen, Exit-Code 1 wenn ungültig. Vor jedem Reload oder Neustart ausführen |
| `ha-notify "Text" ["Titel"]` | Den Nutzer benachrichtigen (Persistent Notification oder `HA_NOTIFY_SERVICE`) |
| `ha` | Offizielle Supervisor-CLI: `ha addons`, `ha addons logs <slug>`, `ha backups new --name X`, `ha core info` |
| `yq` | YAML direkt bearbeiten: `yq -i '.key = "value"' datei.yaml` |

## Regeln

- Zuerst eine vorhandene `CLAUDE.md` in `/config` lesen; sie hat Vorrang vor
  diesen Vorgaben.
- Nach YAML-Änderungen: `ha-check`, dann gezielt die Domain neu laden
  (`ha-api POST services/automation/reload`) statt Core neu zu starten.
- `/config/.storage/` nie bearbeiten, solange Home Assistant läuft; stattdessen
  `ha-ws`.
- Templates zum Testen rendern: `ha-api POST template '{"template": "{{ ... }}"}'`.
- Das Add-on läuft mit der Supervisor-Rolle `manager`. Das herdr-Add-on selbst
  nicht neu starten, stoppen oder umkonfigurieren (das beendet die Sitzung) und
  vor einem Neustart von Core oder anderen Add-ons nachfragen.
- Wenn eine lange oder unbeaufsichtigte Aufgabe fertig ist, `ha-notify` ausführen.

## Stolperfallen

- **YAML-Dashboards** (`mode: yaml`): Home Assistant cacht die Konfiguration und
  prüft nur die mtime der Hauptdatei, nicht die der per `!include` eingebundenen
  Views. Nach Änderungen an einer eingebundenen Datei die Hauptdatei mit `touch`
  anfassen, dann den Browser neu laden.
- **Storage-Dashboards** (UI-Modus, `.storage/lovelace.*`): mit `ha-ws lovelace/config`
  laden und mit `ha-ws lovelace/config/save` speichern, nie die Datei bearbeiten.
- **Umbenennen von Geräten oder Entities**: Ist die gewünschte Entity-ID noch
  belegt (z. B. von einem alten oder umgezogenen Gerät), bekommt die neue Entity
  einen Ersatznamen wie `sensor.0x<ieee>_*` oder `_2`. Vorher mit
  `ha-ws config/entity_registry/list` prüfen, die alte ID frei machen
  (`config/entity_registry/update` mit `new_entity_id` oder löschen) und erst dann
  umbenennen. Gerätenamen sagen nicht sicher, wo ein Gerät steht; im Zweifel
  nachfragen.
- **Automationen abschalten**: `automation.turn_off` bleibt über Neustarts
  erhalten, solange die Automation kein `initial_state` hat.
