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
output_path = os.path.join(output_dir, "puppy_spotlight_soundtrack.wav")

left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

def add_pizzicato_string(start_t, freq, dur=0.35, amp=0.30):
    """Bouncy orchestral pizzicato violin / cello pluck"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-14.0 * t)
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.5 * math.sin(4 * math.pi * freq * t)
        h3 = 0.25 * math.sin(6 * math.pi * freq * t)
        h4 = 0.12 * math.sin(8 * math.pi * freq * t)
        pluck = random.uniform(-0.15, 0.15) * math.exp(-35.0 * t)
        val = (h1 + h2 + h3 + h4 + pluck) * amp * env
        left_channel[idx] += val * 0.95
        right_channel[idx] += val * 1.05

def add_marimba_xylophone(start_t, freq, dur=0.4, amp=0.28):
    """Playful wooden marimba / bright xylophone strike"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-9.0 * t)
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.35 * math.sin(2 * math.pi * (freq * 2.76) * t)
        h3 = 0.15 * math.sin(2 * math.pi * (freq * 5.4) * t)
        strike = math.sin(2 * math.pi * 1200.0 * t) * math.exp(-60.0 * t) * 0.3
        val = (h1 + h2 + h3 + strike) * amp * env
        left_channel[idx] += val * 1.1
        right_channel[idx] += val * 0.9

def add_glockenspiel_bell(start_t, freq, dur=1.2, amp=0.25):
    """Magical sparkling glockenspiel fairy bell"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-3.5 * t)
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.2 * math.sin(4 * math.pi * freq * t)
        val = (h1 + h2) * amp * env
        left_channel[idx] += val * 0.85
        right_channel[idx] += val * 1.15

def add_puppy_chirp_bark(start_t, amp=0.4):
    """Adorable high-pitched puppy yip / playful bark"""
    start_idx = int(start_t * SAMPLE_RATE)
    dur = 0.22
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        # Formant pitch envelope: starts high (650Hz), scoops to 820Hz, drops to 520Hz
        if t < 0.08:
            f = 650.0 + (t / 0.08) * 170.0
        else:
            f = 820.0 - ((t - 0.08) / 0.14) * 300.0
        env = math.sin(math.pi * (t / dur)) ** 1.8
        voice = (
            math.sin(2 * math.pi * f * t) * 0.6 +
            math.sin(4 * math.pi * f * t) * 0.3 +
            math.sin(6 * math.pi * f * t) * 0.15 +
            random.uniform(-0.1, 0.1)
        )
        val = voice * amp * env
        left_channel[idx] += val * 1.05
        right_channel[idx] += val * 0.95

def add_warm_flute_staccato(start_t, freq, dur=0.35, amp=0.25):
    """Playful orchestral concert flute note"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        attack = 0.04
        release = 0.1
        if t < attack:
            env = t / attack
        elif t > (dur - release):
            env = (dur - t) / release
        else:
            env = 1.0
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.15 * math.sin(4 * math.pi * freq * t)
        breath = random.uniform(-0.04, 0.04)
        val = (h1 + h2 + breath) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_fireplace_crackle(start_t, dur=5.0, amp=0.12):
    """Cozy ambient living room fireplace crackle & soft warmth"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        # Random crackle pops
        pop = 0.0
        if random.random() < 0.0018:
            pop = random.uniform(0.3, 0.8)
        rumble = math.sin(2 * math.pi * 60.0 * t) * 0.2 + random.uniform(-0.15, 0.15) * 0.4
        val = (rumble + pop) * amp * min(1.0, t / 0.8)
        left_channel[idx] += val * 0.9
        right_channel[idx] += val * 1.1

def add_warm_lullaby_strings(start_t, dur=5.5, amp=0.30):
    """Sweet gentle string quartet lullaby chord (F - C - G - C)"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    chord = [261.63, 329.63, 392.00, 523.25] # C Major warm
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        fade = min(1.0, t / 1.0) * min(1.0, (dur - t) / 1.2)
        val = 0.0
        for f in chord:
            val += math.sin(2 * math.pi * f * t) + 0.25 * math.sin(4 * math.pi * f * t)
        left_channel[idx] += val * (amp / len(chord)) * fade
        right_channel[idx] += val * (amp / len(chord)) * fade

