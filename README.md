# VideoGen 🎬

A multi-project animated video generation hub powered by **Remotion**, **Three.js**, **Blender 5.0**, **Google Gemini ("Nano Banana 2")**, procedural DSP audio synthesis, and FFmpeg.

This repository houses multiple self-contained, high-production animation and cinema projects across diverse visual styles: 35mm Indian cinematic realism, Pixar 3D CGI animation, Makoto Shinkai / Studio Ghibli anime, Three.js WebGL solarpunk sci-fi, and stylized comedy.

---

## 📽️ Projects Directory

| # | Project Folder | Title & Description | Visual Style | Tech Stack | Duration | Output | Status |
|---|---|---|---|---|---|---|---|
| **04** | [`shivamogga_kannada_drama_04/`](./shivamogga_kannada_drama_04/) | **ಮಲೆನಾಡ ಹಾದಿ (The Malnad Path)**: A rich emotional Kannada drama set across the Western Ghats of Shivamogga — misty Tunga bridge at dawn, heritage Malnad courtyard, Rangamandira theatrical tension, Jog Falls confrontation, and sacred banyan temple reunion. | **Cinematic Realism (35mm Indian Cinema)** | Gemini Visuals + Indian Classical DSP Audio (Bansuri, Tanpura, Tabla) + FFmpeg | 25.0s | MP4 + GIF | ✅ Complete |
| **05** | [`cute_puppy_spotlight_05/`](./cute_puppy_spotlight_05/) | **Cute Puppy Spotlight**: Heartwarming 3D animation spotlight following a curious golden pup from wicker basket yawns and rainbow bubbles to garden butterfly sprints, autumn leaf slides, and cozy fireplace lullabies. | **Pixar / Disney 3D CGI Animation** | Gemini Visuals + Orchestral Pizzicato & Marimba DSP Audio + FFmpeg | 25.0s | MP4 + GIF | ✅ Complete |
| **06** | [`social_media_screenless_06/`](./social_media_screenless_06/) | **Disconnect to Reconnect (デスコネクト リコネクト)**: An evocative film portraying the suffocating doomscroll cycle and anxiety of screen addiction, followed by the deep liberation of powering off, walking in dew-kissed cedar forests, real friendship, and twilight ocean breezes. | **Makoto Shinkai & Ghibli Anime** | Gemini Visuals + Neo-Classical Piano & Orchestral DSP Audio + FFmpeg | 25.0s | MP4 + GIF | ✅ Complete |
| **03** | [`cosmic_odyssey_03/`](./cosmic_odyssey_03/) | **The Seed of Aurora (Cosmic Odyssey)**: A 1-minute sci-fi odyssey tracking an ancient celestial seed through the deep void, across a kaleidoscopic nebula, into alien atmospheric re-entry, blooming into an eternal solarpunk garden of stars. | **Sci-Fi 3D WebGL & Matte Painting** | Remotion + Three.js + Blender + Gemini Visuals + Procedural Score | 60.0s | MP4 + GIF | ✅ Complete |
| **02** | [`war_action_01/`](./war_action_01/) | **Brothers in Arms — No One Left Behind**: A combat rescue mission through artillery craters, smoke screens, suppressive tank armor, and A-10 close air support to extract a wounded brother onto a MEDEVAC Black Hawk. | **Gritty Military Action** | Gemini Visuals + Dynamic Programming + Procedural Audio + FFmpeg | 30.0s | MP4 + GIF | ✅ Complete |
| **01** | [`nano_banana_comedy_01/`](./nano_banana_comedy_01/) | **The Misadventures of Nano Banana 2.0**: Slapstick comedy animated short following a sentient banana escaping a kitchen fruit bowl, dodging a smoothie blender, and strapping to a bottle rocket. | **Stylized Slapstick Cartoon** | Gemini Visuals + Procedural SFX + FFmpeg | 30.0s | MP4 + GIF | ✅ Complete |

---

## 🎭 Project 04: Shivamogga Kannada Drama — "ಮಲೆನಾಡ ಹಾದಿ"

> *"ತುಂಗಾ ತೀರದ ಮುಂಜಾನೆಯಿಂದ ಜೋಗ ಜಲಪಾತದ ರೌದ್ರ ಗಾಂಭೀರ್ಯದವರೆಗೆ — ನೆನಪುಗಳು, ರಂಗಭೂಮಿ ಹಾಗೂ ಕರುಳಿನ ಬಾಂಧವ್ಯದ ಕಥೆ."*

