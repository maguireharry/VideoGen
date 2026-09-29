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
    "scene01_folded_crane.png",
    "scene02_bamboo_bridge.png",
    "scene03_storm_petals.png",
    "scene04_ink_dragon.png",
    "scene05_draw_katana.png",
    "scene06_blossom_clash.png",
    "scene07_crane_flock.png",
    "scene08_dragon_dissolve.png",
    "scene09_sheath_blade.png",
    "scene10_eternal_harmony.png"
]

SUBTITLES = [
    ("[HAIKU CHRONICLE]", "Folded wings take flight / Morning mist upon bamboo / Dawn of cherry blossoms."),
    ("[KENSHIN // ORIGAMI RONIN]", "A warrior's soul is like folded washi paper: humble, yet unbreakable."),
    ("[HAIKU CHRONICLE]", "Sudden mountain gale / A thousand pink petals swirl / Fate calls from the storm."),
    ("[SHADOW DRAGON]", "From spilled calligraphy ink I rise... Darkness shall stain this peaceful land!"),
    ("[KENSHIN // ORIGAMI RONIN]", "Silver foil katana unsheathed... Guided by honor, purified by the wind."),
    ("[CLASH OF BLADES]", "Folded steel meets ancient shadow! A shower of ink splatters across the scroll!"),
    ("[KENSHIN // ORIGAMI RONIN]", "Secret Art: Flock of a Thousand Sacred Paper Cranes, arise!"),
    ("[HARMONY RESTORED]", "The ink darkness dissolves peacefully... Returning to petals and gold leaf upon the lake."),
    ("[KENSHIN // ORIGAMI RONIN]", "The blade is sheathed with reverence. Mount Fuji stands watch over the quiet morning."),
    ("[HAIKU CHRONICLE]", "Floating lanterns glow / Paper cranes reach the heavens / Peace forever folds.")
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

# Pre-generate drifting sakura petals
random.seed(3333)
SAKURA_PETALS = []
for _ in range(50):
    SAKURA_PETALS.append({
        'x': random.uniform(-100, WIDTH),
        'y': random.uniform(-100, HEIGHT),
        'speed_x': random.uniform(2.5, 6.0),
        'speed_y': random.uniform(1.2, 3.2),
        'size': random.uniform(8, 16),
        'rot_speed': random.uniform(0.04, 0.12),
        'hue': random.choice([(255, 185, 205), (255, 160, 190), (255, 215, 225)])
    })

def render_frame_task(frame_idx):
    scene_idx = min(frame_idx // FRAMES_PER_SCENE, 9)
    scene_f = frame_idx % FRAMES_PER_SCENE
    t = scene_f / float(FRAMES_PER_SCENE)

    curr_img = loaded_scenes[scene_idx]
    next_idx = min(scene_idx + 1, 9)
    next_img = loaded_scenes[next_idx]

    zoom = 1.0 + 0.04 * math.sin(t * math.pi)
    pan_x = int(math.sin(t * math.pi * 0.7) * 16.0)
    pan_y = int(math.cos(t * math.pi * 0.7) * 8.0)

    zw = int(WIDTH * zoom)
    zh = int(HEIGHT * zoom)
    scaled = curr_img.resize((zw, zh), Image.Resampling.BILINEAR)
    crop_x = max(0, min(zw - WIDTH, (zw - WIDTH) // 2 + pan_x))
    crop_y = max(0, min(zh - HEIGHT, (zh - HEIGHT) // 2 + pan_y))
    base_frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    if scene_f >= 50 and scene_idx < 9:
        blend_factor = (scene_f - 50) / 10.0
        base_frame = Image.blend(base_frame, next_img, blend_factor)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Swirling Pink Sakura Petals
    for petal in SAKURA_PETALS:
        py = (petal['y'] + frame_idx * petal['speed_y']) % (HEIGHT + 60) - 30
        px = (petal['x'] + frame_idx * petal['speed_x'] + math.sin(frame_idx * 0.1 + petal['y']) * 20.0) % (WIDTH + 60) - 30
        sz = petal['size']
        angle = frame_idx * petal['rot_speed']
        
        # 4-point curved petal polygon
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        dx1 = int(sz * cos_a)
        dy1 = int(sz * sin_a)
        dx2 = int(-sz * 0.5 * sin_a)
        dy2 = int(sz * 0.5 * cos_a)

        p_poly = [
            (px - dx1, py - dy1),
            (px + dx2, py + dy2),
            (px + dx1, py + dy1),
            (px - dx2, py - dy2)
        ]
        pr, pg, pb = petal['hue']
        draw.polygon(p_poly, fill=(pr, pg, pb, 215))

    # 2. Top Japanese Woodblock Banner
    draw.rectangle([(0, 0), (WIDTH, 14)], fill=(28, 20, 22, 230))
    draw.line([(0, 14), (WIDTH, 14)], fill=(195, 45, 60, 200), width=2)
    draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=(28, 20, 22, 230))
    draw.line([(0, HEIGHT - 14), (WIDTH, HEIGHT - 14)], fill=(195, 45, 60, 200), width=2)

    draw.text((35, 18), "UKIYO-E WOODBLOCK // WASHI ORIGAMI ARCHIVE", fill=(255, 200, 210), font=font_hud)
    draw.text((WIDTH - 250, 18), f"CHAPTER {scene_idx+1}/10 • 24 FPS", fill=(255, 170, 180), font=font_hud)

    # 3. BURNED-IN JAPANESE SCROLL SUBTITLE PLACARD
    if scene_f < 6:
        sub_alpha = int(255 * (scene_f / 6.0))
    elif scene_f > 52:
        sub_alpha = int(255 * ((60 - scene_f) / 8.0))
    else:
        sub_alpha = 255

    speaker_tag, sub_text = SUBTITLES[scene_idx]

    box_w = max(720, min(1180, len(sub_text) * 14 + 180))
    box_h = 72
    box_x = (WIDTH - box_w) // 2
    box_y = HEIGHT - 105

    # Textured rice paper scroll placard with vermilion silk border
    bg_alpha = int(215 * (sub_alpha / 255.0))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=10, fill=(24, 20, 22, bg_alpha), outline=(195, 45, 60, sub_alpha), width=2)

    # Red seal stamp box on left
    draw.rectangle([box_x + 10, box_y + 12, box_x + 36, box_y + 38], fill=(185, 30, 45, sub_alpha))
    draw.text((box_x + 14, box_y + 15), "和", fill=(255, 240, 240, sub_alpha), font=font_tag)

    # Speaker tag in soft cherry blossom pink
    draw.text((box_x + 48, box_y + 13), speaker_tag, fill=(255, 180, 195, sub_alpha), font=font_tag)
    # Dialogue in crisp white
    draw.text((box_x + 48, box_y + 38), sub_text, fill=(255, 255, 255, sub_alpha), font=font_sub)

    # Composite overlay
    base_rgba = base_frame.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")

    out_file = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_file, quality=86)
    return frame_idx

def main():
    print(f"Rendering 600 Origami Sakura Samurai animation frames with subtitles across 16 threads...")
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(render_frame_task, range(TOTAL_FRAMES)))
    print(f"✓ All {len(results)} frames successfully saved to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
