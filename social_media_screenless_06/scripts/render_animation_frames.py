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
    "scene01_digital_doomscroll.png",
    "scene02_notification_overload.png",
    "scene03_powering_off.png",
    "scene04_opening_window_breeze.png",
    "scene05_forest_sunlight.png",
    "scene06_sunlight_canopy.png",
    "scene07_real_connection.png",
    "scene08_open_sketchbook.png",
    "scene09_ocean_sunset.png",
    "scene10_starlit_reflection.png"
]

SCENE_TITLES = [
    ("第１幕 (Act I)", "深夜の闇とスクロール (Midnight Gloom & The Doomscroll)"),
    ("第２幕 (Act II)", "通知の嵐と精神の限界 (Notification Overload & Anxiety)"),
    ("第３幕 (Act III)", "電源を切る静寂 (The Choice to Power Off)"),
    ("第４幕 (Act IV)", "開かれた窓と朝の光 (Open Windows & The Morning Breeze)"),
    ("第５幕 (Act V)", "生きている森への一歩 (First Steps into the Living Cedar Forest)"),
    ("第６幕 (Act VI)", "木漏れ日と緑の呼吸 (Komorebi — Sunlight through the Canopy)"),
    ("第７幕 (Act VII)", "友との笑顔と温かいお茶 (Real Connection — Shared Tea & Laughter)"),
    ("第８幕 (Act VIII)", "風のスケッチブック (Sketchbook in the Wildflower Meadow)"),
    ("第９幕 (Act IX)", "海風と夕暮れの静けさ (Twilight Cliffside & The Evening Ocean)"),
    ("第１０幕 (Act X)", "星空の誓い : デスコネクト (Disconnect to Reconnect)")
]

loaded_scenes = []
for f in SCENE_FILES:
    p = os.path.join(SCENES_DIR, f)
    img = Image.open(p).convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    loaded_scenes.append(img)

def draw_notification_badge(draw, x, y, text, count=999, scale=1.0):
    w, h = int(140 * scale), int(34 * scale)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=int(6*scale), fill=(225, 30, 45, 230), outline=(255, 255, 255, 200), width=2)
    draw.ellipse([x + 6, y + 6, x + 24, y + 24], fill=(255, 255, 255))
    draw.text((x + 10, y + 7), "!", fill=(225, 30, 45))
    draw.text((x + 32, y + 7), f"{text} +{count}", fill=(255, 255, 255))

def draw_dandelion_seed(draw, cx, cy, rot=0.0, size=16):
    draw.line([(cx, cy), (cx + int(size * math.cos(rot)), cy + int(size * math.sin(rot)))], fill=(255, 255, 255, 220), width=1)
    # Tuft rays
    for r in range(6):
        a = rot + (r - 2.5) * 0.35
        tx = cx - int(size * 0.7 * math.cos(a))
        ty = cy - int(size * 0.7 * math.sin(a))
        draw.line([(cx, cy), (tx, ty)], fill=(255, 255, 255, 180), width=1)

