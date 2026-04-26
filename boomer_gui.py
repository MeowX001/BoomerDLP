import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ===== Create download folder if it doesn't exist =====
if not os.path.exists("download"):
    os.makedirs("download")

# ========== THEME COLORS ==========
BG       = "#0d0d0d"
BG2      = "#161616"
BG3      = "#1f1f1f"
ACCENT   = "#00e5ff"
ACCENT2  = "#ff4081"
TEXT     = "#e0e0e0"
TEXT_DIM = "#555555"
GREEN    = "#00e676"
RED      = "#ff1744"
YELLOW   = "#ffd740"
BORDER   = "#2a2a2a"
FONT_MONO = ("Courier New", 10)
FONT_UI   = ("Courier New", 11, "bold")
FONT_BIG  = ("Courier New", 16, "bold")
FONT_SM   = ("Courier New", 9)


class BBoomer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BOOMER — yt-dlp GUI")
        self.geometry("780x620")
        self.minsize(700, 560)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.use_local = tk.BooleanVar(value=False)
        self.mode      = tk.StringVar(value="video")
        self.fmt_var   = tk.StringVar(value="MP4")
        self.is_downloading = False

        self._build_ui()
        self._update_formats()

    # ───────────────────────────── UI BUILD ──────────────────────────────

    def _build_ui(self):
        # ── HEADER ──
        hdr = tk.Frame(self, bg=BG, pady=10)
        hdr.pack(fill="x", padx=20)

        tk.Label(hdr, text="◈ BOOMER", font=("Courier New", 22, "bold"),
                 bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(hdr, text="yt-dlp frontend", font=FONT_SM,
                 bg=BG, fg=TEXT_DIM).pack(side="left", padx=(8,0), pady=(8,0))

        # version badge
        badge = tk.Label(hdr, text=" GUI v2 ", font=FONT_SM,
                         bg=ACCENT2, fg="white")
        badge.pack(side="right", padx=4)

        self._sep()

        # ── URL INPUT ──
        url_frame = tk.Frame(self, bg=BG2, pady=12, padx=16,
                             highlightbackground=BORDER, highlightthickness=1)
        url_frame.pack(fill="x", padx=20, pady=(0, 6))

        tk.Label(url_frame, text="URL", font=FONT_UI,
                 bg=BG2, fg=ACCENT).pack(anchor="w")

        entry_row = tk.Frame(url_frame, bg=BG2)
        entry_row.pack(fill="x", pady=(4, 0))

        self.url_entry = tk.Entry(
            entry_row, font=FONT_MONO, bg=BG3, fg=TEXT,
            insertbackground=ACCENT, relief="flat",
            highlightbackground=BORDER, highlightthickness=1,
            highlightcolor=ACCENT
        )
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        paste_btn = self._btn(entry_row, "⟳ PASTE", self._paste_url,
                              bg=BG3, fg=TEXT_DIM, side="left")

        # ── MODE SELECTOR ──
        mode_frame = tk.Frame(self, bg=BG, pady=4)
        mode_frame.pack(fill="x", padx=20)

        tk.Label(mode_frame, text="MODE", font=FONT_SM,
                 bg=BG, fg=TEXT_DIM).pack(side="left", padx=(0,10))

        for label, val in [("▶  VIDEO", "video"), ("♪  AUDIO", "audio")]:
            rb = tk.Radiobutton(
                mode_frame, text=label, variable=self.mode, value=val,
                command=self._update_formats,
                font=FONT_UI, bg=BG, fg=TEXT,
                selectcolor=BG3, activebackground=BG,
                activeforeground=ACCENT, indicatoron=0,
                relief="flat", padx=14, pady=5,
                highlightthickness=0,
                cursor="hand2"
            )
            rb.pack(side="left", padx=(0, 6))
            rb.bind("<Enter>", lambda e, w=rb: w.config(fg=ACCENT))
            rb.bind("<Leave>", lambda e, w=rb: w.config(fg=TEXT))

        # ── FORMAT + QUALITY ROW ──
        opt_frame = tk.Frame(self, bg=BG2, pady=12, padx=16,
                             highlightbackground=BORDER, highlightthickness=1)
        opt_frame.pack(fill="x", padx=20, pady=6)

        left_col = tk.Frame(opt_frame, bg=BG2)
        left_col.pack(side="left", fill="x", expand=True)

        tk.Label(left_col, text="FORMAT", font=FONT_UI,
                 bg=BG2, fg=ACCENT).pack(anchor="w")

        self.fmt_menu = ttk.Combobox(
            left_col, textvariable=self.fmt_var,
            font=FONT_MONO, state="readonly", width=22
        )
        self.fmt_menu.pack(anchor="w", pady=(4, 0))
        self._style_combobox()

        right_col = tk.Frame(opt_frame, bg=BG2)
        right_col.pack(side="right")

        tk.Label(right_col, text="OPTIONS", font=FONT_UI,
                 bg=BG2, fg=ACCENT).pack(anchor="w")

        self.local_cb = tk.Checkbutton(
            right_col, text="Use local yt-dlp.exe",
            variable=self.use_local,
            font=FONT_SM, bg=BG2, fg=TEXT,
            selectcolor=BG3, activebackground=BG2,
            activeforeground=ACCENT,
            highlightthickness=0
        )
        self.local_cb.pack(anchor="w")

        # ── DOWNLOAD BUTTON ──
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(fill="x", padx=20, pady=8)

        self.dl_btn = tk.Button(
            btn_frame, text="⬇  DOWNLOAD",
            font=("Courier New", 13, "bold"),
            bg=ACCENT, fg=BG, relief="flat",
            activebackground="#00b8d4", activeforeground=BG,
            padx=20, pady=10, cursor="hand2",
            command=self._start_download
        )
        self.dl_btn.pack(side="left", fill="x", expand=True)

        upd_btn = tk.Button(
            btn_frame, text="↑ UPDATE",
            font=FONT_UI, bg=BG3, fg=TEXT_DIM,
            relief="flat", padx=14, pady=10,
            activebackground=BORDER, activeforeground=TEXT,
            cursor="hand2", command=self._update_ytdlp
        )
        upd_btn.pack(side="left", padx=(6, 0))

        clr_btn = tk.Button(
            btn_frame, text="✕ CLEAR",
            font=FONT_UI, bg=BG3, fg=TEXT_DIM,
            relief="flat", padx=14, pady=10,
            activebackground=BORDER, activeforeground=RED,
            cursor="hand2", command=self._clear_log
        )
        clr_btn.pack(side="left", padx=(6, 0))

        # ── LOG OUTPUT ──
        self._sep()
        log_label = tk.Frame(self, bg=BG)
        log_label.pack(fill="x", padx=20)
        tk.Label(log_label, text="OUTPUT LOG", font=FONT_SM,
                 bg=BG, fg=TEXT_DIM).pack(side="left")
        self.status_dot = tk.Label(log_label, text="●", font=FONT_SM,
                                   bg=BG, fg=TEXT_DIM)
        self.status_dot.pack(side="right")

        self.log = scrolledtext.ScrolledText(
            self, font=("Courier New", 9), bg=BG2, fg=GREEN,
            relief="flat", state="disabled",
            highlightbackground=BORDER, highlightthickness=1,
            insertbackground=GREEN, wrap="word"
        )
        self.log.pack(fill="both", expand=True, padx=20, pady=(4, 16))

        # tag colors
        self.log.tag_config("info",  foreground=TEXT)
        self.log.tag_config("ok",    foreground=GREEN)
        self.log.tag_config("warn",  foreground=YELLOW)
        self.log.tag_config("err",   foreground=RED)
        self.log.tag_config("dim",   foreground=TEXT_DIM)
        self.log.tag_config("accent",foreground=ACCENT)

        self._log("◈ BOOMER ready. Paste a URL and hit DOWNLOAD.", "accent")
        self._log("Made by Mr. GPT and meowx001", "dim")

    # ───────────────────────────── HELPERS ───────────────────────────────

    def _sep(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=6)

    def _btn(self, parent, text, cmd, bg=BG3, fg=TEXT, side="left"):
        b = tk.Button(parent, text=text, command=cmd, font=FONT_SM,
                      bg=bg, fg=fg, relief="flat", padx=10, pady=4,
                      activebackground=BORDER, cursor="hand2")
        b.pack(side=side)
        return b

    def _style_combobox(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox",
                        fieldbackground=BG3, background=BG3,
                        foreground=TEXT, selectbackground=BG3,
                        selectforeground=ACCENT,
                        bordercolor=BORDER, lightcolor=BG3,
                        darkcolor=BG3, arrowcolor=ACCENT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", BG3)],
                  foreground=[("readonly", TEXT)])

    def _update_formats(self):
        if self.mode.get() == "video":
            opts = ["MP4", "MP4 (1080p)", "WEBM", "WEBM (1080p)", "MKV", "MKV (1080p)"]
        else:
            opts = ["M4A (best audio)", "MP3"]
        self.fmt_menu["values"] = opts
        self.fmt_var.set(opts[0])

    def _paste_url(self):
        try:
            txt = self.clipboard_get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, txt)
        except Exception:
            pass

    def _log(self, msg, tag="info"):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def _set_busy(self, busy: bool):
        self.is_downloading = busy
        if busy:
            self.dl_btn.config(text="⏳ DOWNLOADING…", state="disabled",
                               bg=TEXT_DIM, fg=BG)
            self.status_dot.config(fg=YELLOW)
        else:
            self.dl_btn.config(text="⬇  DOWNLOAD", state="normal",
                               bg=ACCENT, fg=BG)
            self.status_dot.config(fg=TEXT_DIM)

    # ───────────────────────────── COMMANDS ──────────────────────────────

    def _build_cmd(self, url):
        fmt  = self.fmt_var.get()
        mode = self.mode.get()
        output_path = os.path.join(os.getcwd(), "download", "%(title)s.%(ext)s")
        base = f'-o "{output_path}"'

        if mode == "audio":
            if "MP3" in fmt:
                return f'yt-dlp -f bestaudio -x --audio-format mp3 {base} "{url}"'
            else:
                return f'yt-dlp -f bestaudio {base} "{url}"'
        else:
            if fmt == "MP4":
                return f'yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" {base} "{url}"'
            elif fmt == "MP4 (1080p)":
                return f'yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]" {base} "{url}"'
            elif fmt == "WEBM":
                return f'yt-dlp -f "bv*[ext=webm]+ba[ext=webm]/b[ext=webm]" {base} "{url}"'
            elif fmt == "WEBM (1080p)":
                return f'yt-dlp -f "bv*[height<=1080][ext=webm]+ba[ext=webm]/b[height<=1080][ext=webm]" {base} "{url}"'
            elif fmt == "MKV":
                return f'yt-dlp -f "bv+ba/b" --merge-output-format mkv {base} "{url}"'
            elif fmt == "MKV (1080p)":
                return f'yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" --merge-output-format mkv {base} "{url}"'

    def _run_cmd_thread(self, cmd):
        exe = "yt-dlp.exe" if self.use_local.get() else "yt-dlp"
        cmd = cmd.replace("yt-dlp", exe, 1)

        self._log(f"\n$ {cmd}", "dim")
        try:
            proc = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                if "[download]" in line:
                    tag = "ok"
                elif "ERROR" in line or "error" in line.lower():
                    tag = "err"
                elif "WARNING" in line:
                    tag = "warn"
                else:
                    tag = "info"
                self.after(0, self._log, line, tag)

            proc.wait()
            if proc.returncode == 0:
                self.after(0, self._log, "\n✔ Download complete! Saved to ./download/", "ok")
            else:
                self.after(0, self._log, f"\n✘ yt-dlp exited with code {proc.returncode}", "err")
        except Exception as e:
            self.after(0, self._log, f"\n✘ Error: {e}", "err")
        finally:
            self.after(0, self._set_busy, False)

    def _start_download(self):
        if self.is_downloading:
            return
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a URL first.")
            return

        cmd = self._build_cmd(url)
        self._set_busy(True)
        threading.Thread(target=self._run_cmd_thread, args=(cmd,), daemon=True).start()

    def _update_ytdlp(self):
        if self.is_downloading:
            return
        exe = "yt-dlp.exe" if self.use_local.get() else "yt-dlp"
        self._set_busy(True)
        threading.Thread(
            target=self._run_cmd_thread,
            args=(f"{exe} -U",), daemon=True
        ).start()


if __name__ == "__main__":
    app = BBoomer()
    app.mainloop()
