import React from 'react';
import { ThreeCanvas } from '@remotion/three';
import { CosmicSeed3D } from './CosmicSeed3D';
import { ParticleVortex3D } from './ParticleVortex3D';
import { ActConfig } from '../types';

interface ThreeCanvasWrapperProps {
  frame: number;
  fps: number;
  act: ActConfig;
  width: number;
  height: number;
}

export const ThreeCanvasWrapper: React.FC<ThreeCanvasWrapperProps> = ({
  frame,
  fps,
  act,
  width,
  height,
}) => {
  // Cinematic camera gentle orbital drift
  const camX = Math.sin(frame * 0.008) * 0.5;
  const camY = Math.cos(frame * 0.006) * 0.3;
  const camZ = 5.5 + Math.sin(frame * 0.005) * 0.4;

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width,
        height,
        pointerEvents: 'none',
      }}
    >
      <ThreeCanvas
        width={width}
        height={height}
        camera={{ position: [camX, camY, camZ], fov: 45 }}
      >
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 8, 5]} intensity={1.5} color="#ffffff" />
        <pointLight position={[-4, -2, -2]} intensity={2.0} color={act.accentColor} />

        {/* 3D Celestial Seed Artifact */}
        <CosmicSeed3D frame={frame} fps={fps} actIndex={act.actIndex} />

        {/* 3D Dynamic Particle Vortex / Hyperspace Stream / Spores */}
        <ParticleVortex3D
          frame={frame}
          mode={act.particleMode}
          color={act.accentColor}
        />
      </ThreeCanvas>
    </div>
  );
};
