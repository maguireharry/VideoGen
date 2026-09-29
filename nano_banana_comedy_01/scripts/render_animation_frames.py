import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing import Pool, cpu_count

WIDTH = 1280
HEIGHT = 720
TOTAL_FRAMES = 600
FRAMES_PER_SCENE = 60

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEYFRAMES_DIR = os.path.join(BASE_DIR, "keyframes")
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

# Preload and resize keyframes to standard 1280x720
KEYFRAME_FILES = [
    "scene_01_awakening.png",
    "scene_02_fruit_bowl_escape.png",
    "scene_03_blender_horror.png",
    "scene_04_action_slide.png",
    "scene_05_monkey_ambush.png",
    "scene_06_monkey_slip.png",
    "scene_07_supercharged_banana.png",
    "scene_08_rocket_launch.png",
    "scene_09_space_disco.png",
    "scene_10_banana_slip_splat.png"
]

def load_keyframes():
    images = []
    for f in KEYFRAME_FILES:
        path = os.path.join(KEYFRAMES_DIR, f)
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            # Center crop or resize to 1280x720
            img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
            images.append(img)
        else:
            # Fallback placeholder if missing
            img = Image.new("RGB", (WIDTH, HEIGHT), (255, 220, 50))
            images.append(img)
    return images

KEYFRAME_IMAGES = load_keyframes()

def draw_comic_bubble(draw, text, x, y, bg_color=(255, 255, 255), border_color=(0, 0, 0), text_color=(0, 0, 0), font_size=28, padding=12):
    font = get_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    rect = [x - padding, y - padding, x + tw + padding, y + th + padding]
    # Draw drop shadow
    draw.rounded_rectangle([rect[0] + 4, rect[1] + 4, rect[2] + 4, rect[3] + 4], radius=12, fill=(0, 0, 0, 160))
    # Draw background bubble
    draw.rounded_rectangle(rect, radius=12, fill=bg_color, outline=border_color, width=3)
    # Draw text
    draw.text((x, y), text, font=font, fill=text_color)

def draw_sparkle(draw, cx, cy, radius, color, rotation=0.0):
    points = []
    for i in range(8):
        angle = rotation + i * (math.pi / 4.0)
        r = radius if i % 2 == 0 else radius * 0.35
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, fill=color)

