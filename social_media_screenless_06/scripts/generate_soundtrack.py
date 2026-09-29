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
output_path = os.path.join(output_dir, "screenless_reconnect_soundtrack.wav")

left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

def add_digital_glitch_ping(start_t, freq=1200.0, dur=0.08, amp=0.35):
    """Cold harsh digital smartphone alert / notification ping"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-35.0 * t)
        # Square wave digital sound
        sq = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        val = sq * amp * env
        left_channel[idx] += val * 1.1
        right_channel[idx] += val * 0.9

def add_phone_vibrate(start_t, dur=0.4, amp=0.3):
    """Muffled smartphone haptic motor vibration"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 1.5
        motor = math.sin(2 * math.pi * 140.0 * t) + 0.4 * math.sin(2 * math.pi * 70.0 * t)
        val = motor * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_dissonant_synth_drone(start_t, dur=5.0, amp=0.25):
    """Cold dystopian blue screen digital hum"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = min(1.0, t / 0.5) * min(1.0, (dur - t) / 0.5)
        # Minor second dissonance (220Hz and 233Hz)
        s1 = math.sin(2 * math.pi * 220.0 * t)
        s2 = math.sin(2 * math.pi * 233.08 * t)
        s3 = 0.3 * math.sin(2 * math.pi * 880.0 * t) * (1.0 + math.sin(2 * math.pi * 6.0 * t))
        val = (s1 * 0.5 + s2 * 0.5 + s3 * 0.2) * amp * env
        left_channel[idx] += val * 0.9
        right_channel[idx] += val * 1.1

def add_power_off_click(start_t, amp=0.45):
    """Crisp satisfying tactile power-switch shutoff click"""
    start_idx = int(start_t * SAMPLE_RATE)
    dur = 0.05
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-90.0 * t)
        val = random.uniform(-1.0, 1.0) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_piano_key(start_t, freq, dur=2.5, amp=0.35):
    """Makoto Shinkai / Joe Hisaishi style resonant acoustic grand piano note"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-2.2 * t)
        # Piano hammer strike & rich harmonics
        h1 = math.sin(2 * math.pi * freq * t)
        h2 = 0.45 * math.sin(2 * math.pi * 2 * freq * t) * math.exp(-3.0 * t)
        h3 = 0.20 * math.sin(2 * math.pi * 3 * freq * t) * math.exp(-4.5 * t)
        h4 = 0.08 * math.sin(2 * math.pi * 4 * freq * t) * math.exp(-6.0 * t)
        val = (h1 + h2 + h3 + h4) * amp * env
        left_channel[idx] += val * 0.98
        right_channel[idx] += val * 1.02

def add_warm_anime_strings(start_t, dur, chord_freqs, amp=0.28):
    """Emotional soaring anime string orchestra pad"""
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
            s2 = 0.35 * math.sin(2 * math.pi * (f * 1.002) * t)
            val += (s1 + s2)
        left_channel[idx] += val * (amp / len(chord_freqs)) * fade
        right_channel[idx] += val * (amp / len(chord_freqs)) * fade

def add_birdsong_flute(start_t, freq=1800.0, amp=0.18):
    """Gentle morning forest bird warble"""
    start_idx = int(start_t * SAMPLE_RATE)
    dur = 0.35
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 1.5
        # Trill
        f = freq + 250.0 * math.sin(2 * math.pi * 18.0 * t)
        val = math.sin(2 * math.pi * f * t) * amp * env
        left_channel[idx] += val * 0.8
        right_channel[idx] += val * 1.2

def add_ocean_wave(start_t, dur=5.5, amp=0.14):
    """Gentle twilight ocean wave swell and shore foam"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / dur)) ** 2
        noise = random.uniform(-0.5, 0.5)
        # Low frequency surge
        surge = math.sin(2 * math.pi * 0.25 * t) * 0.3
        val = (noise + surge) * amp * env
        left_channel[idx] += val * 1.1
        right_channel[idx] += val * 0.9

print("Synthesizing 25.0s Anime Master Soundtrack: Disconnect to Reconnect...")

# Act 1 (0-5s): Cold Digital Doomscroll
add_dissonant_synth_drone(0.0, dur=5.0, amp=0.22)
add_phone_vibrate(0.5, dur=0.35, amp=0.28)
add_digital_glitch_ping(1.0, freq=1400.0, dur=0.06, amp=0.30)
add_digital_glitch_ping(1.8, freq=1600.0, dur=0.05, amp=0.32)
add_phone_vibrate(2.4, dur=0.45, amp=0.32)
add_digital_glitch_ping(3.1, freq=1250.0, dur=0.08, amp=0.35)
add_digital_glitch_ping(3.9, freq=1800.0, dur=0.05, amp=0.38)
add_phone_vibrate(4.2, dur=0.3, amp=0.25)

# Act 2 (5-10s): Powering Off & First Breath of Morning Light
add_power_off_click(5.05, amp=0.55)
# Silence until 5.8s, then gentle piano starts
add_piano_key(5.8, 261.63, dur=2.5, amp=0.32) # C4
add_piano_key(6.6, 329.63, dur=2.2, amp=0.35) # E4
add_piano_key(7.4, 392.00, dur=2.4, amp=0.38) # G4
add_piano_key(8.4, 523.25, dur=2.8, amp=0.42) # C5

# Act 3 (10-15s): Stepping into the Living Forest
add_birdsong_flute(10.2, freq=2100.0, amp=0.18)
add_birdsong_flute(12.5, freq=2400.0, amp=0.16)
add_piano_key(10.0, 349.23, dur=2.2, amp=0.38) # F4
add_piano_key(11.2, 440.00, dur=2.0, amp=0.40) # A4
add_piano_key(12.4, 523.25, dur=2.2, amp=0.42) # C5
add_piano_key(13.6, 659.25, dur=2.5, amp=0.45) # E5
add_warm_anime_strings(10.5, dur=4.5, chord_freqs=[174.61, 261.63, 349.23, 440.00], amp=0.30)

# Act 4 (15-20s): Real Connection & Laughter in Wildflower Meadow
add_warm_anime_strings(15.0, dur=5.2, chord_freqs=[196.00, 246.94, 293.66, 392.00, 587.33], amp=0.40)
add_piano_key(15.0, 392.00, dur=1.8, amp=0.40) # G4
add_piano_key(15.8, 493.88, dur=1.8, amp=0.42) # B4
add_piano_key(16.6, 587.33, dur=2.0, amp=0.45) # D5
add_piano_key(17.6, 783.99, dur=2.4, amp=0.48) # G5
add_piano_key(18.8, 659.25, dur=2.2, amp=0.44) # E5

# Act 5 (20-25s): Twilight Ocean Serenity - Disconnect to Reconnect
add_ocean_wave(19.8, dur=5.2, amp=0.15)
add_warm_anime_strings(20.0, dur=5.0, chord_freqs=[130.81, 196.00, 261.63, 329.63, 523.25], amp=0.42)
add_piano_key(20.2, 523.25, dur=3.5, amp=0.42) # C5 sustained
add_piano_key(21.8, 392.00, dur=3.2, amp=0.38) # G4
add_piano_key(23.2, 261.63, dur=3.5, amp=0.35) # C4 final peaceful resolution

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

print(f"✓ Anime soundtrack generated: {output_path} ({len(frames_data)} bytes, {DURATION}s)")
