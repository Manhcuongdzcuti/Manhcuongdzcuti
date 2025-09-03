# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import string
import requests
import socket
import time
from datetime import datetime, timedelta, date

# -------------------- Màu sắc --------------------
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
\033[1;32mTools               :  Golike Gộp Vip
\033[1;0mMua Paid Key Tại.   :  https://cardso1vn.x10.mx/add_key.php
\033[1;0mVersion             :  3.2.5
\033[1;32mLink Box Zalo       :  Đang Cập Nhật
\033[1;33mMomo/Mb             :  0859652100(Momo) - 666080629(MB)
\033[1;32m════════════════════════════════════════════════════════════
"""

# -------------------- Cấu hình --------------------
FREE_KEY_FILE = "free_key.json"
PAID_KEY_FILE = "paid_key.txt"
PAID_KEY_URL = "https://cardso1vn.x10.mx/Key.json"   # API Paid Key
LINK4M_API_KEY = "65b5f29631fc8733e718dca9"
BASE_TASK_LINK = "https://key.com/task?id="
TOOL_MAIN_URL = "https://raw.githubusercontent.com/manhcuongsieucute2k9-lang/Golikemcne/refs/heads/main/main.py"

# -------------------- Hàm hỗ trợ --------------------
def get_current_ip():
    try:
        return requests.get("https://kiemtraip.com/raw.php", timeout=5).text.strip()
    except:
        return None

def generate_key(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def shorten_link(url):
    try:
        res = requests.get(f"https://link4m.co/api-shorten/v2?api={LINK4M_API_KEY}&url={url}")
        data = res.json()
        return data.get("shortenedUrl", url) if data.get("status") == "success" else url
    except:
        return url

# -------------------- Free Key --------------------
def create_free_key():
    current_ip = get_current_ip()
    if not current_ip:
        return None
    key = generate_key()
    return {
        "key": key,
        "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ip": current_ip
    }

def validate_free_key(keys):
    try:
        now = datetime.now()
        expire_time = datetime.strptime(keys.get("expire", ""), "%Y-%m-%d %H:%M:%S")
        return now < expire_time
    except:
        return False

def reset_free_key():
    if os.path.exists(FREE_KEY_FILE):
        os.remove(FREE_KEY_FILE)

def get_free_task_link(keys):
    task_url = f"{BASE_TASK_LINK}{keys['key']}"
    print(f"{gl_mc1}\033[1;32mLink Lấy Key Free: \033[1;33m{shorten_link(task_url)}")
    os.system(f"termux-open-url {shorten_link(task_url)}")

# -------------------- Paid Key --------------------
def check_paid_key(user_key: str):
    try:
        response = requests.get(PAID_KEY_URL, timeout=5)
        data = response.json()
        for item in data.get("keys", []):
            if item.get("key") == user_key:
                expires_at = item.get("expires_at")
                exp_date = datetime.strptime(expires_at, "%Y-%m-%d").date()
                if date.today() <= exp_date:
                    days_left = (exp_date - date.today()).days
                    return True, exp_date, days_left
        return False, None, None
    except:
        return False, None, None

def get_saved_paid_key():
    if os.path.exists(PAID_KEY_FILE):
        with open(PAID_KEY_FILE, "r") as f:
            return f.read().strip()
    return None

def save_paid_key(user_key):
    with open(PAID_KEY_FILE, "w") as f:
        f.write(user_key)

def reset_paid_key():
    if os.path.exists(PAID_KEY_FILE):
        os.remove(PAID_KEY_FILE)

# -------------------- Golike Tool --------------------
def golike_tool_main():
    try:
        print("\033[1;0m[*]Đang tải Tool...")
        response = requests.get(TOOL_MAIN_URL, timeout=10)
        response.raise_for_status()
        code = response.text
        os.system('cls' if os.name== 'nt' else 'clear')
        print(BANNER)
        print("\033[1;0m[*] Tải thành công. Đang khởi chạy tool...")
        exec(code, globals())
    except Exception as e:
        print(f"\033[1;31mLỗi khi tải hoặc chạy tool: {e}")
        sys.exit(1)

# -------------------- Main --------------------
def main():
    os.system('cls' if os.name=='nt' else 'clear')
    print(BANNER)

    # Check mạng
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print("\033[1;31mVui lòng kết nối mạng")
        sys.exit()

    # 1. Check Free Key trước
    keys = load_json(FREE_KEY_FILE)
    if keys and validate_free_key(keys):
        expire_time = datetime.strptime(keys["expire"], "%Y-%m-%d %H:%M:%S")
        print(f"\033[1;32mĐang dùng Free Key (hết hạn:\033[1;33m {expire_time})\n")
        time.sleep(1)
        golike_tool_main()
        return

    # 2. Check Paid Key
    paid_key = get_saved_paid_key()
    if paid_key:
        valid, exp_date, days_left = check_paid_key(paid_key)
        if valid:
            print(f"\033[1;32mĐang dùng Paid Key \033[1;33m(còn hạn {days_left} ngày, hết hạn: {exp_date})")
            time.sleep(1)
            golike_tool_main()
            return
        else:
            reset_paid_key()

    # 3. Nếu cả 2 đều không có/hết hạn → hỏi người dùng chọn loại key
    print(gl_mc1+"\033[1;32mChọn Loại Key Vào Tool")
    print(gl_mc+"\033[1;32mNhập [\033[1;33m1\033[1;32m] Free Key (vượt link nhiệm vụ, key free)")
    print(gl_mc+"\033[1;32mNhập [\033[1;33m2\033[1;32m] Paid Key (key mua từ server)")
    print("\033[1;32m═══════════════════")
    choice = input(gl_mc1+"\033[1;32mChọn 1 hoặc 2: \033[1;33m").strip()

    if choice == "1":
        reset_free_key()
        keys = create_free_key()
        if not keys:
            print("\033[1;31mKhông lấy được IP để tạo Free Key.")
            return
        get_free_task_link(keys)

        attempts = 0
        while attempts < 3:
            user_key = input(gl_mc1+"\033[1;32mNhập Free Key: \033[1;33m").strip()
            if user_key == keys.get("key"):
                save_json(FREE_KEY_FILE, keys)
                expire_time = datetime.strptime(keys["expire"], "%Y-%m-%d %H:%M:%S")
                print(f"\033[1;32mFree Key hợp lệ. Hết hạn lúc: \033[1;33m{expire_time}")
                time.sleep(1)
                golike_tool_main()
                return
            else:
                attempts += 1
                print(f"\033[1;31mFree Key sai ({attempts}/3).")
        print("\033[1;31mBạn đã nhập sai Free Key quá 3 lần. Thoát tool.")
        return

    elif choice == "2":
        attempts = 0
        while attempts < 3:
            key = input(gl_mc1+"\033[1;32mNhập Paid Key của bạn:\033[1;33m ").strip()
            valid, exp_date, days_left = check_paid_key(key)
            if valid:
                save_paid_key(key)
                print(f"\033[1;32mPaid Key hợp lệ. Còn hạn \033[1;33m{days_left} \033[1;32mngày (hết hạn: \033[1;33m{exp_date})")
                time.sleep(1)
                golike_tool_main()
                return
            else:
                attempts += 1
                print(f"\033[1;31mPaid Key sai ({attempts}/3).")
        print("\033[1;31mBạn đã nhập sai Paid Key quá 3 lần. Thoát tool.")
        return
    else:
        print("\033[1;31mLựa chọn không hợp lệ.")

# -------------------- Run --------------------
if __name__ == "__main__":
    main()
