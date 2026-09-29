import os
import requests
import json
import base64
import time
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY = os.environ.get("GEMINI_API_KEY", "")
if not KEY:
    if not KEY: raise ValueError("Please set GEMINI_API_KEY environment variable.")

MODEL = "gemini-3.1-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frames"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 30-Second Complete War Story: "BROTHERS IN ARMS: NO ONE LEFT BEHIND"
# 30 continuous sequential narrative beats (20 frames per beat = 600 frames total)
BEATS = [
    # Act 1: The Pinned Down Brother & The Oath (0:00 - 0:06 | Frames 001 - 120)
    (
        "Act 1, Beat 1 (0-1s): Gritty photorealistic war cinema. In a muddy battlefield crater, a wounded young soldier lies pinned down under artillery fire, clutching silver dog tags in shaking, mud-caked hands, extreme close-up on terrified, determined eyes reflecting burning embers.",
        "Extreme macro close-up, silver military dog tags in bloodied, mud-streaked fingers, rain droplets, smoking debris, gritty 35mm war film aesthetic."
    ),
    (
        "Act 1, Beat 2 (1-2s): Gritty photorealistic war cinema. Low-angle shot from inside the mud crater looking out: enemy artillery shells exploding in the distance, sending massive plumes of black dirt and fiery shockwaves into the stormy grey sky.",
        "Low-angle wide shot, artillery impact crater, massive smoke plume, shockwave distortion, raining mud and debris, authentic battlefield realism."
    ),
    (
        "Act 1, Beat 3 (2-3s): Gritty photorealistic war cinema. Fifty yards away across the shattered trench, a battle-hardened squad sergeant behind concrete rubble spots his wounded comrade through cracked ballistic goggles.",
        "Medium close-up, combat sergeant with ballistic helmet, camouflage uniform torn, dust and sweat on face, intense focus and fierce loyalty in his gaze."
    ),
    (
        "Act 1, Beat 4 (3-4s): Gritty photorealistic war cinema. The sergeant locks eyes with the wounded soldier across the smoking no-man's land, a powerful moment of silent brotherhood and resolve, rain pouring over his helmet rim.",
        "Over-the-shoulder shot, looking through thick battlefield smoke toward the trapped soldier, burning vehicle in background, cinematic depth of field."
    ),
    (
        "Act 1, Beat 5 (4-5s): Gritty photorealistic war cinema. The sergeant reaches down to his tactical vest, unclipping a pair of M18 white smoke canisters, thumb gripping the pin with grim determination.",
        "Close-up, tactical gloved hands gripping smoke grenade pin on plate carrier vest, detailed military gear, tense anticipation."
    ),
    (
        "Act 1, Beat 6 (5-6s): Gritty photorealistic war cinema. The sergeant rips the pins with his teeth and hurls the smoke grenades hard across the cratered wasteland, thick white phosphorus smoke beginning to billow violently.",
        "Dynamic action throw, smoke canister flying through air trailing dense white smoke, muzzle flashes lighting the battlefield perimeter."
    ),

    # Act 2: The Sprint into Crossfire (0:06 - 0:12 | Frames 121 - 240)
    (
        "Act 2, Beat 7 (6-7s): Gritty photorealistic war cinema. The white smoke erupts into a massive impenetrable wall of cover across the ruined street, shielding the field from enemy snipers.",
        "Wide shot, explosive wall of dense white smoke spreading rapidly between ruined building facades, dramatic backlit volumetric lighting."
    ),
    (
        "Act 2, Beat 8 (7-8s): Gritty photorealistic war cinema. The sergeant bursts out from behind cover in a full-speed tactical sprint, combat boots slamming into deep mud puddles, water and dirt spraying high.",
        "Low-angle tracking shot, tactical combat boots splashing through muddy trench water, high shutter speed capturing water droplets in mid-air."
    ),
    (
        "Act 2, Beat 9 (8-9s): Gritty photorealistic war cinema. Heavy enemy machine-gun fire rips through the smoke veil, supersonic tracer rounds snapping inches past the sergeant's shoulders and kicking up dirt sparks.",
        "Medium tracking shot of sprinting soldier, red and yellow tracer rounds streaking past, intense kinetic motion blur, gritty war photojournalism."
    ),
    (
        "Act 2, Beat 10 (9-10s): Gritty photorealistic war cinema. A sniper round ricochets violently off a steel beam right beside his head with bright white sparks, the sergeant gritting his teeth and charging forward undeterred.",
        "Tight close-up, steel beam spark explosion near helmet, fierce adrenaline-fueled expression of unwavering resolve, cinematic 8k detail."
    ),
    (
        "Act 2, Beat 11 (10-11s): Gritty photorealistic war cinema. The wounded soldier in the crater looks up through the swirling smoke, seeing the silhouette of his brother running directly into the lethal crossfire to save him.",
        "POV from bottom of crater, silhouette of running soldier emerging through thick white smoke and battlefield fire, beacon of hope in hell."
    ),
    (
        "Act 2, Beat 12 (11-12s): Gritty photorealistic war cinema. A near-miss mortar shell detonates nearby, sending a shockwave that knocks the sergeant sideways, but he scrambles forward on hands and knees without stopping.",
        "Dynamic tumble in mud, dirt flying, soldier immediately pushing back up onto his feet with relentless drive, raw human grit."
    ),

    # Act 3: Suppressive Fire & Reaching the Brother (0:12 - 0:18 | Frames 241 - 360)
    (
        "Act 3, Beat 13 (12-13s): Gritty photorealistic war cinema. Behind him, a friendly armored main battle tank roars onto the scene, its heavy tracks churning over concrete rubble to provide armored cover.",
        "Low-angle heroic wide shot, massive M1 Abrams main battle tank smashing through brick ruins, diesel exhaust and dust billowing."
    ),
    (
        "Act 3, Beat 14 (13-14s): Gritty photorealistic war cinema. The tank's 120mm smoothbore cannon fires directly at the hostile machine-gun bunker, a colossal fireball shockwave shattering the enemy position.",
        "High-speed action frame, massive orange muzzle blast fireball erupting from tank barrel, shockwave ring rippling through dust and air."
    ),
    (
        "Act 3, Beat 15 (14-15s): Gritty photorealistic war cinema. The tank's turret-mounted .50 caliber heavy machine gun lays down deafening suppressive fire, brass shell casings pouring down like rain.",
        "Close-up on heavy machine gun firing, red tracer stream, glowing hot barrel, cascade of gold brass casings bouncing off armored hull."
    ),
    (
        "Act 3, Beat 16 (15-16s): Gritty photorealistic war cinema. Under the cover of the tank's devastating barrage, the sergeant makes a final desperate leap over a burning trench beam.",
        "Mid-air action leap, soldier clearing burning wooden barrier, assault rifle held tight, embers swirling around his uniform."
    ),
    (
        "Act 3, Beat 17 (16-17s): Gritty photorealistic war cinema. The sergeant slides down into the mud crater, slamming to a halt right next to his wounded comrade, chest heaving with exertion.",
        "Low-angle slide into mud crater, dust and water splashing, soldier reaching out both arms toward his fallen brother."
    ),
    (
        "Act 3, Beat 18 (17-18s): Gritty photorealistic war cinema. The sergeant firmly grasps the wounded soldier's tactical vest collar, locking eyes with him: 'I told you I was coming back for you.'",
        "Emotional intimate close-up, two soldiers face to face in mud, blood and sweat, gripping vests, unspoken bond of unbreakable brotherhood."
    ),

    # Act 4: The Fireman's Carry & Air Support Shield (0:18 - 0:24 | Frames 361 - 480)
    (
        "Act 4, Beat 19 (18-19s): Gritty photorealistic war cinema. The sergeant quickly applies a combat tourniquet to the brother's leg, pulling the windlass tight with teeth and hand under deafening gunfire.",
        "Close-up tactical medical emergency, black tourniquet tightened over bleeding combat fatigues, mud and rain, rapid life-saving action."
    ),
    (
        "Act 4, Beat 20 (19-20s): Gritty photorealistic war cinema. With immense physical strength and willpower, the sergeant hoists the wounded soldier onto his shoulders in a textbook fireman's carry.",
        "Medium shot, sergeant straining under the heavy weight of his fully geared wounded brother, rising tall out of the mud crater."
    ),
    (
        "Act 4, Beat 21 (20-21s): Gritty photorealistic war cinema. The sergeant stands upright against the backdrop of war, carrying his brother on his back, beginning the grueling trek back toward safety.",
        "Heroic medium-wide shot, silhouetted soldier carrying comrade on shoulders through burning ruins, embers raining down like fireflies."
    ),
    (
        "Act 4, Beat 22 (21-22s): Gritty photorealistic war cinema. In the sky above, an A-10 Warthog close-air-support jet roars over at treetop level, vapor trails curling off wingtips as it dives into attack.",
        "Dramatic skyward angle, A-10 Thunderbolt II jet banking hard, twin jet engines screaming, nose pointed toward enemy positions."
    ),
    (
        "Act 4, Beat 23 (22-23s): Gritty photorealistic war cinema. The A-10 unleashes its 30mm GAU-8 rotary cannon, a continuous lethal stream of fiery tracer rounds tearing across the ridge behind them.",
        "Wide cinematic view, bright line of 30mm armor-piercing tracers chewing through enemy trench line, smoke erupting in violent plumes."
    ),
    (
        "Act 4, Beat 24 (23-24s): Gritty photorealistic war cinema. A devastating defensive wall of explosions erupts between the retreating soldiers and the enemy, sealing their escape route with a fortress of fire.",
        "Massive high-explosive wall detonation in background, deep orange fireball, silhouettes of the two brothers moving forward unharmed."
    ),

    # Act 5: MEDEVAC Dust-off & Brotherhood Triumph (0:24 - 0:30 | Frames 481 - 600)
    (
        "Act 5, Beat 25 (24-25s): Gritty photorealistic war cinema. Through the clearing smoke, a green smoke flare burns on the landing zone as an MH-60 Black Hawk MEDEVAC helicopter descends through swirling brownout dust.",
        "Wide shot, green extraction smoke plume, Black Hawk helicopter rotor blades churning dust into a massive vortex, landing gear touching down."
    ),
    (
        "Act 5, Beat 26 (25-26s): Gritty photorealistic war cinema. The sergeant reaches the helicopter door in a final burst of adrenaline, crew chief and medic extending their gloved hands to pull the wounded soldier in.",
        "Dynamic angle from inside helicopter cabin looking out, crew hands reaching forward, sergeant lifting brother into the aircraft."
    ),
    (
        "Act 5, Beat 27 (26-27s): Gritty photorealistic war cinema. Both soldiers are safely pulled onto the metal floor of the cabin as the door gunner unleashes a defensive volley of minigun fire into the perimeter.",
        "Interior cabin action, medic immediately treating wounded brother, door gunner firing spinning minigun, spent brass clattering on floor."
    ),
    (
        "Act 5, Beat 28 (27-28s): Gritty photorealistic war cinema. The Black Hawk pulls pitch and climbs steeply into the sky, banking hard away from the smoking battlefield as anti-missile decoy flares burst behind it like angel wings.",
        "Epic exterior wide shot, helicopter climbing into dramatic dusk sky, brilliant golden flares arching outward in defensive pattern over burning valley."
    ),
    (
        "Act 5, Beat 29 (28-29s): Gritty photorealistic war cinema. Inside the rattling cabin, the sergeant sits exhausted against the bulkheads, blood and soot on his face, but a faint, profound smile of relief breaking through.",
        "Intimate medium shot inside cabin, golden sunset light through windows hitting the sergeant's battle-worn face, deep emotional catharsis."
    ),
    (
        "Act 5, Beat 30 (29-30s): Gritty photorealistic war cinema. The wounded soldier reaches out his trembling hand, and the sergeant clasps it tightly in a firm grip of eternal brotherhood; dog tags resting safely on his chest. Mission complete: No one left behind.",
        "Final close-up, two bloodied, mud-caked hands tightly clasped in brotherhood against combat vest, dog tags glinting in the warm sunset light. Profound and complete closure."
    )
]

