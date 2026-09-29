import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor

WIDTH = 1280
HEIGHT = 720
TOTAL_FRAMES = 600
FRAMES_PER_SCENE = 60
FPS = 24

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCENES_DIR = os.path.join(BASE_DIR, "scenes")
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

SCENE_FILES = [
    "scene01_surface_splash.png",
    "scene02_coral_reef.png",
    "scene03_playful_turtle.png",
    "scene04_twilight_descent.png",
    "scene05_bioluminescent_jellyfish.png",
    "scene06_glowing_anglerfish.png",
    "scene07_sunken_galleon.png",
    "scene08_treasure_chest.png",
    "scene09_pearl_dance.png",
    "scene10_surface_sunset.png"
]

SUBTITLES = [
    ("[NARRATOR]", "Meet Barnaby! The tiniest polymer clay dumbo octopus in the whole blue ocean."),
    ("[BARNABY]", "Look at all these colorful corals! And the clownfish are made of orange clay too!"),
    ("[CRUSH THE TURTLE]", "Right on, little dude! High-five your fin to my clay flipper!"),
    ("[NARRATOR]", "Flapping his tiny ear-fins, Barnaby descends down, down into the deep blue twilight."),
    ("[BARNABY]", "Ooh! The glowing jellyfish are throwing a bioluminescent underwater disco party!"),
    ("[SMILEY THE ANGLERFISH]", "Need a little light down here, little friend? My bulb is freshly sculpted!"),
    ("[NARRATOR]", "Deep on the sea floor, half-buried in clay sand... an ancient sunken galleon."),
    ("[BARNABY]", "A pirate chest! And inside... the most magical glowing pearls in the seven seas!"),
    ("[NARRATOR]", "Holding the rainbow pearl high, Barnaby dances with joy with his deep-sea buddies!"),
    ("[BARNABY]", "Floating home under cotton-candy sunset clouds... What an ocean adventure!")
]

# Preload scenes
loaded_scenes = []
for sf in SCENE_FILES:
    p = os.path.join(SCENES_DIR, sf)
    img = Image.open(p).convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    loaded_scenes.append(img)

try:
    font_tag = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 17)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 22)
    font_hud = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 15)
except Exception:
    font_tag = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_hud = ImageFont.load_default()

# Pre-generate tactile clay bubbles
random.seed(5555)
CLAY_BUBBLES = []
for _ in range(45):
    CLAY_BUBBLES.append({
        'x': random.uniform(50, WIDTH - 50),
        'y': random.uniform(0, HEIGHT),
        'r': random.uniform(10, 26),
        'speed_y': random.uniform(1.8, 3.8),
        'wobble_f': random.uniform(2.5, 4.5),
        'hue': random.choice([(180, 240, 255), (255, 210, 240), (200, 255, 230)])
    })

def render_frame_task(frame_idx):
    scene_idx = min(frame_idx // FRAMES_PER_SCENE, 9)
    scene_f = frame_idx % FRAMES_PER_SCENE
    t = scene_f / float(FRAMES_PER_SCENE)

    curr_img = loaded_scenes[scene_idx]
    next_idx = min(scene_idx + 1, 9)
    next_img = loaded_scenes[next_idx]

    # Stop-motion tactile step (simulates 12fps stop-motion keying on 24fps timeline)
    stop_motion_step = (frame_idx // 2) * 2
    jitter_x = int(math.sin(stop_motion_step * 1.7) * 2)
    jitter_y = int(math.cos(stop_motion_step * 2.3) * 2)

    zoom = 1.0 + 0.04 * math.sin(t * math.pi)
    zw = int(WIDTH * zoom)
    zh = int(HEIGHT * zoom)
    scaled = curr_img.resize((zw, zh), Image.Resampling.BILINEAR)
    crop_x = max(0, min(zw - WIDTH, (zw - WIDTH) // 2 + jitter_x))
    crop_y = max(0, min(zh - HEIGHT, (zh - HEIGHT) // 2 + jitter_y))
    base_frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    if scene_f >= 50 and scene_idx < 9:
        blend_factor = (scene_f - 50) / 10.0
        base_frame = Image.blend(base_frame, next_img, blend_factor)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Tactile Clay Floating Bubbles
    for b in CLAY_BUBBLES:
        by = (b['y'] - frame_idx * b['speed_y']) % HEIGHT
        bx = b['x'] + math.sin(frame_idx * 0.1 * b['wobble_f']) * 14.0
        r = b['r'] + math.sin(frame_idx * 0.2) * 1.5
        hr, hg, hb = b['hue']
        # Translucent bubble body
        draw.ellipse([bx - r, by - r, bx + r, by + r], outline=(hr, hg, hb, 180), width=3)
        # Specular light highlight
        hx = bx - r * 0.35
        hy = by - r * 0.35
        draw.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(255, 255, 255, 230))

    # 2. Top Clay Studio Badge
    draw.rounded_rectangle([25, 20, 290, 52], radius=16, fill=(255, 120, 100, 210), outline=(255, 255, 255, 220), width=2)
    draw.text((40, 26), "AARDMAN CLAYMATION", fill=(255, 255, 255), font=font_hud)

    draw.rounded_rectangle([WIDTH - 240, 20, WIDTH - 25, 52], radius=16, fill=(30, 80, 140, 210), outline=(255, 255, 255, 220), width=2)
    draw.text((WIDTH - 222, 26), f"OCEAN TALE // {scene_idx+1}/10", fill=(255, 255, 255), font=font_hud)

    # 3. BURNED-IN SUBTITLE PLACARD
    if scene_f < 6:
        sub_alpha = int(255 * (scene_f / 6.0))
    elif scene_f > 52:
        sub_alpha = int(255 * ((60 - scene_f) / 8.0))
    else:
        sub_alpha = 255

    speaker_tag, sub_text = SUBTITLES[scene_idx]

    box_w = max(700, min(1160, len(sub_text) * 14 + 160))
    box_h = 72
    box_x = (WIDTH - box_w) // 2
    box_y = HEIGHT - 105

    # Sculpted clay rounded card in soft ocean navy and warm peach border
    card_alpha = int(210 * (sub_alpha / 255.0))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=18, fill=(18, 36, 68, card_alpha), outline=(255, 160, 120, sub_alpha), width=3)

    # Speaker tag in soft coral / melon
    draw.text((box_x + 24, box_y + 12), speaker_tag, fill=(255, 180, 130, sub_alpha), font=font_tag)
    # Dialogue in bright clean white
    draw.text((box_x + 24, box_y + 37), sub_text, fill=(255, 255, 255, sub_alpha), font=font_sub)

    # Composite overlay
    base_rgba = base_frame.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")

    out_file = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_file, quality=86)
    return frame_idx

def main():
    print(f"Rendering 600 Claymation Underwater animation frames with subtitles across 16 threads...")
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(render_frame_task, range(TOTAL_FRAMES)))
    print(f"✓ All {len(results)} frames successfully saved to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
