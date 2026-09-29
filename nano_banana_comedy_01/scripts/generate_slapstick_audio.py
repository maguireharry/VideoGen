import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100
DURATION = 30.0 # Exactly 30 seconds
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "slapstick_sfx_track.wav")

left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

def add_tone(start_t, dur, freq, amp=0.3, wave_type="sine", decay=0.0):
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        cur_amp = amp * (1.0 - (i / samples) * decay)
        if wave_type == "sine":
            val = math.sin(2 * math.pi * freq * t)
        elif wave_type == "square":
            val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        elif wave_type == "triangle":
            val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
        elif wave_type == "saw":
            val = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        elif wave_type == "noise":
            val = random.uniform(-1.0, 1.0)
        else:
            val = math.sin(2 * math.pi * freq * t)
        left_channel[idx] += val * cur_amp
        right_channel[idx] += val * cur_amp

def add_slide(start_t, dur, f_start, f_end, amp=0.35, wave_type="sine"):
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    phase = 0.0
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        frac = i / samples
        freq = f_start + (f_end - f_start) * frac
        phase += 2 * math.pi * freq / SAMPLE_RATE
        val = math.sin(phase)
        if wave_type == "triangle":
            val = 2.0 * abs(2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0) - 1.0
        left_channel[idx] += val * amp * (1.0 - 0.2 * frac)
        right_channel[idx] += val * amp * (1.0 - 0.2 * frac)

def add_boing(start_t, dur=0.6, base_freq=180.0, amp=0.4):
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    phase = 0.0
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        # Wobble frequency around base
        mod = math.sin(2 * math.pi * 14.0 * t) * (base_freq * 0.4)
        freq = base_freq + mod + (120.0 * (1.0 - t / dur))
        phase += 2 * math.pi * freq / SAMPLE_RATE
        env = math.exp(-4.5 * t)
        val = math.sin(phase) * amp * env
        left_channel[idx] += val * 0.9
        right_channel[idx] += val * 1.1

def add_splat(start_t, dur=0.5, amp=0.5):
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-12.0 * t)
        noise = random.uniform(-1.0, 1.0)
        low_pop = math.sin(2 * math.pi * (140.0 - 100.0 * (t / dur)) * t)
        val = (noise * 0.6 + low_pop * 0.8) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

print("Synthesizing 30-second comedic cartoon soundtrack...")

# 1. Bouncy rhythmic cartoon bassline across all scenes
chords = [
    # Scene 1 (0-3s): C major bouncy groove
    [261.63, 329.63, 392.00, 523.25],
    # Scene 2 (3-6s): F major bouncy rush
    [349.23, 440.00, 523.25, 698.46],
    # Scene 3 (6-9s): Diminished horror suspense
    [220.00, 261.63, 311.13, 370.00],
    # Scene 4 (9-12s): Action fast funk G major
    [392.00, 493.88, 587.33, 783.99],
    # Scene 5 (12-15s): Sneaky tip-toe A minor
    [220.00, 261.63, 329.63, 440.00],
    # Scene 6 (15-18s): Slapstick chaos chromatic
    [246.94, 293.66, 349.23, 415.30],
    # Scene 7 (18-21s): Supercharged electric high energy
    [329.63, 415.30, 493.88, 659.25],
    # Scene 8 (21-24s): Ascending rocket fanfare
    [261.63, 329.63, 392.00, 523.25],
    # Scene 9 (24-27s): Funk disco groove
    [293.66, 369.99, 440.00, 587.33],
    # Scene 10 (27-30s): Grand finale & comic splat
    [261.63, 329.63, 392.00, 523.25]
]

# Generate bouncy cartoon melody and rhythmic walking bass
step_time = 0.25 # 16th/8th rhythm
total_steps = int(DURATION / step_time)