def draw_bird(draw, cx, cy, wing_phase=0.0, size=12):
    w_y = int(math.sin(wing_phase) * 6)
    # V shape wings
    draw.line([(cx - size, cy - w_y), (cx, cy), (cx + size, cy - w_y)], fill=(30, 40, 60, 230), width=2)

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
        # Slow claustrophobic push-in
        zoom = 1.0 + 0.10 * t
    elif scene_idx == 1:
        # Glitch jitter and anxiety shake
        jitter = 4.0 + 10.0 * (t ** 1.5)
        shake_x = int(random.uniform(-jitter, jitter))
        shake_y = int(random.uniform(-jitter, jitter))
        zoom = 1.04 + 0.06 * t
    elif scene_idx == 2:
        # Sudden stillness as phone powers off
        if t < 0.25:
            zoom = 1.05
        else:
            zoom = 1.05 - 0.05 * ((t - 0.25) / 0.75)
    elif scene_idx == 3:
        # Expansive window opening
        zoom = 1.02 + 0.08 * t
        pan_y = int(-15 * t)
    elif scene_idx == 4:
        # Forest walking motion pan
        zoom = 1.06
        pan_x = int(-40 * t)
    elif scene_idx == 5:
        # Dramatic tilt up to canopy
        zoom = 1.10
        pan_y = int(35 * (1.0 - t))
    elif scene_idx == 6:
        # Real connection slow pan
        zoom = 1.05
        pan_x = int(30 * math.sin(t * math.pi))
    elif scene_idx == 7:
        # Sketchbook focus push
        zoom = 1.0 + 0.06 * t
    elif scene_idx == 8:
        # Twilight cliffside wide ocean pan
        zoom = 1.06
        pan_x = int(-45 * t)
    elif scene_idx == 9:
        # Infinite starlight pull-back
        zoom = 1.08 - 0.08 * t
        
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
    
    # Dynamic Anime VFX per scene
    if scene_idx == 0:
        # Rolling CRT scanlines & blue glow
        scan_offset = (frame_idx * 4) % 12
        for y in range(scan_offset, HEIGHT, 12):
            ov_draw.line([(0, y), (WIDTH, y)], fill=(0, 20, 50, 45), width=2)
            
    elif scene_idx == 1:
        # Notification popups multiplying and vibrating
        count_inc = int(t * 1500)
        draw_notification_badge(ov_draw, 420 + shake_x, 180 + shake_y, "VIRAL ALERT", 999 + count_inc, scale=1.1)
        if t > 0.3:
            draw_notification_badge(ov_draw, 340 - shake_x, 260 + shake_y, "SYSTEM ERR", 420 + count_inc, scale=1.0)
        if t > 0.6:
            draw_notification_badge(ov_draw, 510 + shake_x, 340 - shake_y, "NEW MENTION", 1880 + count_inc, scale=1.05)
        # Horizontal glitch slice lines
        for g in range(4):
            gy = random.randint(100, HEIGHT - 100)
            ov_draw.line([(0, gy), (WIDTH, gy)], fill=(0, 255, 255, 120), width=random.randint(1, 3))
            
    elif scene_idx == 2:
        # Screen power-off collapse
        if t < 0.25:
            # White flash line
            fl_t = t / 0.25
            line_h = max(2, int(15 * (1.0 - fl_t)))
            ov_draw.rectangle([0, HEIGHT//2 - line_h, WIDTH, HEIGHT//2 + line_h], fill=(255, 255, 255, int(220 * (1.0 - fl_t))))
        else:
            # Gentle morning warm glow creeping in
            glow_a = int(60 * ((t - 0.25) / 0.75))
            ov_draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(255, 220, 180, glow_a))
            
    elif scene_idx == 3:
        # Golden sunbeam streaks and flying birds
        for b in range(5):
            bx = int(WIDTH * 0.4 + b * 65 + t * 240)
            by = int(140 + b * 25 - t * 45)
            draw_bird(ov_draw, bx, by, wing_phase=frame_idx * 0.4 + b, size=11)
        # Floating golden particles
        for p in range(30):
            seed = p * 77
            px = int((seed + frame_idx * 2) % WIDTH)
            py = int((seed * 3 + math.sin(frame_idx * 0.05 + p) * 30) % HEIGHT)
            pa = int(140 + 80 * math.sin(frame_idx * 0.1 + p))
            ov_draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 235, 180, pa))
            
    elif scene_idx == 4:
        # Dandelion seeds floating in cedar forest breeze
        for d in range(25):
            seed = d * 113
            dx = int((seed + t * 380) % WIDTH)
            dy = int(180 + (seed % 350) + math.sin(t * math.pi * 3.0 + d) * 25)
            draw_dandelion_seed(ov_draw, dx, dy, rot=t * 2.0 + d, size=14)
            
    elif scene_idx == 5:
        # Rotating radiant Komorebi sunbeam rays
        for ray in range(8):
            angle = 0.5 + ray * 0.18 + math.sin(frame_idx * 0.02) * 0.05
            lx = int(WIDTH * 0.55 + 900 * math.cos(angle))
            ly = int(HEIGHT * 0.15 + 900 * math.sin(angle))
            ov_draw.line([(int(WIDTH * 0.55), int(HEIGHT * 0.15)), (lx, ly)], fill=(255, 250, 200, 35), width=24)
            
    elif scene_idx == 6:
        # Steaming tea curls rising
        for s in range(20):
            st_y = int(380 - s * 14 - (frame_idx * 3) % 250)
            st_x = int(340 + math.sin(st_y * 0.04 + frame_idx * 0.1) * 16)
            st_a = max(0, int(150 * (st_y - 120) / 260.0))
            ov_draw.ellipse([st_x - 4, st_y - 4, st_x + 4, st_y + 4], fill=(255, 255, 255, st_a))
            
    elif scene_idx == 7:
        # Sketching animation: pencil tip trail & flower petals in breeze
        for petal in range(12):
            px = int((petal * 95 + t * 320) % WIDTH)
            py = int(250 + petal * 20 + math.sin(t * 4.0 + petal) * 30)
            ov_draw.ellipse([px - 4, py - 2, px + 4, py + 2], fill=(255, 180, 200, 210))
            
    elif scene_idx == 8:
        # Ocean wave glistening specular sparkles
        for sp in range(25):
            seed = sp * 89
            ox = int((seed * 7) % WIDTH)
            oy = int(480 + (seed % 160))
            oa = int(160 + 95 * math.sin(frame_idx * 0.25 + sp))
            ov_draw.ellipse([ox - 3, oy - 1, ox + 3, oy + 1], fill=(255, 255, 255, oa))
            
    elif scene_idx == 9:
        # Animated shooting star streak!
        # From frame 15 to 45
        if 15 <= scene_frame <= 48:
            st_t = (scene_frame - 15) / 33.0
            sx = int(580 + st_t * 280)
            sy = int(180 + st_t * 190)
            tail_x = int(sx - 90)
            tail_y = int(sy - 60)
            ov_draw.line([(tail_x, tail_y), (sx, sy)], fill=(255, 255, 255, 240), width=3)
            ov_draw.line([(tail_x + 10, tail_y + 7), (sx, sy)], fill=(180, 220, 255, 180), width=5)
            ov_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 255, 255, 255))
            
    # Anime Cinematic Letterbox & Typography
    for y in range(HEIGHT - 85, HEIGHT):
        a = int(195 * ((y - (HEIGHT - 85)) / 85.0))
        ov_draw.line([(0, y), (WIDTH, y)], fill=(8, 12, 22, a))
        
    ov_draw.rectangle([(0, 0), (WIDTH, 14)], fill=(5, 8, 16, 240))
    ov_draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=(5, 8, 16, 240))
    
    act_tag, act_desc = SCENE_TITLES[scene_idx]
    ov_draw.rounded_rectangle([30, HEIGHT - 65, 150, HEIGHT - 35], radius=5, fill=(35, 75, 135, 230), outline=(120, 180, 255, 180), width=1)
    ov_draw.text((38, HEIGHT - 56), act_tag, fill=(220, 240, 255))
    ov_draw.text((165, HEIGHT - 57), act_desc, fill=(250, 250, 250))
    
    ov_draw.text((WIDTH - 270, 2), "SHINKAI AESTHETIC CINEMA", fill=(160, 210, 255))
    
    base_rgba = base_img.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    
    out_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_path, quality=88)
    return frame_idx

def main():
    print(f"Rendering 600 animated frames for Screenless Time anime across {cpu_count()} CPU cores...")
    with Pool(cpu_count()) as pool:
        results = pool.map(render_frame_task, range(TOTAL_FRAMES))
    print(f"✓ All {len(results)} frames successfully rendered to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
