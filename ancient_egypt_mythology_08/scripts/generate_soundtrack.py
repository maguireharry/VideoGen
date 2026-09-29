import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100
DURATION = 25.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "soundtrack.wav")

left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

def clamp(val, min_v=-1.0, max_v=1.0):
    return max(min_v, min(max_v, val))

# 1. Mystical Low Temple Drone & Desert Wind
random.seed(1337)
wind_val = 0.0
for i in range(TOTAL_SAMPLES):
    t = i / SAMPLE_RATE
    white = random.uniform(-1.0, 1.0)
    wind_val = wind_val * 0.96 + white * 0.04
    drone_d = math.sin(2 * math.pi * 73.42 * t) * 0.12 # D2 root
    drone_a = math.sin(2 * math.pi * 110.0 * t) * 0.08 # A2 fifth
    shimmer = math.sin(2 * math.pi * 146.83 * t) * 0.04 # D3 octave
    left_channel[i] += (wind_val * 0.04 + drone_d + drone_a * 0.8 + shimmer)
    right_channel[i] += (wind_val * 0.04 + drone_d * 0.8 + drone_a + shimmer)

def add_darbuka_hit(start_t, amp=0.45, is_dum=True):
    """Deep Dum (bass) or crisp Tek (rim) darbuka drum hit"""
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.35 if is_dum else 0.15
    num_s = int(dur * SAMPLE_RATE)
    f0 = 90.0 if is_dum else 320.0
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp((-10.0 if is_dum else -28.0) * t)
        freq = f0 * math.exp(-15.0 * t) if is_dum else f0
        body = math.sin(2 * math.pi * freq * t)
        snap = random.uniform(-0.5, 0.5) * math.exp(-50.0 * t)
        val = (body + snap) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_sistrum_rattle(start_t, dur=0.18, amp=0.18):
    """Sacred Egyptian bronze sistrum rattle"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 1.8
        jingle = random.uniform(-1.0, 1.0) * math.sin(2 * math.pi * 5400.0 * t)
        val = jingle * amp * env
        left_channel[idx] += val * 1.1
        right_channel[idx] += val * 0.9

def add_nay_flute(start_t, dur, freq, amp=0.32, pan=0.5):
    """Haunting wooden Nay flute with breath vibrato"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        attack = min(1.0, t / 0.3)
        release = min(1.0, (dur - t) / 0.4)
        env = attack * release
        vibrato = math.sin(2 * math.pi * 4.8 * t) * (freq * 0.025) * min(1.0, t / 0.5)
        f = freq + vibrato
        breath = random.uniform(-0.15, 0.15)
        # Nay harmonics: strong fundamental + subtle 2nd & 3rd harmonic
        flute = math.sin(2 * math.pi * f * t) + 0.35 * math.sin(2 * math.pi * 2 * f * t) + 0.15 * math.sin(2 * math.pi * 3 * f * t)
        val = (flute + breath) * amp * env
        left_channel[idx] += val * (1.1 - pan * 0.2)
        right_channel[idx] += val * (0.9 + pan * 0.2)

def add_ra_sun_brass(start_t, dur, freq, amp=0.35):
    """Epic mythological bronze horn / divine blast"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        attack = min(1.0, t / 0.15)
        release = min(1.0, (dur - t) / 0.5)
        env = attack * release
        # Brass sawtooth
        brass = sum((math.sin(2 * math.pi * freq * h * t) / h) for h in range(1, 9)) * 0.3
        val = brass * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

# Rhythmic Darbuka & Sistrum groove (Bayati Maqam rhythm)
# Dum-Tek-Tek-Dum-Tek
rhythm_pattern = [0.0, 0.4, 0.65, 1.0, 1.4] # 1.8s loop
for cycle in range(14):
    cycle_start = cycle * 1.8
    if cycle_start + 1.8 > DURATION:
        break
    if cycle >= 2: # Start rhythm after intro drone
        add_darbuka_hit(cycle_start + 0.0, amp=0.38, is_dum=True)
        add_darbuka_hit(cycle_start + 0.4, amp=0.25, is_dum=False)
        add_sistrum_rattle(cycle_start + 0.5, dur=0.15, amp=0.15)
        add_darbuka_hit(cycle_start + 0.65, amp=0.22, is_dum=False)
        add_darbuka_hit(cycle_start + 1.0, amp=0.35, is_dum=True)
        add_darbuka_hit(cycle_start + 1.4, amp=0.26, is_dum=False)
        add_sistrum_rattle(cycle_start + 1.4, dur=0.2, amp=0.18)

# Nay flute melody in Egyptian Hijaz scale on D (D - Eb - F# - G - A - Bb - C - D)
# Frequencies: D4=293.66, Eb4=311.13, F#4=369.99, G4=392.00, A4=440.00, Bb4=466.16, C5=523.25, D5=587.33
melody = [
    (1.2, 2.5, 293.66), # D4
    (3.8, 1.8, 311.13), # Eb4
    (5.8, 2.6, 369.99), # F#4
    (8.6, 2.2, 392.00), # G4
    (11.0, 2.8, 440.00), # A4
    (14.0, 2.0, 466.16), # Bb4
    (16.2, 2.6, 523.25), # C5
    (19.0, 3.2, 587.33), # D5
    (22.4, 2.4, 440.00), # A4
]
for start, dur, freq in melody:
    add_nay_flute(start, dur, freq, amp=0.32, pan=0.5)

# Climactic Divine Brass during Ra vs Apep battle (Scene 7-8: ~15s - 20s)
add_ra_sun_brass(15.2, 2.8, 146.83, amp=0.35) # D3
add_ra_sun_brass(17.8, 3.2, 184.99, amp=0.4)  # F#3
add_ra_sun_brass(20.5, 3.5, 220.00, amp=0.42) # A3

# Master Normalization
max_amp = max(max(abs(x) for x in left_channel), max(abs(x) for x in right_channel), 0.001)
gain = 0.92 / max_amp

wav_file = wave.open(output_path, "wb")
wav_file.setnchannels(2)
wav_file.setsampwidth(2)
wav_file.setframerate(SAMPLE_RATE)

frames = bytearray()
for i in range(TOTAL_SAMPLES):
    t = i / SAMPLE_RATE
    fade = min(1.0, t / 0.6) * min(1.0, (DURATION - t) / 0.8)
    l = int(clamp(left_channel[i] * gain * fade) * 32767.0)
    r = int(clamp(right_channel[i] * gain * fade) * 32767.0)
    frames.extend(struct.pack("<hh", l, r))

wav_file.writeframes(frames)
wav_file.close()
print(f"Generated Egyptian Soundtrack: {output_path} ({os.path.getsize(output_path)} bytes)")