print("Synthesizing 25.0s Pixar Cute Puppy Spotlight Master Soundtrack...")

# Musical Notes in Hz: C4=261.63, D4=293.66, E4=329.63, F4=349.23, G4=392.00, A4=440.00, B4=493.88, C5=523.25, D5=587.33, E5=659.25, G5=783.99

# Continuous bouncy pizzicato walking bass (0.0s to 20.0s)
tempo_step = 0.35  # ~170 BPM playful allegro
pizzi_notes = [
    130.81, 196.00, 164.81, 196.00, # C - G - E - G
    146.83, 196.00, 174.61, 196.00, # D - G - F - G
    164.81, 196.00, 220.00, 196.00, # E - G - A - G
    130.81, 196.00, 261.63, 196.00  # C - G - c - G
]
for step in range(54):
    t_p = step * tempo_step
    if t_p >= 19.5:
        break
    note_f = pizzi_notes[step % len(pizzi_notes)]
    add_pizzicato_string(t_p, note_f, dur=0.30, amp=0.28)

# Act 1 (0-5s): Waking Up & Yawn
add_glockenspiel_bell(0.5, 783.99, dur=1.5, amp=0.28)
add_warm_flute_staccato(1.0, 523.25, dur=0.3, amp=0.25)
add_warm_flute_staccato(1.4, 659.25, dur=0.3, amp=0.25)
add_warm_flute_staccato(1.8, 783.99, dur=0.5, amp=0.28)
add_puppy_chirp_bark(3.2, amp=0.35)

# Act 2 (5-10s): Floating Bubble Wonder
add_marimba_xylophone(5.2, 523.25, dur=0.3, amp=0.32)
add_marimba_xylophone(5.6, 659.25, dur=0.3, amp=0.32)
add_glockenspiel_bell(6.0, 1046.50, dur=1.8, amp=0.35)
add_marimba_xylophone(7.0, 783.99, dur=0.3, amp=0.30)
add_marimba_xylophone(7.4, 880.00, dur=0.3, amp=0.30)
add_glockenspiel_bell(8.0, 1318.51, dur=1.6, amp=0.32)
add_puppy_chirp_bark(8.8, amp=0.38)

# Act 3 (10-15s): Butterfly Sprint & Joyful Bounding
for idx, f in enumerate([523.25, 587.33, 659.25, 783.99, 880.00, 1046.50]):
    add_marimba_xylophone(10.2 + idx * 0.25, f, dur=0.25, amp=0.30)
add_puppy_chirp_bark(11.8, amp=0.42)
add_puppy_chirp_bark(12.3, amp=0.45)
add_glockenspiel_bell(13.2, 1174.66, dur=1.4, amp=0.30)
add_warm_flute_staccato(13.8, 783.99, dur=0.4, amp=0.28)

# Act 4 (15-20s): Autumn Leaves & Squeaky Ball Slide
add_marimba_xylophone(15.2, 659.25, dur=0.3, amp=0.35)
add_marimba_xylophone(15.6, 783.99, dur=0.3, amp=0.35)
add_marimba_xylophone(16.0, 1046.50, dur=0.4, amp=0.38)
add_puppy_chirp_bark(16.6, amp=0.40)
add_glockenspiel_bell(17.2, 1318.51, dur=1.5, amp=0.35)
add_marimba_xylophone(18.0, 880.00, dur=0.4, amp=0.30)
add_marimba_xylophone(18.6, 783.99, dur=0.5, amp=0.28)

# Act 5 (20-25s): Cozy Fireplace Bedtime Lullaby
add_fireplace_crackle(19.5, dur=5.5, amp=0.15)
add_warm_lullaby_strings(19.8, dur=5.2, amp=0.35)
add_glockenspiel_bell(20.5, 783.99, dur=2.0, amp=0.25)
add_glockenspiel_bell(22.0, 523.25, dur=2.5, amp=0.22)

# Master normalization
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

print(f"✓ Puppy soundtrack generated: {output_path} ({len(frames_data)} bytes, {DURATION}s)")
