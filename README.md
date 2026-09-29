# VideoGen 🎬🍌

A multi-project animated video generation hub powered by **Google Gemini 3.1 Flash Image ("Nano Banana 2")**, procedural cartoon dynamics, and FFmpeg.

This directory is designed as a modular workspace for multiple animation and video generation projects.

---

## Projects Directory

| Project Folder | Description | Duration | FPS | Total Frames | Status |
|---|---|---|---|---|---|
| [`nano_banana_comedy_01/`](./nano_banana_comedy_01/) | **The Misadventures of Nano Banana 2.0**: A slapstick comedy animated short following a sentient banana escaping a kitchen fruit bowl, dodging a terrifying smoothie blender, outsmarting a hungry chef monkey, strapping to a model rocket into orbit, and slipping on its own peel. | 30.0s | 20 FPS | 600 Frames | ✅ Complete |

---

## Project 01: Nano Banana 2 Slapstick Comedy

### Storyboard & Scene Breakdown

1. **0:00 - 0:03 (Frames 001 - 060)**: *The Awakening* — Nano Banana 2.0 wakes up inside the fruit bowl, dons 8-bit shades, and flexes peel biceps.
2. **0:03 - 0:06 (Frames 061 - 120)**: *Fruit Bowl Parkour* — Toothpick pole vault over grumpy apples and oranges.
3. **0:06 - 0:09 (Frames 121 - 180)**: *The Blender of Doom* — Kitchen blender whirs to life; classic Looney-Tunes panic!
4. **0:09 - 0:12 (Frames 181 - 240)**: *Tactical Counter Slide* — Action movie slide under the whirring blades with a cheeky wink.
5. **0:12 - 0:15 (Frames 241 - 300)**: *Hungry Chef Monkey Ambush* — Monkey stalks with fork and knife; tactical banana peel traps deployed!
6. **0:15 - 0:18 (Frames 301 - 360)**: *The 720° Monkey Wipeout* — Monkey slips, spins mid-air, and crashes head-first into whipped cream!
7. **0:18 - 0:21 (Frames 361 - 420)**: *Supercharged Potassium* — Stem plugged into USB charger: over 9000mg potassium electric aura!
8. **0:21 - 0:24 (Frames 421 - 480)**: *NANO-X Bottle Rocket Launch* — Blasting through the kitchen skylight into the clouds!
9. **0:24 - 0:27 (Frames 481 - 540)**: *Zero-G Cosmic Disco* — Grooving in low-Earth orbit surrounded by twinkling stars.
10. **0:27 - 0:30 (Frames 541 - 600)**: *The Ultimate Irony & Splat* — Hero landing attempt thwarted by slipping on its own peel! Comic splat & dizzy stars!

---

## Directory Structure

```
VideoGen/
├── README.md
├── .gitignore
└── nano_banana_comedy_01/
    ├── README.md
    ├── keyframes/               # 10 core AI master scenes from Nano Banana 2
    ├── frames/                  # All 600 distinct 20fps animation frames (frame_0001.png - frame_0600.png)
    ├── audio/                   # 30-second synthesized slapstick cartoon soundtrack
    │   └── slapstick_sfx_track.wav
    ├── output/                  # Final compiled media
    │   ├── nano_banana_2_comedy.mp4     # 30s 20fps 720p HD H.264 + AAC
    │   └── nano_banana_2_preview.gif    # Animated GIF preview
    └── scripts/
        ├── generate_banana_keyframes.py # Calls Gemini 3.1 Flash Image API
        ├── render_animation_frames.py   # Renders 600 frames using 16-core parallel engine
        ├── generate_slapstick_audio.py  # Synthesizes bouncy cartoon sound effects and music
        ├── compile_video.py             # FFmpeg compilation pipeline
        └── optimize_frames.py           # Adaptive palette compression for Git
```

---

## Quick Start & Reproduction

To re-render or build additional animations:

```bash
# 1. Generate keyframes using Nano Banana 2 (Gemini 3.1 Flash Image)
python3 nano_banana_comedy_01/scripts/generate_banana_keyframes.py

# 2. Render all 600 animation frames (multithreaded)
python3 nano_banana_comedy_01/scripts/render_animation_frames.py

# 3. Synthesize the slapstick audio track
python3 nano_banana_comedy_01/scripts/generate_slapstick_audio.py

# 4. Compile video with FFmpeg
python3 nano_banana_comedy_01/scripts/compile_video.py
```
