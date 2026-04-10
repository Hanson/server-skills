---
name: server-check
description: 检查服务器状态（磁盘/CPU/内存/负载）。当用户想查看服务器健康状况、检查服务器资源使用情况、监控服务器状态时使用此 skill。支持 /server-check 命令触发。
---

# 检查服务器状态

通过 SSH 连接服务器，检查磁盘、CPU、内存和负载情况。

## 数据文件

服务器数据存储在 `~/.claude/servers/servers.json`。

## 执行步骤

1. 从用户消息中获取服务器名称
2. 读取 `~/.claude/servers/servers.json`，查找服务器连接信息
3. 如果未找到，模糊匹配给出建议
4. 构建 SSH 命令并执行
5. 解析输出，汇总展示结果

## SSH 命令构建

根据服务器配置选择认证方式：

**密钥认证**（key_path 不为空）：
```bash
ssh -i <key_path> -p <port> -o StrictHostKeyChecking=no [-J <jump_host>] <user>@<host> "命令"
```

**密码认证**（password 不为空且 key_path 为空）：
```bash
sshpass -p '<password>' ssh -p <port> -o StrictHostKeyChecking=no [-J <jump_host>] <user>@<host> "命令"
```

**默认认证**（key_path 和 password 都为空）：
```bash
ssh -p <port> -o StrictHostKeyChecking=no [-J <jump_host>] <user>@<host> "命令"
```

其中 `-J <jump_host>` 仅在 jump_host 字段不为空时添加。

如果 user 不是 root，命令前加 `sudo `。

## 检查命令

合并为一条 SSH 命令减少连接次数：

```bash
echo "=== DISK ===" && df -h 2>/dev/null && echo "=== MEMORY ===" && free -h 2>/dev/null && echo "=== CPU ===" && top -bn1 2>/dev/null | head -5 && echo "=== LOAD ===" && uptime 2>/dev/null
```

## 展示格式

```
服务器状态: prod-web (192.168.1.100)

磁盘使用:
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        40G   15G   23G  40% /

内存使用:
              total        used        free      shared  buff/cache   available
Mem:           3.8G        2.1G        500M        128M        1.2G        1.3G

CPU 负载:
top - 10:30:00 up 30 days, 2:15, 1 user, load average: 0.5, 0.3, 0.2

运行时间:
 10:30:00 up 30 days, 2:15, 1 user, load average: 0.50, 0.30, 0.20
```

## 错误处理

如果 SSH 连接失败：
- 显示完整错误信息
- 提示排查方向：网络连通性、认证配置、SSH 服务状态
- 建议用户手动测试：`ssh -p <port> <user>@<host>`

## 批量检查

支持同时检查多台服务器：
- `/server-check prod-web staging-db` — 检查多台
- `/server-check --tags production` — 按标签批量检查
