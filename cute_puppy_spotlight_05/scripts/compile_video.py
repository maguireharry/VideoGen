import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCENES_DIR = os.path.join(BASE_DIR, "scenes")
AUDIO_FILE = os.path.join(BASE_DIR, "audio", "puppy_spotlight_soundtrack.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "cute_puppy_spotlight.mp4")
OUTPUT_GIF = os.path.join(OUTPUT_DIR, "cute_puppy_spotlight_preview.gif")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SCENES = [
    {
        "file": "scene1_basket_yawn.png",
        "title": "Act I : Waking Up in the Sunlit Basket",
        "subtitle": "Tiny golden paws, sweet sleepy yawn, and bright amber eyes",
        "motion": "zoom_in_face"
    },
    {
        "file": "scene2_bubble_wonder.png",
        "title": "Act II : The Floating Bubble Wonder",
        "subtitle": "A curious head tilt as iridescent rainbow bubbles drift past",
        "motion": "pan_up_bubble"
    },
    {
        "file": "scene3_garden_butterfly.png",
        "title": "Act III : The Joyful Garden Sprint",
        "subtitle": "Bounding through bright spring tulips chasing a glowing blue butterfly",
        "motion": "zoom_out_action"
    },
    {
        "file": "scene4_autumn_ball.png",
        "title": "Act IV : Golden Leaves & The Squeaky Ball",
        "subtitle": "Sliding through amber leaves with pure puppy glee and a bright red ball",
        "motion": "zoom_center"
    },
    {
        "file": "scene5_fireplace_dream.png",
        "title": "Act V : Cozy Fireplace Lullaby",
        "subtitle": "Curled up warm with a little teddy bear, drifting into sweet dreams",
        "motion": "zoom_in_snuggle"
    }
]

FPS = 25
SCENE_DUR = 5.0
TOTAL_DUR = 25.0
TOTAL_FRAMES = int(FPS * TOTAL_DUR)
WIDTH = 1280
HEIGHT = 720
CROSSFADE_FRAMES = 15

loaded_images = []
for sc in SCENES:
    img_path = os.path.join(SCENES_DIR, sc["file"])
    im = Image.open(img_path).convert("RGB")
    loaded_images.append(im)

def get_scene_frame(scene_idx, t_scene):
    sc = SCENES[scene_idx]
    orig_img = loaded_images[scene_idx]
    ow, oh = orig_img.size
    
    p = t_scene / SCENE_DUR
    motion = sc["motion"]
    
    if motion == "zoom_in_face":
        zoom = 1.0 + 0.14 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * (0.50 - 0.04 * p))
        cy = int(oh * (0.52 - 0.05 * p))
    elif motion == "pan_up_bubble":
        zoom = 1.08
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * (0.48 + 0.05 * p))
        cy = int(oh * (0.54 - 0.08 * p))
    elif motion == "zoom_out_action":
        zoom = 1.14 - 0.14 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * 0.50)
        cy = int(oh * 0.50)
    elif motion == "zoom_center":
        zoom = 1.0 + 0.10 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * 0.50)
        cy = int(oh * 0.50)
    else: # zoom_in_snuggle
        zoom = 1.0 + 0.12 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * (0.50 + 0.03 * p))
        cy = int(oh * (0.52 + 0.02 * p))
        
    left = max(0, min(ow - cw, int(cx - cw / 2)))
    top = max(0, min(oh - ch, int(cy - ch / 2)))
    cropped = orig_img.crop((left, top, left + cw, top + ch))
    resized = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    # Soft vignette overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT - 120, HEIGHT):
        alpha = int(175 * ((y - (HEIGHT - 120)) / 120.0))
        ov_draw.line([(0, y), (WIDTH, y)], fill=(20, 15, 30, alpha))
    
    # Rounded badge pill for title
    badge_x = 35
    badge_y = HEIGHT - 85
    ov_draw.rounded_rectangle([badge_x, badge_y, badge_x + 520, badge_y + 30], radius=15, fill=(255, 180, 80, 160))
    
    resized.paste(Image.alpha_composite(resized.convert("RGBA"), overlay).convert("RGB"))
    
    draw = ImageDraw.Draw(resized)
    t_text = sc["title"]
    s_text = sc["subtitle"]
    
    draw.text((badge_x + 18, badge_y + 6), t_text, fill=(30, 20, 10))
    draw.text((38, HEIGHT - 46), s_text, fill=(0, 0, 0))
    draw.text((36, HEIGHT - 48), s_text, fill=(255, 248, 230))
    
    # Watermark / Tag
    draw.text((WIDTH - 260, 10), "PIXAR 3D ANIMATION SPOTLIGHT", fill=(255, 255, 255))
    
    return np.array(resized)

print("Rendering 25s Cute Puppy Spotlight Video...")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", AUDIO_FILE,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_VIDEO
]

process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

for f_idx in range(TOTAL_FRAMES):
    t_total = f_idx / FPS
    sc_idx = min(len(SCENES) - 1, int(t_total / SCENE_DUR))
    t_sc = t_total - (sc_idx * SCENE_DUR)
    
    curr_frame = get_scene_frame(sc_idx, t_sc)
    
    frames_remaining = int((SCENE_DUR - t_sc) * FPS)
    if frames_remaining < CROSSFADE_FRAMES and sc_idx < len(SCENES) - 1:
        next_frame = get_scene_frame(sc_idx + 1, 0.0)
        alpha = (CROSSFADE_FRAMES - frames_remaining) / float(CROSSFADE_FRAMES)
        blended = (curr_frame * (1.0 - alpha) + next_frame * alpha).astype(np.uint8)
        process.stdin.write(blended.tobytes())
    else:
        process.stdin.write(curr_frame.tobytes())

process.stdin.close()
process.wait()

print(f"✓ Video compiled: {OUTPUT_VIDEO} ({round(os.path.getsize(OUTPUT_VIDEO)/1024/1024, 2)} MB)")

print("\nGenerating Animated GIF Preview...")
cmd_gif = [
    "ffmpeg", "-y",
    "-i", OUTPUT_VIDEO,
    "-vf", "fps=8,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-t", "10",
    OUTPUT_GIF
]
subprocess.run(cmd_gif, check=True)
print(f"✓ GIF generated: {OUTPUT_GIF} ({round(os.path.getsize(OUTPUT_GIF)/1024/1024, 2)} MB)")
print("Done!")
