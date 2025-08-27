# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import string
import requests
import hashlib
import socket
import threading
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
\033[1;33mMomo/Mb.           :  0859652100(Momo) - 666080629(MB)
\033[1;31mVui Lòng Tham Gia Box Zalo Để Admin Tiện Cho Việc Hỗ Trợ Các Lỗi!
\033[1;32m════════════════════════════════════════════════════════════
"""

# -------------------- Config (CỐ ĐỊNH – KHÔNG ĐƯỢC SỬA) --------------------
FREE_KEY_FILE = "free_key.json"
PAID_KEY_FILE = "paid_key.txt"
PAID_KEY_URL  = "https://cardso1vn.x10.mx/Key.json"
LINK4M_API_KEY = "65b5f29631fc8733e718dca9"
BASE_TASK_LINK = "https://key.com/task?id="
GOLIKE_TOOL_URL = "https://raw.githubusercontent.com/Manhcuongdzcuti/Manhcuongdzcuti/refs/heads/main/tiktok_golikemc.py"

DEVLOG_URL = "https://https://cardso1vn.x10.mx/devlog.php"  # server nhận log
PING_URLS = ("https://google.com", "https://cloudflare.com")

# === DẤU VÂN TAY CODE (bạn cần cập nhật theo file gốc của bạn) ===
EXPECTED_MD5 = "PUT_YOUR_FILE_MD5_HERE"            # ví dụ: "c1a5298f939e87e8f962a5edfc206918"
EXPECTED_AST_SHA256 = "PUT_YOUR_AST_SHA256_HERE"   # ví dụ: "cfe1f3... (64 hex)"

# ================== Gửi log về server ==================
def send_dev_log(reason: str):
    try:
        data = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "host": socket.gethostname(),
            "user": os.getenv("USERNAME") or os.getenv("USER") or "unknown",
            "reason": reason
        }
        requests.post(DEVLOG_URL, data=data, timeout=5)
    except:
        pass  # không để crash nếu server log không phản hồi

# ================== CHỐNG DEV / BUG ==================
def _file_md5(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def _ast_fingerprint(path: str) -> str:
    """
    Hash AST (loại bỏ whitespace/comment) -> phát hiện thay đổi cấu trúc code.
    """
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    dump = ast.dump(tree, include_attributes=False)
    return hashlib.sha256(dump.encode("utf-8")).hexdigest()

def _assert_constants_unchanged():
    """
    Khóa các hằng số quan trọng -> nếu đổi endpoint/file quan trọng => chặn.
    """
    expected = {
        "FREE_KEY_FILE": "free_key.json",
        "PAID_KEY_FILE": "paid_key.txt",
        "PAID_KEY_URL":  "https://cardso1vn.x10.mx/Key.json",
        "BASE_TASK_LINK": "https://key.com/task?id=",
        "GOLIKE_TOOL_URL": "https://raw.githubusercontent.com/Manhcuongdzcuti/Manhcuongdzcuti/refs/heads/main/tiktok_golikemc.py",
        "DEVLOG_URL": "https://https://cardso1vn.x10.mx/devlog.php",
    }
    now = {
        "FREE_KEY_FILE": FREE_KEY_FILE,
        "PAID_KEY_FILE": PAID_KEY_FILE,
        "PAID_KEY_URL":  PAID_KEY_URL,
        "BASE_TASK_LINK": BASE_TASK_LINK,
        "GOLIKE_TOOL_URL": GOLIKE_TOOL_URL,
        "DEVLOG_URL": DEVLOG_URL,
    }
    for k, v in expected.items():
        if now[k] != v:
            raise RuntimeError(f"Hằng số quan trọng '{k}' đã bị thay đổi!")

def detect_tamper_or_bug_activate():
    """
    Chỉ kích hoạt nếu phát hiện:
    - Thay đổi cấu trúc/code (MD5 hoặc AST SHA256 không khớp).
    - Hằng số endpoint/đường dẫn bị sửa.
    """
    try:
        current_file = os.path.abspath(sys.argv[0])

        # 1) Check constants
        _assert_constants_unchanged()

        # 2) Check MD5 file
        if EXPECTED_MD5 and EXPECTED_MD5 != "PUT_YOUR_FILE_MD5_HERE":
            md5_now = _file_md5(current_file)
            if md5_now != EXPECTED_MD5:
                msg = "Phát hiện code bị chỉnh sửa (MD5 mismatch)."
                print(f"⚠️ {msg}")
                send_dev_log(msg)
                return True

        # 3) Check AST structure
        if EXPECTED_AST_SHA256 and EXPECTED_AST_SHA256 != "PUT_YOUR_AST_SHA256_HERE":
            ast_now = _ast_fingerprint(current_file)
            if ast_now != EXPECTED_AST_SHA256:
                msg = "Phát hiện thay đổi CẤU TRÚC code (AST mismatch)."
                print(f"⚠️ {msg}")
                send_dev_log(msg)
                return True

        # 4) Không kích hoạt nếu mọi thứ ổn
        return False

    except Exception as e:
        msg = f"Lỗi kiểm tra anti-dev: {e}"
        print(f"⚠️ {msg}")
        send_dev_log(msg)
        # Lỗi kiểm tra -> coi như khả nghi
        return True

def check_network_once() -> bool:
    try:
        # socket nhanh đến DNS Google
        sock = socket.create_connection(("8.8.8.8", 53), timeout=3)
        sock.close()
        # thêm một GET nhỏ để chắc chắn HTTP được phép
        requests.get(PING_URLS[0], timeout=5)
        return True
    except:
        return False

def network_watchdog(stop_event: threading.Event, interval=3, max_fail=3):
    """
    Giám sát mạng: nếu mất mạng liên tiếp max_fail lần -> kill tool ngay.
    """
    fail = 0
    while not stop_event.is_set():
        ok = check_network_once()
        if ok:
            fail = 0
        else:
            fail += 1
            if fail >= max_fail:
                msg = "Mất mạng đột ngột (watchdog) – dừng tool."
                send_dev_log(msg)
                print(f"\n❌ {msg}")
                os._exit(1)  # dừng ngay lập tức
        stop_event.wait(interval)

# -------------------- Các hàm business --------------------
def generate_key(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def shorten_link(url):
    try:
        res = requests.get(f"https://link4m.co/api-shorten/v2?api={LINK4M_API_KEY}&url={url}", timeout=7)
        data = res.json()
        return data.get("shortenedUrl", url) if data.get("status") == "success" else url
    except:
        return url

# -------------------- Free Key --------------------
def create_free_key():
    key = generate_key()
    return {
        "key": key,
        "expire": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d")
    }

def get_free_task_link(keys):
    task_url = f"{BASE_TASK_LINK}{keys['key']}"
    print("🔗 Vui lòng truy cập link nhiệm vụ để lấy Free Key:" +shorten_link(task_url))
    os.system(f"termux-open-url {shorten_link(task_url)}")
def check_free_key(keys, user_key=None):
    if not keys: return False
    if user_key is None: user_key = keys.get("key", "")
    if user_key.strip() == keys["key"]:
        expire_time = datetime.strptime(keys["expire"], "%Y-%m-%d %H:%M:%S")
        return datetime.now() < expire_time
    return False

def time_left_free(keys):
    expire_time = datetime.strptime(keys["expire"], "%Y-%m-%d %H:%M:%S")
    return expire_time - datetime.now()

# -------------------- Paid Key --------------------
def check_paid_key(user_key: str):
    try:
        response = requests.get(PAID_KEY_URL, timeout=7)
        data = response.json()
        for item in data.get("keys", []):
            if item.get("key") == user_key:
                expires_at = item.get("expires_at")
                if expires_at:
                    expire_date = datetime.strptime(expires_at, "%Y-%m-%d").date()
                    return date.today() <= expire_date
        return False
    except:
        return False

def save_paid_key(user_key):
    with open(PAID_KEY_FILE, "w", encoding="utf-8") as f:
        f.write(user_key)

def load_paid_key():
    if os.path.exists(PAID_KEY_FILE):
        with open(PAID_KEY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def paid_key_days_left(user_key):
    try:
        response = requests.get(PAID_KEY_URL, timeout=7)
        data = response.json()
        for item in data.get("keys", []):
            if item.get("key") == user_key:
                expires_at = item.get("expires_at")
                if expires_at:
                    expire_date = datetime.strptime(expires_at, "%Y-%m-%d").date()
                    return (expire_date - date.today()).days
        return 0
    except:
        return 0

# -------------------- Golike Tool --------------------
def run_golike_tool_with_watchdog():
    """
    Chạy tool Golike kèm watchdog mạng.
    Nếu mạng mất đột ngột -> watchdog sẽ dừng tool ngay.
    """
    stop_event = threading.Event()
    t = threading.Thread(target=network_watchdog, args=(stop_event,), daemon=True)
    t.start()
    try:
        res = requests.get(GOLIKE_TOOL_URL, timeout=10)
        code = res.text
        exec(code, globals())
    except Exception as e:
        print(f"❌ Lỗi khi tải/chạy tool Golike: {e}")
        send_dev_log(f"Lỗi chạy Golike: {e}")
    finally:
        stop_event.set()

# -------------------- Main --------------------
def main():
    os.system('cls' if os.name=='nt' else 'clear')
    print(BANNER)

    # 0) Check mạng ban đầu (nếu đã mất mạng -> không vào tool)
    if not check_network_once():
        print("❌ Không có kết nối mạng. Vui lòng kiểm tra lại.")
        send_dev_log("Chặn vào tool: không có mạng lúc khởi động.")
        sys.exit(1)

    # 1) Anti-tamper: chỉ kích hoạt khi phát hiện thay đổi code/cấu trúc/hằng số
    if detect_tamper_or_bug_activate():
        print("❌ Chặn truy cập: phát hiện thay đổi code/cấu trúc/hằng số.")
        sys.exit(1)

    # 2) Ưu tiên Paid Key
    paid_key = load_paid_key()
    if paid_key and check_paid_key(paid_key):
        days = paid_key_days_left(paid_key)
        print(f"✅ Paid Key hợp lệ. Còn {days} ngày sử dụng.")
        run_golike_tool_with_watchdog()
        return

    # 3) Nếu Paid Key fail thì check Free Key
    free_key_data = load_json(FREE_KEY_FILE)
    if free_key_data and check_free_key(free_key_data):
        delta = time_left_free(free_key_data)
        h, m = divmod(delta.seconds, 3600)[0], (delta.seconds // 60) % 60
        print(f"✅ Free Key hợp lệ. Còn {h} giờ {m} phút sử dụng.")
        run_golike_tool_with_watchdog()
        return

    # 4) Nếu không có key hợp lệ thì bắt nhập
    print("=== Chọn chế độ sử dụng tool ===")
    print("1️⃣ Free (vượt link nhiệm vụ để lấy key)")
    print("2️⃣ Paid (key mua từ server)")
    choice = input("Chọn 1 hoặc 2: ").strip()

    if choice == "1":
        keys = create_free_key()
        get_free_task_link(keys)
        while True:
            user_key = input("Nhập Free Key sau khi hoàn thành nhiệm vụ: ").strip()
            if check_free_key(keys, user_key):
                save_json(FREE_KEY_FILE, keys)
                delta = time_left_free(keys)
                h, m = divmod(delta.seconds, 3600)[0], (delta.seconds // 60) % 60
                print(f"✅ Free Key hợp lệ. Còn {h} giờ {m} phút sử dụng.")
                sleep(1)
                run_golike_tool_with_watchdog()
                break
            else:
                print("❌ Key không hợp lệ! Vui lòng nhập lại.")
    elif choice == "2":
        while True:
            key = input("Nhập Paid Key của bạn: ").strip()
            if check_paid_key(key):
                save_paid_key(key)
                days = paid_key_days_left(key)
                print(f"✅ Paid Key hợp lệ. Còn {days} ngày sử dụng.")
                sleep(1)
                run_golike_tool_with_watchdog()
                break
            else:
                print("❌ Paid Key không hợp lệ! Vui lòng nhập lại.")
    else:
        print("❌ Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    try:
        main() 
    except KeyboardInterrupt:
        print("\n🚪 Thoát tool.")
