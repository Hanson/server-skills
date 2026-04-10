---
name: server-ssh
description: 在远程服务器上执行命令。当用户想在服务器上执行命令、SSH到服务器、远程操作服务器时使用此 skill。支持 /server-ssh 命令触发。
---

# 远程执行服务器命令

通过 SSH 在指定服务器上执行任意命令并返回输出。

## 数据文件

服务器数据存储在 `~/.claude/servers/servers.json`。

## 执行步骤

1. 从用户消息中获取服务器名称和要执行的命令
2. 读取 JSON 获取连接信息
3. 如果未找到服务器，模糊匹配给出建议
4. 构建 SSH 命令
5. 展示即将执行的命令，让用户确认
6. 执行并返回输出

## 用户输入格式

- `/server-ssh prod-web "ls -la /var/log"`
- `/server-ssh staging-db "systemctl status nginx"`
- `/server-ssh prod-web "docker ps"`
- "帮我看看 muyun 上 supervisor 的状态" → 自动提取服务器名和命令

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

如果 user 不是 root 且命令需要权限，提示用户命令可能需要 sudo。

## 安全规则

- 展示完整命令让用户确认后再执行
- 以下危险命令需要二次确认（即使用户已确认第一次）：
  - `rm -rf`（尤其是 `/`、`/*`、`~` 等路径）
  - `shutdown`、`reboot`、`halt`、`poweroff`
  - `mkfs`、`dd`
  - `:(){:|:&};:` 等 fork bomb
  - `iptables -F`、`ufw disable`
- 密码在命令行中使用 sshpass 时注意引号转义
- 不对密码字段做任何展示

## 输出格式

```
[prod-web] $ ls -la /var/log
total 1234
drwxr-xr-x  10 root root 4096 Apr  9 10:30 .
...
```

如果命令执行失败（非零退出码），标注退出码：

```
[prod-web] $ ls /nonexist (exit code: 2)
ls: cannot access '/nonexist': No such file or directory
```

## 错误处理

如果 SSH 连接失败：
- 显示完整错误信息
- 提示排查方向：网络连通性、认证配置、SSH 服务状态
