# -*- coding: utf-8 -*-
import os
import sys
import requests
import socket
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
def check_network():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print("\033[1;31mMạng không ổn định hoặc bị mất kết nối!")
        sys.exit()
# -------------------- Config API --------------------
CONFIG_URL = "https://raw.githubusercontent.com/Manhcuongdzcuti/Manhcuongdzcuti/refs/heads/main/config.py"
TOOL_URL   = "https://raw.githubusercontent.com/manhcuongsieucute2k9-lang/Golikemcne/refs/heads/main/main.py"

def load_remote_config():
  check_network()
  try:
        res = requests.get(CONFIG_URL, timeout=7)
        res.raise_for_status()
        code = res.text
        cfg = {}
        exec(code, cfg)
        return {
            "TOOL_STATUS": cfg.get("TOOL_STATUS", "on"),
            "UPDATE_MESSAGES": cfg.get("UPDATE_MESSAGES", [])
        }
  except Exception as e:
        print(f"⚠️ Không tải được config từ server: {e}")
        return {"TOOL_STATUS": "on", "UPDATE_MESSAGES": []}

def check_tool_status():
  check_network()
  config = load_remote_config()

  if config["UPDATE_MESSAGES"]:
        print("\033[1;32m════════════════════════════════════════════════════════════")
        for msg in config["UPDATE_MESSAGES"]:
            print(gl_mc + "\033[1;33m" + msg)
        print("\033[1;32m════════════════════════════════════════════════════════════")

  if config["TOOL_STATUS"].lower() != "on":
        print("\n❌ Tool đang bảo trì, vui lòng quay lại sau!")
        sys.exit(1)

# -------------------- Run Tool From API --------------------
def run_remote_tool():
  check_network()
  try:
        res = requests.get(TOOL_URL, timeout=10)
        res.raise_for_status()
        code = res.text
        exec(code, globals())
  except Exception as e:
        print(f"❌ Lỗi tải tool từ server: {e}")
        sys.exit(1)

# -------------------- Main --------------------
def main():
  check_network()
  os.system('cls' if os.name=='nt' else 'clear')
  print(BANNER)
  check_tool_status()

  print(gl_mc + "\033[1;32mĐang tải tool từ server...\n")
  check_network()
  run_remote_tool()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\033[1;31mThoát tool.")