for step in range(total_steps):
    t = step * step_time
    scene_idx = min(int(t // 3.0), 9)
    chord = chords[scene_idx]
    
    # Bass note
    bass_freq = chord[0] * 0.5
    if step % 2 == 0:
        add_tone(t, 0.18, bass_freq, amp=0.15, wave_type="triangle", decay=0.4)
    else:
        add_tone(t, 0.14, bass_freq * 1.5, amp=0.12, wave_type="sine", decay=0.5)
    
    # Marimba / xylophone chirp
    note_idx = (step % 4)
    lead_freq = chord[note_idx]
    if scene_idx not in (2, 5, 9): # normal scenes have happy melody
        add_tone(t, 0.12, lead_freq, amp=0.10, wave_type="triangle", decay=0.7)

# --- Comedic Sound Effects synchronized to each 3-second scene ---

# Scene 1 (0-3s): Waking up, sunglasses glint "PING!" and confident giggle
add_tone(0.4, 0.25, 440.0, amp=0.15, wave_type="sine")
add_slide(1.2, 0.45, 300.0, 900.0, amp=0.25, wave_type="sine") # slide whistle up
add_tone(2.1, 0.35, 1760.0, amp=0.20, wave_type="sine", decay=0.8) # sparkle ping!

# Scene 2 (3-6s): Pole vault spring and zoom!
add_slide(3.5, 0.4, 250.0, 600.0, amp=0.25)
add_boing(4.2, dur=0.7, base_freq=220.0, amp=0.45) # Boing!
add_slide(4.8, 0.5, 800.0, 300.0, amp=0.25) # zoom whoosh

# Scene 3 (6-9s): Blender of Doom! Buzzing blades and panic siren
for st in [6.2, 6.8, 7.4, 8.0]:
    add_slide(st, 0.28, 400.0, 750.0, amp=0.22, wave_type="saw") # panic siren
    add_tone(st, 0.28, 90.0, amp=0.25, wave_type="square") # blender motor hum

# Scene 4 (9-12s): Action slide & wink
add_slide(9.3, 0.8, 1200.0, 200.0, amp=0.30, wave_type="noise") # skid slide
add_boing(10.5, dur=0.5, base_freq=350.0, amp=0.35)
add_tone(11.2, 0.3, 2093.0, amp=0.22, wave_type="sine", decay=0.8) # cheeky wink ping

# Scene 5 (12-15s): Sneaky monkey tip-toe & peel drop
for st in [12.2, 12.7, 13.2, 13.7]:
    add_tone(st, 0.10, 180.0, amp=0.25, wave_type="triangle", decay=0.9)
add_slide(14.1, 0.35, 600.0, 180.0, amp=0.28) # tactical drop whistle

# Scene 6 (15-18s): Monkey slip & whipped cream wipeout
add_slide(15.2, 0.6, 900.0, 150.0, amp=0.45, wave_type="sine") # cartoon slip whistle!
add_boing(15.9, dur=0.8, base_freq=160.0, amp=0.50) # wild 720 spin boing
add_splat(16.8, dur=0.7, amp=0.60) # WHIPPED CREAM SPLAT!

# Scene 7 (18-21s): Supercharged electric power-up
add_slide(18.2, 1.8, 120.0, 1400.0, amp=0.32, wave_type="saw") # charging hum
for z in range(6):
    add_tone(18.5 + z * 0.35, 0.08, random.uniform(900, 1800), amp=0.22, wave_type="square") # electric sparks

# Scene 8 (21-24s): Rocket launch!
for i in range(int(0.6 * SAMPLE_RATE)):
    idx = int(21.2 * SAMPLE_RATE) + i
    if idx < TOTAL_SAMPLES:
        left_channel[idx] += random.uniform(-0.15, 0.15) # fuse hiss
        right_channel[idx] += random.uniform(-0.15, 0.15)
add_slide(22.0, 1.6, 150.0, 1800.0, amp=0.45, wave_type="saw") # roaring rocket ascent!

# Scene 9 (24-27s): Zero-g space disco funky groove
disco_notes = [587.33, 659.25, 783.99, 880.00, 1046.50]
for d in range(12):
    dt = 24.1 + d * 0.22
    dnote = random.choice(disco_notes)
    add_tone(dt, 0.14, dnote, amp=0.18, wave_type="sine", decay=0.6)
    add_tone(dt, 0.06, 120.0, amp=0.20, wave_type="square") # disco kick

# Scene 10 (27-30s): Grand finale: superhero descent, slip whistle, comic SPLAT & bird chirps!
add_slide(27.2, 0.7, 1200.0, 350.0, amp=0.35, wave_type="sine") # falling divebomb
add_slide(28.0, 0.35, 300.0, 850.0, amp=0.45, wave_type="triangle") # sudden SLIP!
add_splat(28.4, dur=0.9, amp=0.75) # MEGA COMIC SPLAT!!
# Dizzy chirping cartoon birds
for bird_t in [28.9, 29.1, 29.3, 29.5, 29.7]:
    add_slide(bird_t, 0.12, 2200.0, 2600.0, amp=0.18, wave_type="sine")

# Master normalization to avoid any clipping
max_amp = max(max(abs(x) for x in left_channel), max(abs(x) for x in right_channel), 0.001)
scale = 30000.0 / max_amp if max_amp > 1.0 else 30000.0

with wave.open(output_path, "w") as wav_file:
    wav_file.setnchannels(2)
    wav_file.setsampwidth(2)
    wav_file.setframerate(SAMPLE_RATE)
    
    frames_data = bytearray()
    for i in range(TOTAL_SAMPLES):
        l_val = int(max(-32767, min(32767, left_channel[i] * scale)))
        r_val = int(max(-32767, min(32767, right_channel[i] * scale)))
        frames_data.extend(struct.pack("<hh", l_val, r_val))
    
    wav_file.writeframes(frames_data)

print(f"✓ Slapstick soundtrack successfully generated at: {output_path} ({len(frames_data)} bytes)")
