---
name: server-add
description: 添加服务器到管理列表。当用户想添加新服务器、注册服务器、新增服务器连接信息时使用此 skill。支持 /server-add 命令触发。
---

# 添加服务器

将新服务器信息写入服务器列表。

## 数据文件

服务器数据存储在 `~/.claude/servers/servers.json`。

## 执行步骤

1. 从用户消息中提取服务器信息
2. 必填字段：`name`（名称）、`host`（地址）
3. 可选字段及默认值：
   - `port` 默认 22
   - `user` 默认 "root"
   - `key_path` 默认 ""（使用本机默认密钥）
   - `password` 默认 ""
   - `jump_host` 默认 ""（格式 `user@host`）
   - `tags` 默认 []
   - `note` 默认 ""
4. 读取现有 JSON，检查 name 是否重复
5. 如果重复，提示用户并建议使用不同名称
6. 将新服务器追加到 servers 数组
7. 写回 JSON 文件
8. 确认添加成功

## 用户输入格式

用户可以用自然语言或结构化方式提供信息：

- `/server-add prod-web 192.168.1.100` — 最简形式，端口和用户用默认值
- `/server-add staging-db 10.0.0.50 admin 2222` — 指定用户和端口
- `/server-add redis 172.16.0.10 --tags cache,production --note "Redis主节点"`
- `/server-add jump-host 1.2.3.4 --key-path ~/.ssh/jump_key`
- `/server-add internal 10.0.0.5 --jump-host ubuntu@1.2.3.4 --password mypass`

也可以从自然语言中提取：
- "帮我加一台服务器，叫 test，地址是 192.168.1.50，用 root 登录"

## 确认输出

```
已添加服务器: prod-web (192.168.1.100:22)
用户: root | 认证: 默认密钥 | 标签: production
```

## 数据文件初始化

如果 `~/.claude/servers/` 目录或 `servers.json` 不存在，自动创建：

```bash
mkdir -p ~/.claude/servers
echo '{"servers":[]}' > ~/.claude/servers/servers.json
```
