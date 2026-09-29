# Cyberpunk Neon Detective 🌆 : 600-Frame Neo-Noir Animated Suite

A 25.0-second continuous animated neo-noir cyberpunk suite rendered across **600 individual animation frames** (24 FPS) featuring burned-in cybernetic HUD subtitles, physical multi-layer falling neon rain, holographic scanning grids, CRT scanlines, and custom procedural analog synthwave audio.

---

## 📽️ Visual Preview
![Cyberpunk Neon Detective Preview](./output/cyberpunk_neon_detective_preview.gif)

---

## 🎬 10 Narrative Scenes with Burned-In Subtitles (60 Frames Each)

| Scene | Frames | Keyframe File | Subtitle Speaker & Narrative Script | Visual & Particle VFX |
|---|---|---|---|---|
| **Scene 01** | 001 - 060 | `scenes/scene01_monsoon_alley.png` | **[JAXON // DECKER-09]**: *"Midnight in Sector 4. The rain never washes the neon away."* | Torrential neon rain streaks, reflecting puddle ripples, slow dolly push-in. |
| **Scene 02** | 061 - 120 | `scenes/scene02_holographic_clue.png` | **[HUD ANALYSIS]**: *"Fragmented neural imprint detected... Encrypted bio-chip signature."* | Hologram flicker pulse, floating cybernetic UI wireframes, lens flare. |
| **Scene 03** | 121 - 180 | `scenes/scene03_flying_hover_traffic.png` | **[JAXON // DECKER-09]**: *"Traffic control won't track the spinner into the lower smog levels."* | Speed trails of flying hovercars, industrial fog billowing between skyscrapers. |
| **Scene 04** | 181 - 240 | `scenes/scene04_noodle_bar_informant.png` | **[INFORMANT // VEX]**: *"They scrubbed the mainframe, Jaxon. The ghost protocol is active."* | Steam rising from noodle bowls, flickering Japanese neon kanji signs. |
| **Scene 05** | 241 - 300 | `scenes/scene05_subway_chase.png` | **[SYSTEM ALERT]**: *"Hostile intercept in Sector 7 Transit! High-speed maglev pursuit engaged."* | Rapid camera tracking, high-speed tunnel light strobes, spark arcs on rails. |
| **Scene 06** | 301 - 360 | `scenes/scene06_rooftop_overlook.png` | **[JAXON // DECKER-09]**: *"From up here, the city looks alive... but it’s just circuits and ghosts."* | Panoramic city skyline pan, searchlight beams sweeping through cloud deck. |
| **Scene 07** | 361 - 420 | `scenes/scene07_quantum_server_vault.png` | **[AI CORE // NEXUS]**: *"Intrusion detected in Quantum Vault. Accessing neural archives..."* | Pulsing neon laser security grid, server bank LED cascades, cyber data stream. |
| **Scene 08** | 421 - 480 | `scenes/scene08_cyber_confrontation.png` | **[CYBER SYNDICATE]**: *"You should have stayed in the shadows, detective. Delete him."* | Heavy weapon plasma discharge sparks, muzzle flash glow, dramatic shadow silhouettes. |
| **Scene 09** | 481 - 540 | `scenes/scene09_memory_extracted.png` | **[SYSTEM OVERRIDE]**: *"Memory extraction complete. The truth is copied to decentralized ledger."* | Glowing neural data tendrils flowing into bio-chip, digital glitch pixelation. |
| **Scene 10** | 541 - 600 | `scenes/scene10_neon_dawn.png` | **[JAXON // DECKER-09]**: *"The sun never truly rises here... but the truth finally did."* | Warm amber and purple sunrise over smog sea, trenchcoat silhouette, resolving neon glow. |

---

## 🎵 Procedural Synthwave Soundtrack Design (`scripts/generate_soundtrack.py`)
- **120 BPM Analog Sawtooth Bass**: Driving syncopated 16th-note synth bass in C-minor.
- **Vangelis CS-80 Lead Synth**: Expressive detuned analog brass leads with pitch vibrato.
- **Procedural Rain & Urban Rumble**: Filtered brown-noise rain wash and low 38Hz subway rumbles.
- **Cybernetic Sound Effects**: Police scanner blips, high-frequency arpeggios, and distant siren echoes.

---

## 🛠️ Video Pipeline (`scripts/render_animation_frames.py` & `scripts/compile_video.py`)
- **Frames**: 600 individual rendered frames (`frames/frame_0001.jpg` - `frames/frame_0600.jpg`)
- **Multi-Core Render**: Parallel 16-thread processing using PIL and `concurrent.futures`
- **Output Video**: `output/cyberpunk_neon_detective.mp4` (1280x720 Progressive, H.264 CRF 18, 24 FPS, AAC audio)
- **Preview GIF**: `output/cyberpunk_neon_detective_preview.gif` (Lanczos palette generation)
