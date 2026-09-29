import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing import Pool, cpu_count

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
    "scene01_tunga_dawn.png",
    "scene02_river_ghat_prayers.png",
    "scene03_malnad_courtyard.png",
    "scene04_old_photo_album.png",
    "scene05_theatre_rehearsal.png",
    "scene06_actor_emotional_clash.png",
    "scene07_monsoon_road.png",
    "scene08_jog_falls_cliff.png",
    "scene09_temple_reunion.png",
    "scene10_brotherly_embrace.png"
]

SCENE_TITLES = [
    ("ದೃಶ್ಯ ೦೧", "ತುಂಗಾ ತೀರದ ಮುಂಜಾನೆ — ಮಂಜು ಮುಸುಕಿದ ಸೇತುವೆ (Dawn upon Tunga River)"),
    ("ದೃಶ್ಯ ೦೨", "ಮಂಗಳಾರತಿ — ಪವಿತ್ರ ನದಿಯ ತೀರ್ಥ ಸ್ನಾನ (Morning Prayers at the Ghat)"),
    ("ದೃಶ್ಯ ೦೩", "ನೆನಪುಗಳ ತೊಟ್ಟಿ ಮನೆ — ಮಲೆನಾಡ ಕಾಫಿಯ ಘಮ (Ancestral Courtyard Memories)"),
    ("ದೃಶ್ಯ ೦೪", "ಹಳೆಯ ಭಾವಚಿತ್ರ — ಹನಿ ಕಣ್ಣೀರು (The Sepia Photograph & A Single Tear)"),
    ("ದೃಶ್ಯ ೦೫", "ರಂಗಮಂದಿರ — ರಂಗದ ಬೆಳಕು ಮತ್ತು ಏಕಾಂತ (Rangamandira Theatrical Spotlight)"),
    ("ದೃಶ್ಯ ೦೬", "ಕಾವ್ಯ ಸಂಘರ್ಷ — ಗುರು ಮತ್ತು ಶಿಷ್ಯನ ವೇದನೆ (The Actor's Emotional Breakdown)"),
    ("ದೃಶ್ಯ ೦೭", "ಮಳೆಗಾಲದ ಮಲೆನಾಡು — ಅಂಬಾಸಿಡರ್ ಕಾರಿನ ಪಯಣ (Monsoon Torrent on the Western Ghats Road)"),
    ("ದೃಶ್ಯ ೦೮", "ಜೋಗ ಜಲಪಾತ — ರೌದ್ರ ಗಾಂಭೀರ್ಯ ಮತ್ತು ಸಿಡಿಲು (Jog Falls Roar & Lightning Tempest)"),
    ("ದೃಶ್ಯ ೦೯", "ದೇವಾಲಯದ ಸನ್ನಿಧಿ — ಮಳೆ ನಿಂತ ಮಧ್ಯಾಹ್ನ (Rain Clears at the Sacred Temple)"),
    ("ದೃಶ್ಯ ೧೦", "ಹೃದಯ ಗೀತೆ — ಕರುಳಿನ ಮಿಲನ ಮತ್ತು ಮುಕ್ತಿ (Song of the Heart — Unbreakable Brotherhood)")
]

loaded_scenes = []
for f in SCENE_FILES:
    p = os.path.join(SCENES_DIR, f)
    img = Image.open(p).convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    loaded_scenes.append(img)

def draw_rain_streaks(draw, num_streaks=80, angle_deg=75, speed_mult=1.0, frame_idx=0):
    rad = math.radians(angle_deg)
    dx = math.cos(rad) * 45 * speed_mult
    dy = math.sin(rad) * 45 * speed_mult
    for i in range(num_streaks):
        seed = i * 199
        x1 = int((seed + frame_idx * 33) % (WIDTH + 200) - 100)
        y1 = int((seed * 7 + frame_idx * 55) % (HEIGHT + 200) - 100)
        x2 = int(x1 + dx)
        y2 = int(y1 + dy)
        alpha = int(90 + 90 * math.sin(i * 1.7))
        draw.line([(x1, y1), (x2, y2)], fill=(215, 230, 245, alpha), width=random.choice([1, 2]))

def draw_arati_flame(draw, cx, cy, size=18, flicker_phase=0.0):
    f = math.sin(flicker_phase) * 0.25
    h = int(size * (1.2 + f))
    w = int(size * (0.6 - f * 0.5))
    flame_poly = [
        (cx, cy - h),
        (cx - w, cy),
        (cx + w, cy)
    ]
    draw.polygon(flame_poly, fill=(255, 180 + int(40*f), 30, 220))
    # Inner yellow core
    draw.polygon([(cx, cy - int(h*0.7)), (cx - int(w*0.5), cy), (cx + int(w*0.5), cy)], fill=(255, 255, 160, 240))

