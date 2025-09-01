# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import string
import requests
import hashlib
import ast
from datetime import datetime, timedelta, date
from time import sleep

gl_mc = "\033[1;0m ➲ "
gl_mc1 = "\033[1;0m==> "

# -------------------- Banner --------------------
BANNER = """
      \033[1;32m██████\033[1;33m╗         \033[1;32m████████\033[1;33m╗ \033[1;32m██████\033[1;33m╗  \033[1;32m██████\033[1;33m╗ \033[1;32m██\033[1;33m╗
     \033[1;32m██\033[1;33m╔════╝         ╚══\033[1;32m██\033[1;33m╔══╝\033[1;32m██\033[1;33m╔═══\033[1;32m██\033[1;33m╗\033[1;32m██\033[1;33m╔═══\033[1;32m██\033[1;33m╗\033[1;32m██\033[1;33m║
    \033[1;32m ██\033[1;33m║       \033[1;32m█████\033[1;33m╗    \033[1;32m██\033[1;33m║   \033[1;32m██\033[1;33m║   \033[1;32m██\033[1;33m║\033[1;32m██\033[1;33m║   \033[1;32m██\033[1;33m║\033[1;32m██\033[1;33m║
    \033[1;32m ██\033[1;33m║       ╚════╝    \033[1;32m██\033[1;33m║   \033[1;32m██\033[1;33m║   \033[1;32m██\033[1;33m║\033[1;32m██\033[1;33m║   \033[1;32m██\033[1;33m║\033[1;32m██\033[1;33m║
     ╚\033[1;32m██████\033[1;33m╗           \033[1;32m ██\033[1;33m║   ╚\033[1;32m██████\033[1;33m╔╝╚\033[1;32m██████\033[1;33m╔╝\033[1;32m███████\033[1;33m╗
      ╚═════╝            ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝\n
\033[1;32m════════════════════════════════════════════════════════════
         \033[1;0m            ADMIN INFORMATION
\033[1;32m════════════════════════════════════════════════════════════
\033[1;35mName                :  Cường Lập Trình
\033[1;35mPosition            :  Admin / Lead Developer
\033[1;34mPhone Zalo          :  0859652100
\033[1;0mFacebook Admin      :  https://fb.com/manhcuongutvl.dz
\033[1;32mTools               :  Golike Tiktok Auto Click
\033[1;0mMua Paid Key Tại    :  https://cardso1vn.x10.mx/add_key.php
\033[1;0mVersion             :  3.2.7 (Secure)
\033[1;33mMomo/Mb             :  0859652100(Momo) - 666080629(MB)
\033[1;31mVui Lòng Tham Gia Box Zalo Để Admin Tiện Cho Việc Hỗ Trợ Các Lỗi!
\033[1;32m════════════════════════════════════════════════════════════
"""

# -------------------- Config API --------------------
CONFIG_URL = "https://raw.githubusercontent.com/Manhcuongdzcuti/Manhcuongdzcuti/refs/heads/main/config.py"

def load_remote_config():
    """
    Tải config.py từ GitHub và parse thành dict
    """
    try:
        res = requests.get(CONFIG_URL, timeout=7)
        res.raise_for_status()
        code = res.text
        cfg = {}
        exec(code, cfg)  # chạy code Python trên server
        return {
            "TOOL_STATUS": cfg.get("TOOL_STATUS", "on"),
            "UPDATE_MESSAGES": cfg.get("UPDATE_MESSAGES", [])
        }
    except Exception as e:
        print(f"⚠️ Không tải được config từ server: {e}")
        return {"TOOL_STATUS": "on", "UPDATE_MESSAGES": []}

def check_tool_status():
    """
    Kiểm tra trạng thái tool (bảo trì hay hoạt động).
    Nếu bảo trì -> in thông báo và thoát.
    """
    config = load_remote_config()

    # Hiển thị thông báo từ server
    if config["UPDATE_MESSAGES"]:
        print("\033[1;32m════════════════════════════════════════════════════════════")
        for msg in config["UPDATE_MESSAGES"]:
            print(gl_mc + "\033[1;33m" + msg)
        print("\033[1;32m════════════════════════════════════════════════════════════")

    # Kiểm tra trạng thái bảo trì
    if config["TOOL_STATUS"].lower() != "on":
        print("\n❌ Tool đang bảo trì, vui lòng quay lại sau!")
        sys.exit(1)

# -------------------- Main --------------------
def main():
    os.system('cls' if os.name=='nt' else 'clear')
    print(BANNER)

    # Kiểm tra trạng thái tool & thông báo
    check_tool_status()

    # TODO: phần chạy tool chính ở đây
    print(gl_mc + "\033[1;32mTool sẵn sàng hoạt động!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\033[1;31mThoát tool.")
