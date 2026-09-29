import os
import requests
import json
import base64
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Read Gemini API key from environment
KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-3.1-flash-image" # Nano Banana 2
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "keyframes"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCENES = [
    (
        "scene_01_awakening.png",
        "Vibrant comic cartoon animation art: A tiny cute anthropomorphic yellow banana character named 'Nano Banana 2.0' waking up inside a wooden kitchen fruit bowl, putting on cool retro pixel black sunglasses with a smug confident grin, flexed little yellow peel arms, clean vibrant digital illustration, 2D animation cel style, crisp colors, high quality."
    ),
    (
        "scene_02_fruit_bowl_escape.png",
        "Vibrant comic cartoon animation art: The tiny yellow banana character using a cocktail toothpick as a pole vault, leaping in mid-air over grumpy red apples and sleepy oranges in a kitchen fruit bowl, cartoon action lines, dynamic parkour leap, 2D animation style, colorful and funny."
    ),
    (
        "scene_03_blender_horror.png",
        "Vibrant comic cartoon animation art: A massive scary kitchen blender with spinning stainless steel blades labeled 'SMOOTHIE OF DOOM' roaring to life, the tiny banana character in the foreground with comical huge wide bugging-out eyes and mouth agape in Looney Tunes slapstick terror, comic shock lines, vibrant colors."
    ),
    (
        "scene_04_action_slide.png",
        "Vibrant comic cartoon animation art: Action movie slide! The tiny yellow banana character sliding smoothly on the kitchen counter right underneath the whirring blender base, throwing a cheeky wink and thumbs-up to the camera with spark trails behind it, dynamic cartoon perspective, bright funny animation style."
    ),
    (
        "scene_05_monkey_ambush.png",
        "Vibrant comic cartoon animation art: A goofy cartoon monkey wearing a white chef hat and red bib holding a giant fork and knife sneaking up on the kitchen counter, while the clever tiny banana character drops tactical yellow banana peels behind it like cartoon landmines, funny cartoon comedy."
    ),
    (
        "scene_06_monkey_slip.png",
        "Vibrant comic cartoon animation art: Slapstick comedy chaos! The goofy chef monkey stepping on a banana peel, legs flailing wildly mid-air spinning upside down, about to crash into a massive fluffy bowl of white whipped cream with comic motion vortex and exclamation marks, hilarious cartoon slapstick."
    ),
    (
        "scene_07_supercharged_banana.png",
        "Vibrant comic cartoon animation art: Supercharged power-up! The tiny banana character plugging its stem into a glowing electric USB kitchen wall charger, surging with crackling yellow anime Super-Saiyan lightning bolts, glowing red laser visor, comic energy aura, high energy funny cartoon."
    ),
    (
        "scene_08_rocket_launch.png",
        "Vibrant comic cartoon animation art: Epic comedy launch! The supercharged tiny banana riding on top of a red and yellow firework model rocket labeled 'NANO-X', blasting off through the kitchen roof window into the blue sky with billowing cartoon smoke and fiery exhaust, dramatic funny angle."
    ),
    (
        "scene_09_space_disco.png",
        "Vibrant comic cartoon animation art: The tiny yellow banana character wearing shiny disco sunglasses floating gracefully in deep outer space with planet Earth below, doing a funny zero-gravity disco Saturday Night Fever dance pose, surrounded by sparkling stars and twinkling cosmic dust, hilarious sci-fi comedy."
    ),
    (
        "scene_10_banana_slip_splat.png",
        "Vibrant comic cartoon animation art: The ultimate slapstick punchline! The tiny banana character crashing back into the kitchen, attempting a cool superhero three-point landing but immediately slipping on its own discarded banana peel, funny spiral eyes, comic 'SPLAT!' impact star, cartoon dizzy birds circling its head, hilarious finish."
    )
]

def generate_keyframe(filename, prompt):
    if not KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable before running keyframe generation.")
    
    target_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 30000:
        print(f"✓ Already generated: {filename} ({os.path.getsize(target_path)} bytes)")
        return filename, True

    print(f"Generating Nano Banana 2 keyframe: {filename}...")
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    for attempt in range(4):
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
                            print(f"✓ Saved {filename} ({len(raw_bytes)} bytes)")
                            return filename, True
            elif r.status_code == 429:
                wait_time = (attempt + 1) * 5
                print(f"Rate limited on {filename}, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Error HTTP {r.status_code} on {filename}: {r.text[:150]}")
                time.sleep(2)
        except Exception as e:
            print(f"Exception on {filename}: {e}")
            time.sleep(2)

    return filename, False

def main():
    print("=" * 60)
    print("Starting Nano Banana 2 (gemini-3.1-flash-image) Keyframe Generation")
    print("=" * 60)

    if not KEY:
        print("Note: GEMINI_API_KEY environment variable is required to generate new keyframes.")
        return

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_keyframe, fname, prompt): fname for fname, prompt in SCENES}
        results = []
        for future in as_completed(futures):
            res = future.result()
            results.append(res)

    success_count = sum(1 for _, ok in results if ok)
    print(f"\nKeyframe Generation Complete: {success_count}/{len(SCENES)} keyframes successfully generated!")

if __name__ == "__main__":
    main()
