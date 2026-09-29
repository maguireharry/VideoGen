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

# 1. Gentle underwater ocean bed ambience (soft low-pass brown noise and warm water currents)
random.seed(777)
water_bed = 0.0
for i in range(TOTAL_SAMPLES):
    t = i / SAMPLE_RATE
    white = random.uniform(-1.0, 1.0)
    water_bed = water_bed * 0.95 + white * 0.05
    swell = math.sin(2 * math.pi * 0.2 * t) * 0.04
    left_channel[i] += (water_bed * 0.05 + swell)
    right_channel[i] += (water_bed * 0.05 + swell)

def add_tactile_marimba(start_t, dur, freq, amp=0.3, pan=0.5):
    """Warm tactile wooden marimba strike with harmonic overtones"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-8.0 * t)
        # Wooden mallet attack click
        click = random.uniform(-0.3, 0.3) * math.exp(-60.0 * t)
        # Marimba overtones (fundamental + 4th harmonic + 10th harmonic)
        f1 = math.sin(2 * math.pi * freq * t)
        f2 = math.sin(2 * math.pi * (freq * 4.0) * t) * 0.3 * math.exp(-20.0 * t)
        f3 = math.sin(2 * math.pi * (freq * 10.0) * t) * 0.1 * math.exp(-35.0 * t)
        val = (f1 + f2 + f3 + click) * amp * env
        left_channel[idx] += val * (1.2 - pan * 0.4)
        right_channel[idx] += val * (0.8 + pan * 0.4)

def add_pizzicato_bass(start_t, dur, freq, amp=0.35):
    """Playful bouncy pizzicato double-bass pluck"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-5.5 * t)
        body = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * (2 * freq) * t)
        pluck = random.uniform(-0.4, 0.4) * math.exp(-50.0 * t)
        val = (body + pluck) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_bubble_pop(start_t, f_start=400.0, amp=0.25, pan=0.5):
    """Resonant rising acoustic bubble chirp / pop"""
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.08
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 1.5
        # Exponential chirp up
        f = f_start * (1.0 + 2.5 * (t / dur))
        val = math.sin(2 * math.pi * f * t) * amp * env
        left_channel[idx] += val * (1.0 - pan)
        right_channel[idx] += val * pan

def add_magic_pearl_glock(start_t, freq, amp=0.22, pan=0.5):
    """Sparkling iridescent crystal bell chime"""
    start_i = int(start_t * SAMPLE_RATE)
    dur = 1.4
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-3.5 * t)
        f1 = math.sin(2 * math.pi * freq * t)
        f2 = math.sin(2 * math.pi * (freq * 2.76) * t) * 0.2
        val = (f1 + f2) * amp * env
        left_channel[idx] += val * (1.0 - pan)
        right_channel[idx] += val * pan

# Cheerful Bouncy 110 BPM Marimba Waltz / Duet
# In C Major / Pentatonic: C4 (261.63), D4 (293.66), E4 (329.63), G4 (392.00), A4 (440.00), C5 (523.25)
marimba_riffs = [
    # Act 1 & 2: Surface splash & reef exploration
    (0.4, 261.63), (0.8, 329.63), (1.2, 392.00), (1.6, 523.25),
    (2.0, 440.00), (2.4, 392.00), (2.8, 329.63), (3.4, 293.66),
    (4.0, 261.63), (4.4, 329.63), (4.8, 392.00), (5.2, 440.00),
    (5.8, 523.25), (6.4, 587.33), (7.0, 659.25), (7.6, 523.25),
    # Act 3: Twilight descent & jellyfish dance
    (9.0, 392.00), (9.5, 329.63), (10.0, 293.66), (10.5, 329.63),
    (11.2, 440.00), (11.8, 523.25), (12.4, 587.33), (13.0, 659.25),
    (14.0, 783.99), (14.5, 659.25), (15.0, 523.25), (15.5, 440.00),
    # Act 4: Shipwreck & treasure discovery
    (17.0, 523.25), (17.4, 587.33), (17.8, 659.25), (18.2, 783.99),
    (18.8, 880.00), (19.4, 1046.5), (20.0, 783.99),
    # Act 5: Sunset return
    (21.2, 659.25), (21.8, 523.25), (22.4, 392.00), (23.0, 261.63),
]
for t_m, f_m in marimba_riffs:
    add_tactile_marimba(t_m, 0.45, f_m, amp=0.28, pan=0.3 + 0.4 * (int(t_m * 2) % 2))

# Pizzicato walking bass
bass_prog = [
    (0.4, 130.81), (1.2, 164.81), (2.0, 196.00), (2.8, 146.83),
    (4.0, 130.81), (4.8, 164.81), (5.8, 196.00), (6.8, 220.00),
    (9.0, 196.00), (10.0, 164.81), (11.2, 220.00), (12.4, 261.63),
    (14.0, 196.00), (15.0, 164.81), (17.0, 130.81), (18.2, 196.00),
    (20.0, 261.63), (21.2, 196.00), (22.4, 130.81)
]
for t_b, f_b in bass_prog:
    add_pizzicato_bass(t_b, 0.5, f_b, amp=0.36)

# Whimsical Bubble Pops throughout the voyage
for b in range(28):
    t_pop = 1.0 + b * 0.8 + random.uniform(-0.2, 0.2)
    if t_pop < DURATION - 1.0:
        f_pop = random.uniform(450.0, 1100.0)
        p_pop = random.uniform(0.15, 0.85)
        add_bubble_pop(t_pop, f_start=f_pop, amp=random.uniform(0.18, 0.28), pan=p_pop)

# Magic pearl shimmering chimes (Act 4 & 5: 18s - 24s)
pearl_chimes = [
    (18.2, 1046.5), (18.6, 1174.66), (19.0, 1318.51), (19.5, 1567.98),
    (20.2, 1760.0), (20.8, 2093.0), (21.5, 1567.98), (22.5, 1318.51),
]
for t_c, f_c in pearl_chimes:
    add_magic_pearl_glock(t_c, f_c, amp=0.22, pan=random.uniform(0.3, 0.7))

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
    fade = min(1.0, t / 0.5) * min(1.0, (DURATION - t) / 0.7)
    l = int(clamp(left_channel[i] * gain * fade) * 32767.0)
    r = int(clamp(right_channel[i] * gain * fade) * 32767.0)
    frames.extend(struct.pack("<hh", l, r))

wav_file.writeframes(frames)
wav_file.close()
print(f"Generated Claymation Underwater Soundtrack: {output_path} ({os.path.getsize(output_path)} bytes)")