def build_prompt_for_frame(frame_idx):
    beat_idx = min(frame_idx // 20, len(BEATS) - 1)
    sub_frame = frame_idx % 20
    main_desc, detail_desc = BEATS[beat_idx]
    
    variations = [
        "cinematic wide angle establishing frame, deep atmospheric dust",
        "medium tracking profile, motion energy, gritty film grain",
        "tight dynamic close-up, intense emotional realism, 8k textures",
        "low-angle heroic composition, heavy smoke, cinematic backlighting",
        "high-shutter speed tactical freeze-frame, flying particles and debris",
        "over-the-shoulder perspective, shallow depth of field, documentary war style",
        "gritty 35mm film texture, mud splatter on lens edge, dramatic lighting",
        "cinematic push-in framing, high contrast battlefield shadows and highlights"
    ]
    var_style = variations[sub_frame % len(variations)]
    
    full_prompt = (
        f"{main_desc} "
        f"Sequence micro-frame #{frame_idx + 1:04d} / 600. "
        f"{detail_desc} "
        f"Art style: Award-winning photojournalistic war cinematography, {var_style}, "
        f"hyperrealistic, photorealistic, no cartoon, no text, no subtitles, no borders."
    )
    return full_prompt

def generate_frame(frame_idx):
    target_filename = f"frame_{frame_idx + 1:04d}.png"
    target_path = os.path.join(OUTPUT_DIR, target_filename)

    if os.path.exists(target_path) and os.path.getsize(target_path) > 30000:
        return frame_idx + 1, True, "cached"

    prompt = build_prompt_for_frame(frame_idx)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for attempt in range(5):
        try:
            r = requests.post(URL, json=payload, headers={"Content-Type": "application/json"}, timeout=45)
            if r.status_code == 200:
                data = r.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for p in parts:
                        if "inlineData" in p:
                            b64 = p["inlineData"]["data"]
                            raw_bytes = base64.b64decode(b64)
                            with open(target_path, "wb") as f:
                                f.write(raw_bytes)
                            return frame_idx + 1, True, f"saved ({len(raw_bytes)} bytes)"
            elif r.status_code == 429:
                wait_time = (attempt + 1) * 5
                time.sleep(wait_time)
            else:
                time.sleep(2)
        except Exception:
            time.sleep(2)

    return frame_idx + 1, False, "failed"

def main():
    print("=" * 60)
    print("Batch Generating 600 Individual War Action Frames: 'NO ONE LEFT BEHIND'")
    print("30.0s @ 20 FPS — Narrative Arc: Brotherhood, Sacrifice & Survival")
    print("=" * 60)

    # Use ThreadPoolExecutor with 3 workers
    total_frames = 600
    completed = 0
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_frame, i): i for i in range(total_frames)}
        for future in as_completed(futures):
            idx, success, status = future.result()
            completed += 1
            if completed % 10 == 0 or completed == total_frames:
                print(f"[{completed}/{total_frames}] Frame #{idx:04d}: {status} (Elapsed: {round(completed/total_frames*100, 1)}%)")

    # Ensure all 600 frames are present (fill any missing with nearest valid frame)
    print("\nVerifying all 600 frames are present...")
    for i in range(1, total_frames + 1):
        p = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        if not os.path.exists(p) or os.path.getsize(p) < 30000:
            # Copy from nearest available frame
            for offset in range(1, 20):
                prev_p = os.path.join(OUTPUT_DIR, f"frame_{max(1, i - offset):04d}.png")
                next_p = os.path.join(OUTPUT_DIR, f"frame_{min(total_frames, i + offset):04d}.png")
                if os.path.exists(prev_p) and os.path.getsize(prev_p) > 30000:
                    shutil.copyfile(prev_p, p)
                    break
                elif os.path.exists(next_p) and os.path.getsize(next_p) > 30000:
                    shutil.copyfile(next_p, p)
                    break

    existing = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("frame_") and f.endswith(".png")]
    print(f"✓ Total verified frames in {OUTPUT_DIR}: {len(existing)}/600")

if __name__ == "__main__":
    main()
