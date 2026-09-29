import numpy as np
import scipy.io.wavfile as wavfile
import os

SAMPLE_RATE = 44100
DURATION = 60.0  # Exactly 60 seconds
N_SAMPLES = int(SAMPLE_RATE * DURATION)
t = np.linspace(0, DURATION, N_SAMPLES, endpoint=False)

left = np.zeros(N_SAMPLES, dtype=np.float32)
right = np.zeros(N_SAMPLES, dtype=np.float32)

print(f"Synthesizing 60.0s Master Soundtrack: 'The Seed of Aurora' ({N_SAMPLES} samples)...")

# --- LAYER 1: Deep Space Ambient Sub-Bass Foundation (Continuous 60s) ---
# Slow undulating F1 (43.65 Hz) and C2 (65.41 Hz) drone
drone_lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
drone_f1 = np.sin(2 * np.pi * 43.65 * t) * 0.35 * drone_lfo
drone_c2 = np.sin(2 * np.pi * 65.41 * t) * 0.25 * (1.0 - 0.5 * drone_lfo)
left += drone_f1 + drone_c2 * 0.7
right += drone_f1 * 0.7 + drone_c2

# Cosmic background hiss / stellar wind
noise = np.random.normal(0, 1, N_SAMPLES).astype(np.float32)
# Lowpass filtered noise using rolling average
kernel_size = 80
wind = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
wind_envelope = 0.05 + 0.04 * np.sin(2 * np.pi * 0.05 * t)
left += wind * wind_envelope
right += wind * wind_envelope * 0.9

# --- ACT 1: The Void & Awakening (0 - 12s) ---
mask_act1 = (t >= 0) & (t < 12)
t_act1 = t[mask_act1]
# Crystalline bell arpeggios (Awakening)
chimes = np.zeros_like(t_act1)
for i, chime_t in enumerate(np.arange(1.0, 11.0, 1.5)):
    freq = 523.25 * (1.5 ** (i % 4))  # Pentatonic crystal notes
    env = np.exp(-3.0 * (t_act1 - chime_t)) * (t_act1 >= chime_t)
    chimes += np.sin(2 * np.pi * freq * t_act1) * env * 0.2
left[mask_act1] += chimes * 0.8
right[mask_act1] += chimes * 0.5

# --- ACT 2: The Nebula Drift (12 - 24s) ---
mask_act2 = (t >= 12) & (t < 24)
t_act2 = t[mask_act2] - 12.0
# Warm analog synth pad (Fm9 -> AbMaj7 -> Eb)
chord_freqs = [174.61, 207.65, 261.63, 311.13, 349.23] # F, Ab, C, Eb, F
pad_l = np.zeros_like(t_act2)
pad_r = np.zeros_like(t_act2)
act2_fade = np.sin(np.pi * t_act2 / 12.0)
for idx, f in enumerate(chord_freqs):
    # Detuned oscillators for lush warmth
    detune = 1.0 + (idx - 2) * 0.003
    sig_l = np.sin(2 * np.pi * f * t_act2) + 0.3 * np.sin(2 * np.pi * f * 2 * t_act2)
    sig_r = np.sin(2 * np.pi * f * detune * t_act2) + 0.3 * np.sin(2 * np.pi * f * detune * 2 * t_act2)
    pad_l += sig_l * 0.06
    pad_r += sig_r * 0.06
left[mask_act2] += pad_l * act2_fade
right[mask_act2] += pad_r * act2_fade

# Rhythmic stardust pulse at 1.0 Hz
pulse = 0.5 * (1 + np.sin(2 * np.pi * 1.0 * t_act2)) ** 4
pulse_sound = np.sin(2 * np.pi * 87.31 * t_act2) * pulse * 0.15 * act2_fade
left[mask_act2] += pulse_sound
right[mask_act2] += pulse_sound

# --- ACT 3: Atmospheric Descent (24 - 36s) ---
mask_act3 = (t >= 24) & (t < 36)
t_act3 = t[mask_act3] - 24.0
act3_env = np.sin(np.pi * t_act3 / 12.0)

# Atmospheric re-entry roar (pitch descending friction noise)
entry_freq = 600.0 - 30.0 * t_act3
entry_rumble = np.sin(2 * np.pi * entry_freq * t_act3) * np.random.uniform(0.7, 1.3, len(t_act3))
entry_rumble = np.convolve(entry_rumble, np.ones(40)/40, mode='same') * 0.35 * (t_act3 / 12.0)
# Low brass braam warning horn
braam = (np.sin(2 * np.pi * 55.0 * t_act3) + 0.5 * np.sin(2 * np.pi * 110.0 * t_act3)) * 0.3 * (1.0 + np.sin(2 * np.pi * 0.5 * t_act3))
left[mask_act3] += (entry_rumble * 0.7 + braam * 0.6) * act3_env
right[mask_act3] += (entry_rumble * 0.9 + braam * 0.6) * act3_env