def render_frame(frame_idx):
    # 0-indexed frame
    scene_idx = frame_idx // FRAMES_PER_SCENE
    scene_frame = frame_idx % FRAMES_PER_SCENE
    t = scene_frame / float(FRAMES_PER_SCENE) # 0.0 to 1.0

    base_img = KEYFRAME_IMAGES[scene_idx].copy()
    
    # --- Camera Transform (Zoom, Pan, Shake) ---
    zoom = 1.0
    pan_x = 0
    pan_y = 0
    shake_x = 0
    shake_y = 0

    if scene_idx == 0:
        # Scene 1: Slow confident zoom-in on sunglasses
        zoom = 1.0 + 0.12 * t
        pan_y = int(-15 * t)
    elif scene_idx == 1:
        # Scene 2: Pole vault jump squash and fast pan
        pan_x = int(-40 * t)
        zoom = 1.0 + 0.08 * math.sin(t * math.pi)
    elif scene_idx == 2:
        # Scene 3: Blender horror: rapid vibration jitter!
        jitter_amp = 3.0 + 7.0 * t
        shake_x = int(random.uniform(-jitter_amp, jitter_amp))
        shake_y = int(random.uniform(-jitter_amp, jitter_amp))
        zoom = 1.0 + 0.10 * t
    elif scene_idx == 3:
        # Scene 4: Action slide: horizontal speed drift
        pan_x = int(50 * (1.0 - t))
        zoom = 1.04
    elif scene_idx == 4:
        # Scene 5: Monkey ambush: suspenseful creep
        pan_x = int(25 * math.sin(t * math.pi * 0.5))
        zoom = 1.02 + 0.05 * t
    elif scene_idx == 5:
        # Scene 6: Monkey slip & 720 spin into cream: shock shake at impact
        if t > 0.4:
            shake_amp = max(0, 15.0 * (1.0 - (t - 0.4) / 0.6))
            shake_x = int(random.uniform(-shake_amp, shake_amp))
            shake_y = int(random.uniform(-shake_amp, shake_amp))
        zoom = 1.0 + 0.15 * math.sin(t * math.pi)
    elif scene_idx == 6:
        # Scene 7: Supercharged banana: electric pulse vibration
        pulse = math.sin(t * math.pi * 12.0)
        zoom = 1.05 + 0.04 * pulse
        shake_x = int(random.uniform(-3, 3))
        shake_y = int(random.uniform(-3, 3))
    elif scene_idx == 7:
        # Scene 8: Rocket launch: camera tracks upwards with blast shake
        pan_y = int(-60 * (t ** 1.5))
        shake_x = int(random.uniform(-4, 4))
        shake_y = int(random.uniform(-4, 4))
        zoom = 1.0 + 0.10 * t
    elif scene_idx == 8:
        # Scene 9: Zero-g space disco: gentle cosmic floating wobble
        pan_x = int(20 * math.sin(t * 2 * math.pi))
        pan_y = int(15 * math.cos(t * 2 * math.pi))
        zoom = 1.03 + 0.03 * math.sin(t * 4 * math.pi)
    elif scene_idx == 9:
        # Scene 10: Comic Splat: fast drop, massive impact shockwave
        if t < 0.45:
            pan_y = int(80 * (t / 0.45))
        else:
            # Impact thud shake
            impact_decay = math.exp(-8.0 * (t - 0.45))
            shake_x = int(random.uniform(-25, 25) * impact_decay)
            shake_y = int(random.uniform(-25, 25) * impact_decay)
            zoom = 1.0 + 0.06 * impact_decay

    # Apply transformation
    if zoom != 1.0 or pan_x != 0 or pan_y != 0 or shake_x != 0 or shake_y != 0:
        zw = int(WIDTH * zoom)
        zh = int(HEIGHT * zoom)
        # Rescale
        scaled = base_img.resize((zw, zh), Image.Resampling.BILINEAR)
        # Crop back to WIDTH, HEIGHT with offsets
        crop_x = (zw - WIDTH) // 2 + pan_x + shake_x
        crop_y = (zh - HEIGHT) // 2 + pan_y + shake_y
        crop_x = max(0, min(zw - WIDTH, crop_x))
        crop_y = max(0, min(zh - HEIGHT, crop_y))
        base_img = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    draw = ImageDraw.Draw(base_img)

    # --- Scene-Specific Comedic Animation Overlays ---

    if scene_idx == 0:
        # Scene 1: Title card & sunglasses glint
        draw_comic_bubble(draw, "🍌 NANO BANANA 2.0 🍌", 380, 40, bg_color=(255, 230, 40), border_color=(40, 20, 0), font_size=36, padding=14)
        draw_comic_bubble(draw, "MISSION: ESCAPE THE BOWL!", 420, 105, bg_color=(255, 255, 255), border_color=(0, 0, 0), font_size=24, padding=8)
        
        # Sunglasses glint sparkle (frames 20-50)
        if 20 <= scene_frame <= 50:
            sp_t = (scene_frame - 20) / 30.0
            sp_r = 16 + 14 * math.sin(sp_t * math.pi)
            draw_sparkle(draw, 640 + int(sp_t * 60), 380, sp_r, (255, 255, 255), rotation=sp_t * math.pi * 2)

    elif scene_idx == 1:
        # Scene 2: Pole vault action lines & comic burst
        draw_comic_bubble(draw, "POLE-VAULT PARKOUR!", 420, 45, bg_color=(255, 120, 50), text_color=(255, 255, 255), font_size=34)
        draw_comic_bubble(draw, "*WHOOOOSH!*", 880, 220, bg_color=(255, 255, 100), font_size=28)
        
        # Action speed lines
        for l in range(8):
            lx = (frame_idx * 45 + l * 160) % WIDTH
            ly = 150 + l * 60
            draw.line([(lx, ly), (lx + 90, ly)], fill=(255, 255, 255, 180), width=4)

    elif scene_idx == 2:
        # Scene 3: Blender horror: warning strobe and Looney Tunes panic
        strobe = int(abs(math.sin(t * math.pi * 6.0)) * 120)
        # Red warning borders
        draw.rectangle([0, 0, WIDTH, 16], fill=(220 + strobe // 4, 20, 20))
        draw.rectangle([0, HEIGHT - 16, WIDTH, HEIGHT], fill=(220 + strobe // 4, 20, 20))
        draw_comic_bubble(draw, "⚠️ DANGER: SMOOTHIE OF DOOM! ⚠️", 320, 40, bg_color=(255, 50, 50), text_color=(255, 255, 255), font_size=32)
        
        buzz_jitter = int(random.uniform(-4, 4))
        draw_comic_bubble(draw, "NOT THE BLENDER!! 😱", 200 + buzz_jitter, 260 + buzz_jitter, bg_color=(255, 255, 255), text_color=(200, 0, 0), font_size=32)
        draw_comic_bubble(draw, "VRRRRRRRRR!", 850 - buzz_jitter, 180 + buzz_jitter, bg_color=(255, 240, 50), font_size=30)

    elif scene_idx == 3:
        # Scene 4: Action slide under blades
        draw_comic_bubble(draw, "ACTION SLIDE! 😎", 480, 45, bg_color=(50, 180, 255), text_color=(255, 255, 255), font_size=34)
        draw_comic_bubble(draw, "*TOO SLICK TO BLEND!*", 750, 560, bg_color=(255, 255, 255), font_size=26)
        
        # Sparks along bottom counter
        for s in range(10):
            sx = int(random.uniform(300, 800))
            sy = int(random.uniform(580, 640))
            sr = random.randint(3, 7)
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, random.randint(180, 240), 30))

    elif scene_idx == 4:
        # Scene 5: Monkey ambush & tactical peel
        draw_comic_bubble(draw, "HUNGRY CHEF MONKEY AMBUSH!", 340, 40, bg_color=(255, 180, 50), text_color=(0, 0, 0), font_size=32)
        draw_comic_bubble(draw, "MONKEY: 'OOH OOH AHH?!' 🍴", 680, 180, bg_color=(255, 255, 255), font_size=26)
        draw_comic_bubble(draw, "⚠️ TACTICAL PEEL DROPPED!", 160, 560, bg_color=(255, 240, 40), font_size=28)
        
        # Animated targeting reticle on monkey
        tx, ty = 850, 320
        draw.ellipse([tx - 40, ty - 40, tx + 40, ty + 40], outline=(255, 50, 50), width=3)
        draw.line([(tx - 55, ty), (tx + 55, ty)], fill=(255, 50, 50), width=2)
        draw.line([(tx, ty - 55), (tx, ty + 55)], fill=(255, 50, 50), width=2)

    elif scene_idx == 5:
        # Scene 6: Monkey slip & whipped cream wipeout
        draw_comic_bubble(draw, "💥 S L I I I I P ! ! 💥", 440, 40, bg_color=(255, 60, 60), text_color=(255, 255, 255), font_size=42, padding=16)
        draw_comic_bubble(draw, "*720° MIDAIR WIPEOUT!*", 180, 200, bg_color=(255, 230, 50), font_size=28)
        
        if scene_frame >= 25:
            draw_comic_bubble(draw, "*FACEPLANT IN WHIPPED CREAM!* 🍨", 400, 620, bg_color=(255, 255, 255), font_size=26)
            # Whipped cream splatters expanding
            cr_t = (scene_frame - 25) / 35.0
            for i in range(14):
                angle = i * (2 * math.pi / 14.0)
                dist = 60 + 260 * cr_t
                cx = 640 + int(dist * math.cos(angle))
                cy = 440 + int(dist * math.sin(angle) * 0.7)
                cr = int(12 + 18 * math.sin(cr_t * math.pi))
                draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255), outline=(220, 220, 240), width=2)

    elif scene_idx == 6:
        # Scene 7: Supercharged banana: electric bolts & power aura
        draw_comic_bubble(draw, "⚡ OVER 9000mg POTASSIUM! ⚡", 340, 40, bg_color=(255, 220, 0), text_color=(0, 0, 0), font_size=36)
        draw_comic_bubble(draw, "SUPERCHARGED NANO BANANA!", 420, 105, bg_color=(0, 0, 0), text_color=(255, 255, 100), font_size=24)
        
        # Electric lightning arcs
        for _ in range(5):
            lx1 = random.randint(450, 750)
            ly1 = random.randint(250, 550)
            lx2 = lx1 + random.randint(-80, 80)
            ly2 = ly1 + random.randint(-80, 80)
            mid_x = (lx1 + lx2) // 2 + random.randint(-25, 25)
            mid_y = (ly1 + ly2) // 2 + random.randint(-25, 25)
            col = random.choice([(255, 255, 100), (100, 240, 255), (255, 255, 255)])
            draw.line([(lx1, ly1), (mid_x, mid_y), (lx2, ly2)], fill=col, width=3)

    elif scene_idx == 7:
        # Scene 8: Rocket launch
        draw_comic_bubble(draw, "🚀 NANO-X BOTTLE ROCKET BLASTOFF! 🚀", 280, 40, bg_color=(255, 100, 40), text_color=(255, 255, 255), font_size=34)
        draw_comic_bubble(draw, "NEXT STOP: ORBIT!", 500, 105, bg_color=(255, 255, 255), font_size=24)
        
        # Rocket flame exhaust particles
        for p in range(16):
            px = int(random.uniform(560, 680))
            py = int(random.uniform(480, 700))
            pr = random.randint(8, 24)
            color = random.choice([(255, 60, 20), (255, 180, 20), (255, 240, 100), (200, 200, 200)])
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=color)

    elif scene_idx == 8:
        # Scene 9: Zero-g space disco
        draw_comic_bubble(draw, "🕺 INTERGALACTIC BANANA DISCO 🕺", 320, 40, bg_color=(180, 50, 255), text_color=(255, 255, 255), font_size=34)
        draw_comic_bubble(draw, "GROOVIN' IN LOW EARTH ORBIT", 440, 105, bg_color=(255, 255, 255), font_size=22)
        
        # Twinkling space stars
        for st_idx in range(25):
            st_x = (st_idx * 51 + 73) % WIDTH
            st_y = (st_idx * 37 + 109) % (HEIGHT - 120) + 60
            twinkle = math.sin((frame_idx * 0.2) + st_idx)
            if twinkle > 0:
                s_size = int(3 + 5 * twinkle)
                s_col = (255, 255, 255) if st_idx % 3 == 0 else ((255, 240, 100) if st_idx % 3 == 1 else (150, 220, 255))
                draw_sparkle(draw, st_x, st_y, s_size, s_col, rotation=frame_idx * 0.05)

    elif scene_idx == 9:
        # Scene 10: Slapstick hero landing & peel slip splat
        if scene_frame < 25:
            draw_comic_bubble(draw, "HERO LANDING RETURN!", 450, 45, bg_color=(50, 180, 255), text_color=(255, 255, 255), font_size=32)
        else:
            # Comic SPLAT punchline!
            draw_comic_bubble(draw, "💥 S P L A T ! ! 💥", 420, 50, bg_color=(255, 40, 40), text_color=(255, 255, 255), font_size=46, padding=18)
            draw_comic_bubble(draw, "SLIPPED ON HIS OWN PEEL! 🍌🤦‍♂️", 380, 130, bg_color=(255, 230, 40), font_size=28)
            
            # Dizzy yellow stars orbiting head
            star_angle = (scene_frame - 25) * 0.35
            for si in range(4):
                sa = star_angle + si * (math.pi / 2.0)
                star_x = 640 + int(90 * math.cos(sa))
                star_y = 380 + int(35 * math.sin(sa))
                draw_sparkle(draw, star_x, star_y, 14, (255, 240, 20), rotation=sa)

        # Final Closing Iris & End Card on frames 45-60
        if scene_frame >= 40:
            fade_p = (scene_frame - 40) / 20.0
            iris_r = int(max(WIDTH, HEIGHT) * (1.0 - fade_p * 0.7))
            
            # Overlay end card
            draw_comic_bubble(draw, "🎬 THE END - STAY SLIPPY! 🍌", 350, 580, bg_color=(0, 0, 0), text_color=(255, 230, 40), border_color=(255, 255, 255), font_size=32)
            draw_comic_bubble(draw, "Generated with Nano Banana 2 (Gemini 3.1 Flash Image)", 420, 640, bg_color=(255, 255, 255), font_size=18, padding=6)

    # Save output frame
    out_filename = f"frame_{frame_idx + 1:04d}.png"
    out_path = os.path.join(FRAMES_DIR, out_filename)
    base_img.save(out_path, "PNG", optimize=True)
    return frame_idx + 1

def main():
    print("=" * 60)
    print(f"Rendering all {TOTAL_FRAMES} comedy animation frames @ 20 FPS (1280x720)...")
    print(f"Utilizing {cpu_count()} CPU cores for parallel rendering")
    print("=" * 60)

    with Pool(processes=cpu_count()) as pool:
        for idx in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=10):
            if idx % 60 == 0:
                print(f"Progress: [{idx}/{TOTAL_FRAMES}] frames rendered ({idx // 20}s / 30s)")

    print(f"✓ Successfully rendered all {TOTAL_FRAMES} frames in {FRAMES_DIR}!")

if __name__ == "__main__":
    main()
