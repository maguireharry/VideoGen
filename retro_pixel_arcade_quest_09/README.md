# Retro Pixel Arcade Quest 🕹️ : 600-Frame 16-Bit SNES Animated Suite

A 25.0-second continuous animated 16-bit arcade fantasy RPG suite rendered across **600 individual animation frames** (24 FPS) featuring classic SNES blue dialogue box subtitles with blinking cursors, CRT curved shadow-mask scanlines, screen-shake combat impact feedback, floating pixel mana sparks, and authentic multi-channel chiptune synthesis.

---

## 📽️ Visual Preview
![Retro Pixel Arcade Quest Preview](./output/retro_pixel_arcade_quest_preview.gif)

---

## 🎬 10 Narrative Scenes with Burned-In Subtitles (60 Frames Each)

| Scene | Frames | Keyframe File | Subtitle Speaker & Narrative Script | Visual & Particle VFX |
|---|---|---|---|---|
| **Scene 01** | 001 - 060 | `scenes/scene01_title_boot.png` | **[SYSTEM // BOOT]**: *"Insert coin to awaken the legendary Chrono Knight in the 16-bit realm!"* | CRT scanline glow, blinking "INSERT COIN", retro pixel title marquee. |
| **Scene 02** | 061 - 120 | `scenes/scene02_dungeon_awaken.png` | **[CHRONO KNIGHT]**: *"Ugh... Where am I? The Forgotten Byte Crypt... My blade is gone!"* | Flickering torchlight pixels, eerie blue dungeon mist, stone dungeon walls. |
| **Scene 03** | 121 - 180 | `scenes/scene03_sword_draw.png` | **[ITEM DISCOVERED]**: *"Found the Legendary Glitch Slayer Broadsword! Attack Power +999!"* | Radiant pixel light pillar, golden star sparkles, triumphant sword raise. |
| **Scene 04** | 181 - 240 | `scenes/scene04_pixel_monsters.png` | **[BATTLE ENGAGED]**: *"Wild Corrupted Slimes and Shadow Bats appeared! Select command: ATTACK!"* | Turn-based RPG combat layout, enemy idle bob animations, active battle timers. |
| **Scene 05** | 241 - 300 | `scenes/scene05_combo_slash.png` | **[COMBO STRIKE]**: *"Critical hit! 3-hit combo slash! 9,999 damage dealt to front row!"* | Screen-shake shudder impact, glowing neon arc slashes, floating damage numbers. |
| **Scene 06** | 301 - 360 | `scenes/scene06_lava_bridge.png` | **[STAGE WARNING]**: *"Stage 4 Foundry: Watch your step over the 8-bit boiling lava bridge!"* | Molten lava bubble pops, heat shimmer distortion, crumbling stone bridge. |
| **Scene 07** | 361 - 420 | `scenes/scene07_boss_chamber.png` | **[BOSS ENCOUNTER]**: *"DANGER! Cyber Glitch Titan awakens! HP: [====================]"* | Imposing mech-boss eye glow, flashing boss warning siren, energy shields. |
| **Scene 08** | 421 - 480 | `scenes/scene08_limit_break.png` | **[LIMIT BREAK]**: *"ULTIMATE ATTACK: CHRONO SLICE! Pixel energy blast cuts through reality!"* | Rainbow screen flash, massive charging laser beam particles, reality shatter. |
| **Scene 09** | 481 - 540 | `scenes/scene09_boss_explode.png` | **[STAGE CLEAR]**: *"BOSS DEFEATED! 100,000 XP gained! All stats maxed out! LEVEL UP!"* | Multi-point pixel fireworks explosion, cascading coin showers, victory stance. |
| **Scene 10** | 541 - 600 | `scenes/scene10_arcade_portal.png` | **[ARCADE PORTAL]**: *"Stepping through the CRT dimension... High score etched into eternity!"* | Spiraling dimensional warp portal, glowing exit corridor, "YOU WIN" fanfare. |

---

## 🎵 Procedural 16-Bit Chiptune Soundtrack (`scripts/generate_soundtrack.py`)
- **140 BPM Heroic Arcade Progression**: High-energy driving fantasy battle theme.
- **Pulse-Width Square Leads**: Variable duty cycles (12.5%, 25%, 50%) for authentic retro bite.
- **Triangle Wave Sub-Bass**: Punchy, rounded basslines emulating the Ricoh 2A03 / SNES SPC700.
- **White-Noise Drum Kit**: 8-bit synthetic kicks, snare pops, and closed hi-hat ticks.
- **Jingle Sound Effects**: Limit-break pitch sweep and iconic coin collection fanfares.

---

## 🛠️ Video Pipeline (`scripts/render_animation_frames.py` & `scripts/compile_video.py`)
- **Frames**: 600 individual rendered frames (`frames/frame_0001.jpg` - `frames/frame_0600.jpg`)
- **Multi-Core Render**: Parallel 16-thread processing using PIL and `concurrent.futures`
- **Output Video**: `output/retro_pixel_arcade_quest.mp4` (1280x720 Progressive, H.264 CRF 18, 24 FPS, AAC audio)
- **Preview GIF**: `output/retro_pixel_arcade_quest_preview.gif` (Lanczos palette generation)
