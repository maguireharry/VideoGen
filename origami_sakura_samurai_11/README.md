# Origami Sakura Samurai 🌸 : 600-Frame Washi & Ukiyo-e Animated Suite

A 25.0-second continuous animated Japanese woodblock and washi paper art film rendered across **600 individual animation frames** (24 FPS) featuring burned-in Japanese calligraphic scroll subtitles with red seal stamps, drifting sakura cherry blossom petals, sumi-e ink wash dispersion, and procedural traditional Koto, Shakuhachi, and Taiko drum music.

---

## 📽️ Visual Preview
![Origami Sakura Samurai Preview](./output/origami_sakura_samurai_preview.gif)

---

## 🎬 10 Narrative Scenes with Burned-In Subtitles (60 Frames Each)

| Scene | Frames | Keyframe File | Subtitle Speaker & Narrative Script | Visual & Particle VFX |
|---|---|---|---|---|
| **Scene 01** | 001 - 060 | `scenes/scene01_folded_crane.png` | **[HAIKU CHRONICLE]**: *"Folded wings take flight / Morning mist upon bamboo / Dawn of cherry blossoms."* | Washi crane wing flaps, misty bamboo stalks, morning fog tilt. |
| **Scene 02** | 061 - 120 | `scenes/scene02_bamboo_bridge.png` | **[KENSHIN // ORIGAMI RONIN]**: *"A warrior's soul is like folded washi paper: humble, yet unbreakable."* | Gentle koi pond ripple reflections, willow branch sway, warrior stance. |
| **Scene 03** | 121 - 180 | `scenes/scene03_storm_petals.png` | **[HAIKU CHRONICLE]**: *"Sudden mountain gale / A thousand pink petals swirl / Fate calls from the storm."* | Swirling sakura petal blizzard vortex, calligraphic rice paper sheets in wind. |
| **Scene 04** | 181 - 240 | `scenes/scene04_ink_dragon.png` | **[SHADOW DRAGON]**: *"From spilled calligraphy ink I rise... Darkness shall stain this peaceful land!"* | Coiling sumi-e black ink tendrils, glowing amber eyes, splash dispersion. |
| **Scene 05** | 241 - 300 | `scenes/scene05_draw_katana.png` | **[KENSHIN // ORIGAMI RONIN]**: *"Silver foil katana unsheathed... Guided by honor, purified by the wind."* | Shimmering blade edge glint, crisp fold highlights, combat focus zoom. |
| **Scene 06** | 301 - 360 | `scenes/scene06_blossom_clash.png` | **[CLASH OF BLADES]**: *"Folded steel meets ancient shadow! A shower of ink splatters across the scroll!"* | Mid-air clash impact, exploding sumi-e ink droplets, flying paper fragments. |
| **Scene 07** | 361 - 420 | `scenes/scene07_crane_flock.png` | **[KENSHIN // ORIGAMI RONIN]**: *"Secret Art: Flock of a Thousand Sacred Paper Cranes, arise!"* | Spiraling double-helix vortex of glowing golden and white paper cranes. |
| **Scene 08** | 421 - 480 | `scenes/scene08_dragon_dissolve.png` | **[HARMONY RESTORED]**: *"The ink darkness dissolves peacefully... Returning to petals and gold leaf upon the lake."* | Ink dissipation into swirling pink petals, gold leaf flakes drifting across lake. |
| **Scene 09** | 481 - 540 | `scenes/scene09_sheath_blade.png` | **[KENSHIN // ORIGAMI RONIN]**: *"The blade is sheathed with reverence. Mount Fuji stands watch over the quiet morning."* | Katana sheath click, morning sun rising behind Mount Fuji, red torii gate. |
| **Scene 10** | 541 - 600 | `scenes/scene10_eternal_harmony.png` | **[HAIKU CHRONICLE]**: *"Floating lanterns glow / Paper cranes reach the heavens / Peace forever folds."* | Panoramic Mount Fuji landscape, floating river lanterns, soaring crane flock. |

---

## 🎵 Procedural Japanese Traditional Soundtrack (`scripts/generate_soundtrack.py`)
- **13-String Koto in Insen Scale**: Authentic Japanese pentatonic melody plucks with expressive finger bends.
- **Shakuhachi Bamboo Flute**: Microtonal ornamentation with airy breath overblows.
- **Thunderous Taiko Drums**: Resonant 55Hz bass impacts punctuating action beats.
- **Hyoshigi Wooden Clappers**: Crisp Kabuki wooden clapper strikes marking dramatic scene turns.

---

## 🛠️ Video Pipeline (`scripts/render_animation_frames.py` & `scripts/compile_video.py`)
- **Frames**: 600 individual rendered frames (`frames/frame_0001.jpg` - `frames/frame_0600.jpg`)
- **Multi-Core Render**: Parallel 16-thread processing using PIL and `concurrent.futures`
- **Output Video**: `output/origami_sakura_samurai.mp4` (1280x720 Progressive, H.264 CRF 18, 24 FPS, AAC audio)
- **Preview GIF**: `output/origami_sakura_samurai_preview.gif` (Lanczos palette generation)
