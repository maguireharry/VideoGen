import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100
DURATION = 25.0  # 25.0 seconds (5 scenes x 5 seconds)
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "shivamogga_drama_soundtrack.wav")

left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

# Frequencies for Raag Bhoopali / Mohanam in C# (Sa = 138.59 Hz)
BASE_FREQ = 138.59

def add_tanpura_drone(start_t=0.0, dur=DURATION, amp=0.22):
    """Rich four-string meditative Indian Tanpura drone"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    strings = [
        (BASE_FREQ * 1.5, 0.25, 0.0),    # Pa
        (BASE_FREQ * 2.0, 0.35, 1.2),    # Sa high
        (BASE_FREQ * 2.0, 0.30, 2.4),    # Sa high
        (BASE_FREQ * 1.0, 0.40, 3.6),    # Sa low
    ]
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        val_l = 0.0
        val_r = 0.0
        for f, st_amp, phase_off in strings:
            cycle = (t + phase_off) % 4.8
            pluck_env = math.exp(-0.8 * cycle) * (1.0 + 0.3 * math.sin(2 * math.pi * 0.25 * t))
            wave_sig = (
                math.sin(2 * math.pi * f * t) * 0.6 +
                math.sin(2 * math.pi * f * 2 * t) * 0.25 +
                math.sin(2 * math.pi * f * 3 * t) * 0.15
            )
            val_l += wave_sig * st_amp * pluck_env
            val_r += wave_sig * st_amp * pluck_env * (0.9 + 0.2 * math.sin(2 * math.pi * 0.1 * t))
        left_channel[idx] += val_l * amp
        right_channel[idx] += val_r * amp

def add_bansuri_note(start_t, dur, freq, amp=0.35, vibrato_rate=5.2, vibrato_depth=0.015):
    """Expressive Indian bamboo flute (Bansuri) note with breath and micro-intonation"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        attack = 0.12
        release = 0.18
        if t < attack:
            env = (t / attack) ** 1.5
        elif t > (dur - release):
            env = max(0.0, (dur - t) / release)
        else:
            env = 1.0
        vib_amp = vibrato_depth * min(1.0, max(0.0, (t - 0.2) / 0.4))
        f_inst = freq * (1.0 + vib_amp * math.sin(2 * math.pi * vibrato_rate * t))
        h1 = math.sin(2 * math.pi * f_inst * t)
        h2 = 0.25 * math.sin(4 * math.pi * f_inst * t)
        h3 = 0.12 * math.sin(6 * math.pi * f_inst * t)
        breath = random.uniform(-0.06, 0.06) * (0.8 + 0.2 * math.sin(2 * math.pi * 3.0 * t))
        val = (h1 + h2 + h3 + breath) * amp * env
        left_channel[idx] += val * 0.95
        right_channel[idx] += val * 1.05

def add_tabla_bayan_bass(start_t, dur=0.8, start_f=120.0, end_f=75.0, amp=0.45):
    """Resonant low-pitch modulated Indian Tabla Bayan (Dagga) bass stroke"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-4.5 * t)
        progress = t / dur
        f = start_f * (1.0 - 0.4 * (progress ** 0.6)) + 15.0 * math.sin(2 * math.pi * 4.0 * t) * math.exp(-3.0 * t)
        val = math.sin(2 * math.pi * f * t) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val * 0.9

def add_tabla_dayan_treble(start_t, dur=0.35, freq=277.18, amp=0.35, harmonic=True):
    """Bright bell-like Tabla Dayan ring stroke"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-8.0 * t)
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.4 * math.sin(4 * math.pi * freq * t) if harmonic else 0.0
        val = (h1 + h2) * amp * env
        left_channel[idx] += val * 0.7
        right_channel[idx] += val * 1.3

def add_temple_bell(start_t, dur=3.5, freq=1108.73, amp=0.3):
    """Sacred bronze temple bell"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    partials = [(1.0, 0.5), (1.414, 0.3), (2.0, 0.25), (2.76, 0.18), (3.54, 0.1)]
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-1.4 * t)
        val = 0.0
        for ratio, p_amp in partials:
            val += math.sin(2 * math.pi * freq * ratio * t) * p_amp
        left_channel[idx] += val * amp * env * 1.1
        right_channel[idx] += val * amp * env * 0.9

def add_river_mist_ambience(start_t=0.0, dur=DURATION, amp=0.08):
    """Gentle Western Ghats river flow and monsoon mist ambience"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        r_l = random.uniform(-0.5, 0.5) * (0.5 + 0.3 * math.sin(2 * math.pi * 0.2 * t))
        r_r = random.uniform(-0.5, 0.5) * (0.5 + 0.3 * math.cos(2 * math.pi * 0.2 * t))
        left_channel[idx] += r_l * amp
        right_channel[idx] += r_r * amp

