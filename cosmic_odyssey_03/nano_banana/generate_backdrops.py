"""
Nano Banana 2 / Gemini Image Generator
Generates the 5 Master Cinematic Backdrops for 'The Seed of Aurora' (Project 03)
"""
import os

PROMPTS = {
    "act1_void": "Breathtaking cinematic deep space cosmic void. In the center, a radiant ethereal celestial rift glows with deep indigo, violet, and electric cyan light, surrounded by distant stars, spiral galaxies, and glowing sacred geometry energy filaments. Photorealistic 8k, widescreen sci-fi film still.",
    "act2_nebula": "Kaleidoscopic cosmic nebula, towering pillars of glowing magenta, celestial pink, and royal violet gas clouds, interstellar stardust nursery with newborn glittering golden stars and luminous cosmic dust streams, widescreen 16:9 cinematic masterpiece, 8k.",
    "act3_descent": "Dramatic atmospheric descent towards a massive alien planet seen from the upper ionosphere. Violet and stormy electric clouds, with glowing orange volcanic fissure lines and jagged mountain ridges visible below across the planetary curve. Cinematic sci-fi epic film still, 16:9 widescreen, 8k.",
    "act4_impact": "Massive ancient stone canyon crater on an alien world where a celestial artifact has struck, sending a monumental radiant golden circular energy shockwave expanding across the rock, luminous bioluminescent veins waking up the stone ground, volumetric dust, cinematic sci-fi concept art, 16:9 widescreen, 8k.",
    "act5_bloom": "Breathtaking solarpunk celestial paradise on an alien world reborn. Monumental towering translucent emerald and amethyst crystal monolith spires rise towards the heavens, surrounded by lush glowing bioluminescent flora, cascading waterfalls, floating spores of light, and twin golden suns rising over an emerald ocean horizon. Photorealistic utopian sci-fi film still, 16:9 widescreen, 8k."
}

def main():
    print("Prompts for The Seed of Aurora 5-Act Narrative:")
    for act, p in PROMPTS.items():
        print(f"\n[{act.upper()}]:\n  {p}")

if __name__ == "__main__":
    main()
