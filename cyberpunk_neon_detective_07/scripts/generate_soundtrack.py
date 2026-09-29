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

# 1. Rain ambience & low city rumble
random.seed(42)
rain_val = 0.0
for i in range(TOTAL_SAMPLES):
    t = i / SAMPLE_RATE
    # Brownian-like low rumble
    white = random.uniform(-1.0, 1.0)
    rain_val = rain_val * 0.92 + white * 0.08
    rumble = math.sin(2 * math.pi * 38.0 * t) * 0.08 + math.sin(2 * math.pi * 55.0 * t) * 0.05
    pan = 0.5 + 0.1 * math.sin(0.3 * t)
    left_channel[i] += (rain_val * 0.06 + rumble) * pan
    right_channel[i] += (rain_val * 0.06 + rumble) * (1.0 - pan)

def add_synthwave_bass(start_t, dur, freq, amp=0.3):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-3.5 * (t / dur)) * min(1.0, t / 0.02)
        # Sawtooth approximation with analog warmth
        saw = 0.0
        for h in range(1, 8):
            saw += (math.sin(2 * math.pi * freq * h * t) / h) * (0.9 ** h)
        val = saw * amp * env
        left_channel[idx] += val * 0.8
        right_channel[idx] += val * 0.8

def add_cyber_arpeggio(start_t, dur, freq, amp=0.2, pan=0.5):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-12.0 * t)
        # Pulse wave
        pulse = 1.0 if (t * freq) % 1.0 < 0.35 else -1.0
        val = pulse * amp * env
        left_channel[idx] += val * (1.0 - pan)
        right_channel[idx] += val * pan

def add_vangelis_lead(start_t, dur, freq, amp=0.25, pan=0.5):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        # Lush attack and release
        attack = min(1.0, t / 0.4)
        release = min(1.0, (dur - t) / 0.6)
        env = attack * release
        vibrato = math.sin(2 * math.pi * 5.2 * t) * (freq * 0.02) * min(1.0, t / 0.8)
        f = freq + vibrato
        s1 = math.sin(2 * math.pi * f * t)
        s2 = math.sin(2 * math.pi * (f * 1.004) * t)
        s3 = math.sin(2 * math.pi * (f * 0.996) * t)
        val = (s1 + s2 * 0.7 + s3 * 0.7) * 0.4 * amp * env
        left_channel[idx] += val * (1.2 - pan * 0.4)
        right_channel[idx] += val * (0.8 + pan * 0.4)

def add_cyber_snare(start_t, amp=0.3):
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.22
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-18.0 * t)
        noise = random.uniform(-1.0, 1.0)
        tone = math.sin(2 * math.pi * 180.0 * math.exp(-30.0 * t) * t)
        val = (noise * 0.7 + tone * 0.3) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_cyber_kick(start_t, amp=0.45):
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.3
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-14.0 * t)
        f = 140.0 * math.exp(-35.0 * t) + 42.0
        val = math.sin(2 * math.pi * f * t) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_police_siren_echo(start_t, dur=4.0, amp=0.12):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = min(1.0, t / 1.0) * min(1.0, (dur - t) / 1.0)
        siren_f = 650.0 + 200.0 * math.sin(2 * math.pi * 0.4 * t)
        pan = 0.2 + 0.6 * (t / dur)
        val = math.sin(2 * math.pi * siren_f * t) * amp * env
        left_channel[idx] += val * (1.0 - pan)
        right_channel[idx] += val * pan

# Build the 25-second cyberpunk progression
# Scenes 1-3 (0 - 7.5s): Monsoon alley, noir investigation
bass_notes = [65.41, 77.78, 87.31, 98.0] # C2, Eb2, F2, G2
tempo = 120 # 0.5s per beat
total_beats = int(DURATION / 0.5)

for b in range(total_beats):
    t_beat = b * 0.5
    note_idx = (b // 4) % len(bass_notes)
    root = bass_notes[note_idx]
    # Driving 16th-note bass
    for sub in range(2):
        t_sub = t_beat + sub * 0.25
        if b >= 4: # Kick in rhythmic bass after beat 4
            add_synthwave_bass(t_sub, 0.22, root, amp=0.26)
        # Hi-hat arpeggio
        arp_f = root * (2 ** (1 + (sub % 3)))
        add_cyber_arpeggio(t_sub, 0.12, arp_f, amp=0.08, pan=0.3 + 0.4 * (b % 2))

    # Drums kick in at beat 8 (4.0s)
    if 8 <= b < 44:
        if b % 2 == 0:
            add_cyber_kick(t_beat, amp=0.4)
        else:
            add_cyber_snare(t_beat, amp=0.28)

# Vangelis Melodic Lead lines
# Noir theme motif
lead_notes = [
    (1.0, 3.0, 261.63), # C4
    (4.2, 2.5, 311.13), # Eb4
    (7.0, 3.5, 392.00), # G4
    (11.0, 2.8, 349.23), # F4
    (14.0, 3.2, 466.16), # Bb4
    (17.5, 2.5, 523.25), # C5
    (20.2, 4.0, 392.00), # G4
]
for start, dur, freq in lead_notes:
    add_vangelis_lead(start, dur, freq, amp=0.28, pan=0.5)

# Siren echoes in distance
add_police_siren_echo(2.5, dur=6.0, amp=0.08)
add_police_siren_echo(15.0, dur=6.5, amp=0.1)

# Master normalization
max_amp = max(max(abs(x) for x in left_channel), max(abs(x) for x in right_channel), 0.001)
gain = 0.92 / max_amp

wav_file = wave.open(output_path, "wb")
wav_file.setnchannels(2)
wav_file.setsampwidth(2)
wav_file.setframerate(SAMPLE_RATE)

frames = bytearray()
for i in range(TOTAL_SAMPLES):
    # Gentle fade in / out
    t = i / SAMPLE_RATE
    fade = min(1.0, t / 0.5) * min(1.0, (DURATION - t) / 0.8)
    l = int(clamp(left_channel[i] * gain * fade) * 32767.0)
    r = int(clamp(right_channel[i] * gain * fade) * 32767.0)
    frames.extend(struct.pack("<hh", l, r))

wav_file.writeframes(frames)
wav_file.close()
print(f"Generated Cyberpunk Soundtrack: {output_path} ({os.path.getsize(output_path)} bytes)")
