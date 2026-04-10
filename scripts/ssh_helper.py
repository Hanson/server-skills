#!/usr/bin/env python3
"""
SSH 辅助脚本 - 生成 SSH 连接命令
用法:
  python ssh_helper.py <servers_json> <server_name> <remote_command>
输出: 可直接执行的 SSH 命令字符串
"""

import json
import shlex
import sys


def build_ssh_command(server, remote_command):
    """根据服务器配置构建 SSH 命令"""
    host = server["host"]
    port = server.get("port", 22)
    user = server.get("user", "root")
    key_path = server.get("key_path", "")
    password = server.get("password", "")
    jump_host = server.get("jump_host", "")

    target = f"{user}@{host}"

    # 构建跳板机参数
    jump_arg = f" -J {shlex.quote(jump_host)}" if jump_host else ""

    if key_path:
        # 密钥认证
        cmd = f"ssh -i {shlex.quote(key_path)} -p {port} -o StrictHostKeyChecking=no{jump_arg} {shlex.quote(target)} {shlex.quote(remote_command)}"
    elif password:
        # 密码认证
        cmd = f"sshpass -p {shlex.quote(password)} ssh -p {port} -o StrictHostKeyChecking=no{jump_arg} {shlex.quote(target)} {shlex.quote(remote_command)}"
    else:
        # 默认认证（使用本机默认密钥）
        cmd = f"ssh -p {port} -o StrictHostKeyChecking=no{jump_arg} {shlex.quote(target)} {shlex.quote(remote_command)}"

    return cmd


def main():
    if len(sys.argv) < 4:
        print("用法: python ssh_helper.py <server_json> <server_name> <remote_command>")
        sys.exit(1)

    server_json = sys.argv[1]
    server_name = sys.argv[2]
    remote_command = sys.argv[3]

    server = json.loads(server_json)
    cmd = build_ssh_command(server, remote_command)
    print(cmd)


if __name__ == "__main__":
    main()
