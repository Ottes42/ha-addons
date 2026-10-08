# herdr

Persistenter [herdr](https://herdr.dev)-Server in Home Assistant. Coding-Agents
(z. B. Claude Code) laufen hier weiter, auch wenn der Client getrennt wird.

## Zugriff

- **Web-Terminal:** Eintrag „herdr“ in der Seitenleiste. Hängt sich an den laufenden Server.
- **SSH / herdr remote:** Port 2222, nur Public-Key-Login als `root`.

  ```sh
  ssh -p 2222 root@homeassistant.local      # dann: herdr
  herdr --remote root@homeassistant.local   # Port 2222 in ~/.ssh/config hinterlegen
  ```

  Beispiel `~/.ssh/config`:

  ```
  Host ha-herdr
    HostName homeassistant.local
    Port 2222
    User root
  ```

## Optionen

```yaml
authorized_keys:
  - ssh-ed25519 AAAA... name
```

## Was erhalten bleibt

Das Home-Verzeichnis liegt in `/data/home` und übersteht Neustarts und Updates:
herdr-Zustand (`~/.config/herdr`), Claude Code samt Anmeldung (`~/.local`, `~/.claude`),
Git-Konfiguration und Shell-Verlauf.

Nach einem Neustart stellt herdr Workspaces, Tabs und Panes mit ihren Verzeichnissen
wieder her. Laufende Prozesse überleben einen Neustart nicht; unterstützte Agents
können ihre Sitzung fortsetzen.

## Umgebung

- `/config`, `/share` und `/addons` sind beschreibbar eingebunden.
- `SUPERVISOR_TOKEN` steht in allen Panes und Login-Shells zur Verfügung
  (`http://supervisor/core/api/...`).
- Claude Code wird beim ersten Start installiert und aktualisiert sich selbst.
