import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100
DURATION = 30.0 # Exactly 30.0 seconds
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "war_action_soundtrack.wav")

left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

def add_sub_bass_braam(start_t, dur=2.5, freq=45.0, amp=0.55):
    """Cinematic Inception/Hans Zimmer style heavy sub-bass braam"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-1.8 * t)
        # Mix fundamental with saw harmonics for deep brassy buzz
        f = freq * (1.0 - 0.08 * (t / dur))
        val = 0.6 * math.sin(2 * math.pi * f * t) + 0.3 * math.sin(4 * math.pi * f * t) + 0.15 * math.sin(6 * math.pi * f * t)
        left_channel[idx] += val * amp * env
        right_channel[idx] += val * amp * env

def add_war_drum(start_t, dur=0.6, freq=65.0, amp=0.6):
    """Militaristic heavy war drum / taiko strike"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-6.0 * t)
        f = freq * math.exp(-5.0 * t)
        noise = random.uniform(-0.15, 0.15) * math.exp(-12.0 * t)
        val = math.sin(2 * math.pi * f * t) * 0.85 + noise
        left_channel[idx] += val * amp * env
        right_channel[idx] += val * amp * env

def add_explosion(start_t, dur=2.0, amp=0.85):
    """Massive concussion blast / C4 demolition / artillery detonation"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        env = math.exp(-2.5 * t)
        # Low frequency rumble + white noise blast
        sub = math.sin(2 * math.pi * (55.0 * math.exp(-2.0 * t)) * t) * 0.7
        noise = random.uniform(-1.0, 1.0) * (0.6 * math.exp(-4.0 * t) + 0.2 * math.exp(-0.8 * t))
        val = (sub + noise) * amp * env
        left_channel[idx] += val
        right_channel[idx] += val

def add_gunfire_burst(start_t, shots=6, rate=12.0, amp=0.5):
    """Rapid automatic assault rifle / machine gun burst"""
    interval = 1.0 / rate
    for s in range(shots):
        t_shot = start_t + s * interval
        start_idx = int(t_shot * SAMPLE_RATE)
        dur = 0.12
        samples = int(dur * SAMPLE_RATE)
        for i in range(samples):
            idx = start_idx + i
            if idx >= TOTAL_SAMPLES:
                break
            t = i / SAMPLE_RATE
            env = math.exp(-25.0 * t)
            crack = random.uniform(-1.0, 1.0)
            pop = math.sin(2 * math.pi * (220.0 * math.exp(-20.0 * t)) * t)
            val = (crack * 0.7 + pop * 0.5) * amp * env
            left_channel[idx] += val
            right_channel[idx] += val

def add_a10_brrrt(start_t, dur=1.2, amp=0.7):
    """Iconic 30mm GAU-8 rotary cannon BRRRRRT roar"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        # 65 Hz firing rate buzz
        buzz = 1.0 if math.sin(2 * math.pi * 65.0 * t) >= 0 else -1.0
        hiss = random.uniform(-0.6, 0.6)
        low_roar = math.sin(2 * math.pi * 130.0 * t) * 0.5
        val = (buzz * 0.5 + hiss * 0.5 + low_roar * 0.3) * amp
        left_channel[idx] += val
        right_channel[idx] += val

def add_helicopter_rotor(start_t, dur=6.0, rate=18.0, amp=0.4):
    """Heavy transport / attack helicopter rotor wash thumping"""
    start_idx = int(start_t * SAMPLE_RATE)
    samples = int(dur * SAMPLE_RATE)
    for i in range(samples):
        idx = start_idx + i
        if idx >= TOTAL_SAMPLES:
            break
        t = i / SAMPLE_RATE
        pulse = (math.sin(2 * math.pi * rate * t) ** 4)
        noise = random.uniform(-0.2, 0.2)
        val = (pulse * 0.8 + noise) * amp * (0.8 + 0.2 * math.sin(2 * math.pi * 0.5 * t))
        left_channel[idx] += val * 0.85
        right_channel[idx] += val * 1.15

print("Synthesizing 30-second hard-hitting cinematic war trailer soundtrack...")

# Continuous driving militaristic war drum heartbeat rhythm (120 BPM = 0.5s per beat)
for beat in range(60):
    t = beat * 0.5
    # Accented downbeats
    if beat % 4 == 0:
        add_war_drum(t, dur=0.8, freq=55.0, amp=0.55)
    elif beat % 2 == 0:
        add_war_drum(t, dur=0.5, freq=65.0, amp=0.40)
    else:
        add_war_drum(t, dur=0.3, freq=90.0, amp=0.25)

# Act 1 (0-6s): Infiltration & Tension
add_sub_bass_braam(0.2, dur=3.5, freq=42.0, amp=0.5)
add_sub_bass_braam(3.8, dur=2.2, freq=40.0, amp=0.5)
# Suppressed sniper shots
add_gunfire_burst(2.5, shots=2, rate=8.0, amp=0.35)
add_gunfire_burst(4.8, shots=3, rate=10.0, amp=0.40)

# Act 2 (6-12s): Explosive C4 Breach & Room Clearance
add_explosion(6.0, dur=2.8, amp=0.95) # THE BREACH DETONATION
add_sub_bass_braam(6.1, dur=3.0, freq=38.0, amp=0.6)
# CQB intense gunfire exchanges
add_gunfire_burst(7.2, shots=8, rate=14.0, amp=0.55)
add_gunfire_burst(8.5, shots=10, rate=15.0, amp=0.60)
add_gunfire_burst(10.2, shots=6, rate=12.0, amp=0.50)

# Act 3 (12-18s): Armor & Heavy Caliber Urban Combat
add_explosion(12.0, dur=2.5, amp=0.85) # 120mm Tank Cannon blast 1
add_sub_bass_braam(12.2, dur=2.5, freq=35.0, amp=0.65)
add_gunfire_burst(13.4, shots=14, rate=10.0, amp=0.65) # .50 cal heavy MG
add_explosion(15.2, dur=2.8, amp=0.90) # Secondary fuel depot explosion
add_gunfire_burst(16.5, shots=12, rate=12.0, amp=0.55)

# Act 4 (18-24s): Close Air Support & A-10 Strafe
add_sub_bass_braam(18.0, dur=2.5, freq=48.0, amp=0.60)
add_a10_brrrt(19.2, dur=1.6, amp=0.75) # A-10 BRRRRRRT
add_explosion(20.9, dur=3.0, amp=0.95) # High-explosive cluster impact
add_sub_bass_braam(21.2, dur=2.5, freq=36.0, amp=0.70)
add_a10_brrrt(22.8, dur=1.2, amp=0.70)

# Act 5 (24-30s): Hot Extraction & Dust-Off
add_helicopter_rotor(24.0, dur=6.0, rate=18.0, amp=0.55) # Rotor wash
add_gunfire_burst(24.8, shots=18, rate=20.0, amp=0.60) # Minigun suppressive fire
add_sub_bass_braam(25.5, dur=4.0, freq=40.0, amp=0.75) # Final cinematic crescendo
add_explosion(27.0, dur=2.5, amp=0.80) # Distance rocket impact
add_sub_bass_braam(28.0, dur=2.0, freq=32.0, amp=0.80) # Final earth-shaking sub-drop

# Master normalization
max_amp = max(max(abs(x) for x in left_channel), max(abs(x) for x in right_channel), 0.001)
scale = 31000.0 / max_amp if max_amp > 1.0 else 31000.0

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

print(f"✓ War action soundtrack generated: {output_path} ({len(frames_data)} bytes)")