def add_cinematic_strings_chord(start_t, dur, chord_freqs, amp=0.25):
    """Warm orchestral string pad underpinning emotional crescendos"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        fade = min(1.0, t / 0.8) * min(1.0, (dur - t) / 0.8)
        val = 0.0
        for f in chord_freqs:
            s1 = math.sin(2 * math.pi * f * t)
            s2 = 0.3 * math.sin(2 * math.pi * (f * 1.003) * t)
            val += (s1 + s2)
        left_channel[idx] += val * (amp / len(chord_freqs)) * fade
        right_channel[idx] += val * (amp / len(chord_freqs)) * fade

print("Synthesizing 25.0s Shivamogga Kannada Drama Master Soundtrack...")

# 1. Foundation Drone & River Ambience
add_tanpura_drone(0.0, DURATION, amp=0.20)
add_river_mist_ambience(0.0, DURATION, amp=0.06)

# 2. Sacred Opening Bell
add_temple_bell(0.3, dur=4.5, freq=1108.73, amp=0.35)
add_temple_bell(10.0, dur=4.0, freq=880.0, amp=0.25)
add_temple_bell(20.0, dur=5.0, freq=1108.73, amp=0.38)

# 3. Flute Melody Lines (Raag Bhoopali / Mohanam: C#, D#, F, G#, A#, c#)
add_bansuri_note(1.0, 1.8, 277.18, amp=0.32) # Sa
add_bansuri_note(2.6, 1.2, 311.13, amp=0.34) # Re
add_bansuri_note(3.7, 1.5, 349.23, amp=0.36) # Ga

add_bansuri_note(5.2, 1.6, 415.30, amp=0.38) # Pa
add_bansuri_note(6.7, 1.2, 466.16, amp=0.36) # Dha
add_bansuri_note(7.8, 2.2, 554.37, amp=0.40) # Sa (high)

add_bansuri_note(10.2, 1.5, 466.16, amp=0.38)
add_bansuri_note(11.6, 1.4, 415.30, amp=0.38)
add_bansuri_note(12.9, 2.0, 349.23, amp=0.40)

add_cinematic_strings_chord(14.5, 5.5, [138.59, 207.65, 277.18, 349.23], amp=0.35)
add_bansuri_note(15.2, 1.8, 415.30, amp=0.42)
add_bansuri_note(16.9, 1.5, 466.16, amp=0.44)
add_bansuri_note(18.3, 2.0, 554.37, amp=0.45)

add_cinematic_strings_chord(20.0, 5.0, [138.59, 174.61, 207.65, 277.18, 415.30], amp=0.45)
add_bansuri_note(20.2, 2.2, 554.37, amp=0.45) # Sa high sustained
add_bansuri_note(22.3, 2.6, 415.30, amp=0.40) # Pa resolution

# 4. Tabla Rhythm
tempo_beats = [
    5.0, 5.8, 6.4, 7.0, 7.8, 8.4, 9.0, 9.8,
    10.5, 11.2, 12.0, 12.8, 13.5, 14.2,
    15.0, 15.6, 16.2, 16.8, 17.4, 18.0, 18.6, 19.2,
    20.0, 20.8, 21.6, 22.4, 23.2, 24.0
]
for idx, b in enumerate(tempo_beats):
    if idx % 3 == 0:
        add_tabla_bayan_bass(b, dur=0.6, start_f=125.0, end_f=75.0, amp=0.45)
        add_tabla_dayan_treble(b, dur=0.4, freq=277.18, amp=0.38)
    else:
        add_tabla_dayan_treble(b, dur=0.25, freq=277.18, amp=0.28)

max_amp = max(max(abs(x) for x in left_channel), max(abs(x) for x in right_channel), 0.001)
scale = 29500.0 / max_amp if max_amp > 0.1 else 29500.0

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

print(f"✓ Soundtrack generated: {output_path} ({len(frames_data)} bytes, {DURATION}s)")
