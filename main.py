#!/usr/bin/env python3
"""
Tic-Tac Installer — Netinstall Version
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import shlex
import os
import sys
import urllib.request # Для скачування
import threading # Щоб не висло
import stat # Для прав доступу

# ============================================================================
# НАЛАШТУВАННЯ (ЗМІНИ ЦЕ!)
# ============================================================================
# Посилання на твій скрипт (має бути версія RAW!)
# Приклад: https://raw.githubusercontent.com/tviy_nik/tviy_repo/main/script.sh
GITHUB_URL = "https://raw.githubusercontent.com/AnnPoshtak/Arch-install-script/refs/heads/main/script.sh"

# Тимчасовий шлях, куди скачається скрипт
LOCAL_SCRIPT_PATH = "/tmp/script.sh"
# ============================================================================


# ---------------------- Utilities -----------------------
def run_cmd_list(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return out.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip() if e.output else ""
    except FileNotFoundError:
        return ""

# ---------------------- Hover Button --------------------
class HoverButton(tk.Button):
    def __init__(self, master=None, **kw):
        bg = kw.pop("bg", "white")
        fg = kw.pop("fg", "#C30309")
        super().__init__(master, bg=bg, fg=fg, **kw)
        self.default_bg = bg
        self.default_fg = fg
        self.hover_bg = kw.pop("_hover_bg", "#C30309")
        self.hover_fg = kw.pop("_hover_fg", "white")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _e):
        self.configure(background=self.hover_bg, foreground=self.hover_fg)

    def on_leave(self, _e):
        self.configure(background=self.default_bg, foreground=self.default_fg)


# ---------------------- Main App ------------------------
class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac Installer")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.quit())
        self.configure(bg="#C30309")

        w = int(self.winfo_screenwidth() * 0.8)
        h = int(self.winfo_screenheight() * 0.75)

        self.card = tk.Frame(self, bg="white", width=w, height=h, bd=0, relief="flat")
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Variables
        self.var_desktop = {name: tk.BooleanVar(value=False) for name in ["KDE", "Gnome", "CuteFish", "Cinnamon", "XFCE"]}
        self.var_display = {name: tk.BooleanVar(value=False) for name in ["SDDM", "GDM", "LightDM"]}
        self.var_fs = {name: tk.BooleanVar(value=False) for name in ["ext4", "btrfs", "xfs"]}
        self.wifi_ssid = tk.StringVar()
        self.wifi_pass = tk.StringVar()
        self.disk_choice = tk.StringVar()
        self.username = tk.StringVar()
        self.user_pass = tk.StringVar()

        self.screens = {}
        self.build_screens()
        self.show_screen("first")

    @staticmethod
    def single_check(selected_name, var_dict):
        for name, var in var_dict.items():
            var.set(name == selected_name)

    # ---------------- Screens building --------------------
    def build_screens(self):
        p_font = ("Arial", 22, "bold")
        h6_font = ("Arial", 16, "bold")
        btn_font = ("Arial", 18, "bold")

        # --- FIRST ---
        first = tk.Frame(self.card, bg="white")
        p_text = "Welcome to Tic-Tac Installer!\nArch-based Netinstall.\nLet's start!"
        tk.Label(first, text=p_text, bg="white", font=p_font, justify="center").pack(expand=True, pady=10)
        HoverButton(first, text="Start", font=btn_font, width=18, height=2,
                    command=lambda: self.show_screen("second")).pack(pady=20)
        self.screens["first"] = first

        # --- SECOND (DM) ---
        second = tk.Frame(self.card, bg="white")
        tk.Label(second, text="Choose Desktop Environment", bg="white", font=p_font).pack(pady=8)
        box_frame = tk.Frame(second, bg="white")
        box_frame.pack()
        for name in self.var_desktop:
            tk.Checkbutton(box_frame, text=name, bg="white", font=h6_font,
                           variable=self.var_desktop[name],
                           command=lambda n=name: self.single_check(n, self.var_desktop)).pack(anchor="w", padx=10)
        HoverButton(second, text="Next", font=btn_font, width=18, height=2,
                    command=lambda: self.show_screen("third")).pack(pady=20)
        self.screens["second"] = second

        # --- THIRD (Display Manager) ---
        third = tk.Frame(self.card, bg="white")
        tk.Label(third, text="Choose Display Manager", bg="white", font=p_font).pack(pady=8)
        box_frame = tk.Frame(third, bg="white")
        box_frame.pack()
        for name in self.var_display:
            tk.Checkbutton(box_frame, text=name, bg="white", font=h6_font,
                           variable=self.var_display[name],
                           command=lambda n=name: self.single_check(n, self.var_display)).pack(anchor="w", padx=10)
        HoverButton(third, text="Next", font=btn_font, width=18, height=2,
                    command=lambda: self.show_screen("fourth")).pack(pady=20)
        self.screens["third"] = third

        # --- FOURTH (FS) ---
        fourth = tk.Frame(self.card, bg="white")
        tk.Label(fourth, text="Choose Root File System", bg="white", font=p_font).pack(pady=8)
        box_frame = tk.Frame(fourth, bg="white")
        box_frame.pack()
        for name in self.var_fs:
            tk.Checkbutton(box_frame, text=name, bg="white", font=h6_font,
                           variable=self.var_fs[name],
                           command=lambda n=name: self.single_check(n, self.var_fs)).pack(anchor="w", padx=10)
        HoverButton(fourth, text="Next", font=btn_font, width=18, height=2,
                    command=lambda: self.show_screen("fifth")).pack(pady=20)
        self.screens["fourth"] = fourth

        # --- FIFTH (Wi-Fi) ---
        fifth = tk.Frame(self.card, bg="white")
        tk.Label(fifth, text="Connect to Wi-Fi", bg="white", font=p_font).pack(pady=8)
        nb_frame = tk.Frame(fifth, bg="white")
        nb_frame.pack(pady=6, fill="both", expand=False)
        self.wifi_listbox = tk.Listbox(nb_frame, height=8, font=("Arial", 12))
        self.wifi_listbox.pack(side="left", fill="both", expand=True, padx=(10, 0))
        tk.Scrollbar(nb_frame, command=self.wifi_listbox.yview).pack(side="right", fill="y")
        
        ctrl_frame = tk.Frame(fifth, bg="white")
        ctrl_frame.pack(pady=6)
        HoverButton(ctrl_frame, text="Scan", font=btn_font, width=12, command=self.scan_wifi).pack(side="left", padx=6)
        HoverButton(ctrl_frame, text="Select", font=btn_font, width=12, command=self.select_wifi_from_list).pack(side="left", padx=6)
        
        tk.Label(fifth, text="Password:", bg="white", font=h6_font).pack(pady=(12, 2))
        ttk.Entry(fifth, textvariable=self.wifi_pass, show="*").pack(pady=(0, 8), ipadx=80)
        HoverButton(fifth, text="Next", font=btn_font, width=18, height=2,
                    command=lambda: self.show_screen("sixth")).pack(pady=10)
        self.screens["fifth"] = fifth

        # --- SIXTH (Disk) ---
        sixth = tk.Frame(self.card, bg="white")
        tk.Label(sixth, text="Select Disk (Will be FORMATTED!)", bg="white", font=p_font, fg="red").pack(pady=6)
        dl_frame = tk.Frame(sixth, bg="white")
        dl_frame.pack(pady=6, fill="both", expand=True)
        self.disk_listbox = tk.Listbox(dl_frame, height=8, font=("Arial", 12))
        self.disk_listbox.pack(side="left", fill="both", expand=True, padx=(10, 0))
        tk.Scrollbar(dl_frame, command=self.disk_listbox.yview).pack(side="right", fill="y")
        
        HoverButton(sixth, text="Refresh", font=btn_font, width=14, command=self.load_disks).pack(pady=8)
        HoverButton(sixth, text="Select", font=btn_font, width=14, command=self.select_disk_from_list).pack(pady=6)
        HoverButton(sixth, text="Next", font=btn_font, width=18, height=2,
                    command=lambda: self.show_screen("seventh")).pack(pady=10)
        self.screens["sixth"] = sixth

        # --- SEVENTH (User) ---
        seventh = tk.Frame(self.card, bg="white")
        tk.Label(seventh, text="Create User", bg="white", font=p_font).pack(pady=8)
        tk.Label(seventh, text="Username:", bg="white", font=h6_font).pack(pady=(8, 2))
        ttk.Entry(seventh, textvariable=self.username).pack(ipadx=80)
        tk.Label(seventh, text="Password:", bg="white", font=h6_font).pack(pady=(10, 2))
        ttk.Entry(seventh, textvariable=self.user_pass, show="*").pack(ipadx=80)
        HoverButton(seventh, text="Next", font=btn_font, width=18, height=2,
                    command=self.prepare_summary).pack(pady=12)
        self.screens["seventh"] = seventh

        # --- EIGHTH (Install) ---
        eighth = tk.Frame(self.card, bg="white")
        tk.Label(eighth, text="Ready to Install!", bg="white", font=p_font).pack(pady=8)
        self.summary_frame = tk.Frame(eighth, bg="white")
        self.summary_frame.pack(pady=6, padx=8, fill="both", expand=False)
        self.summary_label = tk.Label(self.summary_frame, text="", bg="white", justify="left", font=("Arial", 14))
        self.summary_label.pack(anchor="w", padx=6, pady=6)

        # КНОПКА ЗАПУСКУ НЕТІНСТАЛУ
        HoverButton(eighth, text="INSTALL SYSTEM", font=btn_font, width=20, height=3, 
                    bg="#C30309", fg="white",
                    command=self.start_netinstall_thread).pack(pady=20)
        self.screens["eighth"] = eighth

    def show_screen(self, name):
        for scr in self.screens.values(): scr.pack_forget()
        self.screens[name].pack(fill="both", expand=True)

    # --- Wi-Fi Logic ---
    def scan_wifi(self):
        self.wifi_listbox.delete(0, tk.END)
        try:
            out = run_cmd_list(["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list"])
            if not out: raise Exception("no output")
        except:
            messagebox.showerror("Error", "nmcli failed")
            return
        seen = set()
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 3:
                ssid = ":".join(parts[:-2]).strip()
                if ssid and ssid not in seen:
                    seen.add(ssid)
                    self.wifi_listbox.insert(tk.END, f"{ssid} [{parts[-1]}]")

    def select_wifi_from_list(self):
        sel = self.wifi_listbox.curselection()
        if sel:
            ssid = self.wifi_listbox.get(sel[0]).split(" ")[0]
            self.wifi_ssid.set(ssid)
            messagebox.showinfo("Selected", f"SSID: {ssid}")

    def connect_wifi_now(self):
        ssid = self.wifi_ssid.get()
        pwd = self.wifi_pass.get()
        if not ssid: return
        cmd = ["nmcli", "device", "wifi", "connect", ssid]
        if pwd: cmd += ["password", pwd]
        run_cmd_list(cmd)

    # --- Disk Logic ---
    def load_disks(self):
        self.disk_listbox.delete(0, tk.END)
        try:
            out = run_cmd_list(["lsblk", "-o", "NAME,SIZE,MODEL,TYPE", "-n"])
        except: return
        for line in out.splitlines():
            if "disk" in line:
                self.disk_listbox.insert(tk.END, f"/dev/{line.split()[0]} {line}")

    def select_disk_from_list(self):
        sel = self.disk_listbox.curselection()
        if sel:
            self.disk_choice.set(self.disk_listbox.get(sel[0]).split()[0])
            messagebox.showinfo("Selected", f"Disk: {self.disk_choice.get()}")

    # --- Summary ---
    def prepare_summary(self):
        d = next((k for k, v in self.var_desktop.items() if v.get()), "NONE")
        dm = next((k for k, v in self.var_display.items() if v.get()), "NONE")
        fs = next((k for k, v in self.var_fs.items() if v.get()), "ext4")
        summ = f"Desktop: {d}\nDM: {dm}\nFS: {fs}\nDisk: {self.disk_choice.get()}\nUser: {self.username.get()}"
        self.summary_label.config(text=summ)
        self.show_screen("eighth")

    # ========================================================================
    # NETINSTALL LOGIC (THE NEW PART)
    # ========================================================================
    def start_netinstall_thread(self):
        # Спробувати підключити Wi-Fi перед стартом
        if self.wifi_ssid.get():
            try: self.connect_wifi_now()
            except: pass
        
        if not self.disk_choice.get():
            messagebox.showerror("Error", "No disk selected!")
            return

        # Збираємо змінні для Bash
        env = os.environ.copy()
        env["USER_NAME"] = self.username.get()
        env["USER_PASSWORD"] = self.user_pass.get()
        env["TARGET_DISK"] = self.disk_choice.get()
        env["WIFI_SSID"] = self.wifi_ssid.get()
        env["WIFI_PASS"] = self.wifi_pass.get()
        
        # Знаходимо вибрані галочки
        env["DESKTOP_ENV"] = next((k for k, v in self.var_desktop.items() if v.get()), "NONE")
        env["DISPLAY_MANAGER"] = next((k for k, v in self.var_display.items() if v.get()), "NONE")
        env["FILESYSTEM"] = next((k for k, v in self.var_fs.items() if v.get()), "ext4")

        # Запускаємо в потоці
        threading.Thread(target=self._download_and_run, args=(env,)).start()

    def _download_and_run(self, env_vars):
        # Відкриваємо вікно логів
        self.after(0, lambda: self._show_log_window())
        
        try:
            # 1. Скачуємо скрипт
            self._log(f"Downloading script from {GITHUB_URL}...")
            with urllib.request.urlopen(GITHUB_URL) as response, open(LOCAL_SCRIPT_PATH, 'wb') as out:
                out.write(response.read())
            
            # 2. Робимо executable
            st = os.stat(LOCAL_SCRIPT_PATH)
            os.chmod(LOCAL_SCRIPT_PATH, st.st_mode | stat.S_IEXEC)
            self._log("Download complete. Starting Bash script...")

            # 3. Запускаємо Bash з передачею змінних
            proc = subprocess.Popen(
                ["/bin/bash", LOCAL_SCRIPT_PATH],
                env=env_vars,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Читаємо вивід в реальному часі
            for line in proc.stdout:
                self.after(0, lambda l=line: self._log(l, newline=False))
            
            proc.wait()
            if proc.returncode == 0:
                self._log("\n=== INSTALLATION SUCCESSFUL! ===")
            else:
                self._log(f"\n=== ERROR: Code {proc.returncode} ===")

        except Exception as e:
            self._log(f"\nCRITICAL ERROR: {e}")

    def _show_log_window(self):
        top = tk.Toplevel(self)
        top.title("Installation Log")
        top.geometry("800x600")
        top.configure(bg="black")
        self.log_text = tk.Text(top, bg="black", fg="#00ff00", font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True)

    def _log(self, msg, newline=True):
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, msg + ("\n" if newline else ""))
            self.log_text.see(tk.END)

def main():
    app = InstallerApp()
    app.load_disks()
    app.scan_wifi()
    app.mainloop()

if __name__ == "__main__":
    main()