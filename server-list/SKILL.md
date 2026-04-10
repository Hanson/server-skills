---
name: server-list
description: 查看服务器列表。当用户想查看所有已管理的服务器、查看服务器清单、列出服务器时使用此 skill。支持 /server-list 命令触发。
---

# 查看服务器列表

列出所有已管理的服务器信息。

## 数据文件

服务器数据存储在 `~/.claude/servers/servers.json`，格式：

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
      "tags": ["production"],
      "note": "生产服务器"
    }
  ]
}
```

## 执行步骤

1. 读取 `~/.claude/servers/servers.json`
2. 如果文件不存在或为空，提示"暂无服务器记录，请使用 /server-add 添加"
3. 以表格展示所有服务器
4. 在表格下方统计总数

## 展示格式

```
服务器列表 (共 N 台)

| 名称 | 地址 | 端口 | 用户 | 认证方式 | 标签 | 备注 |
|------|------|------|------|----------|------|------|
| prod-web | 192.168.1.100 | 22 | root | 默认密钥 | production | 生产服务器 |
| meilai | 114.55.36.75 | 22 | hanson | 密码+跳板 | meilai | 通过muyun跳板机连接 |
```

认证方式展示规则：
- 有 `key_path` → "密钥"
- 有 `password` → "密码"
- 有 `jump_host` → 追加 "+跳板"
- 都没有 → "默认密钥"

**密码字段永远不展示**，仅显示认证方式类型。

## 支持筛选

用户可以按标签或名称关键词筛选：

- `/server-list --tags xbot` - 只显示带 xbot 标签的服务器
- `/server-list ali` - 模糊匹配名称包含 ali 的服务器

筛选逻辑：遍历 servers 数组，匹配 tags 数组中包含指定标签的项，或 name 中包含关键词的项。
