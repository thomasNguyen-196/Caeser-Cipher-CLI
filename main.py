#!/usr/bin/env python3
"""
Caesar Cipher — Fancy CLI UI
- Màu sắc ANSI (fallback nếu Windows không hỗ trợ)
- Banner lớn (dùng pyfiglet nếu có)
- Menu tương tác, validation input
- Brute-force với scoring (đếm từ tiếng Anh phổ biến)
- Lưu kết quả vào file / copy clipboard nếu có pyperclip
"""
import sys
import os
import time
import threading
import shutil

# Optional enhancements (will be used only if installed)
try:
    import pyfiglet
except Exception:
    pyfiglet = None

try:
    import colorama
    colorama.init()
except Exception:
    colorama = None

try:
    import pyperclip
except Exception:
    pyperclip = None

# ANSI colors (works on most modern terminals)
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"
FG = {
    "red": CSI + "31m",
    "green": CSI + "32m",
    "yellow": CSI + "33m",
    "blue": CSI + "34m",
    "magenta": CSI + "35m",
    "cyan": CSI + "36m",
    "white": CSI + "37m",
}

# Utilities
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def center(text, width=None):
    if width is None:
        width = shutil.get_terminal_size((80, 20)).columns
    return text.center(width)

def banner():
    title = "CAESAR CIPHER"
    subtitle = "CLI — Cool Edition"
    width = shutil.get_terminal_size((80, 20)).columns
    if pyfiglet:
        fig = pyfiglet.figlet_format("CAESAR", font="slant")
        print(FG["cyan"] + fig + RESET)
        print(center(FG["yellow"] + subtitle + RESET, width))
    else:
        # simple ASCII banner
        print(FG["cyan"] + "=" * width + RESET)
        print(center(FG["cyan"] + title + RESET, width))
        print(center(FG["yellow"] + subtitle + RESET, width))
        print(FG["cyan"] + "=" * width + RESET)

def prompt(msg):
    try:
        return input(FG["green"] + msg + RESET)
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)

# Caesar core functions
def caesar_encrypt(plaintext, key):
    result = []
    for char in plaintext:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result.append(chr((ord(char) - shift + key) % 26 + shift))
        else:
            result.append(char)
    return "".join(result)

def caesar_decrypt(ciphertext, key):
    return caesar_encrypt(ciphertext, -key)

# English scoring heuristics for brute-force ranking
COMMON_WORDS = [" the ", " and ", " to ", " of ", " that ", " is ", " in ", " it ", " for ", " you ", " with ", " on "]

def english_score(text):
    lower = " " + text.lower() + " "
    score = 0
    # count common words
    for w in COMMON_WORDS:
        score += lower.count(w) * 10
    # letter frequency similarity (quick heuristic)
    freq = {c: lower.count(c) for c in "etaoinshrdlu"}
    score += sum(freq.values())
    return score

# Spinner for long operations
class Spinner:
    def __init__(self, msg="Processing"):
        self.msg = msg
        self.running = False
        self.thread = None
        self.chars = "|/-\\"

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def _spin(self):
        i = 0
        while self.running:
            print(f"\r{FG['magenta']}{self.msg} {self.chars[i % len(self.chars)]}{RESET}", end="", flush=True)
            i += 1
            time.sleep(0.08)
        print("\r" + " " * (len(self.msg) + 4) + "\r", end="", flush=True)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)

# Pretty-print boxed section
def boxed(title, body):
    width = min(80, shutil.get_terminal_size((80,20)).columns - 4)
    print(FG["blue"] + "┌" + "─" * (width) + "┐" + RESET)
    title_line = f" {title} "
    print(FG["blue"] + "│" + RESET + BOLD + center(title_line, width) + RESET + FG["blue"] + "│" + RESET)
    print(FG["blue"] + "├" + "─" * (width) + "┤" + RESET)
    for line in body.splitlines():
        if len(line) > width:
            # wrap naive
            while line:
                print(FG["blue"] + "│" + RESET + line[:width].ljust(width) + FG["blue"] + "│" + RESET)
                line = line[width:]
        else:
            print(FG["blue"] + "│" + RESET + line.ljust(width) + FG["blue"] + "│" + RESET)
    print(FG["blue"] + "└" + "─" * (width) + "┘" + RESET)

# Main interactive functions
def encrypt_flow():
    clear()
    banner()
    boxed("ENCRYPT", "Nhập văn bản cần mã hóa và khóa (số nguyên).")
    plaintext = prompt("Plaintext: ")
    while True:
        key_s = prompt("Key (integer, can be negative): ").strip()
        if key_s.lstrip("-").isdigit():
            key = int(key_s)
            break
        print(FG["red"] + "Key phải là số nguyên. Thử lại." + RESET)
    ciphertext = caesar_encrypt(plaintext, key)
    boxed("KẾT QUẢ", ciphertext)
    post_output_actions(ciphertext)

def decrypt_flow():
    clear()
    banner()
    boxed("DECRYPT", "Nhập ciphertext và khóa (số nguyên).")
    ciphertext = prompt("Ciphertext: ")
    while True:
        key_s = prompt("Key (integer): ").strip()
        if key_s.lstrip("-").isdigit():
            key = int(key_s)
            break
        print(FG["red"] + "Key phải là số nguyên. Thử lại." + RESET)
    plaintext = caesar_decrypt(ciphertext, key)
    boxed("KẾT QUẢ", plaintext)
    post_output_actions(plaintext)

