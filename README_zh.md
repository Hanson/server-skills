<div align="center">

# Server Skills

**Claude Code 服务器管理技能插件 — 用自然语言管理你的服务器**

[English](./README.md) | [中文](#概述)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://docs.anthropic.com/en/docs/claude-code)

</div>

---

## 概述

Server Skills 是一组 [Claude Code 技能插件](https://docs.anthropic.com/en/docs/claude-code)，将自然语言转化为服务器管理操作。添加服务器、检查健康状况、远程执行命令——全部通过对话式 AI 完成。

```text
> /server-check prod-web

服务器状态: prod-web (192.168.1.100)

磁盘使用:
/dev/vda1   40G  15G  23G  40%  /

内存使用:
Mem:  3.8G  2.1G  500M  128M  1.2G  1.3G

负载: 0.50, 0.30, 0.20  |  运行时间: 30 天
```

### 核心特性

- **自然语言输入** — 用中文对话管理服务器，无需记忆命令参数
- **5 个技能插件** — 列表、添加、删除、健康检查、远程执行
- **多种认证方式** — SSH 密钥、密码、默认密钥、跳板机
- **批量操作** — 同时检查多台服务器，按标签筛选
- **安全防护** — 危险命令需二次确认
- **模糊匹配** — 输入错误自动建议相似服务器名

---

## 快速开始

### 前置条件

- 已安装 [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- 系统有 SSH 客户端
- `sshpass`（仅密码认证时需要）

```bash
# 按需安装 sshpass
apt install sshpass                            # Debian/Ubuntu
brew install hudochenkov/sshpass/sshpass        # macOS
```

### 安装

```bash
git clone https://github.com/Hanson/server-skills.git
cd server-skills
make install
```

安装会将技能插件复制到 `~/.claude/skills/`，并在 `~/.claude/servers/servers.json` 创建数据文件。

### 使用

打开 Claude Code，开始管理服务器：

```text
/server-add prod-web 192.168.1.100
/server-add db 10.0.0.50 admin 2222 --tags production
/server-list
/server-check prod-web db
/server-ssh prod-web "docker ps"
/server-del staging
```

也支持自然语言：

> "帮我在 prod-web 上看看 nginx 状态"
>
> "加一台服务器叫 staging，地址 192.168.1.200"
>
> "检查所有 production 标签的服务器"

---

## 技能参考

| 技能 | 命令 | 说明 |
|------|------|------|
| server-list | `/server-list [筛选]` | 查看服务器列表，按名称或 `--tags` 筛选 |
| server-add | `/server-add <名称> <地址> [选项]` | 添加服务器到管理列表 |
| server-del | `/server-del <名称>` | 从列表中删除服务器（需确认） |
| server-check | `/server-check <名称>...` | 通过 SSH 检查磁盘/CPU/内存/负载 |
| server-ssh | `/server-ssh <名称> "<命令>"` | 在远程服务器上执行命令 |

### server-list — 查看服务器列表

```text
/server-list                    # 列出全部
/server-list --tags production  # 按标签筛选
/server-list ali                # 按名称模糊匹配
```

输出示例：

```text
服务器列表 (共 3 台)

| 名称     | 地址           | 端口 | 用户  | 认证方式  | 标签        | 备注         |
|----------|---------------|------|------|----------|-------------|-------------|
| prod-web | 192.168.1.100 | 22   | root | 默认密钥  | production  | 生产Web服务  |
| prod-db  | 10.0.0.50     | 22   | admin| 密钥     | production  | 生产数据库   |
| jump     | 1.2.3.4       | 22   | ubuntu| 密码+跳板| relay       | 跳板机       |
```

### server-add — 添加服务器

```text
/server-add prod-web 192.168.1.100                                    # 最简形式
/server-add db 10.0.0.50 admin 2222                                   # 指定用户和端口
/server-add cache 172.16.0.10 --tags production,redis --note "Redis主节点"
/server-add internal 10.0.0.5 --jump-host ubuntu@1.2.3.4 --password mypass
```

也支持自然语言输入：

> "帮我加一台服务器，叫 test，地址是 192.168.1.50，用 root 登录"

### server-del — 删除服务器

```text
/server-del my-server
```

会先展示服务器信息确认后再删除。

### server-check — 检查服务器状态

```text
/server-check prod-web            # 单台
/server-check prod-web staging db # 多台
/server-check --tags production   # 按标签批量检查
```

### server-ssh — 远程执行命令

```text
/server-ssh prod-web "ls -la /var/log"
/server-ssh prod-db "systemctl status nginx"
/server-ssh prod-web "docker ps"
```

危险命令（`rm -rf`、`shutdown`、`reboot`、`dd` 等）执行前需要二次确认。

---

## 数据格式

服务器数据存储在本地 `~/.claude/servers/servers.json`：

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
      "note": "生产Web服务器"
    }
  ]
}
```

### 字段说明

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | 是 | — | 服务器名称，唯一标识 |
| `host` | 是 | — | IP 地址或域名 |
| `port` | 否 | `22` | SSH 端口 |
| `user` | 否 | `root` | 登录用户名 |
| `key_path` | 否 | `""` | SSH 密钥路径，为空则使用默认密钥 |
| `password` | 否 | `""` | SSH 密码，为空则使用密钥认证 |
| `jump_host` | 否 | `""` | 跳板机地址，格式 `user@host` |
| `tags` | 否 | `[]` | 标签列表，用于分组和筛选 |
| `note` | 否 | `""` | 备注说明 |

## 认证方式

支持三种 SSH 认证，按优先级自动选择：

| 优先级 | 方式 | 条件 |
|--------|------|------|
| 1 | 密钥认证 | 设置了 `key_path` → `ssh -i <key>` |
| 2 | 密码认证 | 设置了 `password` → `sshpass -p <pass> ssh` |
| 3 | 默认密钥 | 两者都为空 → `ssh`（使用本机默认密钥） |

配置了 `jump_host` 时，自动追加 `-J <jump_host>` 参数通过跳板机连接。

---

## 项目结构

```text
server-skills/
├── Makefile                    # install / uninstall / list / clean
├── server-list/SKILL.md        # 查看和筛选服务器
├── server-add/SKILL.md         # 添加服务器
├── server-del/SKILL.md         # 删除服务器
├── server-check/SKILL.md       # 健康检查
├── server-ssh/SKILL.md         # 远程命令执行
└── scripts/
    ├── server_manager.py       # 服务器列表 CRUD 管理
    └── ssh_helper.py           # SSH 命令生成
```

## Makefile 命令

| 命令 | 说明 |
|------|------|
| `make install` | 安装全部插件到 `~/.claude/skills/` |
| `make uninstall` | 卸载全部插件 |
| `make list` | 查看安装状态和已注册服务器数量 |
| `make clean` | 卸载插件并删除服务器数据（慎用） |

---

## 安全说明

- 密码以明文存储在本地 JSON 文件中，请确保 `~/.claude/servers/` 目录权限安全
- 列表展示时不显示密码，仅显示认证方式类型
- 执行危险远程命令前需二次确认
- 建议优先使用密钥认证，避免在配置中存储密码

## 开源协议

[MIT](LICENSE)
