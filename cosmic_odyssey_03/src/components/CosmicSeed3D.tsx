import React, { useMemo } from 'react';
import * as THREE from 'three';
import { interpolate, spring } from 'remotion';

interface CosmicSeedProps {
  frame: number;
  fps: number;
  actIndex: number;
}

export const CosmicSeed3D: React.FC<CosmicSeedProps> = ({ frame, fps, actIndex }) => {
  // Rotational animation mapped to frame
  const rotX = frame * 0.015;
  const rotY = frame * 0.022;
  const rotZ = frame * 0.018;

  // Pulse effect synced with music
  const pulse = 1.0 + 0.08 * Math.sin(frame * 0.12);

  // Position & Scale choreography per Act
  let posX = 0;
  let posY = 0;
  let posZ = 0;
  let scale = 1.0;

  if (actIndex === 1) {
    // Act 1: Emerges from deep space center
    scale = interpolate(frame, [0, 150], [0.3, 1.2], { extrapolateRight: 'clamp' }) * pulse;
    posY = Math.sin(frame * 0.03) * 0.2;
  } else if (actIndex === 2) {
    // Act 2: Soaring gracefully across nebula
    scale = 1.3 * pulse;
    posX = Math.sin(frame * 0.04) * 0.8;
    posY = Math.cos(frame * 0.03) * 0.5;
  } else if (actIndex === 3) {
    // Act 3: Plunging violently downward
    scale = interpolate(frame, [0, 360], [1.4, 0.7], { extrapolateRight: 'clamp' });
    posX = 0.5 - (frame / 360) * 1.0;
    posY = 1.5 - (frame / 360) * 3.5; // Plunges down
  } else if (actIndex === 4) {
    // Act 4: Impact at ground center, core opening
    scale = interpolate(frame, [0, 80], [0.8, 1.5], { extrapolateRight: 'clamp' }) * pulse;
    posY = -0.5;
  } else if (actIndex === 5) {
    // Act 5: Ascending towards the heavens as guardian star
    scale = interpolate(frame, [0, 360], [1.2, 2.0], { extrapolateRight: 'clamp' });
    posY = interpolate(frame, [0, 360], [-0.5, 2.0], { extrapolateRight: 'clamp' });
  }

  // Torus Rings rotations
  const ring1Rot: [number, number, number] = [rotX * 1.5, rotY * 0.8, 0];
  const ring2Rot: [number, number, number] = [0, rotY * 1.8, rotZ * 1.2];
  const ring3Rot: [number, number, number] = [rotX * 0.9, 0, rotZ * 2.1];

  return (
    <group position={[posX, posY, posZ]} scale={[scale, scale, scale]}>
      {/* 1. Inner Radiant Crystalline Core */}
      <mesh rotation={[rotX, rotY, rotZ]}>
        <icosahedronGeometry args={[0.9, 0]} />
        <meshStandardMaterial
          color="#fde047"
          emissive="#eab308"
          emissiveIntensity={1.8}
          roughness={0.15}
          metalness={0.85}
          wireframe={false}
        />
      </mesh>

      {/* Core Glowing Point Light */}
      <pointLight color="#fde047" intensity={3.5} distance={10} />

      {/* 2. Concentric Gyroscope Rings (Blender Design) */}
      <mesh rotation={ring1Rot}>
        <torusGeometry args={[1.5, 0.045, 16, 64]} />
        <meshStandardMaterial
          color="#38bdf8"
          emissive="#0284c7"
          emissiveIntensity={1.2}
          roughness={0.2}
          metalness={0.9}
        />
      </mesh>

      <mesh rotation={ring2Rot}>
        <torusGeometry args={[2.0, 0.04, 16, 64]} />
        <meshStandardMaterial
          color="#c084fc"
          emissive="#9333ea"
          emissiveIntensity={1.4}
          roughness={0.2}
          metalness={0.9}
        />
      </mesh>

      <mesh rotation={ring3Rot}>
        <torusGeometry args={[2.5, 0.035, 16, 64]} />
        <meshStandardMaterial
          color="#fbbf24"
          emissive="#d97706"
          emissiveIntensity={1.5}
          roughness={0.2}
          metalness={0.9}
        />
      </mesh>

      {/* 3. Outer Sacred Geometry Lattice Wireframe Cage */}
      <mesh rotation={[-rotX * 0.7, -rotY * 0.7, -rotZ * 0.7]}>
        <dodecahedronGeometry args={[2.8, 0]} />
        <meshStandardMaterial
          color="#fef08a"
          emissive="#ca8a04"
          emissiveIntensity={0.8}
          wireframe={true}
          transparent={true}
          opacity={0.65}
        />
      </mesh>
    </group>
  );
};
