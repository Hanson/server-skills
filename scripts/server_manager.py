#!/usr/bin/env python3
"""
服务器列表管理脚本
用法:
  python server_manager.py list                    # 列出所有服务器
  python server_manager.py add <json_data>         # 添加服务器
  python server_manager.py delete <name>           # 删除服务器
  python server_manager.py get <name>              # 获取单个服务器信息
  python server_manager.py init                    # 初始化数据文件
"""

import json
import os
import sys
from pathlib import Path

SERVERS_FILE = Path.home() / ".claude" / "servers" / "servers.json"


def load_servers():
    """加载服务器列表"""
    if not SERVERS_FILE.exists():
        return {"servers": []}
    with open(SERVERS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return {"servers": []}
        return json.loads(content)


def save_servers(data):
    """保存服务器列表"""
    SERVERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SERVERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_init():
    """初始化数据文件"""
    SERVERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not SERVERS_FILE.exists() or SERVERS_FILE.stat().st_size == 0:
        save_servers({"servers": []})
        print("初始化完成: " + str(SERVERS_FILE))
    else:
        print("数据文件已存在: " + str(SERVERS_FILE))


def cmd_list():
    """列出所有服务器"""
    data = load_servers()
    servers = data.get("servers", [])
    if not servers:
        print("暂无服务器记录，请使用 /add-server 添加")
        return

    print(f"服务器列表 (共 {len(servers)} 台)\n")
    print(f"| {'名称':<15} | {'地址':<18} | {'端口':<6} | {'用户':<10} | {'标签':<20} | {'备注':<20} |")
    print(f"|{'-'*17}|{'-'*20}|{'-'*8}|{'-'*12}|{'-'*22}|{'-'*22}|")
    for s in servers:
        name = s.get("name", "")
        host = s.get("host", "")
        port = s.get("port", 22)
        user = s.get("user", "")
        tags = ", ".join(s.get("tags", []))
        note = s.get("note", "")
        auth = "密钥" if s.get("key_path") else ("密码" if s.get("password") else "默认")
        print(f"| {name:<15} | {host:<18} | {port:<6} | {user:<10} | {tags:<20} | {note:<20} |")


def cmd_add(json_data):
    """添加服务器"""
    server = json.loads(json_data)
    data = load_servers()
    servers = data.get("servers", [])

    name = server.get("name", "")
    if not name:
        print("错误: 服务器名称不能为空")
        sys.exit(1)

    for s in servers:
        if s.get("name") == name:
            print(f"错误: 服务器 '{name}' 已存在")
            sys.exit(1)

    server.setdefault("port", 22)
    server.setdefault("user", "root")
    server.setdefault("key_path", "")
    server.setdefault("password", "")
    server.setdefault("tags", [])
    server.setdefault("note", "")

    servers.append(server)
    data["servers"] = servers
    save_servers(data)
    print(f"已添加服务器: {name} ({server['host']}:{server['port']})")


def cmd_delete(name):
    """删除服务器"""
    data = load_servers()
    servers = data.get("servers", [])

    found = None
    for s in servers:
        if s.get("name") == name:
            found = s
            break

    if not found:
        # 模糊匹配
        suggestions = [s for s in servers if name.lower() in s.get("name", "").lower()]
        if suggestions:
            print(f"未找到服务器 '{name}'，你是否指:")
            for s in suggestions:
                print(f"  - {s['name']} ({s['host']})")
        else:
            print(f"未找到服务器 '{name}'")
        sys.exit(1)

    servers.remove(found)
    data["servers"] = servers
    save_servers(data)
    print(f"已删除服务器: {name} ({found['host']})")


def cmd_get(name):
    """获取单个服务器信息，输出 JSON"""
    data = load_servers()
    servers = data.get("servers", [])

    for s in servers:
        if s.get("name") == name:
            print(json.dumps(s, ensure_ascii=False))
            return

    # 模糊匹配
    suggestions = [s for s in servers if name.lower() in s.get("name", "").lower()]
    if suggestions:
        print(f"未找到服务器 '{name}'，你是否指:")
        for s in suggestions:
            print(f"  - {s['name']} ({s['host']})")
    else:
        print(f"未找到服务器 '{name}'")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        cmd_init()
    elif command == "list":
        cmd_list()
    elif command == "add":
        if len(sys.argv) < 3:
            print("错误: 缺少服务器数据 JSON")
            sys.exit(1)
        cmd_add(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("错误: 缺少服务器名称")
            sys.exit(1)
        cmd_delete(sys.argv[2])
    elif command == "get":
        if len(sys.argv) < 3:
            print("错误: 缺少服务器名称")
            sys.exit(1)
        cmd_get(sys.argv[2])
    else:
        print(f"未知命令: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
