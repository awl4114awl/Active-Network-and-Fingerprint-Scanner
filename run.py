import tkinter as tk
import os
import sys
import ctypes

from src.gui import NetworkScannerGUI


def main():
    root = tk.Tk()

    # --------------------------------------------------
    # LOAD ICON (Title bar + Taskbar)
    # --------------------------------------------------
    icon_path = os.path.join("screenshots", "icon.ico")

    if os.path.exists(icon_path):
        try:
            # Title bar icon
            root.iconbitmap(icon_path)

            # ---------- WINDOWS TASKBAR FIX ----------
            if sys.platform.startswith("win"):
                # Give the app a unique, stable AppUserModelID
                app_id = "ActiveNetworkFingerprintScanner"

                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

                # Force taskbar to refresh icon
                hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
                ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, 0)
        except Exception as e:
            print(f"[WARN] Could not load taskbar icon: {e}")
    else:
        print("[WARN] icon.ico not found")

    # --------------------------------------------------

    app = NetworkScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()