# --- ACT 4: Touchdown & Energy Shockwave (36 - 48s) ---
mask_act4 = (t >= 36) & (t < 48)
t_act4 = t[mask_act4] - 36.0

# Massive Impact blast at t=0 of act 4 (36.0s)
impact_time = t_act4
sub_drop = np.sin(2 * np.pi * np.maximum(25.0, 120.0 * np.exp(-1.5 * impact_time)) * impact_time)
impact_env = np.exp(-0.8 * impact_time)
impact_sound = sub_drop * impact_env * 0.7
left[mask_act4] += impact_sound
right[mask_act4] += impact_sound

# Expanding shockwave resonance sweep
shockwave_t = np.maximum(0.0, impact_time - 0.5)
shockwave_env = np.sin(np.pi * np.clip(shockwave_t / 11.5, 0, 1))
shockwave_freq = 110.0 + 220.0 * (shockwave_t / 12.0)
shockwave_drone = np.sin(2 * np.pi * shockwave_freq * shockwave_t) * 0.25 * shockwave_env
left[mask_act4] += shockwave_drone * 0.8
right[mask_act4] += shockwave_drone * 1.0

# Bioluminescent vein harmonic pulses
vein_pulse = np.sin(2 * np.pi * 329.63 * t_act4) * (0.5 + 0.5 * np.sin(2 * np.pi * 2.0 * t_act4)) * 0.15 * shockwave_env
left[mask_act4] += vein_pulse
right[mask_act4] += vein_pulse

# --- ACT 5: The Cosmic Bloom & Triumphant Rebirth (48 - 60s) ---
mask_act5 = (t >= 48) & (t <= 60)
t_act5 = t[mask_act5] - 48.0
act5_env = np.ones_like(t_act5)
# Fade in quickly at start of act 5, fade out smoothly at the very end (57-60s)
act5_env = np.clip(t_act5 / 2.0, 0, 1) * np.clip((12.0 - t_act5) / 3.0, 0, 1)

# Major key triumphant progression (F Major -> Bb Major -> C Major -> F Major)
# Glorious brass & angelic choir chords
triumph_chords = [
    [174.61, 220.00, 261.63, 349.23, 440.00], # F Maj (0-3s)
    [233.08, 293.66, 349.23, 466.16, 587.33], # Bb Maj (3-6s)
    [261.63, 329.63, 392.00, 523.25, 659.25], # C Maj (6-9s)
    [349.23, 440.00, 523.25, 698.46, 880.00], # F Maj High (9-12s)
]

triumph_l = np.zeros_like(t_act5)
triumph_r = np.zeros_like(t_act5)

for seg_idx, chord in enumerate(triumph_chords):
    t_start = seg_idx * 3.0
    t_end = (seg_idx + 1) * 3.0
    seg_mask = (t_act5 >= t_start) & (t_act5 <= t_end)
    t_seg = t_act5[seg_mask]
    seg_env = np.sin(np.pi * (t_seg - t_start) / 3.0)
    for f in chord:
        triumph_l[seg_mask] += (np.sin(2 * np.pi * f * t_seg) + 0.3 * np.sin(2 * np.pi * f * 2 * t_seg)) * 0.08 * seg_env
        triumph_r[seg_mask] += (np.sin(2 * np.pi * f * 1.002 * t_seg) + 0.3 * np.sin(2 * np.pi * f * 2.004 * t_seg)) * 0.08 * seg_env

left[mask_act5] += triumph_l * act5_env
right[mask_act5] += triumph_r * act5_env

# Master Celestial Chime arpeggios in Act 5
celestial_bells = np.zeros_like(t_act5)
for i, bell_t in enumerate(np.arange(0.5, 10.0, 0.75)):
    f_bell = 698.46 * (1.25 ** (i % 6))
    env_bell = np.exp(-4.0 * (t_act5 - bell_t)) * (t_act5 >= bell_t)
    celestial_bells += np.sin(2 * np.pi * f_bell * t_act5) * env_bell * 0.15
left[mask_act5] += celestial_bells * act5_env * 0.7
right[mask_act5] += celestial_bells * act5_env * 1.0

# Master Limiter & Normalization
master_max = max(np.max(np.abs(left)), np.max(np.abs(right)))
if master_max > 0:
    left = (left / master_max) * 0.92
    right = (right / master_max) * 0.92

# Convert to 16-bit PCM stereo
audio_stereo = np.column_stack((
    (left * 32767).astype(np.int16),
    (right * 32767).astype(np.int16)
))

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cosmic_soundtrack.wav"))
wavfile.write(out_path, SAMPLE_RATE, audio_stereo)
print(f"✓ Master Soundtrack written to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB)")
