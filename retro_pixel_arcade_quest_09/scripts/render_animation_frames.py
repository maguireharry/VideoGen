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
    "scene01_title_boot.png",
    "scene02_dungeon_awaken.png",
    "scene03_sword_draw.png",
    "scene04_pixel_monsters.png",
    "scene05_combo_slash.png",
    "scene06_lava_bridge.png",
    "scene07_boss_chamber.png",
    "scene08_limit_break.png",
    "scene09_boss_explode.png",
    "scene10_arcade_portal.png"
]

SUBTITLES = [
    ("[SYSTEM // BOOT]", "Insert coin to awaken the legendary Chrono Knight in the 16-bit realm!"),
    ("[CHRONO KNIGHT]", "Ugh... Where am I? The Forgotten Byte Crypt... My blade is gone!"),
    ("[ITEM DISCOVERED]", "Found the Legendary Glitch Slayer Broadsword! Attack Power +999!"),
    ("[BATTLE ENGAGED]", "Wild Corrupted Slimes and Shadow Bats appeared! Select command: ATTACK!"),
    ("[COMBO STRIKE]", "Critical hit! 3-hit combo slash! 9,999 damage dealt to front row!"),
    ("[STAGE WARNING]", "Stage 4 Foundry: Watch your step over the 8-bit boiling lava bridge!"),
    ("[BOSS ENCOUNTER]", "DANGER! Cyber Glitch Titan awakens! HP: [====================]"),
    ("[LIMIT BREAK]", "ULTIMATE ATTACK: CHRONO SLICE! Pixel energy blast cuts through reality!"),
    ("[STAGE CLEAR]", "BOSS DEFEATED! 100,000 XP gained! All stats maxed out! LEVEL UP!"),
    ("[ARCADE PORTAL]", "Stepping through the CRT dimension... High score etched into eternity!")
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
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 21)
    font_hud = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 15)
except Exception:
    font_tag = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_hud = ImageFont.load_default()

# Pre-generate 8-bit pixel sparkle stars
random.seed(4242)
PIXEL_SPARKS = []
for _ in range(50):
    PIXEL_SPARKS.append({
        'x': random.uniform(0, WIDTH),
        'y': random.uniform(0, HEIGHT),
        'size': random.choice([3, 4, 6]),
        'speed_y': random.uniform(1.0, 3.0),
        'color': random.choice([(255, 235, 50), (100, 220, 255), (255, 80, 180), (120, 255, 120)])
    })

def render_frame_task(frame_idx):
    scene_idx = min(frame_idx // FRAMES_PER_SCENE, 9)
    scene_f = frame_idx % FRAMES_PER_SCENE
    t = scene_f / float(FRAMES_PER_SCENE)

    curr_img = loaded_scenes[scene_idx]
    next_idx = min(scene_idx + 1, 9)
    next_img = loaded_scenes[next_idx]

    # Screen shake shudder during action scenes (scenes 4, 7 = combo & limit break)
    shake_x = 0
    shake_y = 0
    if scene_idx in [4, 7] and (frame_idx % 4 < 2):
        shake_x = random.choice([-5, 5])
        shake_y = random.choice([-4, 4])

    zoom = 1.0 + 0.03 * math.sin(t * math.pi)
    zw = int(WIDTH * zoom)
    zh = int(HEIGHT * zoom)
    scaled = curr_img.resize((zw, zh), Image.Resampling.BILINEAR)
    crop_x = max(0, min(zw - WIDTH, (zw - WIDTH) // 2 + shake_x))
    crop_y = max(0, min(zh - HEIGHT, (zh - HEIGHT) // 2 + shake_y))
    base_frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    if scene_f >= 50 and scene_idx < 9:
        blend_factor = (scene_f - 50) / 10.0
        base_frame = Image.blend(base_frame, next_img, blend_factor)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. 8-Bit Pixel Sparkles
    for spark in PIXEL_SPARKS:
        sy = int((spark['y'] - frame_idx * spark['speed_y']) % HEIGHT)
        sx = int(spark['x'] + math.sin(frame_idx * 0.1 + spark['y']) * 10) % WIDTH
        sz = spark['size']
        draw.rectangle([sx, sy, sx + sz, sy + sz], fill=spark['color'])

    # 2. CRT Scanlines
    for y in range(0, HEIGHT, 3):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, 40))

    # 3. Top SNES RPG Stats HUD
    draw.rounded_rectangle([25, 20, 360, 52], radius=4, fill=(10, 20, 60, 220), outline=(255, 255, 255, 240), width=2)
    draw.text((35, 26), "HP 9999/9999  MP 777/777  LV.99", fill=(255, 220, 40), font=font_hud)

    # Score & Stage
    draw.rounded_rectangle([WIDTH - 300, 20, WIDTH - 25, 52], radius=4, fill=(10, 20, 60, 220), outline=(255, 255, 255, 240), width=2)
    score = 120400 + frame_idx * 250
    draw.text((WIDTH - 285, 26), f"SCORE: {score:07d}  ACT {scene_idx+1}", fill=(100, 240, 255), font=font_hud)

    # 4. BURNED-IN 16-BIT RETRO SUBTITLE DIALOG BOX
    if scene_f < 6:
        sub_alpha = int(255 * (scene_f / 6.0))
    elif scene_f > 52:
        sub_alpha = int(255 * ((60 - scene_f) / 8.0))
    else:
        sub_alpha = 255

    speaker_tag, sub_text = SUBTITLES[scene_idx]

    box_w = max(700, min(1160, len(sub_text) * 13 + 180))
    box_h = 74
    box_x = (WIDTH - box_w) // 2
    box_y = HEIGHT - 105

    # Classic blue RPG dialog box with double white border
    bg_alpha = int(225 * (sub_alpha / 255.0))
    draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill=(12, 32, 105, bg_alpha), outline=(255, 255, 255, sub_alpha), width=3)
    draw.rectangle([box_x + 4, box_y + 4, box_x + box_w - 4, box_y + box_h - 4], outline=(80, 140, 255, sub_alpha), width=2)

    # Speaker tag in bright gold
    draw.text((box_x + 22, box_y + 12), speaker_tag, fill=(255, 225, 50, sub_alpha), font=font_tag)
    # Dialogue text in crisp white
    draw.text((box_x + 22, box_y + 38), sub_text, fill=(255, 255, 255, sub_alpha), font=font_sub)

    # Blinking 16-bit dialog cursor arrow at bottom-right
    if (frame_idx // 6) % 2 == 0:
        cx = box_x + box_w - 28
        cy = box_y + box_h - 22
        draw.polygon([(cx, cy), (cx + 12, cy), (cx + 6, cy + 8)], fill=(255, 220, 50, sub_alpha))

    # Composite overlay
    base_rgba = base_frame.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")

    out_file = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_file, quality=86)
    return frame_idx

def main():
    print(f"Rendering 600 Retro Pixel Arcade animation frames with subtitles across 16 threads...")
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(render_frame_task, range(TOTAL_FRAMES)))
    print(f"✓ All {len(results)} frames successfully saved to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
