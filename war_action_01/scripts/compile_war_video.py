import os
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRAMES_PATTERN = os.path.join(BASE_DIR, "frames", "frame_%04d.jpg")
AUDIO_FILE = os.path.join(BASE_DIR, "audio", "war_action_soundtrack.wav")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "output", "war_action_hardhitting.mp4")
OUTPUT_GIF = os.path.join(BASE_DIR, "output", "war_action_preview.gif")

os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)

print("=" * 60)
print("Compiling 30-second 20 FPS War Action Film with FFmpeg...")
print("=" * 60)

cmd = [
    "ffmpeg", "-y",
    "-framerate", "20",
    "-i", FRAMES_PATTERN,
    "-i", AUDIO_FILE,
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-r", "20",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_VIDEO
]

print("Executing FFmpeg encode...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"✓ Video successfully generated: {OUTPUT_VIDEO}")
    print(f"File size: {round(os.path.getsize(OUTPUT_VIDEO) / 1024 / 1024, 2)} MB")
else:
    print("FFmpeg error:", res.stderr)
    exit(1)

# Generate high-impact preview GIF
print("\nGenerating animated GIF preview for README...")
gif_cmd = [
    "ffmpeg", "-y",
    "-i", OUTPUT_VIDEO,
    "-vf", "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-t", "10",
    OUTPUT_GIF
]
res_gif = subprocess.run(gif_cmd, capture_output=True, text=True)
if res_gif.returncode == 0:
    print(f"✓ Animated preview GIF generated: {OUTPUT_GIF} ({round(os.path.getsize(OUTPUT_GIF) / 1024 / 1024, 2)} MB)")