### Visual Preview
![Shivamogga Drama Preview](./shivamogga_kannada_drama_04/output/shivamogga_kannada_drama_preview.gif)

- **Style**: Photorealistic 35mm Indian Cinematic Drama with rich Malnad regional aesthetics.
- **Key Scenes**: Tunga Bridge at dawn, heritage Thotti Mane courtyard, Rangamandira theatrical clash, Jog Falls mist cascade, sacred temple banyan reunion.
- **Soundtrack**: Raag Bhoopali / Mohanam scale in C# with micro-tonal Bansuri flute, meditative Tanpura, Tala Roopaka Tabla (pitch-bending Bayan bass), and temple bells.

---

## 🐾 Project 05: Cute Puppy Spotlight (Pixar 3D Animation)

> *"A day in the life of the fluffiest golden explorer — curious bubbles, flying ears, and sweet bedtime dreams."*

### Visual Preview
![Puppy Spotlight Preview](./cute_puppy_spotlight_05/output/cute_puppy_spotlight_preview.gif)

- **Style**: Pixar / Disney 3D CGI animation with volumetric lighting, soft subsurface scattering fur, and expressive facial animation.
- **Key Scenes**: Wicker basket yawn, rainbow soap bubble wonder, spring tulip butterfly chase, autumn leaf slide with squeaky ball, cozy fireplace sleep with teddy bear.
- **Soundtrack**: Playful pizzicato strings (170 BPM allegro), marimba/xylophone mallet melodies, procedural puppy yelps/barks, and a warm hearth lullaby.

---

## 🍃 Project 06: Social Media vs Screenless Time — "Disconnect to Reconnect"

> *"When the screen goes dark, the real world begins."*

### Visual Preview
![Screenless Time Preview](./social_media_screenless_06/output/social_media_screenless_preview.gif)

- **Style**: Makoto Shinkai & Studio Ghibli cinematic anime art with dramatic sky gradients, radiant sunbeams, and lush hand-painted nature.
- **Key Scenes**: Dystopian blue doomscroll gloom, tactile power-off moment of resolve, dew-kissed cedar forest awakening, tea and laughter with real friends in a wildflower meadow, twilight ocean cliffside under shooting stars.
- **Soundtrack**: Cold square-wave glitch pings & haptic buzzes transforming abruptly at the power-off click into an emotional acoustic grand piano melody, birdsong, and ocean surf.

---

## 📁 Repository Directory Structure

```
VideoGen/
├── README.md
├── .gitignore
├── shivamogga_kannada_drama_04/    # Project 4: Kannada Drama (Shivamogga / Malnad)
│   ├── README.md
│   ├── scenes/                     # 5 Master 4K keyframe scenes
│   ├── audio/                      # Procedural Indian classical score (.wav)
│   ├── output/                     # Final 25s MP4 video + preview GIF
│   └── scripts/                    # Audio synthesis & Ken Burns compile scripts
├── cute_puppy_spotlight_05/        # Project 5: Cute Puppy Spotlight (Pixar 3D)
│   ├── README.md
│   ├── scenes/                     # 5 Master Pixar 3D keyframe scenes
│   ├── audio/                      # Procedural pizzicato & marimba score (.wav)
│   ├── output/                     # Final 25s MP4 video + preview GIF
│   └── scripts/                    # Audio synthesis & Ken Burns compile scripts
├── social_media_screenless_06/     # Project 6: Disconnect to Reconnect (Anime)
│   ├── README.md
│   ├── scenes/                     # 5 Master Shinkai anime scenes
│   ├── audio/                      # Procedural neo-classical piano score (.wav)
│   ├── output/                     # Final 25s MP4 video + preview GIF
│   └── scripts/                    # Audio synthesis & Ken Burns compile scripts
├── cosmic_odyssey_03/              # Project 3: Remotion + Three.js + Blender
│   ├── README.md
│   └── ...
├── war_action_01/                  # Project 2: Hard-hitting War Action
│   ├── README.md
│   └── ...
└── nano_banana_comedy_01/          # Project 1: Slapstick Comedy
    ├── README.md
    └── ...
```
