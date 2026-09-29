# Claymation Underwater Odyssey 🐙 : 600-Frame Tactile Stop-Motion Animation

A 25.0-second continuous animated tactile stop-motion short film rendered across **600 individual animation frames** (24 FPS) featuring burned-in coral clay subtitle placards, authentic 12-FPS tactile clay jitter keying, floating physical polymer bubbles with specular sheen, and procedural warm acoustic marimba & ocean bubble pop audio.

---

## 📽️ Visual Preview
![Claymation Underwater Odyssey Preview](./output/claymation_underwater_odyssey_preview.gif)

---

## 🎬 10 Narrative Scenes with Burned-In Subtitles (60 Frames Each)

| Scene | Frames | Keyframe File | Subtitle Speaker & Narrative Script | Visual & Particle VFX |
|---|---|---|---|---|
| **Scene 01** | 001 - 060 | `scenes/scene01_surface_splash.png` | **[NARRATOR]**: *"Meet Barnaby! The tiniest polymer clay dumbo octopus in the whole blue ocean."* | Cotton water ripples, splashing droplet beads, sunny surface glints. |
| **Scene 02** | 061 - 120 | `scenes/scene02_coral_reef.png` | **[BARNABY]**: *"Look at all these colorful corals! And the clownfish are made of orange clay too!"* | Swaying sea anemone tentacles, playful clownfish swimming wiggles. |
| **Scene 03** | 121 - 180 | `scenes/scene03_playful_turtle.png` | **[CRUSH THE TURTLE]**: *"Right on, little dude! High-five your fin to my clay flipper!"* | Gliding sea turtle stroke, seaweed currents, high-five flipper tap. |
| **Scene 04** | 181 - 240 | `scenes/scene04_twilight_descent.png` | **[NARRATOR]**: *"Flapping his tiny ear-fins, Barnaby descends down, down into the deep blue twilight."* | Deepening indigo ocean gradient, floating clay bubble trails, ear-fin flapping. |
| **Scene 05** | 241 - 300 | `scenes/scene05_bioluminescent_jellyfish.png` | **[BARNABY]**: *"Ooh! The glowing jellyfish are throwing a bioluminescent underwater disco party!"* | Pulsing neon translucency, undulating bell umbrellas, floating light spores. |
| **Scene 06** | 301 - 360 | `scenes/scene06_glowing_anglerfish.png` | **[SMILEY THE ANGLERFISH]**: *"Need a little light down here, little friend? My bulb is freshly sculpted!"* | Swinging clay angler lure bulb, friendly toothy grin, deep abyss shadows. |
| **Scene 07** | 361 - 420 | `scenes/scene07_sunken_galleon.png` | **[NARRATOR]**: *"Deep on the sea floor, half-buried in clay sand... an ancient sunken galleon."* | Tactile wood grain texture, sea urchins on hull, slow exploratory crawl. |
| **Scene 08** | 421 - 480 | `scenes/scene08_treasure_chest.png` | **[BARNABY]**: *"A pirate chest! And inside... the most magical glowing pearls in the seven seas!"* | Hinged chest lid squeak, rainbow iridescent pearl radiance, star sparkles. |
| **Scene 09** | 481 - 540 | `scenes/scene09_pearl_dance.png` | **[NARRATOR]**: *"Holding the rainbow pearl high, Barnaby dances with joy with his deep-sea buddies!"* | Swirling celebratory octopus spin, rising bubble spirals, laughing sea creatures. |
| **Scene 10** | 541 - 600 | `scenes/scene10_surface_sunset.png` | **[BARNABY]**: *"Floating home under cotton-candy sunset clouds... What an ocean adventure!"* | Pastel pink sunset water reflection, cotton clouds, sleepy smile finale. |

---

## 🎵 Procedural Acoustic Marimba Soundtrack (`scripts/generate_soundtrack.py`)
- **110 BPM Wooden Marimba Melody**: Warm, tactile wooden mallet strikes playing pentatonic arpeggios.
- **Pizzicato Double Bass**: Bouncy, playful plucked upright bassline.
- **Procedural Bubble Pops**: Resonant ascending frequency sweeps mimicking water bubbles.
- **Crystal Pearl Bells**: Shimmering glockenspiel chimes celebrating the treasure discovery.

---

## 🛠️ Video Pipeline (`scripts/render_animation_frames.py` & `scripts/compile_video.py`)
- **Frames**: 600 individual rendered frames (`frames/frame_0001.jpg` - `frames/frame_0600.jpg`)
- **Multi-Core Render**: Parallel 16-thread processing using PIL and `concurrent.futures`
- **Output Video**: `output/claymation_underwater_odyssey.mp4` (1280x720 Progressive, H.264 CRF 18, 24 FPS, AAC audio)
- **Preview GIF**: `output/claymation_underwater_odyssey_preview.gif` (Lanczos palette generation)
