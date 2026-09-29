import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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
    "scene01_monsoon_alley.png",
    "scene02_holographic_clue.png",
    "scene03_flying_hover_traffic.png",
    "scene04_noodle_bar_informant.png",
    "scene05_subway_chase.png",
    "scene06_rooftop_overlook.png",
    "scene07_quantum_server_vault.png",
    "scene08_cyber_confrontation.png",
    "scene09_memory_extracted.png",
    "scene10_neon_dawn.png"
]

SUBTITLES = [
    ("[JAXON // DECKER-09]", "Midnight in Sector 4. The rain never washes the neon away."),
    ("[HUD ANALYSIS]", "Fragmented neural imprint detected... Encrypted bio-chip signature."),
    ("[JAXON // DECKER-09]", "Traffic control won't track the spinner into the lower smog levels."),
    ("[INFORMANT // VEX]", "They scrubbed the mainframe, Jaxon. The ghost protocol is active."),
    ("[SYSTEM ALERT]", "Hostile intercept in Sector 7 Transit! High-speed maglev pursuit engaged."),
    ("[JAXON // DECKER-09]", "From up here, the city looks alive... but it’s just circuits and ghosts."),
    ("[AI CORE // NEXUS]", "Intrusion detected in Quantum Vault. Accessing neural archives..."),
    ("[CYBER SYNDICATE]", "You should have stayed in the shadows, detective. Delete him."),
    ("[SYSTEM OVERRIDE]", "Memory extraction complete. The truth is copied to decentralized ledger."),
    ("[JAXON // DECKER-09]", "The sun never truly rises here... but the truth finally did.")
]

# Preload scenes
loaded_scenes = []
for sf in SCENE_FILES:
    p = os.path.join(SCENES_DIR, sf)
    img = Image.open(p).convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    loaded_scenes.append(img)

# Try loading TrueType fonts
try:
    font_tag = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 17)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 22)
    font_hud = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 14)
except Exception:
    font_tag = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_hud = ImageFont.load_default()

# Pre-generate deterministic neon rain particles
random.seed(2099)
RAIN_DROPS = []
for _ in range(80):
    RAIN_DROPS.append({
        'x': random.uniform(0, WIDTH + 200),
        'y': random.uniform(-HEIGHT, HEIGHT),
        'speed': random.uniform(25, 45),
        'length': random.uniform(18, 38),
        'color': random.choice([(0, 240, 255), (255, 0, 180), (160, 220, 255), (0, 255, 200)])
    })

def render_frame_task(frame_idx):
    scene_idx = min(frame_idx // FRAMES_PER_SCENE, 9)
    scene_f = frame_idx % FRAMES_PER_SCENE
    t = scene_f / float(FRAMES_PER_SCENE) # 0.0 to 1.0

    curr_img = loaded_scenes[scene_idx]
    next_idx = min(scene_idx + 1, 9)
    next_img = loaded_scenes[next_idx]

    # Camera subtle dolly & pan
    zoom = 1.0 + 0.05 * math.sin(t * math.pi)
    pan_x = int(math.sin(t * math.pi * 0.8) * 18.0)
    pan_y = int(math.cos(t * math.pi * 0.8) * 10.0)

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

    # Dynamic procedural cyber VFX overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Multi-layer falling neon rain streaks
    wind_x = 7.0
    for drop in RAIN_DROPS:
        dy = (drop['y'] + (frame_idx * drop['speed'])) % (HEIGHT + 100) - 50
        dx = (drop['x'] - (frame_idx * wind_x)) % (WIDTH + 150) - 50
        r, g, b = drop['color']
        alpha = int(140 + 70 * math.sin(frame_idx * 0.3 + drop['speed']))
        draw.line([
            (dx, dy),
            (dx - wind_x * (drop['length'] / drop['speed']), dy - drop['length'])
        ], fill=(r, g, b, alpha), width=2)

    # 2. Subtle CRT scanlines
    for y in range(0, HEIGHT, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, 30))

    # 3. Cyber HUD Overlays (Crosshairs & corner target brackets)
    corner_col = (0, 240, 255, 140)
    # Top-left target
    draw.line([(25, 25), (65, 25)], fill=corner_col, width=2)
    draw.line([(25, 25), (25, 65)], fill=corner_col, width=2)
    # Top-right target
    draw.line([(WIDTH - 65, 25), (WIDTH - 25, 25)], fill=corner_col, width=2)
    draw.line([(WIDTH - 25, 25), (WIDTH - 25, 65)], fill=corner_col, width=2)
    # Top status HUD text
    rec_pulse = int(180 + 75 * math.sin(frame_idx * 0.25))
    draw.ellipse([35, 33, 47, 45], fill=(255, 30, 80, rec_pulse))
    draw.text((55, 30), f"SYS.REC // SECTOR-04 // LAT 35.689 // FPS: {FPS}", fill=(0, 240, 255, 200), font=font_hud)
    draw.text((WIDTH - 230, 30), f"TIMECODE: 00:00:{scene_idx*2 + int(t*2.5):02d}:{scene_f:02d}", fill=(255, 0, 180, 200), font=font_hud)

    # 4. Cinematic Letterbox Bars
    draw.rectangle([(0, 0), (WIDTH, 16)], fill=(5, 5, 12, 240))
    draw.rectangle([(0, HEIGHT - 16), (WIDTH, HEIGHT)], fill=(5, 5, 12, 240))

    # 5. BURNED-IN SUBTITLE BOX & TYPOGRAPHY
    # Scene subtitle fade-in / fade-out
    if scene_f < 6:
        sub_alpha = int(255 * (scene_f / 6.0))
    elif scene_f > 52:
        sub_alpha = int(255 * ((60 - scene_f) / 8.0))
    else:
        sub_alpha = 255

    speaker_tag, sub_text = SUBTITLES[scene_idx]

    # Calculate subtitle width and draw sleek cyberpunk card
    box_w = max(680, min(1140, len(sub_text) * 14 + 180))
    box_h = 70
    box_x = (WIDTH - box_w) // 2
    box_y = HEIGHT - 105

    # Semi-transparent dark frosted glass card with cyan glow border
    card_bg = (10, 14, 25, int(195 * (sub_alpha / 255.0)))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=8, fill=card_bg, outline=(0, 240, 255, int(180 * (sub_alpha / 255.0))), width=2)
    # Accent cyber corner brackets
    draw.line([(box_x + 5, box_y + 8), (box_x + 18, box_y + 8)], fill=(255, 0, 180, sub_alpha), width=3)
    draw.line([(box_x + box_w - 18, box_y + box_h - 8), (box_x + box_w - 5, box_y + box_h - 8)], fill=(255, 0, 180, sub_alpha), width=3)

    # Speaker tag pill
    draw.text((box_x + 22, box_y + 12), speaker_tag, fill=(0, 255, 230, sub_alpha), font=font_tag)
    # Subtitle dialogue text
    draw.text((box_x + 22, box_y + 36), sub_text, fill=(255, 255, 255, sub_alpha), font=font_sub)

    # Composite overlay
    base_rgba = base_frame.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")

    out_file = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_file, quality=86)
    return frame_idx

def main():
    print(f"Rendering 600 Cyberpunk animation frames with subtitles across 16 threads...")
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(render_frame_task, range(TOTAL_FRAMES)))
    print(f"✓ All {len(results)} frames successfully saved to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
