<div align="center">

# Server Skills

**Claude Code server management skills — manage servers via natural language**

[English](#overview) | [中文文档](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://docs.anthropic.com/en/docs/claude-code)

</div>

---

## Overview

Server Skills is a collection of [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code) that turns natural language into server management operations. Add servers, check health, and execute remote commands — all through conversational AI.

```text
> /server-check prod-web

Server Status: prod-web (192.168.1.100)

Disk:
/dev/vda1   40G  15G  23G  40%  /

Memory:
Mem:  3.8G  2.1G  500M  128M  1.2G  1.3G

Load: 0.50, 0.30, 0.20  |  Uptime: 30 days
```

### Key Features

- **Natural language input** — conversational server management, not CLI flags
- **5 skills** — list, add, delete, health check, remote execute
- **Multiple auth methods** — SSH key, password, default key, jump host
- **Batch operations** — check multiple servers or filter by tags
- **Safety guards** — dangerous commands require double confirmation
- **Fuzzy matching** — typo-tolerant server name lookup

---

## Quick Start

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- SSH client available
- `sshpass` (only for password-based auth)

```bash
# Install sshpass if needed
apt install sshpass          # Debian/Ubuntu
brew install hudochenkov/sshpass/sshpass  # macOS
```

### Install

```bash
git clone https://github.com/Hanson/server-skills.git
cd server-skills
make install
```

This copies all skills to `~/.claude/skills/` and creates the data file at `~/.claude/servers/servers.json`.

### Use

Open Claude Code and start managing servers:

```text
/server-add prod-web 192.168.1.100
/server-add db 10.0.0.50 admin 2222 --tags production
/server-list
/server-check prod-web db
/server-ssh prod-web "docker ps"
/server-del staging
```

Or just talk naturally:

> "Check nginx status on prod-web"
>
> "Add a server named staging, address 192.168.1.200"
>
> "Check all servers tagged production"

---

## Skills Reference

| Skill | Command | Description |
|-------|---------|-------------|
| server-list | `/server-list [filter]` | List servers, filter by name or `--tags` |
| server-add | `/server-add <name> <host> [options]` | Add a server to inventory |
| server-del | `/server-del <name>` | Remove a server (with confirmation) |
| server-check | `/server-check <name>...` | Check disk/CPU/memory/load via SSH |
| server-ssh | `/server-ssh <name> "<cmd>"` | Execute command on remote server |

### server-list

```text
/server-list                  # List all
/server-list --tags production  # Filter by tag
/server-list ali              # Fuzzy match by name
```

### server-add

```text
/server-add prod-web 192.168.1.100
/server-add db 10.0.0.50 admin 2222
/server-add cache 172.16.0.10 --tags production,redis --note "Redis master"
/server-add internal 10.0.0.5 --jump-host ubuntu@1.2.3.4 --password secret
```

### server-check

```text
/server-check prod-web            # Single server
/server-check prod-web staging db # Multiple servers
/server-check --tags production   # By tag
```

### server-ssh

```text
/server-ssh prod-web "ls -la /var/log"
/server-ssh prod-db "systemctl status nginx"
/server-ssh prod-web "docker ps"
```

Dangerous commands (`rm -rf`, `shutdown`, `reboot`, `dd`, etc.) require a second confirmation before execution.

---

## Data Format

Server data is stored locally at `~/.claude/servers/servers.json`:

```json
{
  "servers": [
    {
      "name": "prod-web",
      "host": "192.168.1.100",
      "port": 22,
      "user": "root",
      "key_path": "",
      "password": "",
      "jump_host": "",
      "tags": ["production", "web"],
      "note": "Production web server"
    }
  ]
}
```

### Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `name` | Yes | — | Unique server identifier |
| `host` | Yes | — | IP address or hostname |
| `port` | No | `22` | SSH port |
| `user` | No | `root` | Login username |
| `key_path` | No | `""` | SSH key path (empty = default key) |
| `password` | No | `""` | SSH password (empty = key auth) |
| `jump_host` | No | `""` | Jump host, format `user@host` |
| `tags` | No | `[]` | Tags for grouping and filtering |
| `note` | No | `""` | Description |

## Authentication

Three SSH auth methods, selected by priority:

| Priority | Method | Condition |
|----------|--------|-----------|
| 1 | Key auth | `key_path` is set → `ssh -i <key>` |
| 2 | Password auth | `password` is set → `sshpass -p <pass> ssh` |
| 3 | Default key | Both empty → `ssh` (uses local default key) |

When `jump_host` is configured, `-J <jump_host>` is appended automatically.

---

## Project Structure

```text
server-skills/
├── Makefile                    # install / uninstall / list / clean
├── server-list/SKILL.md        # List & filter servers
├── server-add/SKILL.md         # Add server
├── server-del/SKILL.md         # Delete server
├── server-check/SKILL.md       # Health check
├── server-ssh/SKILL.md         # Remote command execution
└── scripts/
    ├── server_manager.py       # Server CRUD operations
    └── ssh_helper.py           # SSH command builder
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make install` | Install all skills to `~/.claude/skills/` |
| `make uninstall` | Remove all installed skills |
| `make list` | Show install status and registered server count |
| `make clean` | Uninstall + delete all server data (destructive) |

---

## Security Notes

- Passwords are stored in plaintext in the local JSON file — protect `~/.claude/servers/` directory permissions
- Passwords are never displayed in output — only auth type is shown
- Dangerous remote commands require a second confirmation
- Prefer key-based authentication over storing passwords

## License

[MIT](LICENSE)
