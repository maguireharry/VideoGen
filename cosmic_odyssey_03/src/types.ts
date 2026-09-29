export interface ActConfig {
  actIndex: number;
  title: string;
  subtitle: string;
  narration: string;
  backdropImage: string;
  startFrame: number;
  durationInFrames: number;
  accentColor: string;
  particleMode: 'vortex' | 'stream' | 'plasma' | 'shockwave' | 'spores';
}

export const ACTS: ActConfig[] = [
  {
    actIndex: 1,
    title: "ACT I: THE AWAKENING",
    subtitle: "IN THE DEEP VOID OF CREATION",
    narration: "Before the stars could dream, a silent seed listened to the dark...",
    backdropImage: "images/act1_void.png",
    startFrame: 0,
    durationInFrames: 360, // 0 - 12s
    accentColor: "#38bdf8", // Sky blue / cyan
    particleMode: 'vortex',
  },
  {
    actIndex: 2,
    title: "ACT II: THE NEBULA DRIFT",
    subtitle: "WEAVING A MANTLE OF LIGHT",
    narration: "Gathering the embers of dying suns, its crystalline heart unfurled...",
    backdropImage: "images/act2_nebula.png",
    startFrame: 360,
    durationInFrames: 360, // 12 - 24s
    accentColor: "#e879f9", // Magenta / Fuchsia
    particleMode: 'stream',
  },
  {
    actIndex: 3,
    title: "ACT III: THE DESCENT",
    subtitle: "ACROSS THE VIOLENT IONOSPHERE",
    narration: "A barren world waiting for dawn. One final journey into fire...",
    backdropImage: "images/act3_descent.png",
    startFrame: 720,
    durationInFrames: 360, // 24 - 36s
    accentColor: "#f97316", // Fiery orange
    particleMode: 'plasma',
  },
  {
    actIndex: 4,
    title: "ACT IV: THE TOUCHDOWN",
    subtitle: "THE RESONANCE OF THE SEED",
    narration: "Upon shattered stone, the heart opened... waking the sleeping veins.",
    backdropImage: "images/act4_impact.png",
    startFrame: 1080,
    durationInFrames: 360, // 36 - 48s
    accentColor: "#facc15", // Golden glow
    particleMode: 'shockwave',
  },
  {
    actIndex: 5,
    title: "ACT V: THE AURORA BLOOM",
    subtitle: "GENESIS OF THE CELESTIAL GARDEN",
    narration: "Where there was silence, now sings an eternal garden of stars.",
    backdropImage: "images/act5_bloom.png",
    startFrame: 1440,
    durationInFrames: 360, // 48 - 60s
    accentColor: "#34d399", // Emerald green / Aurora
    particleMode: 'spores',
  },
];
