# VideoGen 🎬

A multi-project animated video generation hub powered by **Google Gemini 3.1 Flash Image ("Nano Banana 2")**, cinematic sound design, procedural dynamics, and FFmpeg.

This directory is designed as a modular workspace for multiple animation and video generation projects.

---

## Projects Directory

| Project Folder | Description | Duration | FPS | Total Frames | Status |
|---|---|---|---|---|---|
| [`nano_banana_comedy_01/`](./nano_banana_comedy_01/) | **The Misadventures of Nano Banana 2.0**: A slapstick comedy animated short following a sentient banana escaping a kitchen fruit bowl, dodging a smoothie blender, outsmarting a hungry chef monkey, strapping to a bottle rocket, and slipping on its own peel. | 30.0s | 20 FPS | 600 Frames | ✅ Complete |
| [`war_action_01/`](./war_action_01/) | **Brothers in Arms — No One Left Behind**: A hard-hitting, impactful cinematic war action film following a desperate combat rescue through artillery craters, smoke screens, suppressive tank armor, and A-10 close air support to extract a wounded brother onto a MEDEVAC Black Hawk into the sunset. | 30.0s | 20 FPS | 600 Individual AI Frames | ✅ Complete |

---

## Project 02: War Action — "No One Left Behind"

### Visual Preview
![War Action Preview](./war_action_01/output/war_action_preview.gif)

### Storyboard Arc
1. **Act 1: The Pinned Brother & The Oath (0-6s | Frames 001-120)**: Wounded soldier clutching dog tags in mud crater; sergeant locks eyes across no-man's land and deploys smoke canisters.
2. **Act 2: The Sprint into Crossfire (6-12s | Frames 121-240)**: Full-speed sprint into enemy machine-gun fire; sniper sparks ricochet; mortar concussions.
3. **Act 3: Suppressive Fire & Reaching the Brother (12-18s | Frames 241-360)**: Friendly M1 Abrams 120mm tank cannon obliterates enemy bunker; sergeant reaches crater: *"I told you I was coming back for you."*
4. **Act 4: Fireman's Carry & A-10 CAS (18-24s | Frames 361-480)**: Field tourniquet applied; brother carried on shoulders; A-10 Warthog unleashes 30mm Avenger rotary cannon defensive wall of fire.
5. **Act 5: MEDEVAC Dust-off & Brotherhood (24-30s | Frames 481-600)**: Black Hawk touchdown in green smoke; suppressive minigun fire; flares blooming in dusk; the two brothers clasp hands inside cabin: *No one left behind.*

---

## Project 01: Nano Banana 2 Slapstick Comedy

### Storyboard Arc
1. **The Awakening (0-3s)**: Nano Banana 2.0 dons 8-bit sunglasses and flexes in the fruit bowl.
2. **Fruit Bowl Parkour (3-6s)**: Toothpick pole vault over apples and oranges.
3. **The Blender of Doom (6-9s)**: Looney-Tunes panic as the blender roars.
4. **Tactical Counter Slide (9-12s)**: Action slide under spinning blades.
5. **Hungry Chef Monkey Ambush (12-15s)**: Peel drop defense.
6. **The 720° Monkey Wipeout (15-18s)**: Monkey spins and faceplants in whipped cream.
7. **Supercharged Potassium (18-21s)**: USB fast charging electric aura.
8. **NANO-X Bottle Rocket Launch (21-24s)**: Skylight rocket launch.
9. **Zero-G Cosmic Disco (24-27s)**: Space disco over planet Earth.
10. **The Ultimate Splat (27-30s)**: Superhero landing slips on own peel!

---

## Directory Structure

```
VideoGen/
├── README.md
├── .gitignore
├── nano_banana_comedy_01/          # Project 1: Slapstick Comedy
│   ├── README.md
│   ├── keyframes/
│   ├── frames/                     # 600 frames
│   ├── audio/
│   ├── output/
│   └── scripts/
└── war_action_01/                  # Project 2: Hard-hitting War Action
    ├── README.md
    ├── frames/                     # 600 individual AI images (frame_0001.jpg - frame_0600.jpg)
    ├── audio/                      # 30-second synthesized war trailer soundtrack
    │   └── war_action_soundtrack.wav
    ├── output/                     # Final media
    │   ├── war_action_hardhitting.mp4  # 30s @ 20 FPS H.264 + AAC
    │   └── war_action_preview.gif     # Animated GIF preview
    └── scripts/
        ├── generate_war_600_frames.py # Generates 600 AI frames via Gemini 3.1 Flash Image
        ├── generate_war_soundtrack.py # Synthesizes 30s war trailer score & sound design
        ├── compile_war_video.py       # FFmpeg compilation pipeline
        └── optimize_war_frames.py     # Optimizes JPEG compression for git
```
