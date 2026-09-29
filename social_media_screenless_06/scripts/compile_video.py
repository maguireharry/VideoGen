import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCENES_DIR = os.path.join(BASE_DIR, "scenes")
AUDIO_FILE = os.path.join(BASE_DIR, "audio", "screenless_reconnect_soundtrack.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "social_media_screenless.mp4")
OUTPUT_GIF = os.path.join(OUTPUT_DIR, "social_media_screenless_preview.gif")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SCENES = [
    {
        "file": "scene1_digital_doomscroll.png",
        "title": "第１幕 : 終わりのないスクロール (The Infinite Doomscroll)",
        "subtitle": "Trapped in the cold neon glow: toxic alerts, anxiety, and digital isolation",
        "motion": "zoom_in_phone"
    },
    {
        "file": "scene2_powering_off.png",
        "title": "第２幕 : 電源を切る決意 (The Choice to Power Off)",
        "subtitle": "Turning the screen black, closing eyes, and inhaling the morning light",
        "motion": "zoom_center"
    },
    {
        "file": "scene3_forest_sunlight.png",
        "title": "第３幕 : 生きている森の呼吸 (Awakening in the Living Forest)",
        "subtitle": "Barefoot on dew-kissed moss, looking up at ancient cedars and golden sunbeams",
        "motion": "pan_up_canopy"
    },
    {
        "file": "scene4_real_connection.png",
        "title": "第４幕 : 本物の繋がりと笑顔 (Genuine Human Presence)",
        "subtitle": "Shared laughter, hot tea in ceramic cups, and real conversation under the sky",
        "motion": "pan_right_friends"
    },
    {
        "file": "scene5_ocean_sunset.png",
        "title": "第５幕 : デスコネクトとリコネクト (Disconnect to Reconnect)",
        "subtitle": "Peace at the twilight cliffside, feeling the ocean breeze and endless stars",
        "motion": "zoom_out_horizon"
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
    
    if motion == "zoom_in_phone":
        zoom = 1.0 + 0.12 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * 0.50)
        cy = int(oh * (0.50 + 0.05 * p))
    elif motion == "zoom_center":
        zoom = 1.0 + 0.10 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * 0.50)
        cy = int(oh * 0.50)
    elif motion == "pan_up_canopy":
        zoom = 1.10
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * 0.50)
        cy = int(oh * (0.60 - 0.12 * p))
    elif motion == "pan_right_friends":
        zoom = 1.08
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(cw * 0.5 + (ow - cw) * (0.2 + 0.6 * p))
        cy = int(oh * 0.50)
    else: # zoom_out_horizon
        zoom = 1.12 - 0.12 * p
        cw, ch = int(ow / zoom), int(oh / zoom)
        cx = int(ow * (0.50 - 0.03 * p))
        cy = int(oh * 0.50)
        
    left = max(0, min(ow - cw, int(cx - cw / 2)))
    top = max(0, min(oh - ch, int(cy - ch / 2)))
    cropped = orig_img.crop((left, top, left + cw, top + ch))
    resized = cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    # Elegant anime cinematic lower-third overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for y in range(HEIGHT - 110, HEIGHT):
        alpha = int(185 * ((y - (HEIGHT - 110)) / 110.0))
        ov_draw.line([(0, y), (WIDTH, y)], fill=(10, 15, 25, alpha))
        
    # Top and bottom ultra-thin cinematic lines
    ov_draw.rectangle([(0, 0), (WIDTH, 20)], fill=(5, 8, 15, 220))
    ov_draw.rectangle([(0, HEIGHT - 20), (WIDTH, HEIGHT)], fill=(5, 8, 15, 220))
    
    resized.paste(Image.alpha_composite(resized.convert("RGBA"), overlay).convert("RGB"))
    
    draw = ImageDraw.Draw(resized)
    t_text = sc["title"]
    s_text = sc["subtitle"]
    
    # Shadow and main text
    draw.text((42, HEIGHT - 76), t_text, fill=(0, 0, 0))
    draw.text((40, HEIGHT - 78), t_text, fill=(200, 235, 255))
    
    draw.text((42, HEIGHT - 46), s_text, fill=(0, 0, 0))
    draw.text((40, HEIGHT - 48), s_text, fill=(240, 240, 240))
    
    # Top banner
    draw.text((WIDTH - 290, 4), "SHINKAI AESTHETIC CINEMA", fill=(180, 210, 240))
    
    return np.array(resized)

print("Rendering 25s Screenless Time Anime Video...")
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
