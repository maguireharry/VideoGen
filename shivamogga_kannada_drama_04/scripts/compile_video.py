import os
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCENES_DIR = os.path.join(BASE_DIR, "scenes")
AUDIO_FILE = os.path.join(BASE_DIR, "audio", "shivamogga_drama_soundtrack.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "shivamogga_kannada_drama.mp4")
OUTPUT_GIF = os.path.join(OUTPUT_DIR, "shivamogga_kannada_drama_preview.gif")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SCENES = [
    {
        "file": "scene1_tunga_dawn.png",
        "title": "ಅಧ್ಯಾಯ ೧ : ತುಂಗಾ ತೀರದ ಮುಂಜಾನೆ",
        "subtitle": "Act I: Dawn Upon the Sacred Tunga River — Shivamogga",
        "motion": "pan_right"
    },
    {
        "file": "scene2_malnad_courtyard.png",
        "title": "ಅಧ್ಯಾಯ ೨ : ನೆನಪುಗಳ ತೊಟ್ಟಿ ಮನೆ",
        "subtitle": "Act II: Echoes of the Malnad Courtyard & Heritage",
        "motion": "zoom_in"
    },
    {
        "file": "scene3_theatre_rehearsal.png",
        "title": "ಅಧ್ಯಾಯ ೩ : ರಂಗಭೂಮಿಯ ಕಾವ್ಯ ಸಂಘರ್ಷ",
        "subtitle": "Act III: Passion of the Rangamandira Stage Rehearsal",
        "motion": "zoom_center"
    },
    {
        "file": "scene4_jog_falls_cliff.png",
        "title": "ಅಧ್ಯಾಯ ೪ : ಜೋಗ ಜಲಪಾತದ ರೌದ್ರ ಗಾಂಭೀರ್ಯ",
        "subtitle": "Act IV: Confrontation Amidst the Thundering Jog Falls Mist",
        "motion": "pan_down"
    },
    {
        "file": "scene5_temple_reunion.png",
        "title": "ಅಧ್ಯಾಯ ೫ : ಭಾವಪೂರ್ಣ ಮಿಲನ",
        "subtitle": "Act V: Bhaavapoorna — Reunion Beneath the Sacred Banyan Tree",
        "motion": "zoom_out"
    }
]

FPS = 25
SCENE_DUR = 5.0
TOTAL_DUR = 25.0
TOTAL_FRAMES = int(FPS * TOTAL_DUR)
WIDTH = 1280
HEIGHT = 720
CROSSFADE_FRAMES = 15

# Load scene images
loaded_images = []
for sc in SCENES:
    img_path = os.path.join(SCENES_DIR, sc["file"])
    im = Image.open(img_path).convert("RGB")
    loaded_images.append(im)

def get_scene_frame(scene_idx, t_scene):
    """Generate dynamic Ken Burns frame with subtitle card and cinematic grade"""
    sc = SCENES[scene_idx]
    orig_img = loaded_images[scene_idx]
    ow, oh = orig_img.size
    
    # Progress from 0.0 to 1.0 within the scene
    p = t_scene / SCENE_DUR
    motion = sc["motion"]
    
    if motion == "zoom_in":
        zoom = 1.0 + 0.12 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx, cy = int(ow * 0.5), int(oh * 0.5)
    elif motion == "zoom_out":
        zoom = 1.12 - 0.12 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx, cy = int(ow * 0.5), int(oh * 0.5)
    elif motion == "pan_right":
        zoom = 1.08
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(cw * 0.5 + (ow - cw) * (0.2 + 0.6 * p))
        cy = int(oh * 0.5)
    elif motion == "pan_down":
        zoom = 1.08
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * 0.5)
        cy = int(ch * 0.5 + (oh - ch) * (0.2 + 0.6 * p))
    else: # zoom_center
        zoom = 1.0 + 0.10 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx, cy = int(ow * 0.5), int(oh * 0.5)
        
    left = max(0, min(ow - cw, int(cx - cw / 2)))
    top = max(0, min(oh - ch, int(cy - ch / 2)))
    cropped = orig_img.crop((left, top, left + cw, top + ch))
    resized = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    # Cinematic lower third overlay
    draw = ImageDraw.Draw(resized, "RGBA")
    
    # Gradient vignette at bottom
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT - 120, HEIGHT):
        alpha = int(180 * ((y - (HEIGHT - 120)) / 120.0))
        ov_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))
    
    # Top subtle letterbox bar
    ov_draw.rectangle([(0, 0), (WIDTH, 24)], fill=(0, 0, 0, 200))
    ov_draw.rectangle([(0, HEIGHT - 24), (WIDTH, HEIGHT)], fill=(0, 0, 0, 200))
    
    resized.paste(Image.alpha_composite(resized.convert("RGBA"), overlay).convert("RGB"))
    
    # Text overlay
    draw = ImageDraw.Draw(resized)
    
    # Primary Title (White with shadow)
    t_text = sc["title"]
    s_text = sc["subtitle"]
    
    # Shadow
    draw.text((42, HEIGHT - 82), t_text, fill=(0, 0, 0))
    draw.text((40, HEIGHT - 84), t_text, fill=(255, 230, 140))
    
    draw.text((42, HEIGHT - 52), s_text, fill=(0, 0, 0))
    draw.text((40, HEIGHT - 54), s_text, fill=(230, 230, 230))
    
    # Subtle timecode & title top right
    draw.text((WIDTH - 240, 6), "SHIVAMOGGA CINEMA 4K", fill=(200, 200, 200))
    
    return np.array(resized)

print("Rendering 25s Shivamogga Kannada Drama Video...")
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
    
    # Check if within crossfade zone to next scene
    frames_into_scene = int(t_sc * FPS)
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
