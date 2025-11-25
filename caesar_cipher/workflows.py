"""
Application workflows that orchestrate the UI and cipher logic.
"""

import sys
import time
from . import ui
from . import cipher
from . import analysis

def _read_text_input(label: str) -> str:
    """
    Reads potentially large text either from stdin (if piped), a file, or direct input.

    Direct terminal input is limited by the terminal's line buffer (~1k chars per line
    in canonical mode). Offering a file/piped option avoids paste truncation.
    """
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        return data.rstrip("\n")

    print(ui.FG["yellow"] + "Văn bản dài (trên ~1k ký tự) nên nhập qua file để tránh bị cắt." + ui.RESET)
    mode = ui.prompt("Chọn nhập trực tiếp [Enter] hoặc gõ 'f' để đọc từ file: ").strip().lower()
    if mode == "f":
        while True:
            path = ui.prompt("Đường dẫn file: ").strip()
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(ui.FG["red"] + f"Lỗi đọc file: {e}" + ui.RESET)
                retry = ui.prompt("Thử lại? (y/n): ").strip().lower()
                if retry != "y":
                    return ""
    return ui.prompt(f"{label}: ")

def encrypt_flow():
    """Workflow for encrypting a message."""
    ui.clear()
    ui.banner()
    ui.boxed("ENCRYPT", "Nhập văn bản cần mã hóa và khóa (số nguyên).")
    plaintext = _read_text_input("Plaintext")
    while True:
        key_s = ui.prompt("Key (integer, can be negative): ").strip()
        if key_s.lstrip("-").isdigit():
            key = int(key_s)
            break
        print(ui.FG["red"] + "Key phải là số nguyên. Thử lại." + ui.RESET)
    ciphertext = cipher.caesar_encrypt(plaintext, key)
    ui.boxed("KẾT QUẢ", ciphertext)
    post_output_actions(ciphertext)

def decrypt_flow():
    """Workflow for decrypting a message."""
    ui.clear()
    ui.banner()
    ui.boxed("DECRYPT", "Nhập ciphertext và khóa (số nguyên).")
    ciphertext = _read_text_input("Ciphertext")
    while True:
        key_s = ui.prompt("Key (integer): ").strip()
        if key_s.lstrip("-").isdigit():
            key = int(key_s)
            break
        print(ui.FG["red"] + "Key phải là số nguyên. Thử lại." + ui.RESET)
    plaintext = cipher.caesar_decrypt(ciphertext, key)
    ui.boxed("KẾT QUẢ", plaintext)
    post_output_actions(plaintext)

def brute_flow():
    """Workflow for brute-forcing a ciphertext."""
    ui.clear()
    ui.banner()
    ui.boxed("BRUTE-FORCE", "Thử tất cả khóa 1..25 và xếp theo gợi ý (score). Chọn dòng để xem chi tiết.")
    ciphertext = _read_text_input("Ciphertext to brute-force")
    spinner = ui.Spinner("Brute-forcing")
    spinner.start()
    results = []
    for key in range(1, 26):
        dec = cipher.caesar_decrypt(ciphertext, key)
        score = analysis.english_score(dec)
        results.append((score, key, dec))
        time.sleep(0.02)  # Small delay to make spinner visible
    spinner.stop()

    results.sort(reverse=True, key=lambda x: x[0])
    lines = []
    for idx, (score, key, dec) in enumerate(results, 1):
        short = dec if len(dec) <= 60 else dec[:57] + "..."
        lines.append(f"{idx:2d}. Key {key:2d} | score={score:3d} | {short}")
    ui.boxed("BRUTE-FORCE RESULTS (sorted)", "\n".join(lines))

    print("Nhập số thứ tự (ví dụ 1) để hiển thị plaintext tương ứng, 'a' để lưu tất cả, 'q' để về menu.")
    while True:
        cmd = ui.prompt("> ").strip().lower()
        if cmd in ("q", ""):
            return
        if cmd == "a":
            text_all = "\n".join([f"Key {k}: {d}" for _, k, d in results])
            save_or_copy_flow(text_all)
            continue
        if cmd.isdigit():
            n = int(cmd)
            if 1 <= n <= len(results):
                score, key, dec = results[n-1]
                ui.boxed(f"Key {key} (score={score})", dec)
                post_output_actions(dec)
            else:
                print(ui.FG["red"] + "Số không hợp lệ." + ui.RESET)
        else:
            print(ui.FG["yellow"] + "Lệnh không hiểu. Nhập số, 'a' hoặc 'q'." + ui.RESET)

def post_output_actions(text: str):
    """Handles actions after a result is generated (copy, save, etc.)."""
    print()
    print(ui.FG["cyan"] + "[1] Copy vào clipboard (nếu có pyperclip)   [2] Lưu vào file   [Enter] Quay lại" + ui.RESET)
    cmd = ui.prompt("Chọn: ").strip()
    if cmd == "1":
        if ui.pyperclip:
            try:
                ui.pyperclip.copy(text)
                print(ui.FG["green"] + "Đã copy vào clipboard." + ui.RESET)
            except Exception as e:
                print(ui.FG["red"] + f"Copy thất bại: {e}" + ui.RESET)
        else:
            print(ui.FG["yellow"] + "pyperclip không cài, không thể copy. Bạn có thể pip install pyperclip." + ui.RESET)
    elif cmd == "2":
        fname = ui.prompt("Tên file lưu (mặc định output.txt): ").strip() or "output.txt"
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(text)
            print(ui.FG["green"] + f"Đã lưu vào {fname}" + ui.RESET)
        except Exception as e:
            print(ui.FG["red"] + f"Lưu thất bại: {e}" + ui.RESET)
    else:
        return
    ui.prompt("Nhấn Enter để tiếp tục...")

def save_or_copy_flow(text: str):
    """A mini-flow for saving or copying a large block of text."""
    print(ui.FG["cyan"] + "Bạn muốn (1) copy, (2) lưu file, (3) in ra console, (q) hủy?" + ui.RESET)
    cmd = ui.prompt("> ").strip().lower()
    if cmd == "1":
        if ui.pyperclip:
            ui.pyperclip.copy(text)
            print(ui.FG["green"] + "Đã copy toàn bộ kết quả." + ui.RESET)
        else:
            print(ui.FG["yellow"] + "pyperclip không có." + ui.RESET)
    elif cmd == "2":
        fname = ui.prompt("Tên file: ").strip() or "brute_results.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(text)
        print(ui.FG["green"] + f"Đã lưu vào {fname}" + ui.RESET)
    elif cmd == "3":
        print("\n" + text + "\n")
    else:
        print("Hủy.")

def show_help():
    """Displays the help screen."""
    ui.clear()
    ui.banner()
    help_text = (
        "Hướng dẫn ngắn:\n"
        "- Mã hóa/giải mã với khóa nguyên.\n"
        "- Văn bản dài có thể đọc từ file (chọn 'f') hoặc pipe: cat file.txt | caesar\n"
        "- Brute-force sẽ thử các khóa 1..25 và gợi ý bằng heuristic (common words + freq).\n"
        "- Sau khi có kết quả, bạn có thể copy hoặc lưu file.\n"
        "- Nếu muốn giao diện xịn hơn: pip install pyfiglet colorama pyperclip\n"
    )
    ui.boxed("HELP", help_text)
    ui.prompt("Nhấn Enter để về menu...")
