# Cute Puppy Spotlight 🐾 : 600-Frame Pixar 3D Animation

A 25-second continuous animated short film rendered across **600 individual animation frames** (24 FPS) featuring character animation, dynamic particle physics (floating & popping soap bubbles, fluttering animated butterflies with fairy dust trails, swirling autumn wind vortexes, and crackling fireplace embers), subpixel Ken Burns camera tracking, and procedural orchestral music.

---

## 📽️ Visual Preview
![Puppy Spotlight Preview](./output/cute_puppy_spotlight_preview.gif)

---

## 🎬 10 Continuous Narrative Scenes (60 Frames Each)

| Scene | Frames | Keyframe File | Narrative & Animation Action |
|---|---|---|---|
| **Scene 01** | 001 - 060 | `scenes/scene01_basket_yawn.png` | **Morning Yawn in Sunlit Basket**: Gentle slow camera push-in, floating golden morning dust motes drifting in sunbeams, puppy stretching paws and yawning. |
| **Scene 02** | 061 - 120 | `scenes/scene02_first_clumsy_steps.png` | **First Clumsy Steps — Whoops!**: Playful camera bounce and squash, clumsy paws tumbling over basket rim onto kitchen tile floor with motion dashes. |
| **Scene 03** | 121 - 180 | `scenes/scene03_bubble_wonder.png` | **A Giant Iridescent Bubble Appears**: Head tilt camera motion, 8 procedural translucent soap bubbles floating across the screen with surface tension wobbles and rainbow color cycling. |
| **Scene 04** | 181 - 240 | `scenes/scene04_bubble_pop_surprise.png` | ***POP!* The Surprise on the Nose**: Bubble wobbles on the nose and violently explodes into a splash ring of 32 physical water droplets with gravity arcs and surprise camera snap! |
| **Scene 05** | 241 - 300 | `scenes/scene05_garden_butterfly.png` | **Chasing the Glowing Blue Butterfly**: High-speed camera tracking through tulips, animated blue butterfly flapping wings in a sinusoidal flight path, trailing glowing fairy dust particles. |
| **Scene 06** | 301 - 360 | `scenes/scene06_butterfly_on_nose.png` | **The Butterfly Lands on the Nose!**: Puppy sits frozen in awe, cross-eyed smile as butterfly perches on nose gently fluttering wings, surrounded by twinkling magical sparkles. |
| **Scene 07** | 361 - 420 | `scenes/scene07_autumn_ball.png` | **Rolling the Squeaky Ball through Autumn Leaves**: Squeaky red ball rolling with motion blur, puppy sliding across the ground, kicking up a rooster tail of 25 colorful autumn leaves. |
| **Scene 08** | 421 - 480 | `scenes/scene08_leaf_pile_peekaboo.png` | **Peek-a-Boo! Leaf on the Head**: Spring-loaded bounce popping head out of leaf pile, ears flopping up and down, maple leaf fluttering on head, swirling leaves in a wind vortex. |
| **Scene 09** | 481 - 540 | `scenes/scene09_fireplace_dream.png` | **Cozy Fireplace Snuggle & Teddy Bear**: Intimate slow zoom by glowing stone hearth, warm light pulsing across fur, 30 animated rising embers and fire sparks drifting into the chimney. |
| **Scene 10** | 541 - 600 | `scenes/scene10_dreaming_paws.png` | **Dreaming of Infinite Green Fields**: Dream bubbles floating and pulsing upwards with miniature puppy running silhouettes, twitching paws, heart sparkles, and C-major lullaby strings. |

---

## 🎵 Procedural Soundtrack Design (`scripts/generate_soundtrack.py`)
- **170 BPM Allegro Pizzicato Bass**: Bouncy staccato upright bass line keeping energetic puppy momentum.
- **Marimba & Xylophone Melody**: Bright, rounded mallet percussion playing joyful arpeggios.
- **Procedural Puppy Yips**: Formant synthesized puppy vocalizations tuned to the playful action.
- **Glissando Fairy Bells**: Chimes and glockenspiel sparkling when the magical butterfly appears.
- **Warm Hearth Lullaby**: Gentle C-Major string orchestra and crackling fireplace audio for the cozy bedtime finale.

---

## 🛠️ Video Pipeline (`scripts/render_animation_frames.py` & `scripts/compile_video.py`)
- **Frames**: 600 individual rendered PNG frames (`frames/frame_0001.png` - `frames/frame_0600.png`)
- **Parallel Render**: Multi-core rendering across 16 CPU cores via `multiprocessing.Pool`
- **Output Video**: `output/cute_puppy_spotlight.mp4` (1280x720 Progressive, H.264 CRF 18, 24 FPS, AAC audio)
- **Preview GIF**: `output/cute_puppy_spotlight_preview.gif` (Lanczos palette generation)
