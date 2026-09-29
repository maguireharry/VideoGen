# Disconnect to Reconnect : デスコネクトとリコネクト 🍃
*(The Downsides of Social Media & The Beauty of Screenless Time)*

A 25-second cinematic anime short film created in the **Makoto Shinkai & Studio Ghibli** aesthetic, illustrating the journey from digital doomscroll anxiety to the profound peace of the real world.

---

## 📽️ Visual Preview
![Screenless Time Preview](./output/social_media_screenless_preview.gif)

---

## 🎬 Narrative Acts

| Act | Scene | Visual Setting | Narrative Beat |
|---|---|---|---|
| **Act I** | `scenes/scene1_digital_doomscroll.png` | Dark bedroom illuminated solely by harsh blue smartphone glare, red alert badges | **終わりのないスクロール (The Infinite Doomscroll)**: Anxiety, eye fatigue, notifications inundating the mind in isolation |
| **Act II** | `scenes/scene2_powering_off.png` | Sunlit student desk, smartphone turning black, eyes closed in calm resolve | **電源を切る決意 (The Choice to Power Off)**: Setting the phone face-down, releasing digital pressure, inhaling the morning sunrise |
| **Act III** | `scenes/scene3_forest_sunlight.png` | Ancient moss-covered cedar forest, golden sunbeams piercing morning mist | **生きている森の呼吸 (Awakening in the Living Forest)**: Walking barefoot on cool moss, dandelions drifting, touching living nature |
| **Act IV** | `scenes/scene4_real_connection.png` | Wildflower meadow bench, bicycles leaning on fence, open sketchbook | **本物の繋がりと笑顔 (Genuine Human Presence)**: Real friends toasting hot ceramic tea mugs, unhurried laughter and heartfelt companionship |
| **Act V** | `scenes/scene5_ocean_sunset.png` | Cliffside at purple twilight overlooking shimmering ocean, shooting star | **デスコネクトとリコネクト (Disconnect to Reconnect)**: True stillness under infinite stars, breathing the evening sea breeze |

---

## 🎵 Procedural Soundtrack Design (`scripts/generate_soundtrack.py`)
- **Dystopian Glitch & Digital Alarm (0:00 - 0:05)**: Cold square-wave alert pings (1,200 - 1,800 Hz), dissonant minor second drone (220 Hz & 233 Hz), and tactile haptic motor buzzes.
- **Power Off Tactile Click (0:05)**: Sudden silence as the phone shuts down, punctuated by a tactile switch click.
- **Neo-Classical Shinkai Grand Piano (0:06 - 0:25)**: Rich acoustic piano melody (C, E, G, A, B, D) transitioning into Joe Hisaishi / Tenmon inspired emotive phrasing.
- **Organic Field Foley**: Crisp morning forest birdsong warbles and gentle shore ocean wave swells.
- **Soaring Anime Strings**: Expansive string orchestra chord pads lifting the emotional release in Acts IV and V.

---

## 🛠️ Video Pipeline (`scripts/compile_video.py`)
- **Resolution**: 1280x720 Progressive (16:9 Widescreen) @ 25 FPS
- **Cinematography**: Custom Ken Burns camera moves emphasizing environmental atmosphere, canopy sunbeams, and the horizon.
- **Transitions**: 15-frame optical cross-dissolves between scenes.
- **Typography**: Dual-script Japanese Kanji/Katakana and English subtitles with subtle letterboxing and deep blue cinematic tones.
- **Audio Codec**: AAC stereo @ 192 kbps.