def render_frame_task(frame_idx):
    scene_idx = frame_idx // FRAMES_PER_SCENE
    scene_frame = frame_idx % FRAMES_PER_SCENE
    t = scene_frame / float(FRAMES_PER_SCENE)
    
    base_img = loaded_scenes[scene_idx].copy()
    ow, oh = base_img.size
    
    zoom = 1.0
    pan_x = 0
    pan_y = 0
    shake_x = 0
    shake_y = 0
    
    if scene_idx == 0:
        # Epic slow tracking pan across Tunga bridge
        zoom = 1.05
        pan_x = int(-40 * t)
    elif scene_idx == 1:
        # River ghat slow zoom into arati flames
        zoom = 1.0 + 0.08 * t
    elif scene_idx == 2:
        # Ancestral courtyard gentle push-in
        zoom = 1.0 + 0.06 * t
        pan_y = int(-10 * t)
    elif scene_idx == 3:
        # Intimate macro zoom onto sepia photograph and tear
        zoom = 1.02 + 0.08 * t
    elif scene_idx == 4:
        # Rangamandira spotlight swing pan
        zoom = 1.06
        pan_x = int(35 * math.sin(t * math.pi))
    elif scene_idx == 5:
        # Dramatic actor breakdown snap zoom
        if t < 0.35:
            zoom = 1.0 + 0.04 * (t / 0.35)
        else:
            zoom = 1.06 + 0.04 * math.sin((t - 0.35) * math.pi * 3.0) * math.exp(-2.0 * (t - 0.35))
    elif scene_idx == 6:
        # Monsoon road car tracking pan
        zoom = 1.08
        pan_x = int(50 * (1.0 - t))
    elif scene_idx == 7:
        # Jog Falls lightning tempest shake!
        if 25 <= scene_frame <= 36:
            thunder_decay = math.exp(-4.0 * ((scene_frame - 25) / 11.0))
            shake_x = int(random.uniform(-10, 10) * thunder_decay)
            shake_y = int(random.uniform(-10, 10) * thunder_decay)
            zoom = 1.06 + 0.04 * thunder_decay
        else:
            zoom = 1.06
    elif scene_idx == 8:
        # Rain clearing temple pan
        zoom = 1.0 + 0.06 * t
        pan_y = int(-12 * t)
    elif scene_idx == 9:
        # Emotional climax brotherly embrace warm zoom
        zoom = 1.02 + 0.08 * t
        
    # Apply camera transform
    if zoom != 1.0 or pan_x != 0 or pan_y != 0 or shake_x != 0 or shake_y != 0:
        zw = int(ow * zoom)
        zh = int(oh * zoom)
        scaled = base_img.resize((zw, zh), Image.Resampling.BILINEAR)
        cx = (zw - WIDTH) // 2 + pan_x + shake_x
        cy = (zh - HEIGHT) // 2 + pan_y + shake_y
        cx = max(0, min(zw - WIDTH, cx))
        cy = max(0, min(zh - HEIGHT, cy))
        base_img = scaled.crop((cx, cy, cx + WIDTH, cy + HEIGHT))
        
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # 35mm Indian Cinema Procedural VFX per scene
    if scene_idx == 0:
        # Rolling morning river mist layers
        for m in range(15):
            my = int(320 + m * 25)
            mx = int((m * 140 + frame_idx * 2) % WIDTH)
            ma = int(35 + 20 * math.sin(frame_idx * 0.05 + m))
            ov_draw.ellipse([mx - 150, my - 25, mx + 150, my + 25], fill=(230, 240, 250, ma))
            
    elif scene_idx == 1:
        # Flickering arati flames and glowing fire sparks
        for fl in range(4):
            fx = 650 + fl * 120
            fy = 240 + fl * 35
            draw_arati_flame(ov_draw, fx, fy, size=20, flicker_phase=frame_idx * 0.5 + fl)
        # Rising camphor smoke
        for sm in range(20):
            sy = int(220 - (frame_idx * 3 + sm * 15) % 180)
            sx = int(720 + math.sin(sy * 0.05 + frame_idx * 0.1) * 22)
            sa = max(0, int(90 * (sy - 40) / 180.0))
            ov_draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(245, 245, 250, sa))
            
    elif scene_idx == 2:
        # Filter coffee steam curling upwards in courtyard
        for cs in range(16):
            cy = int(480 - (frame_idx * 2.5 + cs * 12) % 160)
            cx = int(450 + math.sin(cy * 0.06 + frame_idx * 0.1) * 14)
            ca = max(0, int(110 * (cy - 320) / 160.0))
            ov_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, ca))
            
    elif scene_idx == 3:
        # Tear sliding down photograph glass
        tear_y = int(340 + t * 90)
        tear_x = 590
        ov_draw.ellipse([tear_x - 3, tear_y - 5, tear_x + 3, tear_y + 5], fill=(255, 255, 255, 220))
        ov_draw.line([(tear_x, 340), (tear_x, tear_y)], fill=(255, 255, 255, 120), width=2)
        
    elif scene_idx == 4:
        # Theatrical overhead spotlight cone swinging
        spot_x = int(WIDTH * 0.5 + math.sin(t * math.pi) * 80)
        spot_poly = [
            (WIDTH * 0.5, 0),
            (spot_x - 280, HEIGHT),
            (spot_x + 280, HEIGHT)
        ]
        ov_draw.polygon(spot_poly, fill=(255, 245, 210, 32))
        # Dancing dust motes in spotlight
        for d in range(25):
            seed = d * 83
            dx = int(spot_x - 120 + ((seed + frame_idx) % 240))
            dy = int(100 + (seed * 3 % (HEIGHT - 200)))
            da = int(120 + 80 * math.sin(frame_idx * 0.1 + d))
            ov_draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 245, 200, da))
            
    elif scene_idx == 5:
        # Emotional stage spotlight intensity pulse
        pulse = 0.5 + 0.5 * math.sin(frame_idx * 0.3)
        spot_poly = [(640, 20), (320, HEIGHT), (960, HEIGHT)]
        ov_draw.polygon(spot_poly, fill=(255, 230, 180, int(30 + 20 * pulse)))
        
    elif scene_idx == 6:
        # Torrential monsoon rain downpour on Western Ghats road!
        draw_rain_streaks(ov_draw, num_streaks=120, angle_deg=78, speed_mult=1.4, frame_idx=frame_idx)
        # Headlight beam glare
        ov_draw.ellipse([380, 440, 430, 490], fill=(255, 255, 200, 70))
        ov_draw.ellipse([505, 440, 555, 490], fill=(255, 255, 200, 70))
        
    elif scene_idx == 7:
        # Jog Falls lightning sheet flash & heavy rain
        if 25 <= scene_frame <= 29:
            # White lightning flash!
            ov_draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(240, 250, 255, 140))
        draw_rain_streaks(ov_draw, num_streaks=140, angle_deg=82, speed_mult=1.6, frame_idx=frame_idx)
        
    elif scene_idx == 8:
        # Gentle golden clearing drizzle
        draw_rain_streaks(ov_draw, num_streaks=40, angle_deg=80, speed_mult=0.8, frame_idx=frame_idx)
        # Golden sun ray breaking through stone pillars
        ov_draw.polygon([(0, 0), (WIDTH * 0.4, 0), (WIDTH * 0.8, HEIGHT), (WIDTH * 0.2, HEIGHT)], fill=(255, 235, 180, 28))
        
    elif scene_idx == 9:
        # Divine warm golden sun wrap around brothers
        ov_draw.ellipse([450, 200, 830, 580], fill=(255, 230, 170, 40))
        # Floating marigold petals
        for p in range(15):
            px = int((p * 85 + t * 240) % WIDTH)
            py = int(320 + p * 20 + math.sin(t * 3.0 + p) * 25)
            ov_draw.ellipse([px - 4, py - 3, px + 4, py + 3], fill=(255, 150, 20, 210))
            
    # 35mm Cinema Letterboxing & Dual-Script Kannada Typography
    for y in range(HEIGHT - 85, HEIGHT):
        a = int(195 * ((y - (HEIGHT - 85)) / 85.0))
        ov_draw.line([(0, y), (WIDTH, y)], fill=(12, 10, 8, a))
        
    ov_draw.rectangle([(0, 0), (WIDTH, 14)], fill=(10, 8, 6, 240))
    ov_draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=(10, 8, 6, 240))
    
    k_tag, k_desc = SCENE_TITLES[scene_idx]
    ov_draw.rounded_rectangle([30, HEIGHT - 65, 135, HEIGHT - 35], radius=5, fill=(185, 95, 25, 230), outline=(255, 195, 110, 180), width=1)
    ov_draw.text((38, HEIGHT - 56), k_tag, fill=(255, 245, 225))
    ov_draw.text((150, HEIGHT - 57), k_desc, fill=(250, 240, 225))
    
    ov_draw.text((WIDTH - 280, 2), "35MM KANNADA CINEMA REALISM", fill=(245, 205, 130))
    
    base_rgba = base_img.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    
    out_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_path, quality=88)
    return frame_idx

def main():
    print(f"Rendering 600 animated frames for Shivamogga Kannada Drama across {cpu_count()} CPU cores...")
    with Pool(cpu_count()) as pool:
        results = pool.map(render_frame_task, range(TOTAL_FRAMES))
    print(f"✓ All {len(results)} frames successfully rendered to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
