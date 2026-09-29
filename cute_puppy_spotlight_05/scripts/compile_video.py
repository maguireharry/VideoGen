import os
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
AUDIO_FILE = os.path.join(BASE_DIR, "audio", "puppy_spotlight_soundtrack.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "cute_puppy_spotlight.mp4")
OUTPUT_GIF = os.path.join(OUTPUT_DIR, "cute_puppy_spotlight_preview.gif")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Compiling 600 animated frames into 24 FPS MP4...")
cmd_video = [
    "ffmpeg", "-y",
    "-r", "24",
    "-i", os.path.join(FRAMES_DIR, "frame_%04d.jpg"),
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
subprocess.run(cmd_video, check=True)
print(f"✓ Video compiled: {OUTPUT_VIDEO} ({round(os.path.getsize(OUTPUT_VIDEO)/1024/1024, 2)} MB)")

print("\nGenerating Animated GIF Preview...")
cmd_gif = [
    "ffmpeg", "-y",
    "-i", OUTPUT_VIDEO,
    "-vf", "fps=10,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-t", "12",
    OUTPUT_GIF
]
subprocess.run(cmd_gif, check=True)
print(f"✓ GIF generated: {OUTPUT_GIF} ({round(os.path.getsize(OUTPUT_GIF)/1024/1024, 2)} MB)")
print("Done!")
