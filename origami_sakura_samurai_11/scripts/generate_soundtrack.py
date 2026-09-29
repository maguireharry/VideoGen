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

# 1. Bamboo grove breeze & gentle temple wind
random.seed(888)
wind_val = 0.0
for i in range(TOTAL_SAMPLES):
    t = i / SAMPLE_RATE
    white = random.uniform(-1.0, 1.0)
    wind_val = wind_val * 0.97 + white * 0.03
    gust = math.sin(2 * math.pi * 0.15 * t) * 0.03
    left_channel[i] += (wind_val * 0.04 + gust)
    right_channel[i] += (wind_val * 0.04 + gust)

def add_koto_pluck(start_t, dur, freq, amp=0.35, pan=0.5):
    """Traditional Japanese 13-string Koto silk string pluck with pitch inflection"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-4.5 * t)
        # Subtle pitch bend (oshi-de technique)
        f_bend = freq * (1.0 + 0.02 * math.sin(2 * math.pi * 1.5 * t) * min(1.0, t / 0.2))
        # Koto string harmonics
        s1 = math.sin(2 * math.pi * f_bend * t)
        s2 = math.sin(2 * math.pi * (2 * f_bend) * t) * 0.4 * math.exp(-6.0 * t)
        s3 = math.sin(2 * math.pi * (3 * f_bend) * t) * 0.25 * math.exp(-10.0 * t)
        s4 = math.sin(2 * math.pi * (4 * f_bend) * t) * 0.15 * math.exp(-15.0 * t)
        pick = random.uniform(-0.5, 0.5) * math.exp(-80.0 * t)
        val = (s1 + s2 + s3 + s4 + pick) * amp * env
        left_channel[idx] += val * (1.15 - pan * 0.3)
        right_channel[idx] += val * (0.85 + pan * 0.3)

def add_shakuhachi_flute(start_t, dur, freq, amp=0.28, pan=0.5):
    """Expressive bamboo Shakuhachi flute with breathy overblowing"""
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        attack = min(1.0, t / 0.35)
        release = min(1.0, (dur - t) / 0.4)
        env = attack * release
        vibrato = math.sin(2 * math.pi * 4.5 * t) * (freq * 0.02) * min(1.0, t / 0.5)
        f = freq + vibrato
        breath = random.uniform(-0.25, 0.25) * (0.3 + 0.7 * math.exp(-8.0 * t))
        tone = math.sin(2 * math.pi * f * t) + 0.3 * math.sin(2 * math.pi * 2 * f * t) + 0.15 * math.sin(2 * math.pi * 3 * f * t)
        val = (tone + breath) * amp * env
        left_channel[idx] += val * (1.0 - pan)
        right_channel[idx] += val * pan

def add_taiko_drum(start_t, amp=0.5):
    """Deep thunderous Japanese Taiko drum boom"""
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.8
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-5.0 * t)
        # Deep frequency sweep
        f = 55.0 * math.exp(-12.0 * t) + 38.0
        drum = math.sin(2 * math.pi * f * t)
        crack = random.uniform(-0.6, 0.6) * math.exp(-40.0 * t)
        val = (drum * 0.8 + crack * 0.2) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_hyoshigi_clapper(start_t, amp=0.35):
    """Sharp wooden Kabuki / Dojo Hyoshigi clapper strike"""
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.1
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-35.0 * t)
        wood = math.sin(2 * math.pi * 1420.0 * t) * math.exp(-25.0 * t) + math.sin(2 * math.pi * 2850.0 * t) * 0.5
        val = wood * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

# Traditional Insen scale on D: D (293.66), Eb (311.13), G (392.00), A (440.00), C (523.25), D5 (587.33)
# Poetic Koto melody
koto_melody = [
    # Scene 1 & 2: Crane flight & bamboo bridge
    (0.6, 1.8, 293.66), (1.4, 1.5, 311.13), (2.2, 2.0, 392.00), (3.0, 2.5, 440.00),
    (4.2, 1.6, 523.25), (5.0, 1.8, 440.00), (5.8, 2.2, 392.00), (6.8, 2.5, 293.66),
    # Scene 3 & 4: Petal storm & ink dragon
    (7.8, 1.4, 311.13), (8.6, 1.5, 392.00), (9.4, 1.8, 440.00), (10.2, 2.2, 587.33),
    (11.2, 1.5, 523.25), (12.0, 1.6, 440.00), (12.8, 2.0, 392.00),
    # Scene 7 & 8: Crane flock & dragon dissolve
    (16.5, 1.5, 440.00), (17.2, 1.6, 523.25), (18.0, 2.0, 587.33), (19.0, 2.5, 622.25),
    # Scene 9 & 10: Sheath & Mt Fuji sunrise
    (20.5, 2.0, 523.25), (21.5, 2.2, 440.00), (22.5, 2.5, 392.00), (23.2, 3.0, 293.66),
]
for start, dur, freq in koto_melody:
    add_koto_pluck(start, dur, freq, amp=0.32, pan=random.uniform(0.3, 0.7))

# Shakuhachi Flute phrases
shakuhachi_phrases = [
    (1.0, 3.2, 440.00), # A4
    (4.5, 3.0, 523.25), # C5
    (8.0, 3.5, 392.00), # G4
    (13.5, 3.2, 587.33), # D5
    (17.5, 3.8, 523.25), # C5
    (21.0, 3.5, 440.00), # A4
]
for start, dur, freq in shakuhachi_phrases:
    add_shakuhachi_flute(start, dur, freq, amp=0.26, pan=0.5)

# Taiko Drum Impacts (Marking dramatic scene moments)
taiko_times = [0.0, 4.0, 7.5, 10.0, 12.5, 14.8, 15.0, 15.3, 17.5, 20.0]
for t_t in taiko_times:
    add_taiko_drum(t_t, amp=0.45)

# Hyoshigi Clappers (Kabuki drama beats)
hyoshigi_times = [0.2, 0.5, 7.3, 7.6, 12.3, 12.5, 14.6, 14.9, 20.2, 20.5]
for t_h in hyoshigi_times:
    add_hyoshigi_clapper(t_h, amp=0.32)

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
print(f"Generated Origami Sakura Samurai Soundtrack: {output_path} ({os.path.getsize(output_path)} bytes)")