def brute_flow():
    clear()
    banner()
    boxed("BRUTE-FORCE", "Thử tất cả khóa 1..25 và xếp theo gợi ý (score). Chọn dòng để xem chi tiết.")
    ciphertext = prompt("Ciphertext to brute-force: ")
    spinner = Spinner("Brute-forcing")
    spinner.start()
    results = []
    for key in range(1, 26):
        dec = caesar_decrypt(ciphertext, key)
        score = english_score(dec)
        results.append((score, key, dec))
        time.sleep(0.02)  # small delay to make spinner visible
    spinner.stop()
    # sort by score desc
    results.sort(reverse=True, key=lambda x: x[0])
    lines = []
    for idx, (score, key, dec) in enumerate(results, 1):
        short = dec if len(dec) <= 60 else dec[:57] + "..."
        lines.append(f"{idx:2d}. Key {key:2d} | score={score:3d} | {short}")
    boxed("BRUTE-FORCE RESULTS (sorted)", "\n".join(lines))
    print("Nhập số thứ tự (ví dụ 1) để hiển thị plaintext tương ứng, 'a' để lưu tất cả, 'q' để về menu.")
    while True:
        cmd = prompt("> ").strip().lower()
        if cmd == "q" or cmd == "":
            return
        if cmd == "a":
            text_all = "\n".join([f"Key {k}: {d}" for _, k, d in results])
            save_or_copy_flow(text_all)
            continue
        if cmd.isdigit():
            n = int(cmd)
            if 1 <= n <= len(results):
                score, key, dec = results[n-1]
                boxed(f"Key {key} (score={score})", dec)
                post_output_actions(dec)
            else:
                print(FG["red"] + "Số không hợp lệ." + RESET)
        else:
            print(FG["yellow"] + "Lệnh không hiểu. Nhập số, 'a' hoặc 'q'." + RESET)

def post_output_actions(text):
    print()
    print(FG["cyan"] + "[1] Copy vào clipboard (nếu có pyperclip)   [2] Lưu vào file   [Enter] Quay lại" + RESET)
    cmd = prompt("Chọn: ").strip()
    if cmd == "1":
        if pyperclip:
            try:
                pyperclip.copy(text)
                print(FG["green"] + "Đã copy vào clipboard." + RESET)
            except Exception as e:
                print(FG["red"] + f"Copy thất bại: {e}" + RESET)
        else:
            print(FG["yellow"] + "pyperclip không cài, không thể copy. Bạn có thể pip install pyperclip." + RESET)
    elif cmd == "2":
        fname = prompt("Tên file lưu (mặc định output.txt): ").strip() or "output.txt"
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(text)
            print(FG["green"] + f"Đã lưu vào {fname}" + RESET)
        except Exception as e:
            print(FG["red"] + f"Lưu thất bại: {e}" + RESET)
    else:
        return
    prompt("Nhấn Enter để tiếp tục...")

def save_or_copy_flow(text):
    print(FG["cyan"] + "Bạn muốn (1) copy, (2) lưu file, (3) in ra console, (q) hủy?" + RESET)
    cmd = prompt("> ").strip().lower()
    if cmd == "1":
        if pyperclip:
            pyperclip.copy(text)
            print(FG["green"] + "Đã copy toàn bộ kết quả." + RESET)
        else:
            print(FG["yellow"] + "pyperclip không có." + RESET)
    elif cmd == "2":
        fname = prompt("Tên file: ").strip() or "brute_results.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(text)
        print(FG["green"] + f"Đã lưu vào {fname}" + RESET)
    elif cmd == "3":
        print("\n" + text + "\n")
    else:
        print("Hủy.")

def show_help():
    clear()
    banner()
    help_text = (
        "Hướng dẫn ngắn:\n"
        "- Mã hóa/giải mã với khóa nguyên.\n"
        "- Brute-force sẽ thử các khóa 1..25 và gợi ý bằng heuristic (common words + freq).\n"
        "- Sau khi có kết quả, bạn có thể copy hoặc lưu file.\n"
        "- Nếu muốn giao diện xịn hơn: pip install pyfiglet colorama pyperclip\n"
    )
    boxed("HELP", help_text)
    prompt("Nhấn Enter để về menu...")

def main_loop():
    while True:
        clear()
        banner()
        width = shutil.get_terminal_size((80, 20)).columns
        menu = (
            "1) Mã hóa (Encrypt)\n"
            "2) Giải mã (Decrypt)\n"
            "3) Brute-force decrypt (gợi ý kết quả)\n"
            "4) Help\n"
            "5) Exit\n"
        )
        boxed("MAIN MENU", menu)
        choice = prompt("Chọn (1-5): ").strip()
        if choice == "1":
            encrypt_flow()
        elif choice == "2":
            decrypt_flow()
        elif choice == "3":
            brute_flow()
        elif choice == "4":
            show_help()
        elif choice == "5":
            print(FG["magenta"] + "Tạm biệt — mã hóa an toàn nhé!" + RESET)
            time.sleep(0.6)
            break
        else:
            print(FG["red"] + "Lựa chọn không hợp lệ. Thử lại." + RESET)
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n" + FG["magenta"] + "Thoát." + RESET)
        sys.exit(0)
