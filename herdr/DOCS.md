# herdr

A persistent [herdr](https://herdr.dev) server inside Home Assistant. Coding agents
such as Claude Code keep running here, even when the client disconnects.

## Access

- **Web terminal:** "herdr" in the sidebar. Attaches to the running server.
- **SSH / herdr remote:** port 2222, public key login as `root` only.

  Example `~/.ssh/config`:

  ```
  Host ha-herdr
    HostName homeassistant.local
    Port 2222
    User root
  ```

  ```sh
  herdr --remote ha-herdr   # thin local client, herdr installed locally
  ssh ha-herdr              # or plain SSH, then run: herdr
  ```

## Configuration

```yaml
authorized_keys:
  - ssh-ed25519 AAAA... name
ha_secrets:
  - grocy_api_key               # exported as GROCY_API_KEY
  - OPENAI_API_KEY=openai_token # custom variable name
env_vars:
  - name: SOME_TOKEN
    value: "..."
```

### `authorized_keys`

Public keys allowed to log in via SSH. Without keys, SSH login is not possible
(the web terminal still works).

### Environment variables

API keys and tokens (e.g. for Grocy or other online services) can be provided to
all herdr panes and login shells. There are three optional sources; when a name
appears more than once, the later source wins:

1. **`ha_secrets`**: keys from Home Assistant's `/config/secrets.yaml`. Only the
   keys listed here are exported, never the whole file. `grocy_api_key` becomes
   `GROCY_API_KEY`; `NAME=secret_key` sets a custom name.
2. **Env file**: `/addon_configs/<slug>_herdr/env` (visible via Samba or the
   Studio Code Server add-on), one `KEY=value` per line, `#` for comments.
   The file is created with examples on first start.
3. **`env_vars`**: name/value pairs set in the add-on configuration UI. Values are
   masked in the UI.

`HOME`, `PATH`, `SHELL`, `TERM` and `SUPERVISOR_TOKEN` are managed by the add-on
and cannot be overridden. The add-on log lists the names of loaded variables,
never their values.

Changes take effect after restarting the add-on. Running panes are lost on a
restart, see below.

## What persists

The home directory lives in `/data/home` and survives restarts and updates:
herdr state (`~/.config/herdr`), Claude Code including its login (`~/.local`,
`~/.claude`), git configuration and shell history.

After a restart, herdr restores workspaces, tabs and panes with their working
directories. Running processes do not survive a restart; supported agents can
resume their sessions.

## Environment

- `/config`, `/share` and `/addons` are mounted read-write; the add-on's own
  config folder is at `/addon_config`.
- `SUPERVISOR_TOKEN` is available in all panes and login shells
  (`http://supervisor/core/api/...`).
- Claude Code is installed on first start and updates itself.

## Security

This add-on gives full shell access with write access to your Home Assistant
configuration and the Supervisor API. Only add keys you trust, and do not expose
port 2222 to the internet.
