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

# Authentic Chiptune Waveforms
def pulse_wave(freq, t, duty=0.5):
    cycle = (t * freq) % 1.0
    return 1.0 if cycle < duty else -1.0

def triangle_wave(freq, t):
    cycle = (t * freq) % 1.0
    return 4.0 * abs(cycle - 0.5) - 1.0

def add_square_lead(start_t, dur, freq, duty=0.5, amp=0.25, pan=0.5):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        # ADSR envelope
        attack = min(1.0, t / 0.01)
        decay = math.exp(-2.5 * (t / dur))
        env = attack * decay
        val = pulse_wave(freq, t, duty) * amp * env
        left_channel[idx] += val * (1.0 - pan)
        right_channel[idx] += val * pan

def add_triangle_bass(start_t, dur, freq, amp=0.35):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-1.8 * (t / dur))
        val = triangle_wave(freq, t) * amp * env
        left_channel[idx] += val * 0.9
        right_channel[idx] += val * 0.9

def add_chiptune_noise_drum(start_t, dur=0.08, amp=0.25, is_snare=False):
    start_i = int(start_t * SAMPLE_RATE)
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp((-18.0 if is_snare else -35.0) * t)
        noise = random.choice([-1.0, 1.0])
        val = noise * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_chiptune_kick(start_t, amp=0.38):
    start_i = int(start_t * SAMPLE_RATE)
    dur = 0.18
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = math.exp(-22.0 * t)
        f = 130.0 * math.exp(-45.0 * t) + 35.0
        val = triangle_wave(f, t) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_limit_break_sfx(start_t, amp=0.4):
    start_i = int(start_t * SAMPLE_RATE)
    dur = 1.2
    num_s = int(dur * SAMPLE_RATE)
    for j in range(num_s):
        idx = start_i + j
        if idx >= TOTAL_SAMPLES:
            break
        t = j / SAMPLE_RATE
        env = min(1.0, t / 0.1) * math.exp(-3.0 * t)
        f = 300.0 + 1200.0 * (t / dur)
        val = pulse_wave(f, t, 0.25) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_coin_fanfare(start_t, amp=0.3):
    notes = [987.77, 1318.51] # B5, E6
    add_square_lead(start_t, 0.08, notes[0], duty=0.5, amp=amp, pan=0.3)
    add_square_lead(start_t + 0.08, 0.35, notes[1], duty=0.5, amp=amp, pan=0.7)

# 140 BPM Heroic Arcade Progression (0.428s per beat)
BPM = 140
beat_dur = 60.0 / BPM # ~0.4285s
step_dur = beat_dur / 2.0 # 8th note ~0.214s

# Progression chords: Am -> F -> C -> G
prog_roots = [110.0, 87.31, 130.81, 98.0] # A2, F2, C3, G2
total_steps = int(DURATION / step_dur)

random.seed(999)
for s in range(total_steps):
    t_step = s * step_dur
    if t_step + step_dur > DURATION:
        break
    chord_idx = (s // 16) % len(prog_roots)
    root = prog_roots[chord_idx]

    # Bassline (Triangle wave syncopated)
    bass_freq = root if (s % 4 in [0, 2]) else root * 1.5
    if s >= 4:
        add_triangle_bass(t_step, step_dur * 0.9, bass_freq, amp=0.32)

    # Drums
    if 8 <= s < total_steps - 12:
        if s % 4 == 0:
            add_chiptune_kick(t_step, amp=0.4)
        elif s % 4 == 2:
            add_chiptune_noise_drum(t_step, dur=0.12, amp=0.25, is_snare=True)
        else:
            add_chiptune_noise_drum(t_step, dur=0.04, amp=0.1, is_snare=False)

    # 16-bit Fast Arpeggio (Pulse 25%)
    if s >= 8 and s < 80:
        arp_scale = [root * 2, root * 2.5, root * 3.0, root * 4.0]
        arp_f = arp_scale[s % len(arp_scale)]
        add_square_lead(t_step, step_dur * 0.8, arp_f, duty=0.25, amp=0.12, pan=0.2 if s % 2 == 0 else 0.8)

# Heroic Melody Line (Pulse 50%)
melody_notes = [
    (1.7, 0.35, 440.0), # A4
    (2.1, 0.35, 523.25), # C5
    (2.5, 0.6, 659.25), # E5
    (3.4, 0.4, 587.33), # D5
    (4.0, 0.8, 523.25), # C5
    (5.2, 0.4, 440.0), # A4
    (5.8, 0.4, 493.88), # B4
    (6.4, 0.8, 523.25), # C5
    (7.6, 1.2, 659.25), # E5
    # Act 2 (Battle theme)
    (9.0, 0.3, 659.25),
    (9.4, 0.3, 659.25),
    (9.8, 0.3, 698.46), # F5
    (10.2, 0.6, 783.99), # G5
    (11.0, 0.4, 659.25),
    (11.6, 0.8, 587.33),
    (12.8, 0.4, 523.25),
    (13.4, 0.8, 587.33),
    (14.5, 1.2, 659.25),
]
for start, dur, freq in melody_notes:
    add_square_lead(start, dur, freq, duty=0.5, amp=0.28, pan=0.5)

# Boss Limit Break SFX (18.5s)
add_limit_break_sfx(18.5, amp=0.45)

# Victory fanfare & coin collection (21.0s - 24.0s)
victory_fanfare = [
    (20.5, 0.18, 523.25), # C5
    (20.7, 0.18, 523.25),
    (20.9, 0.18, 523.25),
    (21.1, 0.5, 659.25),  # E5
    (21.7, 0.2, 587.33),  # D5
    (22.0, 0.7, 783.99),  # G5
]
for start, dur, freq in victory_fanfare:
    add_square_lead(start, dur, freq, duty=0.5, amp=0.35, pan=0.5)

for c_time in [21.5, 22.2, 22.8, 23.4]:
    add_coin_fanfare(c_time, amp=0.3)

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
    fade = min(1.0, t / 0.4) * min(1.0, (DURATION - t) / 0.6)
    l = int(clamp(left_channel[i] * gain * fade) * 32767.0)
    r = int(clamp(right_channel[i] * gain * fade) * 32767.0)
    frames.extend(struct.pack("<hh", l, r))

wav_file.writeframes(frames)
wav_file.close()
print(f"Generated 16-Bit Arcade Soundtrack: {output_path} ({os.path.getsize(output_path)} bytes)")
