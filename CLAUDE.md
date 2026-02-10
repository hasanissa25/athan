# Athan — Islamic Prayer Times App

## What This Is
A Python desktop app that displays the 5 daily Islamic prayer times and plays the Athan (call to prayer) audio. Built as a Mac prototype — will be ported to iPhone later.

**Owner:** Hasan (limited programming background — keep everything simple and beginner-friendly).

## MVP Scope (Phase 1)
Only two features. Nothing else:
1. **Display prayer times** — Show today's 5 prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha) based on the user's location
2. **Play Athan audio** — A play button that plays the Athan audio clip

No automatic scheduling. No notifications. No background features. No settings screen. Just a simple window with times and a play button.

## Audio
- Source: https://youtu.be/EGcdX_L8arE
- Extract using `yt-dlp`: `yt-dlp -x --audio-format mp3 -o "audio/athan.mp3" https://youtu.be/EGcdX_L8arE`
- Install yt-dlp if needed: `brew install yt-dlp`
- Store the audio file at `audio/athan.mp3`

## Tech Stack
- **Language:** Python 3
- **UI:** tkinter (comes built-in with Python — no install needed)
- **Prayer time calculation:** `adhan` Python library (`pip install adhan`)
- **Audio playback:** macOS built-in `afplay` command via subprocess (zero dependencies)
- **Location:** Hardcoded coordinates for now (simplest approach), configurable later
- **IDE:** VS Code

## Project Structure
```
athan/
├── CLAUDE.md
├── requirements.txt       # Python dependencies (just adhan)
├── main.py                # Everything — UI, prayer times, audio playback
└── audio/
    └── athan.mp3          # The Athan audio file
```

## Build & Run
1. `pip install -r requirements.txt`
2. `python main.py`

## Coding Guidelines
- **Keep it minimal.** No abstractions, no design patterns, no over-engineering. Write the simplest code that works.
- **One file.** Keep everything in `main.py` until it gets genuinely unmanageable.
- **No tests yet.** MVP first, tests later.
- **No virtual environments** unless dependency conflicts arise.
- **Comments only where something is non-obvious.**
- **Use subprocess + afplay for audio** — it's the simplest way to play audio on macOS with zero extra dependencies.

## Future Phases (not now)
These are for later. Do NOT build these in Phase 1:
- Automatic Athan playback at prayer times (scheduling)
- Push notifications
- iPhone / iOS support (SwiftUI rewrite)
- Qibla compass
- Multiple Athan audio options
- Prayer time calculation method settings
- Auto-detect location via IP geolocation
- App Store submission
