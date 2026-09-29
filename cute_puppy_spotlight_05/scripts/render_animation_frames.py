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
    "scene01_basket_yawn.png",
    "scene02_first_clumsy_steps.png",
    "scene03_bubble_wonder.png",
    "scene04_bubble_pop_surprise.png",
    "scene05_garden_butterfly.png",
    "scene06_butterfly_on_nose.png",
    "scene07_autumn_ball.png",
    "scene08_leaf_pile_peekaboo.png",
    "scene09_fireplace_dream.png",
    "scene10_dreaming_paws.png"
]

SCENE_TITLES = [
    ("SCENE 01", "Morning Yawn in the Sunlit Basket"),
    ("SCENE 02", "First Clumsy Steps — Whoops!"),
    ("SCENE 03", "A Giant Iridescent Bubble Appears"),
    ("SCENE 04", "*POP!* The Surprise on the Nose"),
    ("SCENE 05", "Chasing the Glowing Blue Butterfly"),
    ("SCENE 06", "The Butterfly Lands on the Nose!"),
    ("SCENE 07", "Rolling the Squeaky Ball through Autumn Leaves"),
    ("SCENE 08", "Peek-a-Boo! Leaf on the Head"),
    ("SCENE 09", "Cozy Fireplace Snuggle & Teddy Bear"),
    ("SCENE 10", "Dreaming of Infinite Green Fields")
]

# Preload images
loaded_scenes = []
for f in SCENE_FILES:
    p = os.path.join(SCENES_DIR, f)
    img = Image.open(p).convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    loaded_scenes.append(img)

def draw_bubble(draw, x, y, r, alpha=180, phase=0.0):
    # Iridescent soap bubble
    color_ring = (
        int(200 + 45 * math.sin(phase)),
        int(220 + 35 * math.cos(phase)),
        int(255)
    )
    # Outer ring
    draw.ellipse([x - r, y - r, x + r, y + r], outline=(*color_ring, alpha), width=3)
    # Inner specular highlight
    hr = max(2, int(r * 0.28))
    hx = x - int(r * 0.4)
    hy = y - int(r * 0.4)
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 255, 255, min(255, alpha + 50)))
    # Secondary rim glint
    hr2 = max(1, int(r * 0.12))
    hx2 = x + int(r * 0.45)
    hy2 = y + int(r * 0.45)
    draw.ellipse([hx2 - hr2, hy2 - hr2, hx2 + hr2, hy2 + hr2], fill=(255, 230, 255, min(200, alpha)))

def draw_butterfly(draw, cx, cy, wing_scale=1.0, size=24, angle=0.0):
    # Wing flapping: wing_scale goes from 0.2 to 1.0
    w_width = int(size * abs(wing_scale))
    w_height = int(size * 1.3)
    
    # Left wing
    left_poly = [
        (cx, cy),
        (cx - w_width, cy - w_height),
        (cx - int(w_width * 1.3), cy),
        (cx - int(w_width * 0.7), cy + int(w_height * 0.6))
    ]
    # Right wing
    right_poly = [
        (cx, cy),
        (cx + w_width, cy - w_height),
        (cx + int(w_width * 1.3), cy),
        (cx + int(w_width * 0.7), cy + int(w_height * 0.6))
    ]
    draw.polygon(left_poly, fill=(80, 210, 255, 220), outline=(220, 250, 255, 255))
    draw.polygon(right_poly, fill=(80, 210, 255, 220), outline=(220, 250, 255, 255))
    # Body
    draw.line([(cx, cy - int(w_height * 0.4)), (cx, cy + int(w_height * 0.5))], fill=(30, 80, 140, 255), width=3)
    # Antennae
    draw.line([(cx, cy - int(w_height * 0.4)), (cx - 6, cy - int(w_height * 0.7))], fill=(200, 240, 255, 200), width=2)
    draw.line([(cx, cy - int(w_height * 0.4)), (cx + 6, cy - int(w_height * 0.7))], fill=(200, 240, 255, 200), width=2)

def draw_leaf(draw, cx, cy, size=18, rot=0.0, color=(240, 110, 20)):
    # Maple leaf diamond shape
    points = []
    for i in range(6):
        a = rot + i * (math.pi / 3.0)
        r = size if i % 2 == 0 else size * 0.45
        points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(points, fill=color)

