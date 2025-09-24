#!/usr/bin/env python3
"""
This script is the command-line entry point for the application.
"""

import sys
import time

from . import ui, workflows

def main_loop():
    """The main menu loop of the application."""
    while True:
        ui.clear()
        ui.banner()
        menu = (
            "1) Mã hóa (Encrypt)\n"
            "2) Giải mã (Decrypt)\n"
            "3) Brute-force decrypt (gợi ý kết quả)\n"
            "4) Help\n"
            "5) Exit\n"
        )
        ui.boxed("MAIN MENU", menu)
        choice = ui.prompt("Chọn (1-5): ").strip()

        if choice == "1":
            workflows.encrypt_flow()
        elif choice == "2":
            workflows.decrypt_flow()
        elif choice == "3":
            workflows.brute_flow()
        elif choice == "4":
            workflows.show_help()
        elif choice == "5":
            print(ui.FG["magenta"] + "Tạm biệt — mã hóa an toàn nhé!" + ui.RESET)
            time.sleep(0.6)
            break
        else:
            print(ui.FG["red"] + "Lựa chọn không hợp lệ. Thử lại." + ui.RESET)
            time.sleep(0.8)

def main():
    """Main function to run the application."""
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n" + ui.FG["magenta"] + "Thoát." + ui.RESET)
        sys.exit(0)

if __name__ == "__main__":
    main()
