import os
import shutil
import subprocess
import numpy as np
from PIL import Image

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
CONTINUOUS_FRAMES_DIR = os.path.join(BASE_DIR, "frames_continuous")
AUDIO_FILE = os.path.join(BASE_DIR, "audio", "war_action_soundtrack.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

OUTPUT_4FPS_VIDEO = os.path.join(OUTPUT_DIR, "war_action_continuous.mp4")
OUTPUT_SMOOTH_VIDEO = os.path.join(OUTPUT_DIR, "war_action_continuous_smooth.mp4")
OUTPUT_GIF = os.path.join(OUTPUT_DIR, "war_action_continuous_preview.gif")

os.makedirs(CONTINUOUS_FRAMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("1. Extracting Descriptors for 600 War Action Frames...")
print("=" * 60)

frames_data = []
for i in range(1, 601):
    p = os.path.join(FRAMES_DIR, f"frame_{i:04d}.jpg")
    im = Image.open(p).convert("RGB")
    small = np.array(im.resize((64, 36)), dtype=np.float32) / 255.0
    r_hist, _ = np.histogram(small[:,:,0], bins=8, range=(0,1))
    g_hist, _ = np.histogram(small[:,:,1], bins=8, range=(0,1))
    b_hist, _ = np.histogram(small[:,:,2], bins=8, range=(0,1))
    hist = np.concatenate([r_hist, g_hist, b_hist]).astype(np.float32)
    hist /= (np.linalg.norm(hist) + 1e-6)
    frames_data.append((i, small, hist))

print(f"Loaded {len(frames_data)} frames.")

def sim(i1, i2):
    s1, h1 = frames_data[i1][1], frames_data[i1][2]
    s2, h2 = frames_data[i2][1], frames_data[i2][2]
    cos_sim = np.dot(h1, h2)
    mse = np.mean((s1 - s2)**2)
    return cos_sim - 2.5 * mse

print("\n2. Running Global Dynamic Programming Continuity Optimization (4 FPS = 120 Frames)...")
beat_quads = []
for beat in range(30):
    start = beat * 20
    end = (beat + 1) * 20
    w0 = list(range(start, start + 5))
    w1 = list(range(start + 5, start + 10))
    w2 = list(range(start + 10, start + 15))
    w3 = list(range(start + 15, end))
    
    quad_scores = []
    for i0 in w0:
        for i1 in w1:
            s01 = sim(i0, i1)
            for i2 in w2:
                s12 = sim(i1, i2)
                for i3 in w3:
                    s23 = sim(i2, i3)
                    intra_score = s01 + s12 + s23
                    quad_scores.append((intra_score, (i0, i1, i2, i3)))
    quad_scores.sort(key=lambda x: x[0], reverse=True)
    beat_quads.append([q for q in quad_scores[:12]])

dp = []
backtrack = []

dp.append([q[0] for q in beat_quads[0]])
backtrack.append([-1] * len(beat_quads[0]))

for b in range(1, 30):
    curr_dp = []
    curr_bt = []
    for curr_q_idx, (intra_score, curr_quad) in enumerate(beat_quads[b]):
        best_prev_score = -1e9
        best_prev_idx = -1
        for prev_q_idx, (prev_intra, prev_quad) in enumerate(beat_quads[b-1]):
            trans_score = sim(prev_quad[-1], curr_quad[0])
            total = dp[b-1][prev_q_idx] + trans_score + intra_score
            if total > best_prev_score:
                best_prev_score = total
                best_prev_idx = prev_q_idx
        curr_dp.append(best_prev_score)
        curr_bt.append(best_prev_idx)
    dp.append(curr_dp)
    backtrack.append(curr_bt)

best_end_idx = int(np.argmax(dp[-1]))
best_path_quads = [best_end_idx]
for b in range(29, 0, -1):
    best_path_quads.append(backtrack[b][best_path_quads[-1]])
best_path_quads.reverse()

selected_indices = []
for b, q_idx in enumerate(best_path_quads):
    selected_indices.extend(beat_quads[b][q_idx][1])

print(f"✓ Selected {len(selected_indices)} frames with optimal visual continuity across all 30 story beats.")
consec = [sim(selected_indices[i], selected_indices[i+1]) for i in range(len(selected_indices)-1)]
print(f"  Mean Continuity Score: {np.mean(consec):.3f} (Median: {np.median(consec):.3f})")

print("\n3. Exporting & Standardizing Selected Frames to 1376x768...")
for idx, f_idx in enumerate(selected_indices):
    orig_num = frames_data[f_idx][0]
    src_file = os.path.join(FRAMES_DIR, f"frame_{orig_num:04d}.jpg")
    dst_file = os.path.join(CONTINUOUS_FRAMES_DIR, f"frame_{idx+1:04d}.jpg")
    im = Image.open(src_file)
    if im.size != (1376, 768):
        im = im.resize((1376, 768), Image.Resampling.LANCZOS)
    im.save(dst_file, "JPEG", quality=88, optimize=True)

print(f"✓ Exported {len(selected_indices)} frames into {CONTINUOUS_FRAMES_DIR}")

print("\n4. Compiling 4 FPS Continuous Video with Synchronized Audio...")
cmd_4fps = [
    "ffmpeg", "-y",
    "-framerate", "4",
    "-i", os.path.join(CONTINUOUS_FRAMES_DIR, "frame_%04d.jpg"),
    "-i", AUDIO_FILE,
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "-r", "4",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_4FPS_VIDEO
]
subprocess.run(cmd_4fps, check=True)
print(f"✓ 4 FPS Video compiled: {OUTPUT_4FPS_VIDEO} ({round(os.path.getsize(OUTPUT_4FPS_VIDEO)/1024/1024, 2)} MB)")

print("\n5. Compiling Motion-Blended Cinematic Smooth Video...")
cmd_smooth = [
    "ffmpeg", "-y",
    "-i", OUTPUT_4FPS_VIDEO,
    "-vf", "minterpolate=fps=20:mi_mode=blend",
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    "-c:a", "copy",
    OUTPUT_SMOOTH_VIDEO
]
subprocess.run(cmd_smooth, check=True)
print(f"✓ Motion-Blended Video compiled: {OUTPUT_SMOOTH_VIDEO} ({round(os.path.getsize(OUTPUT_SMOOTH_VIDEO)/1024/1024, 2)} MB)")

print("\n6. Generating Preview Animated GIF...")
cmd_gif = [
    "ffmpeg", "-y",
    "-i", OUTPUT_SMOOTH_VIDEO,
    "-vf", "fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-t", "10",
    OUTPUT_GIF
]
subprocess.run(cmd_gif, check=True)
print(f"✓ Animated GIF preview generated: {OUTPUT_GIF} ({round(os.path.getsize(OUTPUT_GIF)/1024/1024, 2)} MB)")
print("Done!")