def render_frame_task(frame_idx):
    scene_idx = frame_idx // FRAMES_PER_SCENE
    scene_frame = frame_idx % FRAMES_PER_SCENE
    t = scene_frame / float(FRAMES_PER_SCENE) # 0.0 to 1.0
    
    base_img = loaded_scenes[scene_idx].copy()
    ow, oh = base_img.size
    
    # Camera Dynamics per scene
    zoom = 1.0
    pan_x = 0
    pan_y = 0
    shake_x = 0
    shake_y = 0
    
    if scene_idx == 0:
        # Slow warm zoom into morning yawn
        zoom = 1.0 + 0.08 * t
        pan_y = int(-10 * t)
    elif scene_idx == 1:
        # Clumsy tumble camera bounce
        bounce = math.sin(t * math.pi * 3.0) * math.exp(-2.5 * t)
        zoom = 1.04 + 0.04 * bounce
        shake_x = int(5 * bounce)
        shake_y = int(8 * bounce)
    elif scene_idx == 2:
        # Head tilt tracking slow pan
        zoom = 1.05
        pan_x = int(35 * math.sin(t * math.pi))
    elif scene_idx == 3:
        # Bubble pop surprise snap zoom
        if t < 0.40:
            zoom = 1.0 + 0.06 * (t / 0.40)
        else:
            # Impact pop bounce
            pop_t = (t - 0.40) / 0.60
            decay = math.exp(-6.0 * pop_t)
            zoom = 1.06 + 0.05 * decay
            shake_x = int(random.uniform(-8, 8) * decay)
            shake_y = int(random.uniform(-8, 8) * decay)
    elif scene_idx == 4:
        # Fast garden chase pan
        zoom = 1.08
        pan_x = int(-60 * t)
    elif scene_idx == 5:
        # Butterfly on nose: gentle micro-breathing
        zoom = 1.0 + 0.03 * math.sin(t * math.pi * 2.0)
    elif scene_idx == 6:
        # Autumn ball slide: tracking speed pan
        zoom = 1.06
        pan_x = int(50 * (1.0 - t))
    elif scene_idx == 7:
        # Peek-a-boo: sudden spring-up bounce
        spring = math.sin(t * math.pi * 0.5)
        zoom = 1.02 + 0.06 * spring
        pan_y = int(25 * (1.0 - spring))
    elif scene_idx == 8:
        # Fireplace snuggle: slow intimate zoom
        zoom = 1.0 + 0.05 * t
    elif scene_idx == 9:
        # Dreaming puppy: gentle floating drift
        zoom = 1.04
        pan_y = int(12 * math.sin(t * math.pi * 2.0))
        
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
        
    # RGBA overlay layer for rich animated VFX
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # Scene-Specific Dynamic Animation Effects
    if scene_idx == 0:
        # Floating morning golden dust motes
        for i in range(25):
            seed = i * 137
            mx = int((seed + frame_idx * 1.5) % WIDTH)
            my = int((seed * 3 + math.sin(frame_idx * 0.08 + i) * 35) % HEIGHT)
            alpha = int(120 + 80 * math.sin(frame_idx * 0.1 + i))
            ov_draw.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=(255, 235, 170, alpha))
            
    elif scene_idx == 1:
        # Tile floor light reflections and cute comic speed dashes
        for s in range(5):
            lx = 500 + s * 45 + int(t * 80)
            ly = 520 + s * 15
            ov_draw.line([(lx, ly), (lx + 25, ly)], fill=(255, 255, 255, 160), width=3)
            
    elif scene_idx == 2:
        # 8 floating iridescent soap bubbles drifting across screen
        for b in range(8):
            bx = int(350 + b * 110 + math.sin(t * math.pi * 2.0 + b) * 45)
            by = int(180 + b * 55 + math.cos(t * math.pi * 2.0 + b * 1.5) * 30 - t * 40)
            br = int(22 + 10 * math.sin(b * 2.1))
            draw_bubble(ov_draw, bx, by, br, alpha=170, phase=t * 6.0 + b)
            
    elif scene_idx == 3:
        # Bubble pop splash particles!
        # At t >= 0.40, splash ring of 30 droplets exploding outward from nose (cx=640, cy=350)
        if t < 0.40:
            # Bubble wobbling on nose
            wobble_r = int(55 + 6 * math.sin(t * 35.0))
            draw_bubble(ov_draw, 640, 340, wobble_r, alpha=210, phase=t * 12.0)
        else:
            pop_t = (t - 0.40) / 0.60
            for d in range(32):
                angle = d * (math.pi / 16.0)
                speed = 90 + (d % 5) * 35
                dist = pop_t * speed
                dx = int(640 + dist * math.cos(angle))
                dy = int(340 + dist * math.sin(angle) + 0.5 * 180 * (pop_t ** 2)) # gravity
                alpha = max(0, int(230 * (1.0 - pop_t)))
                dr = max(1, int(4 * (1.0 - pop_t * 0.7)))
                ov_draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=(220, 245, 255, alpha))
                
    elif scene_idx == 4:
        # Animated flying blue butterfly fluttering in sinusoidal flight path
        bf_t = t * 3.0
        bf_x = int(250 + t * 750)
        bf_y = int(320 - math.sin(t * math.pi * 4.0) * 90)
        wing_flap = math.sin(frame_idx * 1.2)
        draw_butterfly(ov_draw, bf_x, bf_y, wing_scale=wing_flap, size=26)
        # Trailing fairy sparkle dust
        for sp in range(12):
            sp_x = bf_x - int(sp * 14 + random.uniform(-6, 6))
            sp_y = bf_y + int(random.uniform(-15, 15))
            sp_a = max(0, int(200 - sp * 16))
            ov_draw.ellipse([sp_x - 2, sp_y - 2, sp_x + 2, sp_y + 2], fill=(160, 230, 255, sp_a))
            
    elif scene_idx == 5:
        # Butterfly perched on nose gently flapping wings + emitting gentle magic aura
        bf_x, bf_y = 780, 275
        wing_flap = 0.4 + 0.6 * abs(math.sin(frame_idx * 0.35))
        draw_butterfly(ov_draw, bf_x, bf_y, wing_scale=wing_flap, size=24)
        # Twinkling sparkles
        for sp in range(15):
            a = frame_idx * 0.1 + sp * (math.pi * 2.0 / 15.0)
            rad = 30 + 15 * math.sin(frame_idx * 0.15 + sp)
            sx = int(bf_x + rad * math.cos(a))
            sy = int(bf_y + rad * math.sin(a))
            sa = int(140 + 100 * math.sin(frame_idx * 0.2 + sp))
            ov_draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 200, sa))
            
    elif scene_idx == 6:
        # Rolling squeaky ball & 25 swirling autumn leaves in the breeze
        for leaf in range(25):
            lx = int((leaf * 73 + t * 400) % (WIDTH + 100) - 50)
            ly = int(450 + leaf * 10 + math.sin(t * math.pi * 3.0 + leaf) * 35)
            rot = t * 6.0 + leaf
            color = (235, 100 + (leaf % 4) * 30, 25, 220)
            draw_leaf(ov_draw, lx, ly, size=15, rot=rot, color=color)
            
    elif scene_idx == 7:
        # Peekaboo swirling leaves vortex
        for leaf in range(20):
            angle = t * 4.0 + leaf * (math.pi * 2.0 / 20.0)
            r_dist = 180 + 60 * math.sin(t * 3.0 + leaf)
            lx = int(640 + r_dist * math.cos(angle))
            ly = int(380 + r_dist * math.sin(angle) * 0.5)
            rot = angle * 2.0
            ov_draw.ellipse([lx - 4, ly - 4, lx + 4, ly + 4], fill=(255, 160, 40, 210))
            
    elif scene_idx == 8:
        # Warm crackling fireplace embers & sparks rising
        for em in range(30):
            seed = em * 91
            ex = int(580 + (seed % 140) + math.sin(frame_idx * 0.15 + em) * 25)
            ey = int(480 - ((seed + frame_idx * 4) % 280))
            alpha = max(0, int(255 * (ey - 200) / 280.0))
            ov_draw.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 210, 80, alpha))
            
    elif scene_idx == 9:
        # Dream bubbles floating and pulsating upwards
        for db in range(6):
            db_x = int(400 + db * 130 + math.sin(t * math.pi * 2.0 + db) * 25)
            db_y = int(220 + math.cos(t * math.pi * 2.0 + db) * 20 - t * 30)
            draw_bubble(ov_draw, db_x, db_y, 35, alpha=180, phase=t * 4.0 + db)
            
    # Pixar Style Vignette & Cinematic Badge
    for y in range(HEIGHT - 85, HEIGHT):
        a = int(190 * ((y - (HEIGHT - 85)) / 85.0))
        ov_draw.line([(0, y), (WIDTH, y)], fill=(15, 20, 30, a))
        
    # Ultra-thin top/bottom cinema borders
    ov_draw.rectangle([(0, 0), (WIDTH, 14)], fill=(10, 15, 25, 230))
    ov_draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=(10, 15, 25, 230))
    
    # Pixar Badge pill in bottom left
    s_tag, s_desc = SCENE_TITLES[scene_idx]
    ov_draw.rounded_rectangle([30, HEIGHT - 65, 120, HEIGHT - 35], radius=6, fill=(255, 180, 50, 230))
    ov_draw.text((38, HEIGHT - 56), s_tag, fill=(20, 20, 20))
    
    # Narrative text
    ov_draw.text((135, HEIGHT - 57), s_desc, fill=(255, 255, 255))
    
    # Studio top right tag
    ov_draw.text((WIDTH - 240, 2), "PIXAR 3D ANIMATION", fill=(255, 210, 120))
    
    # Composite overlay onto base frame
    base_rgba = base_img.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, overlay).convert("RGB")
    
    out_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx+1:04d}.jpg")
    composited.save(out_path, quality=88)
    return frame_idx

def main():
    print(f"Rendering 600 animated frames for Cute Puppy Spotlight across {cpu_count()} CPU cores...")
    with Pool(cpu_count()) as pool:
        results = pool.map(render_frame_task, range(TOTAL_FRAMES))
    print(f"✓ All {len(results)} frames successfully rendered to {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
