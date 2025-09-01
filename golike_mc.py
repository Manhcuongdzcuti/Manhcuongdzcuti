# -*- coding: utf-8 -*-
import os, sys, requests

gl_mc = "\033[1;0m ➲ "
gl_mc1 = "\033[1;0m==> "

# Link config và code chính
CONFIG_URL = "https://raw.githubusercontent.com/Manhcuongdzcuti/Manhcuongdzcuti/refs/heads/main/config.py"
TOOL_URL   = "https://raw.githubusercontent.com/manhcuongsieucute2k9-lang/Golikemcne/refs/heads/main/main.py"

def startup_check():
    try:
        print("[*] Đang kiểm tra trạng thái tool...")

        # --- Tải config từ GitHub ---
        res_cfg = requests.get(CONFIG_URL, timeout=7)
        res_cfg.raise_for_status()
        cfg = {}
        exec(res_cfg.text, cfg)

        # In thông báo từ server (nếu có)
        update_messages = cfg.get("UPDATE_MESSAGES", [])
        if update_messages:
            print("\033[1;32m════════════════════════════════════════════════════════════")
            for msg in update_messages:
                print(gl_mc + "\033[1;33m" + msg)
            print("\033[1;32m════════════════════════════════════════════════════════════")

        # Nếu tool đang bảo trì thì thoát
        if cfg.get("TOOL_STATUS", "on").lower() != "on":
            print("❌ Tool đang bảo trì, vui lòng quay lại sau!")
            sys.exit(1)

        # --- Tải code chính ---
        print("[*] Đang truy cập tool!")
        res_tool = requests.get(TOOL_URL, timeout=10)
        res_tool.raise_for_status()
        exec(res_tool.text, globals())  # chạy code chính của tool

    except requests.exceptions.ConnectionError:
        print("❌ Không có kết nối mạng, vui lòng kiểm tra lại!")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("❌ Kết nối tới server quá hạn (timeout). Thử lại sau!")
        sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Lỗi khi tải dữ liệu từ server. Vui lòng thử lại sau!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        startup_check()
    except KeyboardInterrupt:
        print("\n\033[1;31mThoát tool.")
