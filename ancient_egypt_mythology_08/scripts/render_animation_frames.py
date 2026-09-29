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
    "scene01_nile_twilight.png",
    "scene02_temple_karnak.png",
    "scene03_sacred_altar.png",
    "scene04_solar_bark_launches.png",
    "scene05_underworld_gates.png",
    "scene06_scales_of_maat.png",
    "scene07_battle_apep.png",
    "scene08_horus_triumph.png",
    "scene09_dawn_over_pyramids.png",
    "scene10_eternal_egypt.png"
]

SUBTITLES = [
    ("[CHRONICLER OF THE NILE]", "Before the dawn of dynasties, the sacred river reflected the eternal stars."),
    ("[HIGH PRIEST AMUN-RA]", "Enter Karnak's sacred columns... Where incense rises to meet the gods."),
    ("[INVOCATION OF KHEPRI]", "By the Golden Scarab, let Ra awaken the cosmic breath of life across the land."),
    ("[THE CELESTIAL VOYAGE]", "The Solar Barque sets sail across the sapphire celestial waters of Nut."),
    ("[ANUBIS // WEIGHER OF HEARTS]", "Tread softly, mortal soul. You stand before the Twelve Gates of the Underworld."),
    ("[JUDGMENT OF MA'AT]", "The heart is placed upon the scale... lighter than the ostrich feather of truth."),
    ("[THE WRATH OF RA]", "Apep, serpent of chaos, shall be smitten by the spears of blinding solar fire!"),
    ("[HORUS VICTORIOUS]", "With wings of gold and lapis lazuli, the Eye of Horus restores divine cosmic order."),
    ("[DAWN OVER GIZA]", "The golden capstones catch the first morning rays... Immortality etched in limestone."),
    ("[ETERNAL HYMN OF RA]", "Fertile lands, flowing Nile, eternal glory. Egypt shines under the everlasting sun.")
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
    font_hud = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 14)
except Exception:
    font_tag = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_hud = ImageFont.load_default()

# Pre-generate golden sand and divine light motes
random.seed(1337)
GOLDEN_MOTES = []
for _ in range(70):
    GOLDEN_MOTES.append({
        'x': random.uniform(0, WIDTH),
        'y': random.uniform(0, HEIGHT),
        'radius': random.uniform(1.5, 4.0),
        'speed_y': random.uniform(0.6, 2.2),
        'drift_x': random.uniform(0.8, 2.0),
        'color': random.choice([(255, 215, 80), (255, 190, 40), (255, 240, 150), (240, 160, 40)])
    })

def render_frame_task(frame_idx):
    scene_idx = min(frame_idx // FRAMES_PER_SCENE, 9)
    scene_f = frame_idx % FRAMES_PER_SCENE
    t = scene_f / float(FRAMES_PER_SCENE)

    curr_img = loaded_scenes[scene_idx]
    next_idx = min(scene_idx + 1, 9)
    next_img = loaded_scenes[next_idx]

    # Camera majestic slow push-in & panoramic drift
    zoom = 1.0 + 0.04 * math.sin(t * math.pi * 0.9)
    pan_x = int(math.sin(t * math.pi) * 14.0)
    pan_y = int((t - 0.5) * 8.0)

    zw = int(WIDTH * zoom)
    zh = int(HEIGHT * zoom)
    scaled = curr_img.resize((zw, zh), Image.Resampling.BILINEAR)
    crop_x = max(0, min(zw - WIDTH, (zw - WIDTH) // 2 + pan_x))
    crop_y = max(0, min(zh - HEIGHT, (zh - HEIGHT) // 2 + pan_y))
    base_frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    # Crossfade between scenes on last 10 frames
    if scene_f >= 50 and scene_idx < 9:
        blend_factor = (scene_f - 50) / 10.0
        base_frame = Image.blend(base_frame, next_img, blend_factor)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Swirling Golden Desert Sand Motes & Fire Embers
    for mote in GOLDEN_MOTES:
        my = (mote['y'] - (frame_idx * mote['speed_y'])) % HEIGHT
        mx = (mote['x'] + math.sin(frame_idx * 0.08 + mote['x']) * 15.0 + frame_idx * mote['drift_x']) % WIDTH
        r = mote['radius']
        alpha = int(140 + 80 * math.sin(frame_idx * 0.15 + mote['x']))
        cr, cg, cb = mote['color']
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=(cr, cg, cb, alpha))
        # Core glint
        draw.ellipse([mx - r * 0.5, my - r * 0.5, mx + r * 0.5, my + r * 0.5], fill=(255, 255, 230, min(255, alpha + 50)))

    # 2. Pulsing Solar Rays from above
    sun_pulse = int(25 + 15 * math.sin(frame_idx * 0.12))
    for ray in range(5):
        rx1 = int(WIDTH * 0.3 + ray * 140 + math.sin(frame_idx * 0.05 + ray) * 40)
        rx2 = int(rx1 + 180)
        draw.polygon([(rx1, 0), (rx2, 0), (rx2 + 80, HEIGHT), (rx1 - 80, HEIGHT)], fill=(255, 215, 120, sun_pulse))

    # 3. Top Egyptian Golden Cartouche Border
    draw.rectangle([(0, 0), (WIDTH, 14)], fill=(20, 14, 8, 240))
    draw.line([(0, 14), (WIDTH, 14)], fill=(218, 165, 32, 180), width=2)
    draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=(20, 14, 8, 240))
    draw.line([(0, HEIGHT - 14), (WIDTH, HEIGHT - 14)], fill=(218, 165, 32, 180), width=2)

    # Top title tag
    draw.text((35, 18), "ANCIENT EGYPT // SACRED MYTHOLOGY ARCHIVE", fill=(245, 205, 95, 210), font=font_hud)
    draw.text((WIDTH - 260, 18), f"CHRONICLE {scene_idx+1}/10 • 24 FPS 4K", fill=(218, 165, 32, 210), font=font_hud)

    # 4. BURNED-IN SUBTITLE BOX & TYPOGRAPHY
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

    # Rich dark papyrus placard with gold leaf border and inner pinstripe
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=10, fill=(24, 16, 10, int(205 * (sub_alpha / 255.0))), outline=(218, 165, 32, int(210 * (sub_alpha / 255.0))), width=2)
    # Inner gold border
    draw.rectangle([box_x + 5, box_y + 5, box_x + box_w - 5, box_y + box_h - 5], outline=(184, 134, 11, int(120 * (sub_alpha / 255.0))), width=1)

    # Speaker tag in brilliant hieroglyphic gold
    draw.text((box_x + 24, box_y + 12), speaker_tag, fill=(255, 215, 60, sub_alpha), font=font_tag)
    # Subtitle dialogue text
    draw.text((box_x + 24, box_y + 37), sub_text, fill=(255, 250, 235, sub_alpha), font=font_sub)

    # Composite overlay
    base_rgba = base_frame.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")

    out_file = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_file, quality=86)
    return frame_idx

def main():
    print(f"Rendering 600 Ancient Egypt animation frames with subtitles across 16 threads...")
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(render_frame_task, range(TOTAL_FRAMES)))
    print(f"✓ All {len(results)} frames successfully saved to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
