# herdr Add-on

![Supports amd64](https://img.shields.io/badge/amd64-yes-green.svg)
![Supports aarch64](https://img.shields.io/badge/aarch64-yes-green.svg)

A persistent [herdr](https://herdr.dev) server inside Home Assistant. herdr is a
terminal multiplexer for coding agents such as Claude Code: sessions keep running
in the add-on, whether the client disconnects, the laptop lid closes or the SSH
connection drops.

## Features

- herdr server starts automatically with Home Assistant (with watchdog)
- **Web terminal** in the sidebar (ingress)
- **SSH on port 2222** (public key only) for `herdr --remote` from your machine
- **Claude Code** is installed on first start and updates itself
- **Environment variables** for API keys and tokens, from `secrets.yaml`, an env
  file or the configuration UI
- `/config`, `/share` and `/addons` writable, `SUPERVISOR_TOKEN` in all panes
- Home directory in `/data`: herdr layout, Claude login, git config and history
  survive restarts and updates

## Installation

1. Add this repository to the add-on store:

   [![Add repository](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FOttes42%2Fha-addons)

2. Install "herdr". The image is built locally, which takes a few minutes.
3. Add your SSH public keys under `authorized_keys` in the configuration.
4. Start the add-on and open "herdr" in the sidebar.

## Connecting from your machine

`~/.ssh/config`:

```
Host ha-herdr
  HostName homeassistant.local
  Port 2222
  User root
```

```sh
herdr --remote ha-herdr   # herdr installed locally, thin client
ssh ha-herdr              # or plain SSH, then run: herdr
```

## Restarts

After a restart, herdr restores workspaces, tabs and panes with their working
directories. Running processes do not survive a restart; supported agents can
resume their sessions.

More details, including environment variables: [DOCS.md](DOCS.md)
