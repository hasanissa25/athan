import tkinter as tk
from tkinter import ttk
import subprocess
import os
import time as time_mod
from datetime import date, datetime
from adhan.adhan import adhan
from adhan.methods import ISNA, ASR_STANDARD

# --- Config ---
LATITUDE = 45.4215    # Ottawa, ON — change to your city
LONGITUDE = -75.6972
AUDIO_FILE = os.path.join(os.path.dirname(__file__), "audio", "athan.mp3")
AUDIO_DURATION = 251  # seconds (4:11)

# --- Prayer time calculation ---
def get_prayer_times():
    tz_offset = -time_mod.timezone / 3600
    if time_mod.daylight and time_mod.localtime().tm_isdst:
        tz_offset = -time_mod.altzone / 3600

    params = {**ISNA, **ASR_STANDARD}
    times = adhan(date.today(), (LATITUDE, LONGITUDE), params, timezone_offset=tz_offset)

    # Return only the 5 daily prayers (skip shuruq/sunrise)
    return {
        "Fajr": times["fajr"],
        "Dhuhr": times["zuhr"],
        "Asr": times["asr"],
        "Maghrib": times["maghrib"],
        "Isha": times["isha"],
    }

# --- Audio playback ---
audio_process = None
audio_start_time = None

def play_athan():
    global audio_process, audio_start_time
    if audio_process and audio_process.poll() is None:
        # Already playing — stop it
        audio_process.terminate()
        audio_process = None
        audio_start_time = None
        play_btn.config(text="▶  Play Athan")
        progress_bar["value"] = 0
        time_label.config(text="")
    else:
        audio_process = subprocess.Popen(["afplay", AUDIO_FILE])
        audio_start_time = time_mod.time()
        play_btn.config(text="⏹  Stop Athan")
        update_progress()

def update_progress():
    if audio_process and audio_process.poll() is None and audio_start_time:
        elapsed = time_mod.time() - audio_start_time
        progress_bar["value"] = min(elapsed / AUDIO_DURATION * 100, 100)
        mins_elapsed = int(elapsed) // 60
        secs_elapsed = int(elapsed) % 60
        mins_total = AUDIO_DURATION // 60
        secs_total = AUDIO_DURATION % 60
        time_label.config(text=f"{mins_elapsed}:{secs_elapsed:02d} / {mins_total}:{secs_total:02d}")
        root.after(500, update_progress)
    else:
        # Audio finished
        progress_bar["value"] = 0
        time_label.config(text="")
        play_btn.config(text="▶  Play Athan")

# --- Auto-play scheduler ---
# Tracks which prayers have already been announced today
announced_today = set()

def check_prayer_times():
    now = datetime.now()
    for prayer, prayer_dt in prayer_times.items():
        # Trigger if we're within 60 seconds of the prayer time and haven't announced yet
        diff = (now - prayer_dt).total_seconds()
        if 0 <= diff <= 60 and prayer not in announced_today:
            announced_today.add(prayer)
            # Highlight the active prayer row
            if prayer in row_labels:
                row_labels[prayer].config(bg="#4ecca3", fg="#1a1a2e")
            # Auto-play the athan
            play_athan()

    # Check every 10 seconds
    root.after(10000, check_prayer_times)

# --- UI ---
root = tk.Tk()
root.title("Athan")
root.configure(bg="#1a1a2e")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Prayer Times", font=("Helvetica", 24, "bold"),
                 fg="#e0e0e0", bg="#1a1a2e", pady=15)
title.pack()

# Date
date_label = tk.Label(root, text=date.today().strftime("%A, %B %d, %Y"),
                      font=("Helvetica", 13), fg="#888888", bg="#1a1a2e")
date_label.pack()

# Prayer times
prayer_times = get_prayer_times()
frame = tk.Frame(root, bg="#1a1a2e", padx=40, pady=20)
frame.pack()

row_labels = {}
for prayer, prayer_dt in prayer_times.items():
    row = tk.Frame(frame, bg="#16213e", padx=20, pady=10)
    row.pack(fill="x", pady=4)

    name_label = tk.Label(row, text=prayer, font=("Helvetica", 16),
                          fg="#e0e0e0", bg="#16213e", anchor="w", width=10)
    name_label.pack(side="left")
    tk.Label(row, text=prayer_dt.strftime("%I:%M %p"), font=("Helvetica", 16, "bold"),
             fg="#4ecca3", bg="#16213e", anchor="e", width=10).pack(side="right")
    row_labels[prayer] = name_label

# Status label
status_label = tk.Label(root, text="Auto-athan is ON — will play at each prayer time",
                        font=("Helvetica", 11), fg="#4ecca3", bg="#1a1a2e")
status_label.pack()

# Progress bar
style = ttk.Style()
style.theme_use("default")
style.configure("Athan.Horizontal.TProgressbar", troughcolor="#16213e",
                background="#4ecca3", thickness=8)
progress_bar = ttk.Progressbar(root, style="Athan.Horizontal.TProgressbar",
                               length=280, mode="determinate", maximum=100)
progress_bar.pack(padx=40, pady=(10, 0))

time_label = tk.Label(root, text="", font=("Helvetica", 11), fg="#888888", bg="#1a1a2e")
time_label.pack()

# Play button
play_btn = tk.Button(root, text="▶  Play Athan", font=("Helvetica", 16, "bold"),
                     fg="#1a1a2e", bg="#4ecca3", activebackground="#3ba88a",
                     activeforeground="#1a1a2e", relief="flat", padx=30, pady=10,
                     command=play_athan)
play_btn.pack(pady=20)

# Center window on screen
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"+{x}+{y}")

# Start the auto-play scheduler
check_prayer_times()

root.mainloop()
