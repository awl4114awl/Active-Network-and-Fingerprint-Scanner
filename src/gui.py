"""
gui.py
Tkinter GUI for the Active Network & Fingerprint Scanner.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import csv

from .scanner import scan_network, fingerprint_device


class NetworkScannerGUI:

    def __init__(self, root: tk.Tk):
        self.root = root

        # Window setup AFTER icon is already set in run.py
        self.root.title("Active Network & Fingerprint Scanner")
        self.root.configure(bg="#222222")

        # --- FIXED WINDOW SIZE ---
        self.root.geometry("600x400")   # starting size
        self.root.minsize(600, 400)     # cannot shrink smaller
        self.root.maxsize(600, 400)     # cannot grow larger
        self.root.resizable(False, False)

        self._configure_styles()

        # Columns for Treeview
        self.columns = ("IP Address", "MAC Address", "Operating System")

        # Build GUI
        self._build_layout()

        # Status footer
        self.status_var = tk.StringVar(value="Ready.")
        self._build_status_footer()

        # STORE RESULTS
        self.devices = []

    # -----------------------------
    # Styles
    # -----------------------------
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#333333",
            foreground="white",
            rowheight=25,
            fieldbackground="#333333",
        )
        style.map("Treeview", background=[("selected", "#666666")])

        style.configure("TButton", background="#444444", foreground="white", borderwidth=1)
        style.map("TButton", background=[("active", "#555555")])

        style.configure("TEntry", background="#333333", foreground="white", fieldbackground="#333333")
        style.configure("TLabel", background="#222222", foreground="white")
        style.configure("TFrame", background="#222222")

    # -----------------------------
    # Layout
    # -----------------------------
    def _build_layout(self):
        # INPUT BAR
        frame = ttk.Frame(self.root)
        frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame, text="IP Range:").pack(side="left", padx=5)

        self.ip_entry = ttk.Entry(frame, width=18)
        self.ip_entry.pack(side="left", padx=5)
        self.ip_entry.insert(0, "")

        self.scan_button = ttk.Button(frame, text="Scan", command=self._start_scan_thread)
        self.scan_button.pack(side="left", padx=5)

        self.export_button = ttk.Button(frame, text="Export CSV", command=self._export_csv, state="disabled")
        self.export_button.pack(side="left", padx=5)

        # PROGRESS BAR
        self.progress = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress.pack(padx=10, fill="x")

        # TABLE WRAPPER FRAME
        table_frame = ttk.Frame(self.root)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # TABLE
        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings",
            selectmode="browse",
        )

        # Column widths to fit 600px
        self.tree.column("IP Address", width=120, anchor="center")
        self.tree.column("MAC Address", width=140, anchor="center")
        self.tree.column("Operating System", width=240, anchor="center")

        # Column headings
        for col in self.columns:
            self.tree.heading(
                col,
                text=col,
                command=lambda c=col: self._sort_by_column(c, False),
            )

        self.tree.pack(side="left", fill="both", expand=True)

        # SCROLLBAR
        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    # -----------------------------
    # Footer
    # -----------------------------
    def _build_status_footer(self):
        footer = ttk.Frame(self.root)
        footer.pack(fill="x", padx=10, pady=(0, 10))

        self.status_label = ttk.Label(footer, textvariable=self.status_var, anchor="w")
        self.status_label.pack(side="left", anchor="w")

    # -----------------------------
    # Scan Button Trigger
    # -----------------------------
    def _start_scan_thread(self):
        ip_range = self.ip_entry.get().strip()
        if not ip_range:
            messagebox.showwarning("Missing IP Range", "Please enter an IP range.")
            return

        self.scan_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.status_var.set("Scanning…")
        self.progress.start(10)

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Start scan worker thread
        thread = threading.Thread(target=self._scan_worker, args=(ip_range,), daemon=True)
        thread.start()

    # -----------------------------
    # Scan Worker Thread
    # -----------------------------
    def _scan_worker(self, ip_range):
        start_time = time.time()
        devices = scan_network(ip_range)
        self.devices = devices

        # Insert base rows
        def insert_initial():
            for d in devices:
                self.tree.insert("", "end", values=(d["ip"], d["mac"], "Resolving OS…"))
        self.root.after(0, insert_initial)

        # OS detection
        for index, device in enumerate(devices):
            os_text = fingerprint_device(device["ip"])

            def update(idx=index, os_text=os_text):
                items = self.tree.get_children()
                if idx < len(items):
                    item = items[idx]
                    values = list(self.tree.item(item, "values"))
                    values[2] = os_text
                    self.tree.item(item, values=values)

            self.root.after(0, update)

        elapsed = time.time() - start_time

        # Finish
        def finish():
            self.progress.stop()
            self.scan_button.config(state="normal")
            count = len(devices)

            if count > 0:
                self.export_button.config(state="normal")
                self.status_var.set(f"{count} devices found • Completed in {elapsed:.1f}s")
            else:
                self.status_var.set("No devices found.")

        self.root.after(0, finish)

    # -----------------------------
    # Sorting
    # -----------------------------
    def _sort_by_column(self, col, reverse):
        rows = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        rows.sort(reverse=reverse)

        for i, (_, k) in enumerate(rows):
            self.tree.move(k, "", i)

        self.tree.heading(col, command=lambda c=col: self._sort_by_column(c, not reverse))

    # -----------------------------
    # CSV Export
    # -----------------------------
    def _export_csv(self):
        if not self.tree.get_children():
            messagebox.showinfo("No Data", "There is nothing to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Results",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item, "values"))

            messagebox.showinfo("Export Complete", f"Saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting:\n{e}")
